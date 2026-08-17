#!/usr/bin/env python3
"""Fail-closed validation for the public, metadata-only artifact registry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = "1.0.0"
ROOT_FIELDS = {"schema_version", "registry_status", "project_id", "artifacts"}
REGISTRY_STATUSES = {"DESIGN_SCAFFOLD", "ACTIVE", "RETIRED"}
ARTIFACT_FIELDS = {
    "artifact_id", "artifact_revision", "provisional", "artifact_type",
    "artifact_status", "title", "caption_status", "analysis_source", "generator",
    "required_inputs", "data_classification", "execution_environment",
    "protected_execution_required", "protected_execution_reference",
    "scientific_approval_required", "scientific_decision_reference",
    "disclosure_review_required", "disclosure_state",
    "disclosure_decision_reference", "publication_status",
    "publication_approval_reference", "candidate_output_path",
    "manuscript_destination", "manuscript_reference_key", "provenance_required",
    "validation_required", "validation_receipt_reference", "artifact_sha256",
    "published_sha256", "supersedes",
}
REQUIRED_ARTIFACT_FIELDS = {
    "artifact_id", "artifact_revision", "provisional", "artifact_type",
    "artifact_status", "title", "caption_status", "analysis_source", "generator",
    "required_inputs", "data_classification", "execution_environment",
    "protected_execution_required", "scientific_approval_required",
    "disclosure_review_required", "disclosure_state", "publication_status",
    "manuscript_destination", "manuscript_reference_key", "provenance_required",
    "validation_required", "supersedes",
}
GENERATOR_FIELDS = {"status", "path", "repository_revision", "sha256"}
ARTIFACT_TYPES = {"TABLE", "FIGURE", "SUPPLEMENT", "DOCUMENT", "RECEIPT"}
ARTIFACT_STATUSES = {
    "DESIGN_CANDIDATE", "SYNTHETIC_CANDIDATE", "SYNTHETIC_VALIDATED",
    "PROTECTED_GENERATED", "PROTECTED_VALIDATED", "QUARANTINED",
    "SUPERSEDED", "WITHDRAWN",
}
CAPTION_STATUSES = {"NOT_REQUIRED", "DRAFT", "SYNTHETIC_DISCLAIMER", "APPROVED"}
DATA_CLASSES = {"PUBLIC_METADATA", "PUBLIC_SYNTHETIC", "PROTECTED_AGGREGATE", "DISCLOSURE_APPROVED_PUBLIC"}
INPUT_CLASSES = {"PUBLIC_SYNTHETIC_INPUT", "PUBLIC_METADATA_INPUT", "PROTECTED_PARTICIPANT_INPUT_REQUIRED"}
DISCLOSURE_STATES = {"NOT_APPLICABLE_SYNTHETIC", "NOT_SUBMITTED", "PENDING", "APPROVED", "REJECTED", "WITHDRAWN"}
PUBLICATION_STATUSES = {"NOT_PROPOSED", "CANDIDATE", "NOT_APPROVED", "APPROVED", "PUBLISHED", "WITHDRAWN"}
GENERATOR_STATUSES = {"PLANNED", "EXISTS", "NOT_REQUIRED"}
FORBIDDEN_FIELD_NAMES = {
    "estimate", "effect_estimate", "p_value", "ci_lower", "ci_upper",
    "standard_error", "effect_size", "n", "count", "percentage", "mean",
    "median", "sd", "participant_id", "subject_id", "patient_id", "row_data",
    "model_frame", "residuals", "predictions", "result_values",
}
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){2,}$")
REF_RE = re.compile(r"^[A-Z][A-Z0-9_-]{2,}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SECRET_RE = re.compile(r"(?i)(authorization\s*:\s*bearer|ghp_[a-z0-9]+|(?:token|password|secret|api[_-]?key)\s*[=:])")
PLACEHOLDER_RE = re.compile(r"\{\{artifact:([A-Z][A-Z0-9-]+)\|use=(research_result|supplement_evidence|synthetic_demo|repository_provenance)\}\}")
ANY_PLACEHOLDER_RE = re.compile(r"\{\{artifact:[^}]+\}\}")
FORBIDDEN_ROOTS = {"data/raw", "data/restricted", "secrets", "credentials"}


class ValidationError(Exception):
    def __init__(self, code: str, path: str = "$") -> None:
        super().__init__(code)
        self.code = code
        self.path = path


def fail(code: str, path: str = "$") -> None:
    raise ValidationError(code, path)


def require_type(value: object, kind: type, path: str) -> None:
    if kind is int and (not isinstance(value, int) or isinstance(value, bool)):
        fail("TYPE", path)
    if kind is not int and not isinstance(value, kind):
        fail("TYPE", path)


def check_keys(value: dict, allowed: set[str], required: set[str], path: str) -> None:
    forbidden = set(value) & FORBIDDEN_FIELD_NAMES
    if forbidden:
        fail("FORBIDDEN_FIELD", path)
    if set(value) - allowed:
        fail("UNKNOWN_FIELD", path)
    if required - set(value):
        fail("MISSING_FIELD", path)


def check_enum(value: object, allowed: set[str], path: str) -> None:
    if not isinstance(value, str) or value not in allowed:
        fail("ENUM", path)


def check_safe_strings(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_FIELD_NAMES:
                fail("FORBIDDEN_FIELD", path)
            check_safe_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_safe_strings(child, f"{path}[{index}]")
    elif isinstance(value, str) and SECRET_RE.search(value):
        fail("SECRET_PATTERN", path)


def check_repo_path(value: object, path: str) -> None:
    require_type(value, str, path)
    if not value or "\\" in value or re.match(r"^[A-Za-z]:", value) or value.startswith(("/", "~")):
        fail("UNSAFE_PATH", path)
    candidate = PurePosixPath(value)
    if ".." in candidate.parts or "." in candidate.parts:
        fail("UNSAFE_PATH", path)
    normalized = candidate.as_posix().rstrip("/")
    if any(normalized == root or normalized.startswith(root + "/") for root in FORBIDDEN_ROOTS):
        fail("FORBIDDEN_ROOT", path)


def check_digest(value: object, regex: re.Pattern[str], path: str) -> None:
    if not isinstance(value, str) or not regex.fullmatch(value):
        fail("DIGEST_FORMAT", path)


def validate_generator(generator: object, path: str) -> None:
    require_type(generator, dict, path)
    check_keys(generator, GENERATOR_FIELDS, {"status"}, path)
    check_enum(generator["status"], GENERATOR_STATUSES, f"{path}.status")
    if generator["status"] == "EXISTS":
        for field in ("path", "repository_revision", "sha256"):
            if field not in generator:
                fail("MISSING_GENERATOR_PROVENANCE", path)
        check_repo_path(generator["path"], f"{path}.path")
        check_digest(generator["repository_revision"], GIT_SHA_RE, f"{path}.repository_revision")
        check_digest(generator["sha256"], SHA256_RE, f"{path}.sha256")
    elif set(generator) != {"status"}:
        fail("UNEXPECTED_GENERATOR_PROVENANCE", path)


def validate_artifact(artifact: object, index: int) -> None:
    path = f"$.artifacts[{index}]"
    require_type(artifact, dict, path)
    check_keys(artifact, ARTIFACT_FIELDS, REQUIRED_ARTIFACT_FIELDS, path)
    if not isinstance(artifact["artifact_id"], str) or not ID_RE.fullmatch(artifact["artifact_id"]):
        fail("ID_FORMAT", f"{path}.artifact_id")
    require_type(artifact["artifact_revision"], int, f"{path}.artifact_revision")
    if artifact["artifact_revision"] < 1:
        fail("REVISION", f"{path}.artifact_revision")
    for field in ("provisional", "protected_execution_required", "scientific_approval_required", "disclosure_review_required", "provenance_required", "validation_required"):
        require_type(artifact[field], bool, f"{path}.{field}")
    check_enum(artifact["artifact_type"], ARTIFACT_TYPES, f"{path}.artifact_type")
    check_enum(artifact["artifact_status"], ARTIFACT_STATUSES, f"{path}.artifact_status")
    check_enum(artifact["caption_status"], CAPTION_STATUSES, f"{path}.caption_status")
    check_enum(artifact["data_classification"], DATA_CLASSES, f"{path}.data_classification")
    check_enum(artifact["disclosure_state"], DISCLOSURE_STATES, f"{path}.disclosure_state")
    check_enum(artifact["publication_status"], PUBLICATION_STATUSES, f"{path}.publication_status")
    for field in ("title", "analysis_source", "execution_environment", "manuscript_destination"):
        if not isinstance(artifact[field], str) or not artifact[field].strip():
            fail("EMPTY_STRING", f"{path}.{field}")
    if not isinstance(artifact["manuscript_reference_key"], str) or not REF_RE.fullmatch(artifact["manuscript_reference_key"]):
        fail("REFERENCE_FORMAT", f"{path}.manuscript_reference_key")
    require_type(artifact["required_inputs"], list, f"{path}.required_inputs")
    if len(artifact["required_inputs"]) != len(set(artifact["required_inputs"])):
        fail("DUPLICATE_INPUT_CLASS", f"{path}.required_inputs")
    for value in artifact["required_inputs"]:
        check_enum(value, INPUT_CLASSES, f"{path}.required_inputs")
    validate_generator(artifact["generator"], f"{path}.generator")
    if "candidate_output_path" in artifact:
        check_repo_path(artifact["candidate_output_path"], f"{path}.candidate_output_path")
    for field in ("artifact_sha256", "published_sha256"):
        if field in artifact:
            check_digest(artifact[field], SHA256_RE, f"{path}.{field}")
    status = artifact["artifact_status"]
    protected = status in {"PROTECTED_GENERATED", "PROTECTED_VALIDATED"}
    materialized = status in {"SYNTHETIC_VALIDATED", "PROTECTED_GENERATED", "PROTECTED_VALIDATED"}
    if materialized and "artifact_sha256" not in artifact:
        fail("MISSING_ARTIFACT_CHECKSUM", path)
    if protected:
        if not artifact["protected_execution_required"] or "protected_execution_reference" not in artifact:
            fail("MISSING_PROTECTED_REFERENCE", path)
        if "candidate_output_path" in artifact:
            fail("PROTECTED_PUBLIC_PATH", f"{path}.candidate_output_path")
    if artifact["data_classification"] == "PUBLIC_SYNTHETIC":
        if artifact["caption_status"] != "SYNTHETIC_DISCLAIMER":
            fail("MISSING_SYNTHETIC_DISCLAIMER", path)
        if artifact["disclosure_state"] != "NOT_APPLICABLE_SYNTHETIC":
            fail("SYNTHETIC_DISCLOSURE_STATE", path)
    if artifact["disclosure_state"] == "APPROVED":
        if "disclosure_decision_reference" not in artifact or "artifact_sha256" not in artifact:
            fail("DISCLOSURE_EVIDENCE", path)
    publication = artifact["publication_status"]
    if artifact["provisional"] and publication in {"APPROVED", "PUBLISHED"}:
        fail("PROVISIONAL_PUBLICATION", path)
    if publication in {"APPROVED", "PUBLISHED"}:
        if "publication_approval_reference" not in artifact:
            fail("PUBLICATION_EVIDENCE", path)
        if artifact["data_classification"] in {"PROTECTED_AGGREGATE", "DISCLOSURE_APPROVED_PUBLIC"} and artifact["disclosure_state"] != "APPROVED":
            fail("PUBLICATION_BEFORE_DISCLOSURE", path)
    if publication == "PUBLISHED" and "published_sha256" not in artifact:
        fail("MISSING_PUBLISHED_CHECKSUM", path)
    if artifact["scientific_approval_required"] and publication in {"APPROVED", "PUBLISHED"} and "scientific_decision_reference" not in artifact:
        fail("SCIENTIFIC_EVIDENCE", path)
    supersedes = artifact["supersedes"]
    if supersedes is not None and (not isinstance(supersedes, str) or not ID_RE.fullmatch(supersedes)):
        fail("SUPERSEDES_FORMAT", f"{path}.supersedes")


def validate_registry(registry: object) -> dict:
    require_type(registry, dict, "$")
    check_keys(registry, ROOT_FIELDS, ROOT_FIELDS, "$")
    if registry["schema_version"] != SCHEMA_VERSION:
        fail("SCHEMA_VERSION", "$.schema_version")
    check_enum(registry["registry_status"], REGISTRY_STATUSES, "$.registry_status")
    if registry["project_id"] != "A1":
        fail("PROJECT_ID", "$.project_id")
    require_type(registry["artifacts"], list, "$.artifacts")
    check_safe_strings(registry)
    for index, artifact in enumerate(registry["artifacts"]):
        validate_artifact(artifact, index)
    ids = [item["artifact_id"] for item in registry["artifacts"]]
    refs = [item["manuscript_reference_key"] for item in registry["artifacts"]]
    if len(ids) != len(set(ids)):
        fail("DUPLICATE_ID", "$.artifacts")
    if len(refs) != len(set(refs)):
        fail("DUPLICATE_REFERENCE", "$.artifacts")
    by_id = {item["artifact_id"]: item for item in registry["artifacts"]}
    for artifact in registry["artifacts"]:
        target = artifact["supersedes"]
        if target is not None and target not in by_id:
            fail("UNKNOWN_SUPERSESSION", "$.artifacts")
        seen = {artifact["artifact_id"]}
        while target is not None:
            if target in seen:
                fail("SUPERSESSION_CYCLE", "$.artifacts")
            seen.add(target)
            target = by_id[target]["supersedes"]
    return registry


def validate_placeholders(text: str, registry: dict) -> None:
    matches = list(PLACEHOLDER_RE.finditer(text))
    if len(matches) != len(ANY_PLACEHOLDER_RE.findall(text)):
        fail("PLACEHOLDER_FORMAT", "$placeholders")
    by_id = {item["artifact_id"]: item for item in registry["artifacts"]}
    for match in matches:
        artifact = by_id.get(match.group(1))
        if artifact is None:
            fail("UNKNOWN_PLACEHOLDER", "$placeholders")
        if artifact["artifact_status"] in {"QUARANTINED", "SUPERSEDED", "WITHDRAWN"}:
            fail("INACTIVE_PLACEHOLDER", "$placeholders")
        use = match.group(2)
        if use == "research_result":
            if artifact["data_classification"] == "PUBLIC_SYNTHETIC":
                fail("SYNTHETIC_RESEARCH_RESULT", "$placeholders")
            if artifact["publication_status"] not in {"APPROVED", "PUBLISHED"}:
                fail("UNAPPROVED_RESEARCH_RESULT", "$placeholders")
            if artifact["data_classification"] in {"PROTECTED_AGGREGATE", "DISCLOSURE_APPROVED_PUBLIC"} and artifact["disclosure_state"] != "APPROVED":
                fail("UNDISCLOSED_RESEARCH_RESULT", "$placeholders")
        elif use == "synthetic_demo" and artifact["data_classification"] != "PUBLIC_SYNTHETIC":
            fail("NON_SYNTHETIC_DEMO", "$placeholders")


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError):
        fail("JSON_READ", "$")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--placeholders", type=Path)
    args = parser.parse_args(argv)
    try:
        registry = validate_registry(load_json(args.registry))
        if args.placeholders is not None:
            try:
                text = args.placeholders.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                fail("PLACEHOLDER_READ", "$placeholders")
            validate_placeholders(text, registry)
    except ValidationError as error:
        print(f"ARTIFACT_REGISTRY=FAIL code={error.code} path={error.path}", file=sys.stderr)
        return 1
    print("ARTIFACT_REGISTRY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
