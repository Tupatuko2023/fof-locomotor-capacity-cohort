#!/usr/bin/env python3
"""Build the deterministic A1 public-synthetic QC/provenance bundle."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts/validation/validate_qc_provenance_bundle.py"
SPEC = importlib.util.spec_from_file_location("qc_provenance_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def write_json(path: Path, value: object) -> None:
    path.write_bytes(validator.canonical_bytes(value))


def base_metadata() -> dict[str, object]:
    return {
        "schema_version": validator.SCHEMA_VERSION,
        "artifact_id": validator.ARTIFACT_ID,
        "data_classification": validator.CLASSIFICATION,
        "synthetic_disclaimer": validator.DISCLAIMER,
    }


def build(root: Path, output_dir: Path) -> tuple[Path, str]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("output directory must be empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = output_dir / validator.BUNDLE_NAME
    bundle.mkdir()

    control = validator.read_control(root)
    common = base_metadata()
    input_receipt = {
        **common,
        "input_classification": "PUBLIC_SYNTHETIC_INPUT",
        "input_reference": control["path"],
        "input_sha256": control["sha256"],
        "control_reference": "data/synthetic/k50_wide_authoritative_test_control.lock",
        "control_sha256": validator.sha256_file(root / "data/synthetic/k50_wide_authoritative_test_control.lock"),
    }
    modeled_receipt = {
        **common,
        "analysis_scope": "STRUCTURAL_VALIDATION_ONLY",
        "cohort_data_state": "NO_PARTICIPANT_DATA",
        "result_claim_state": "NOT_RESEARCH_RESULTS",
    }
    decision = {
        **common,
        "decision_state": "NO_SCIENTIFIC_DECISION",
        "evidence_scope": "TECHNICAL_SYNTHETIC_VALIDATION_ONLY",
    }
    generator_path = "scripts/demo/build_qc_provenance_bundle.py"
    runtime = {
        **common,
        "runtime_profile": "PYTHON_STANDARD_LIBRARY",
        "generator_path": generator_path,
        "generator_repository_revision": validator.repository_revision(root),
        "generator_sha256": validator.sha256_file(root / generator_path),
        "timestamp_policy": validator.TIMESTAMP_POLICY,
    }
    write_json(bundle / "synthetic_input_receipt.json", input_receipt)
    write_json(bundle / "modeled_cohort_synthetic_receipt.json", modeled_receipt)
    write_json(bundle / "decision_evidence.json", decision)
    write_json(bundle / "runtime_metadata.json", runtime)

    qc_rows = [
        ("generator_binding", "PASS", "REPOSITORY_SOURCE_HASH"),
        ("public_safety_contract", "PASS", "FAIL_CLOSED_ALLOWLIST"),
        ("synthetic_input_binding", "PASS", "SYNTHETIC_CONTROL_HASH"),
    ]
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("gate", "status", "evidence"))
    writer.writerows(qc_rows)
    (bundle / "qc_table.csv").write_bytes(stream.getvalue().encode("utf-8"))

    payload_manifest = {
        **common,
        "artifact_revision": 1,
        "canonical_json": validator.CANONICAL_JSON,
        "timestamp_policy": validator.TIMESTAMP_POLICY,
        "members": [
            {"path": name, "role": name.rsplit(".", 1)[0], "sha256": validator.sha256_file(bundle / name)}
            for name in validator.PAYLOAD_FILES
        ],
    }
    write_json(bundle / "payload_manifest.json", payload_manifest)
    payload_sha = validator.validate_payload(bundle, root)

    validator_path = "scripts/validation/validate_qc_provenance_bundle.py"
    validation_receipt = {
        "schema_version": validator.SCHEMA_VERSION,
        "receipt_id": "A1-RECEIPT-QC-PROVENANCE-VALIDATION-01",
        "artifact_id": validator.ARTIFACT_ID,
        "artifact_revision": 1,
        "payload_sha256": payload_sha,
        "validator_path": validator_path,
        "validator_sha256": validator.sha256_file(root / validator_path),
        "validation_result": "PASS",
        "data_classification": validator.CLASSIFICATION,
        "synthetic_disclaimer": validator.DISCLAIMER,
    }
    write_json(bundle / "validation_receipt.json", validation_receipt)

    member_names = tuple(name for name in validator.ALL_FILES if name != "bundle_manifest.json")
    bundle_manifest = {
        **common,
        "artifact_revision": 1,
        "canonical_json": validator.CANONICAL_JSON,
        "timestamp_policy": validator.TIMESTAMP_POLICY,
        "exact_member_names": list(validator.ALL_FILES),
        "members": [
            {"path": name, "role": name.rsplit(".", 1)[0], "sha256": validator.sha256_file(bundle / name)}
            for name in member_names
        ],
        "payload_manifest_sha256": payload_sha,
        "validation_receipt_sha256": validator.sha256_file(bundle / "validation_receipt.json"),
        "artifact_hash_contract": "SHA256_EXACT_BUNDLE_MANIFEST_BYTES",
    }
    write_json(bundle / "bundle_manifest.json", bundle_manifest)
    artifact_sha = validator.validate_bundle(bundle, root)
    return bundle, artifact_sha


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    bundle, digest = build(args.root, args.output_dir)
    print(f"QC_PROVENANCE_BUNDLE=PASS bundle={bundle.name} artifact_sha256={digest}")


if __name__ == "__main__":
    main()
