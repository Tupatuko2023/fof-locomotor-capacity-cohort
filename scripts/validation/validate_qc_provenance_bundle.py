#!/usr/bin/env python3
"""Fail-closed validation for the A1 public-synthetic QC/provenance bundle."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ARTIFACT_ID = "A1-SUPPLEMENT-QC-PROVENANCE-01"
SCHEMA_VERSION = "1.0.0"
CLASSIFICATION = "PUBLIC_SYNTHETIC"
DISCLAIMER = "Synthetic structural-validation evidence only; not study findings."
CANONICAL_JSON = "UTF-8_NO_BOM_LF_SORTED_KEYS_COMPACT"
TIMESTAMP_POLICY = "OMITTED_FROM_CANONICAL_IDENTITY"
BUNDLE_NAME = ARTIFACT_ID
CANONICAL_BUNDLE_NAME = "bundle"
PAYLOAD_FILES = (
    "decision_evidence.json",
    "modeled_cohort_synthetic_receipt.json",
    "qc_table.csv",
    "runtime_metadata.json",
    "synthetic_input_receipt.json",
)
ALL_FILES = tuple(sorted(PAYLOAD_FILES + (
    "payload_manifest.json", "validation_receipt.json", "bundle_manifest.json",
)))
JSON_FILES = tuple(name for name in ALL_FILES if name.endswith(".json"))
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
UNSAFE_RE = re.compile(
    r"(?i)(authorization\s*:\s*bearer|ghp_[a-z0-9]+|(?:password|secret|api[_-]?key|token)\s*[=:]|"
    r"(?:^|[/\\])(?:home|data/(?:raw|restricted)|secrets?|credentials?)(?:[/\\]|$)|"
    r"(?:participant|subject|patient)[_-]?id|production[_ -]?(?:snapshot|identifier)|raw sessioninfo)"
)
RESEARCH_FIELD_RE = re.compile(
    r"(?i)^(estimate|effect_estimate|p_value|p\.value|ci_lower|ci_upper|std(?:andard)?_?error|"
    r"effect_size|count|percentage|mean|median|sd|n|result_values?)$"
)


class BundleValidationError(ValueError):
    pass


def fail(code: str) -> None:
    raise BundleValidationError(code)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_canonical_json(path: Path) -> dict:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        fail("NON_CANONICAL_ENCODING")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail("INVALID_JSON")
    if not isinstance(value, dict) or raw != canonical_bytes(value):
        fail("NON_CANONICAL_JSON")
    return value


def exact_keys(value: dict, expected: set[str], code: str) -> None:
    if set(value) != expected:
        fail(code)


def safe_reference(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def scan_safe(value: object, key: str = "") -> None:
    if key and RESEARCH_FIELD_RE.fullmatch(key):
        fail("RESEARCH_RESULT_FIELD")
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if not isinstance(child_key, str):
                fail("NON_STRING_KEY")
            scan_safe(child_value, child_key)
    elif isinstance(value, list):
        for child in value:
            scan_safe(child, key)
    elif isinstance(value, str):
        if "\n" in value or "\r" in value or UNSAFE_RE.search(value):
            fail("FORBIDDEN_CONTENT")


def repository_revision(root: Path) -> str:
    try:
        value = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        fail("GIT_REVISION_UNAVAILABLE")
    if not GIT_SHA_RE.fullmatch(value):
        fail("GIT_REVISION_INVALID")
    return value


def git_object_bytes(root: Path, revision: str, path: str) -> bytes:
    if not GIT_SHA_RE.fullmatch(revision):
        fail("GENERATOR_REVISION_INVALID")
    try:
        return subprocess.run(
            ["git", "show", f"{revision}:{path}"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        fail("GENERATOR_REVISION_UNAVAILABLE")


def read_control(root: Path) -> dict[str, str]:
    path = root / "data/synthetic/k50_wide_authoritative_test_control.lock"
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or "=" not in line:
            fail("CONTROL_FORMAT")
        key, value = line.split("=", 1)
        if key in fields:
            fail("CONTROL_DUPLICATE_FIELD")
        fields[key] = value
    required = {"snapshot_role", "snapshot_id", "path", "md5", "sha256", "rows_loaded_expected", "selection_reason"}
    if set(fields) != required:
        fail("CONTROL_FIELDS")
    if fields["snapshot_role"] != "synthetic_wide_test_control" or not fields["snapshot_id"].startswith("SYN-K50-WIDE-"):
        fail("CONTROL_CLASSIFICATION")
    if fields["path"] != "data/synthetic/k50_wide_structural_fixture.csv":
        fail("CONTROL_PATH")
    fixture = root / fields["path"]
    if sha256_file(fixture) != fields["sha256"]:
        fail("SYNTHETIC_INPUT_HASH_MISMATCH")
    return fields


def validate_qc(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        fail("NON_CANONICAL_QC_ENCODING")
    try:
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    except UnicodeDecodeError:
        fail("INVALID_QC_ENCODING")
    if not rows or list(rows[0]) != ["gate", "status", "evidence"]:
        fail("QC_SCHEMA")
    expected = [
        {"gate": "generator_binding", "status": "PASS", "evidence": "REPOSITORY_SOURCE_HASH"},
        {"gate": "public_safety_contract", "status": "PASS", "evidence": "FAIL_CLOSED_ALLOWLIST"},
        {"gate": "synthetic_input_binding", "status": "PASS", "evidence": "SYNTHETIC_CONTROL_HASH"},
    ]
    if rows != expected:
        fail("QC_CONTENT")


def validate_payload(bundle: Path, root: Path) -> str:
    input_receipt = load_canonical_json(bundle / "synthetic_input_receipt.json")
    exact_keys(input_receipt, {
        "schema_version", "artifact_id", "data_classification", "synthetic_disclaimer",
        "input_classification", "input_reference", "input_sha256", "control_reference", "control_sha256",
    }, "INPUT_RECEIPT_FIELDS")
    control = read_control(root)
    expected_input = {
        "schema_version": SCHEMA_VERSION, "artifact_id": ARTIFACT_ID,
        "data_classification": CLASSIFICATION, "synthetic_disclaimer": DISCLAIMER,
        "input_classification": "PUBLIC_SYNTHETIC_INPUT", "input_reference": control["path"],
        "input_sha256": control["sha256"],
        "control_reference": "data/synthetic/k50_wide_authoritative_test_control.lock",
        "control_sha256": sha256_file(root / "data/synthetic/k50_wide_authoritative_test_control.lock"),
    }
    if input_receipt != expected_input:
        fail("SYNTHETIC_INPUT_CONTROL_BINDING")

    modeled = load_canonical_json(bundle / "modeled_cohort_synthetic_receipt.json")
    exact_keys(modeled, {
        "schema_version", "artifact_id", "data_classification", "synthetic_disclaimer",
        "analysis_scope", "cohort_data_state", "result_claim_state",
    }, "MODELED_RECEIPT_FIELDS")
    if modeled != {
        "schema_version": SCHEMA_VERSION, "artifact_id": ARTIFACT_ID,
        "data_classification": CLASSIFICATION, "synthetic_disclaimer": DISCLAIMER,
        "analysis_scope": "STRUCTURAL_VALIDATION_ONLY", "cohort_data_state": "NO_PARTICIPANT_DATA",
        "result_claim_state": "NOT_RESEARCH_RESULTS",
    }:
        fail("MODELED_RECEIPT_CONTENT")

    decision = load_canonical_json(bundle / "decision_evidence.json")
    exact_keys(decision, {
        "schema_version", "artifact_id", "data_classification", "synthetic_disclaimer",
        "decision_state", "evidence_scope",
    }, "DECISION_FIELDS")
    if decision["decision_state"] != "NO_SCIENTIFIC_DECISION" or decision["evidence_scope"] != "TECHNICAL_SYNTHETIC_VALIDATION_ONLY":
        fail("DECISION_CONTENT")

    runtime = load_canonical_json(bundle / "runtime_metadata.json")
    exact_keys(runtime, {
        "schema_version", "artifact_id", "data_classification", "synthetic_disclaimer",
        "runtime_profile", "generator_path", "generator_repository_revision", "generator_sha256", "timestamp_policy",
    }, "RUNTIME_FIELDS")
    generator_path = "scripts/demo/build_qc_provenance_bundle.py"
    expected_runtime = {
        "schema_version": SCHEMA_VERSION, "artifact_id": ARTIFACT_ID,
        "data_classification": CLASSIFICATION, "synthetic_disclaimer": DISCLAIMER,
        "runtime_profile": "PYTHON_STANDARD_LIBRARY", "generator_path": generator_path,
        "generator_repository_revision": runtime["generator_repository_revision"],
        "generator_sha256": sha256_file(root / generator_path), "timestamp_policy": TIMESTAMP_POLICY,
    }
    if runtime != expected_runtime:
        fail("GENERATOR_BINDING")
    if sha256_bytes(git_object_bytes(
        root, runtime["generator_repository_revision"], generator_path
    )) != runtime["generator_sha256"]:
        fail("GENERATOR_REVISION_HASH_MISMATCH")
    validate_qc(bundle / "qc_table.csv")
    for name in PAYLOAD_FILES:
        if name.endswith(".json"):
            scan_safe(load_canonical_json(bundle / name))

    manifest = load_canonical_json(bundle / "payload_manifest.json")
    exact_keys(manifest, {
        "schema_version", "artifact_id", "artifact_revision", "data_classification",
        "synthetic_disclaimer", "canonical_json", "timestamp_policy", "members",
    }, "PAYLOAD_MANIFEST_FIELDS")
    if manifest["schema_version"] != SCHEMA_VERSION or manifest["artifact_id"] != ARTIFACT_ID or manifest["artifact_revision"] != 1:
        fail("PAYLOAD_IDENTITY")
    if manifest["data_classification"] != CLASSIFICATION or manifest["synthetic_disclaimer"] != DISCLAIMER:
        fail("PAYLOAD_CLASSIFICATION")
    if manifest["canonical_json"] != CANONICAL_JSON or manifest["timestamp_policy"] != TIMESTAMP_POLICY:
        fail("PAYLOAD_CANONICAL_CONTRACT")
    expected_members = [
        {"path": name, "role": name.rsplit(".", 1)[0], "sha256": sha256_file(bundle / name)}
        for name in PAYLOAD_FILES
    ]
    if manifest["members"] != expected_members:
        fail("PAYLOAD_MEMBER_HASH_MISMATCH")
    scan_safe(manifest)
    return sha256_file(bundle / "payload_manifest.json")


def validate_bundle(bundle: Path, root: Path) -> str:
    if bundle.name not in {BUNDLE_NAME, CANONICAL_BUNDLE_NAME} or bundle.is_symlink() or not bundle.is_dir():
        fail("BUNDLE_PATH")
    names = sorted(item.name for item in bundle.iterdir())
    if names != list(ALL_FILES):
        fail("MEMBER_SET")
    if any(item.is_symlink() or not item.is_file() for item in bundle.iterdir()):
        fail("MEMBER_FILE_TYPE")
    payload_sha = validate_payload(bundle, root)

    receipt = load_canonical_json(bundle / "validation_receipt.json")
    exact_keys(receipt, {
        "schema_version", "receipt_id", "artifact_id", "artifact_revision", "payload_sha256",
        "validator_path", "validator_sha256", "validation_result", "data_classification", "synthetic_disclaimer",
    }, "VALIDATION_RECEIPT_FIELDS")
    validator_path = "scripts/validation/validate_qc_provenance_bundle.py"
    expected_receipt = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": "A1-RECEIPT-QC-PROVENANCE-VALIDATION-01",
        "artifact_id": ARTIFACT_ID, "artifact_revision": 1, "payload_sha256": payload_sha,
        "validator_path": validator_path, "validator_sha256": sha256_file(root / validator_path),
        "validation_result": "PASS", "data_classification": CLASSIFICATION,
        "synthetic_disclaimer": DISCLAIMER,
    }
    if receipt != expected_receipt:
        fail("VALIDATION_RECEIPT_BINDING")
    scan_safe(receipt)

    manifest = load_canonical_json(bundle / "bundle_manifest.json")
    exact_keys(manifest, {
        "schema_version", "artifact_id", "artifact_revision", "data_classification", "synthetic_disclaimer",
        "canonical_json", "timestamp_policy", "exact_member_names", "members", "payload_manifest_sha256",
        "validation_receipt_sha256", "artifact_hash_contract",
    }, "BUNDLE_MANIFEST_FIELDS")
    member_names = tuple(name for name in ALL_FILES if name != "bundle_manifest.json")
    expected_members = [
        {"path": name, "role": name.rsplit(".", 1)[0], "sha256": sha256_file(bundle / name)}
        for name in member_names
    ]
    expected_fixed = {
        "schema_version": SCHEMA_VERSION, "artifact_id": ARTIFACT_ID, "artifact_revision": 1,
        "data_classification": CLASSIFICATION, "synthetic_disclaimer": DISCLAIMER,
        "canonical_json": CANONICAL_JSON, "timestamp_policy": TIMESTAMP_POLICY,
        "exact_member_names": list(ALL_FILES), "members": expected_members,
        "payload_manifest_sha256": payload_sha,
        "validation_receipt_sha256": sha256_file(bundle / "validation_receipt.json"),
        "artifact_hash_contract": "SHA256_EXACT_BUNDLE_MANIFEST_BYTES",
    }
    if manifest != expected_fixed:
        fail("BUNDLE_MANIFEST_BINDING")
    scan_safe(manifest)
    return sha256_file(bundle / "bundle_manifest.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        digest = validate_bundle(args.bundle.resolve(), args.root.resolve())
    except (BundleValidationError, OSError) as error:
        code = str(error) if isinstance(error, BundleValidationError) else "IO_ERROR"
        print(f"QC_PROVENANCE_BUNDLE=FAIL code={code}", file=sys.stderr)
        return 1
    print(f"QC_PROVENANCE_BUNDLE=PASS artifact_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
