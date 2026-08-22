import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

validator = load_module("qc_provenance_validator_test", "scripts/validation/validate_qc_provenance_bundle.py")
builder = load_module("qc_provenance_builder_test", "scripts/demo/build_qc_provenance_bundle.py")

def write_json(path, value):
    path.write_bytes(validator.canonical_bytes(value))

def refresh_hash_chain(bundle):
    payload = json.loads((bundle / "payload_manifest.json").read_text())
    payload["members"] = [
        {"path": name, "role": name.rsplit(".", 1)[0], "sha256": validator.sha256_file(bundle / name)}
        for name in validator.PAYLOAD_FILES
    ]
    write_json(bundle / "payload_manifest.json", payload)
    payload_sha = validator.sha256_file(bundle / "payload_manifest.json")
    receipt = json.loads((bundle / "validation_receipt.json").read_text())
    receipt["payload_sha256"] = payload_sha
    write_json(bundle / "validation_receipt.json", receipt)
    manifest = json.loads((bundle / "bundle_manifest.json").read_text())
    names = tuple(name for name in validator.ALL_FILES if name != "bundle_manifest.json")
    manifest["members"] = [
        {"path": name, "role": name.rsplit(".", 1)[0], "sha256": validator.sha256_file(bundle / name)}
        for name in names
    ]
    manifest["payload_manifest_sha256"] = payload_sha
    manifest["validation_receipt_sha256"] = validator.sha256_file(bundle / "validation_receipt.json")
    write_json(bundle / "bundle_manifest.json", manifest)

class QCProvenanceBundleTests(unittest.TestCase):
    def build(self, parent):
        return builder.build(ROOT, parent)[0]

    def assert_json_mutation_rejected(self, filename, mutation):
        with tempfile.TemporaryDirectory() as td:
            bundle = self.build(Path(td))
            path = bundle / filename
            value = json.loads(path.read_text())
            mutation(value)
            write_json(path, value)
            refresh_hash_chain(bundle)
            with self.assertRaises(validator.BundleValidationError):
                validator.validate_bundle(bundle, ROOT)

    def test_deterministic_exact_eight_member_hash_contract(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one, digest_one = builder.build(ROOT, Path(first))
            two, digest_two = builder.build(ROOT, Path(second))
            self.assertEqual(digest_one, digest_two)
            self.assertEqual(sorted(path.name for path in one.iterdir()), list(validator.ALL_FILES))
            self.assertEqual(len(validator.ALL_FILES), 8)
            for name in validator.ALL_FILES:
                self.assertEqual((one / name).read_bytes(), (two / name).read_bytes())
            self.assertEqual(digest_one, validator.sha256_file(one / "bundle_manifest.json"))
            self.assertEqual(digest_one, validator.validate_bundle(one, ROOT))

    def test_receipt_disclaimer_registry_and_state_separation(self):
        with tempfile.TemporaryDirectory() as td:
            bundle = self.build(Path(td))
            payload = json.loads((bundle / "payload_manifest.json").read_text())
            receipt = json.loads((bundle / "validation_receipt.json").read_text())
            manifest = json.loads((bundle / "bundle_manifest.json").read_text())
            self.assertEqual(receipt["payload_sha256"], validator.sha256_file(bundle / "payload_manifest.json"))
            self.assertEqual(manifest["payload_manifest_sha256"], receipt["payload_sha256"])
            self.assertEqual(manifest["synthetic_disclaimer"], validator.DISCLAIMER)
            self.assertEqual(payload["timestamp_policy"], validator.TIMESTAMP_POLICY)
            registry = json.loads((ROOT / "config/artifacts/artifact_registry.json").read_text())
            item = next(x for x in registry["artifacts"] if x["artifact_id"] == validator.ARTIFACT_ID)
            self.assertEqual((item["artifact_status"], item["disclosure_state"], item["publication_status"]),
                             ("SYNTHETIC_CANDIDATE", "NOT_APPLICABLE_SYNTHETIC", "NOT_APPROVED"))
            self.assertNotIn("artifact_sha256", item)
            self.assertNotIn("validation_receipt_reference", item)

    def test_missing_extra_and_renamed_members_fail(self):
        for mode in ("missing", "extra", "renamed"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as td:
                bundle = self.build(Path(td))
                if mode == "missing": (bundle / "qc_table.csv").unlink()
                elif mode == "extra": (bundle / "unexpected.txt").write_text("synthetic")
                else: (bundle / "qc_table.csv").rename(bundle / "qc.csv")
                with self.assertRaisesRegex(validator.BundleValidationError, "MEMBER_SET"):
                    validator.validate_bundle(bundle, ROOT)

    def test_modified_byte_and_invalid_hash_fail(self):
        with tempfile.TemporaryDirectory() as td:
            bundle = self.build(Path(td))
            with (bundle / "qc_table.csv").open("ab") as stream: stream.write(b"x")
            with self.assertRaises(validator.BundleValidationError): validator.validate_bundle(bundle, ROOT)
        with tempfile.TemporaryDirectory() as td:
            bundle = self.build(Path(td))
            manifest = json.loads((bundle / "payload_manifest.json").read_text())
            manifest["members"][0]["sha256"] = "0" * 64
            write_json(bundle / "payload_manifest.json", manifest)
            with self.assertRaises(validator.BundleValidationError): validator.validate_bundle(bundle, ROOT)

    def test_unsafe_metadata_and_unknown_fields_fail(self):
        cases = (
            ("runtime_metadata.json", lambda x: x.update({"unknown_field": "x"})),
            ("synthetic_input_receipt.json", lambda x: x.update({"input_reference": "/private/input.csv"})),
            ("synthetic_input_receipt.json", lambda x: x.update({"input_reference": "production_snapshot_01"})),
            ("runtime_metadata.json", lambda x: x.update({"participant_id": "synthetic"})),
            ("runtime_metadata.json", lambda x: x.update({"runtime_profile": "token=synthetic-secret"})),
            ("runtime_metadata.json", lambda x: x.update({"runtime_profile": "raw sessionInfo()"})),
            ("runtime_metadata.json", lambda x: x.update({"estimate": "synthetic-result"})),
        )
        for filename, mutation in cases:
            with self.subTest(filename=filename): self.assert_json_mutation_rejected(filename, mutation)

    def test_disclaimer_validator_generator_and_control_tampering_fail(self):
        cases = (
            ("decision_evidence.json", lambda x: x.pop("synthetic_disclaimer")),
            ("validation_receipt.json", lambda x: x.update({"validator_sha256": "0" * 64})),
            ("runtime_metadata.json", lambda x: x.update({"generator_sha256": "0" * 64})),
            ("synthetic_input_receipt.json", lambda x: x.update({"input_sha256": "0" * 64})),
        )
        for filename, mutation in cases:
            with self.subTest(filename=filename): self.assert_json_mutation_rejected(filename, mutation)

    def test_schema_declares_public_synthetic_contract(self):
        schema = json.loads((ROOT / "config/artifacts/qc_provenance_bundle.schema.json").read_text())
        self.assertEqual(schema["properties"]["artifact_id"]["const"], validator.ARTIFACT_ID)
        self.assertEqual(schema["properties"]["data_classification"]["const"], validator.CLASSIFICATION)
        self.assertEqual(schema["properties"]["exact_member_names"]["minItems"], 8)
        self.assertEqual(schema["properties"]["members"]["minItems"], 7)

if __name__ == "__main__": unittest.main()
