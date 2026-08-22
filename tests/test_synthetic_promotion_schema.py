import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SyntheticPromotionSchemaTests(unittest.TestCase):
    def test_registry_schema_requires_validated_evidence_and_safe_states(self):
        schema = json.loads((ROOT / "config/artifacts/artifact_registry.schema.json").read_text())
        artifact = schema["$defs"]["artifact"]
        self.assertIn("validation_receipt_sha256", artifact["properties"])
        rule = artifact["allOf"][0]
        self.assertEqual(rule["if"]["properties"]["artifact_status"]["const"], "SYNTHETIC_VALIDATED")
        self.assertEqual(set(rule["then"]["required"]), {
            "candidate_output_path", "artifact_sha256",
            "validation_receipt_reference", "validation_receipt_sha256",
        })
        properties = rule["then"]["properties"]
        self.assertEqual(properties["required_inputs"]["const"], ["PUBLIC_SYNTHETIC_INPUT"])
        self.assertTrue(properties["provisional"]["const"])
        self.assertFalse(properties["protected_execution_required"]["const"])
        self.assertFalse(properties["disclosure_review_required"]["const"])
        self.assertEqual(properties["publication_status"]["const"], "NOT_APPROVED")
        self.assertTrue(properties["validation_required"]["const"])

    def test_receipt_schema_is_closed_deterministic_and_supports_both_profiles(self):
        schema = json.loads((ROOT / "config/artifacts/synthetic_promotion_receipt.schema.json").read_text())
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["properties"]["validation_profile"]["enum"]), {
            "SINGLE_FILE_TABLE_V1", "QC_PROVENANCE_BUNDLE_V1",
        })
        self.assertEqual(schema["properties"]["receipt_classification"]["const"], "PUBLIC_SYNTHETIC_VALIDATION")
        self.assertEqual(schema["properties"]["validation_result"]["const"], "PASS")
        self.assertEqual(schema["properties"]["timestamp_policy"]["const"], "OMITTED_FROM_CANONICAL_IDENTITY")
        self.assertEqual(set(schema["required"]), set(schema["properties"]))


if __name__ == "__main__":
    unittest.main()
