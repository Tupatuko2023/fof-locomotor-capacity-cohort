import copy
import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "artifact_registry"
VALIDATOR_PATH = ROOT / "scripts" / "validation" / "validate_artifact_registry.py"
SPEC = importlib.util.spec_from_file_location("artifact_registry_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ArtifactRegistryTests(unittest.TestCase):
    def assert_invalid(self, registry, code):
        with self.assertRaises(validator.ValidationError) as caught:
            validator.validate_registry(registry)
        self.assertEqual(caught.exception.code, code)

    def test_positive_synthetic_fixtures(self):
        names = (
            "valid_empty_registry.json",
            "valid_design_candidate.json",
            "valid_synthetic_candidate.json",
            "valid_synthetic_validated.json",
            "valid_publication_approved.json",
        )
        for name in names:
            with self.subTest(name=name):
                validator.validate_registry(load(name))

    def test_canonical_registry_is_empty(self):
        registry = json.loads(
            (ROOT / "config" / "artifacts" / "artifact_registry.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["artifacts"], [])
        validator.validate_registry(registry)

    def test_invalid_fixture_matrix_is_complete(self):
        cases = load("invalid_cases.json")["synthetic_test_cases"]
        self.assertEqual(len(cases), len(set(cases)))
        self.assertEqual(set(cases), {
            "unknown_field", "duplicate_id", "duplicate_reference", "bad_enum",
            "p_value_field", "n_field", "participant_id_field", "token_pattern",
            "protected_path", "missing_checksum", "short_git_sha",
            "disclosure_approval_without_reference", "publication_before_disclosure",
            "supersession_cycle", "unknown_placeholder", "synthetic_as_research_result",
        })

    def test_allowed_fields_and_enums_fail_closed(self):
        base = load("valid_design_candidate.json")
        artifact = base["artifacts"][0]
        for field in ("unknown_test_field", "p_value", "n", "participant_id"):
            case = copy.deepcopy(base)
            case["artifacts"][0][field] = "SYNTHETIC_TEST_SENTINEL"
            self.assert_invalid(case, "FORBIDDEN_FIELD" if field != "unknown_test_field" else "UNKNOWN_FIELD")
        case = copy.deepcopy(base)
        case["artifacts"][0]["artifact_status"] = "UNKNOWN_STATUS"
        self.assert_invalid(case, "ENUM")

    def test_duplicate_ids_and_reference_keys(self):
        base = load("valid_design_candidate.json")
        duplicate = copy.deepcopy(base["artifacts"][0])
        duplicate["manuscript_reference_key"] = "TEST_TBL_DESIGN_02"
        base["artifacts"].append(duplicate)
        self.assert_invalid(base, "DUPLICATE_ID")
        base = load("valid_design_candidate.json")
        duplicate = copy.deepcopy(base["artifacts"][0])
        duplicate["artifact_id"] = "TEST-TBL-DESIGN-02"
        base["artifacts"].append(duplicate)
        self.assert_invalid(base, "DUPLICATE_REFERENCE")

    def test_provenance_and_path_rules(self):
        case = load("valid_synthetic_validated.json")
        del case["artifacts"][0]["artifact_sha256"]
        self.assert_invalid(case, "MISSING_ARTIFACT_CHECKSUM")
        case = load("valid_synthetic_candidate.json")
        case["artifacts"][0]["generator"]["repository_revision"] = "abcdef0"
        self.assert_invalid(case, "DIGEST_FORMAT")
        case = load("valid_design_candidate.json")
        case["artifacts"][0]["candidate_output_path"] = "data/restricted/test-output.csv"
        self.assert_invalid(case, "FORBIDDEN_ROOT")

    def test_secret_errors_do_not_echo_rejected_content(self):
        case = load("valid_design_candidate.json")
        sentinel = "token=SYNTHETIC_TEST_CREDENTIAL_SENTINEL"
        case["artifacts"][0]["title"] = sentinel
        self.assert_invalid(case, "SECRET_PATTERN")
        temporary = FIXTURES / ".invalid_secret_runtime.json"
        temporary.write_text(json.dumps(case), encoding="utf-8")
        try:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = validator.main([str(temporary)])
            self.assertEqual(result, 1)
            self.assertNotIn(sentinel, stderr.getvalue())
        finally:
            temporary.unlink(missing_ok=True)

    def test_disclosure_and_publication_invariants(self):
        case = load("valid_publication_approved.json")
        del case["artifacts"][0]["disclosure_decision_reference"]
        self.assert_invalid(case, "DISCLOSURE_EVIDENCE")
        case = load("valid_publication_approved.json")
        case["artifacts"][0]["disclosure_state"] = "PENDING"
        del case["artifacts"][0]["disclosure_decision_reference"]
        self.assert_invalid(case, "PUBLICATION_BEFORE_DISCLOSURE")

    def test_supersession_cycles_fail(self):
        registry = load("valid_design_candidate.json")
        first = registry["artifacts"][0]
        second = copy.deepcopy(first)
        second["artifact_id"] = "TEST-TBL-DESIGN-02"
        second["manuscript_reference_key"] = "TEST_TBL_DESIGN_02"
        first["supersedes"] = second["artifact_id"]
        second["supersedes"] = first["artifact_id"]
        registry["artifacts"].append(second)
        self.assert_invalid(registry, "SUPERSESSION_CYCLE")

    def test_placeholder_contract(self):
        registry = validator.validate_registry(load("valid_synthetic_candidate.json"))
        valid = (FIXTURES / "placeholders_valid.qmd").read_text(encoding="utf-8")
        validator.validate_placeholders(valid, registry)
        unknown = (FIXTURES / "placeholders_unknown.qmd").read_text(encoding="utf-8")
        with self.assertRaisesRegex(validator.ValidationError, "UNKNOWN_PLACEHOLDER"):
            validator.validate_placeholders(unknown, registry)
        research = (FIXTURES / "placeholders_synthetic_research.qmd").read_text(encoding="utf-8")
        with self.assertRaisesRegex(validator.ValidationError, "SYNTHETIC_RESEARCH_RESULT"):
            validator.validate_placeholders(research, registry)

    def test_schema_and_validator_enums_are_aligned(self):
        schema = load_from_path(ROOT / "config" / "artifacts" / "artifact_registry.schema.json")
        properties = schema["$defs"]["artifact"]["properties"]
        self.assertEqual(set(properties["artifact_status"]["enum"]), validator.ARTIFACT_STATUSES)
        self.assertEqual(set(properties["disclosure_state"]["enum"]), validator.DISCLOSURE_STATES)
        self.assertEqual(set(properties["publication_status"]["enum"]), validator.PUBLICATION_STATUSES)


def load_from_path(path):
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
