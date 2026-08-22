#!/usr/bin/env python3
"""Validate filesystem-backed SYNTHETIC_VALIDATED promotion evidence."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_VALIDATOR_PATH = ROOT / "scripts/validation/validate_artifact_registry.py"
SPEC = importlib.util.spec_from_file_location("artifact_registry_validator", REGISTRY_VALIDATOR_PATH)
registry_validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(registry_validator)

SCHEMA_VERSION = "1.0.0"
CLASSIFICATION = "PUBLIC_SYNTHETIC_VALIDATION"
DISCLAIMER = "Synthetic structural-validation evidence only; not study findings."
TIMESTAMP_POLICY = "OMITTED_FROM_CANONICAL_IDENTITY"
PROFILES = {
    "SINGLE_FILE_TABLE_V1": {
        "artifact_type": "TABLE",
        "hash_contract": "SHA256_EXACT_FILE_BYTES",
        "checks": {
            "ARTIFACT_HASH_MATCH", "GENERATOR_IDENTITY_MATCH", "SYNTHETIC_INPUT_CONTROL_MATCH",
            "VALIDATOR_IDENTITY_MATCH", "SYNTHETIC_BOUNDARY_PASS", "TABLE_SCHEMA_PASS",
        },
    },
    "QC_PROVENANCE_BUNDLE_V1": {
        "artifact_type": "SUPPLEMENT",
        "hash_contract": "SHA256_EXACT_BUNDLE_MANIFEST_BYTES",
        "checks": {
            "ARTIFACT_HASH_MATCH", "GENERATOR_IDENTITY_MATCH", "SYNTHETIC_INPUT_CONTROL_MATCH",
            "VALIDATOR_IDENTITY_MATCH", "SYNTHETIC_BOUNDARY_PASS", "BUNDLE_CONTRACT_PASS",
        },
    },
}
RECEIPT_FIELDS = {
    "schema_version", "receipt_id", "receipt_classification", "artifact_id", "artifact_revision",
    "artifact_type", "artifact_path", "artifact_sha256", "artifact_hash_contract", "generator_path",
    "generator_repository_revision", "generator_sha256", "synthetic_input_bindings",
    "execution_identity_sha256", "validator_path", "validator_repository_revision", "validator_sha256",
    "validation_profile", "validation_result", "validated_checks", "supporting_evidence",
    "synthetic_disclaimer", "timestamp_policy",
}
INPUT_FIELDS = {"input_classification", "input_reference", "input_sha256", "control_reference", "control_sha256"}
EVIDENCE_FIELDS = {"classification", "reference", "sha256"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FORBIDDEN_RE = re.compile(
    r"(?i)(authorization\s*:\s*bearer|ghp_[a-z0-9]+|(?:password|secret|api[_-]?key|token)\s*[=:]|"
    r"(?:participant|subject|patient)[_-]?id|(?:production|protected)[_-]?(?:snapshot|input|path))"
)


class PromotionValidationError(ValueError):
    pass


def fail(code: str) -> None:
    raise PromotionValidationError(code)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_canonical_json(path: Path) -> dict:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        fail("NON_CANONICAL_RECEIPT_ENCODING")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail("INVALID_RECEIPT_JSON")
    if not isinstance(value, dict) or raw != canonical_bytes(value):
        fail("NON_CANONICAL_RECEIPT_JSON")
    return value


def check_digest(value: object, regex: re.Pattern[str], code: str) -> None:
    if not isinstance(value, str) or not regex.fullmatch(value):
        fail(code)


def check_safe_values(value: object) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if FORBIDDEN_RE.search(str(key)):
                fail("FORBIDDEN_RECEIPT_FIELD")
            check_safe_values(child)
    elif isinstance(value, list):
        for child in value:
            check_safe_values(child)
    elif isinstance(value, str) and ("\n" in value or "\r" in value or FORBIDDEN_RE.search(value)):
        fail("FORBIDDEN_RECEIPT_VALUE")


def safe_relative(value: object) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", value):
        fail("UNSAFE_PATH")
    path = PurePosixPath(value)
    if not path.parts or any(part in {".", ".."} for part in path.parts):
        fail("UNSAFE_PATH")
    if path.parts[0] in {".git", "GPT", "secrets", "credentials"}:
        fail("FORBIDDEN_PATH_ROOT")
    if path.parts[0] == "data" and path.parts[:2] != ("data", "synthetic"):
        fail("FORBIDDEN_PATH_ROOT")
    return path


def resolve_repo_file(root: Path, value: object) -> Path:
    relative = safe_relative(value)
    path = root.joinpath(*relative.parts)
    if path.is_symlink() or not path.is_file():
        fail("MISSING_OR_UNSAFE_FILE")
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail("PATH_OUTSIDE_REPOSITORY")
    return path


def under_canonical_root(value: str, roots: tuple[PurePosixPath, ...]) -> bool:
    path = safe_relative(value)
    return any(path == root or root in path.parents for root in roots)


def git_object_bytes(root: Path, revision: str, path: str) -> bytes:
    check_digest(revision, GIT_SHA_RE, "GIT_REVISION_FORMAT")
    safe_relative(path)
    try:
        return subprocess.run(
            ["git", "show", f"{revision}:{path}"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        fail("GIT_OBJECT_UNAVAILABLE")


def validate_source_identity(root: Path, path: str, revision: str, digest: str, prefix: str) -> None:
    check_digest(digest, SHA256_RE, f"{prefix}_HASH_FORMAT")
    current = resolve_repo_file(root, path)
    if sha256_file(current) != digest:
        fail(f"{prefix}_CURRENT_HASH_MISMATCH")
    if sha256_bytes(git_object_bytes(root, revision, path)) != digest:
        fail(f"{prefix}_REVISION_HASH_MISMATCH")


def execution_identity(receipt: dict) -> str:
    identity = {
        "artifact_id": receipt["artifact_id"], "artifact_revision": receipt["artifact_revision"],
        "generator_path": receipt["generator_path"],
        "generator_repository_revision": receipt["generator_repository_revision"],
        "generator_sha256": receipt["generator_sha256"],
        "synthetic_input_bindings": receipt["synthetic_input_bindings"],
        "validation_profile": receipt["validation_profile"],
    }
    return sha256_bytes(canonical_bytes(identity))


def validate_table(path: Path) -> None:
    raw = path.read_bytes()
    if path.suffix.lower() != ".csv" or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        fail("TABLE_CANONICAL_FORMAT")
    try:
        reader = csv.reader(io.StringIO(raw.decode("utf-8")))
        header = next(reader)
    except (UnicodeDecodeError, StopIteration, csv.Error):
        fail("TABLE_SCHEMA")
    if not header or any(not value.strip() for value in header) or len(header) != len(set(header)):
        fail("TABLE_SCHEMA")


def validate_bundle(root: Path, manifest: Path) -> None:
    validator_path = root / "scripts/validation/validate_qc_provenance_bundle.py"
    spec = importlib.util.spec_from_file_location("qc_bundle_validator", validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    digest = module.validate_bundle(manifest.parent, root)
    if digest != sha256_file(manifest):
        fail("BUNDLE_VALIDATOR_HASH_MISMATCH")


def validate_promotion(registry_path: Path, root: Path, canonical_roots: list[str], artifact_id: str | None = None) -> None:
    root = root.resolve()
    roots = tuple(safe_relative(value) for value in canonical_roots)
    if not roots:
        fail("CANONICAL_ROOT_REQUIRED")
    registry = registry_validator.validate_registry(registry_validator.load_json(registry_path))
    selected = [item for item in registry["artifacts"] if item["artifact_status"] == "SYNTHETIC_VALIDATED"]
    if artifact_id is not None:
        selected = [item for item in selected if item["artifact_id"] == artifact_id]
    if not selected:
        fail("VALIDATED_ARTIFACT_NOT_FOUND")
    for artifact in selected:
        if not under_canonical_root(artifact["candidate_output_path"], roots) or not under_canonical_root(artifact["validation_receipt_reference"], roots):
            fail("OUTSIDE_CANONICAL_ROOT")
        artifact_path = resolve_repo_file(root, artifact["candidate_output_path"])
        receipt_path = resolve_repo_file(root, artifact["validation_receipt_reference"])
        if sha256_file(receipt_path) != artifact["validation_receipt_sha256"]:
            fail("RECEIPT_HASH_MISMATCH")
        receipt = load_canonical_json(receipt_path)
        if set(receipt) != RECEIPT_FIELDS:
            fail("RECEIPT_FIELDS")
        check_safe_values(receipt)
        profile = PROFILES.get(receipt["validation_profile"])
        if profile is None:
            fail("VALIDATION_PROFILE")
        expected = {
            "schema_version": SCHEMA_VERSION, "receipt_classification": CLASSIFICATION,
            "artifact_id": artifact["artifact_id"], "artifact_revision": artifact["artifact_revision"],
            "artifact_type": artifact["artifact_type"], "artifact_path": artifact["candidate_output_path"],
            "artifact_sha256": artifact["artifact_sha256"], "generator_path": artifact["generator"]["path"],
            "generator_repository_revision": artifact["generator"]["repository_revision"],
            "generator_sha256": artifact["generator"]["sha256"], "validation_result": "PASS",
            "synthetic_disclaimer": DISCLAIMER, "timestamp_policy": TIMESTAMP_POLICY,
        }
        if any(receipt.get(key) != value for key, value in expected.items()):
            fail("RECEIPT_REGISTRY_BINDING")
        if receipt["artifact_type"] != profile["artifact_type"] or receipt["artifact_hash_contract"] != profile["hash_contract"]:
            fail("PROFILE_ARTIFACT_CONTRACT")
        if set(receipt["validated_checks"]) != profile["checks"] or len(receipt["validated_checks"]) != len(profile["checks"]):
            fail("VALIDATED_CHECKS")
        if receipt["execution_identity_sha256"] != execution_identity(receipt):
            fail("EXECUTION_IDENTITY_MISMATCH")
        if sha256_file(artifact_path) != artifact["artifact_sha256"]:
            fail("ARTIFACT_HASH_MISMATCH")
        validate_source_identity(root, receipt["generator_path"], receipt["generator_repository_revision"], receipt["generator_sha256"], "GENERATOR")
        if not receipt["validator_path"].startswith("scripts/validation/"):
            fail("VALIDATOR_PATH_BOUNDARY")
        validate_source_identity(root, receipt["validator_path"], receipt["validator_repository_revision"], receipt["validator_sha256"], "VALIDATOR")
        if not isinstance(receipt["synthetic_input_bindings"], list) or not receipt["synthetic_input_bindings"]:
            fail("INPUT_BINDINGS")
        for binding in receipt["synthetic_input_bindings"]:
            if not isinstance(binding, dict) or set(binding) != INPUT_FIELDS or binding["input_classification"] != "PUBLIC_SYNTHETIC_INPUT":
                fail("INPUT_BINDING_FIELDS")
            input_path = resolve_repo_file(root, binding["input_reference"])
            control_path = resolve_repo_file(root, binding["control_reference"])
            if sha256_file(input_path) != binding["input_sha256"] or sha256_file(control_path) != binding["control_sha256"]:
                fail("INPUT_CONTROL_HASH_MISMATCH")
        if not isinstance(receipt["supporting_evidence"], list):
            fail("SUPPORTING_EVIDENCE")
        for evidence in receipt["supporting_evidence"]:
            if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_FIELDS or evidence["classification"] != "PUBLIC_SYNTHETIC_VALIDATION_EVIDENCE":
                fail("SUPPORTING_EVIDENCE_FIELDS")
            if sha256_file(resolve_repo_file(root, evidence["reference"])) != evidence["sha256"]:
                fail("SUPPORTING_EVIDENCE_HASH_MISMATCH")
        if receipt["validation_profile"] == "SINGLE_FILE_TABLE_V1":
            validate_table(artifact_path)
        else:
            validate_bundle(root, artifact_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--canonical-root", action="append", required=True)
    parser.add_argument("--artifact-id")
    args = parser.parse_args(argv)
    try:
        validate_promotion(args.registry, args.root, args.canonical_root, args.artifact_id)
    except (PromotionValidationError, registry_validator.ValidationError, OSError) as error:
        code = error.code if isinstance(error, registry_validator.ValidationError) else str(error)
        print(f"SYNTHETIC_PROMOTION=FAIL code={code}", file=sys.stderr)
        return 1
    print("SYNTHETIC_PROMOTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
