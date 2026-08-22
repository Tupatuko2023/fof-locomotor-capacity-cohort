import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


promotion = load_module("synthetic_promotion_test", "scripts/validation/validate_synthetic_promotion.py")
bundle_builder = load_module("qc_bundle_builder_promotion_test", "scripts/demo/build_qc_provenance_bundle.py")


def write_json(path, value):
    path.write_bytes(promotion.canonical_bytes(value))


def current_revision():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        stdout=subprocess.PIPE, text=True,
    ).stdout.strip()


class SyntheticPromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".promotion-", dir=ROOT / "tests")
        self.base = Path(self.temp.name)
        self.canonical = self.base / "canonical"
        self.canonical.mkdir()
        self.root_relative = self.canonical.relative_to(ROOT).as_posix()

    def tearDown(self):
        self.temp.cleanup()

    def source(self, path):
        return {
            "path": path,
            "repository_revision": current_revision(),
            "sha256": promotion.sha256_file(ROOT / path),
        }

    def input_bindings(self):
        fixture = "data/synthetic/k50_wide_structural_fixture.csv"
        control = "data/synthetic/k50_wide_authoritative_test_control.lock"
        return [{
            "input_classification": "PUBLIC_SYNTHETIC_INPUT",
            "input_reference": fixture,
            "input_sha256": promotion.sha256_file(ROOT / fixture),
            "control_reference": control,
            "control_sha256": promotion.sha256_file(ROOT / control),
        }]

    def make_case(self, profile="SINGLE_FILE_TABLE_V1"):
        revision = current_revision()
        validator = self.source("scripts/validation/validate_qc_provenance_bundle.py")
        if profile == "SINGLE_FILE_TABLE_V1":
            artifact_id = "TEST-TABLE-SYNTHETIC-01"
            artifact_type = "TABLE"
            artifact_path = self.canonical / "artifact.csv"
            artifact_path.write_bytes(b"field,status\nsynthetic,PASS\n")
            generator = self.source("scripts/K50/K50.r")
            hash_contract = "SHA256_EXACT_FILE_BYTES"
            checks = sorted(promotion.PROFILES[profile]["checks"])
            supporting = []
        else:
            artifact_id = "A1-SUPPLEMENT-QC-PROVENANCE-01"
            artifact_type = "SUPPLEMENT"
            bundle, _ = bundle_builder.build(ROOT, self.canonical)
            artifact_path = bundle / "bundle_manifest.json"
            generator = self.source("scripts/demo/build_qc_provenance_bundle.py")
            hash_contract = "SHA256_EXACT_BUNDLE_MANIFEST_BYTES"
            checks = sorted(promotion.PROFILES[profile]["checks"])
            evidence_path = bundle / "validation_receipt.json"
            supporting = [{
                "classification": "PUBLIC_SYNTHETIC_VALIDATION_EVIDENCE",
                "reference": evidence_path.relative_to(ROOT).as_posix(),
                "sha256": promotion.sha256_file(evidence_path),
            }]
        artifact_reference = artifact_path.relative_to(ROOT).as_posix()
        receipt_path = self.canonical / "promotion_validation_receipt.json"
        receipt = {
            "schema_version": "1.0.0",
            "receipt_id": f"{artifact_id}-VALIDATION-R1",
            "receipt_classification": "PUBLIC_SYNTHETIC_VALIDATION",
            "artifact_id": artifact_id,
            "artifact_revision": 1,
            "artifact_type": artifact_type,
            "artifact_path": artifact_reference,
            "artifact_sha256": promotion.sha256_file(artifact_path),
            "artifact_hash_contract": hash_contract,
            "generator_path": generator["path"],
            "generator_repository_revision": generator["repository_revision"],
            "generator_sha256": generator["sha256"],
            "synthetic_input_bindings": self.input_bindings(),
            "execution_identity_sha256": "0" * 64,
            "validator_path": validator["path"],
            "validator_repository_revision": validator["repository_revision"],
            "validator_sha256": validator["sha256"],
            "validation_profile": profile,
            "validation_result": "PASS",
            "validated_checks": checks,
            "supporting_evidence": supporting,
            "synthetic_disclaimer": promotion.DISCLAIMER,
            "timestamp_policy": promotion.TIMESTAMP_POLICY,
        }
        receipt["execution_identity_sha256"] = promotion.execution_identity(receipt)
        write_json(receipt_path, receipt)
        artifact = {
            "artifact_id": artifact_id,
            "artifact_revision": 1,
            "provisional": True,
            "artifact_type": artifact_type,
            "artifact_status": "SYNTHETIC_VALIDATED",
            "title": "Synthetic promotion contract test",
            "caption_status": "SYNTHETIC_DISCLAIMER",
            "analysis_source": "Wholly synthetic validation fixture",
            "generator": {"status": "EXISTS", **generator},
            "required_inputs": ["PUBLIC_SYNTHETIC_INPUT"],
            "data_classification": "PUBLIC_SYNTHETIC",
            "execution_environment": "PUBLIC_SYNTHETIC_TEST",
            "protected_execution_required": False,
            "scientific_approval_required": False,
            "disclosure_review_required": False,
            "disclosure_state": "NOT_APPLICABLE_SYNTHETIC",
            "publication_status": "NOT_APPROVED",
            "candidate_output_path": artifact_reference,
            "manuscript_destination": "NEEDS_VERIFICATION",
            "manuscript_reference_key": "TEST_SYNTHETIC_PROMOTION_01",
            "provenance_required": True,
            "validation_required": True,
            "validation_receipt_reference": receipt_path.relative_to(ROOT).as_posix(),
            "validation_receipt_sha256": promotion.sha256_file(receipt_path),
            "artifact_sha256": promotion.sha256_file(artifact_path),
            "supersedes": None,
        }
        registry = {"schema_version": "1.0.0", "registry_status": "ACTIVE", "project_id": "A1", "artifacts": [artifact]}
        registry_path = self.base / "registry.json"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        return registry, registry_path, receipt, receipt_path, artifact_path

    def persist(self, registry, registry_path, receipt, receipt_path, refresh_execution=False):
        if refresh_execution:
            receipt["execution_identity_sha256"] = promotion.execution_identity(receipt)
        write_json(receipt_path, receipt)
        registry["artifacts"][0]["validation_receipt_sha256"] = promotion.sha256_file(receipt_path)
        registry_path.write_text(json.dumps(registry), encoding="utf-8")

    def assert_invalid(self, registry_path, code=None, canonical_root=None):
        with self.assertRaises(promotion.PromotionValidationError) as caught:
            promotion.validate_promotion(
                registry_path, ROOT, [canonical_root or self.root_relative]
            )
        if code is not None:
            self.assertEqual(str(caught.exception), code)

    def test_table_and_bundle_profiles_pass(self):
        for profile in promotion.PROFILES:
            with self.subTest(profile=profile):
                if any(self.canonical.iterdir()):
                    self.tearDown(); self.setUp()
                _, registry_path, _, _, _ = self.make_case(profile)
                promotion.validate_promotion(registry_path, ROOT, [self.root_relative])

    def test_registry_cross_field_contract_fails_closed(self):
        registry, _, _, _, _ = self.make_case()
        mutations = (
            lambda x: x.pop("artifact_sha256"),
            lambda x: x.pop("validation_receipt_reference"),
            lambda x: x.update({"validation_required": False}),
            lambda x: x.update({"publication_status": "APPROVED"}),
            lambda x: x.update({"disclosure_state": "PENDING"}),
            lambda x: x.update({"provisional": False}),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                candidate = copy.deepcopy(registry)
                mutation(candidate["artifacts"][0])
                with self.assertRaises(promotion.registry_validator.ValidationError):
                    promotion.registry_validator.validate_registry(candidate)

    def test_receipt_and_artifact_binding_failures(self):
        cases = (
            ("stale_revision", lambda a, r: a.update({"artifact_revision": 2}), False),
            ("wrong_receipt_revision", lambda a, r: r.update({"artifact_revision": 2}), False),
            ("wrong_generator_hash", lambda a, r: r.update({"generator_sha256": "0" * 64}), False),
            ("wrong_generator_revision", lambda a, r: r.update({"generator_repository_revision": "0" * 40}), False),
            ("wrong_input_hash", lambda a, r: r["synthetic_input_bindings"][0].update({"input_sha256": "0" * 64}), True),
            ("wrong_control_hash", lambda a, r: r["synthetic_input_bindings"][0].update({"control_sha256": "0" * 64}), True),
            ("wrong_validator_hash", lambda a, r: r.update({"validator_sha256": "0" * 64}), False),
            ("missing_disclaimer", lambda a, r: r.pop("synthetic_disclaimer"), False),
            ("protected_reference", lambda a, r: r["synthetic_input_bindings"][0].update({"input_reference": "data/restricted/input.csv"}), True),
        )
        for label, mutation, refresh_execution in cases:
            with self.subTest(label=label):
                self.tearDown(); self.setUp()
                registry, registry_path, receipt, receipt_path, _ = self.make_case()
                mutation(registry["artifacts"][0], receipt)
                self.persist(registry, registry_path, receipt, receipt_path, refresh_execution)
                self.assert_invalid(registry_path)

    def test_missing_receipt_hash_mismatch_artifact_tamper_and_outside_root_fail(self):
        registry, registry_path, _, receipt_path, artifact_path = self.make_case()
        receipt_path.unlink()
        self.assert_invalid(registry_path)
        self.tearDown(); self.setUp()
        registry, registry_path, receipt, receipt_path, artifact_path = self.make_case()
        receipt_path.write_bytes(receipt_path.read_bytes() + b"x")
        self.assert_invalid(registry_path, "RECEIPT_HASH_MISMATCH")
        self.tearDown(); self.setUp()
        _, registry_path, _, _, artifact_path = self.make_case()
        artifact_path.write_bytes(artifact_path.read_bytes() + b"x")
        self.assert_invalid(registry_path, "ARTIFACT_HASH_MISMATCH")
        self.tearDown(); self.setUp()
        _, registry_path, _, _, _ = self.make_case()
        self.assert_invalid(registry_path, "OUTSIDE_CANONICAL_ROOT", "tests/nonexistent-canonical-root")

    def test_global_path_selection_and_validator_boundaries_fail(self):
        for canonical_root in (".", "GPT/canonical", ".git/canonical", "data/raw/canonical"):
            with self.subTest(canonical_root=canonical_root):
                with self.assertRaises(promotion.PromotionValidationError):
                    promotion.validate_promotion(
                        self.base / "missing.json", ROOT, [canonical_root]
                    )
        empty_registry = self.base / "empty_registry.json"
        empty_registry.write_text(json.dumps({
            "schema_version": "1.0.0", "registry_status": "ACTIVE",
            "project_id": "A1", "artifacts": [],
        }))
        self.assert_invalid(empty_registry, "VALIDATED_ARTIFACT_NOT_FOUND")
        registry, registry_path, receipt, receipt_path, _ = self.make_case()
        invalid_validator = self.source("scripts/K50/K50.r")
        receipt["validator_path"] = invalid_validator["path"]
        receipt["validator_repository_revision"] = invalid_validator["repository_revision"]
        receipt["validator_sha256"] = invalid_validator["sha256"]
        self.persist(registry, registry_path, receipt, receipt_path)
        self.assert_invalid(registry_path, "VALIDATOR_PATH_BOUNDARY")

    def test_static_receipt_and_invalid_case_fixtures_are_complete(self):
        valid_path = ROOT / "tests/fixtures/synthetic_promotion/valid_receipt_contract.json"
        raw = valid_path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
        self.assertEqual(raw, promotion.canonical_bytes(value))
        self.assertEqual(set(value), promotion.RECEIPT_FIELDS)
        cases = json.loads((ROOT / "tests/fixtures/synthetic_promotion/invalid_receipt_cases.json").read_text())["synthetic_test_cases"]
        self.assertEqual(len(cases), 17)
        self.assertEqual(len(cases), len(set(cases)))


if __name__ == "__main__":
    unittest.main()
