import importlib.util
import json
import unittest
from pathlib import Path
from urllib.error import HTTPError


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "zenodo" / "zenodo_sandbox_diagnostic.py"
SPEC = importlib.util.spec_from_file_location("zenodo_sandbox_diagnostic", MODULE_PATH)
diagnostic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagnostic)


class Response:
    def __init__(self, payload, url):
        self.payload = json.dumps(payload).encode()
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def geturl(self):
        return self.url

    def read(self):
        return self.payload


class DiagnosticTests(unittest.TestCase):
    def test_exact_get_allowlist_and_bearer_header(self):
        calls = []

        def opener(request, timeout):
            calls.append((request.method, request.full_url, request.get_header("Authorization"), timeout))
            return Response({"id": 587120}, request.full_url)

        diagnostic.authenticated_get(diagnostic.DRAFT_URL, "not-a-real-token", opener)
        diagnostic.authenticated_get(diagnostic.FILES_URL, "not-a-real-token", opener)
        self.assertEqual([call[:2] for call in calls], [
            ("GET", diagnostic.DRAFT_URL),
            ("GET", diagnostic.FILES_URL),
        ])
        self.assertTrue(all(call[2] == "Bearer not-a-real-token" for call in calls))
        with self.assertRaises(diagnostic.Stop):
            diagnostic.authenticated_get(diagnostic.DRAFT_URL + "/unexpected", "x", opener)
        with self.assertRaises(diagnostic.Stop):
            diagnostic.authenticated_get("https://zenodo.org/api/deposit/depositions/587120", "x", opener)

    def test_redirect_and_http_error_fail_closed(self):
        with self.assertRaisesRegex(diagnostic.Stop, "redirect refused"):
            diagnostic.RejectRedirects().redirect_request(
                None, None, 302, "found", {}, "https://evil.invalid/steal"
            )
        redirect = lambda request, timeout: Response({}, diagnostic.FILES_URL)
        with self.assertRaisesRegex(diagnostic.Stop, "response URL differs"):
            diagnostic.authenticated_get(diagnostic.DRAFT_URL, "x", redirect)

        def forbidden(request, timeout):
            raise HTTPError(request.full_url, 403, "forbidden", {}, None)

        with self.assertRaisesRegex(diagnostic.Stop, "HTTP 403"):
            diagnostic.authenticated_get(diagnostic.DRAFT_URL, "x", forbidden)

    def test_report_is_redacted_and_preserves_license_shape(self):
        draft = {
            "id": 587120,
            "submitted": False,
            "published": False,
            "state": "unsubmitted",
            "status": "draft",
            "modified": "2026-08-14T16:13:06Z",
            "metadata": {
                "title": "Public title",
                "license": {"id": "mit", "title": "MIT License"},
                "related_identifiers": [{
                    "identifier": diagnostic.EXPECTED_REPOSITORY_IDENTIFIER,
                    "relation": "isSupplementTo",
                    "scheme": "url",
                    "resource_type": "software",
                    "server_detail": {"normalized": True},
                }],
            },
            "links": {"bucket": "https://sandbox.zenodo.org/api/files/secret-bucket"},
            "owner": 123,
        }
        files = [{
            "filename": "example.zip",
            "filesize": 42,
            "checksum": "md5:secret",
            "links": {"download": "https://example.invalid/private"},
        }]
        report = diagnostic.redacted_report(draft, files)
        self.assertEqual(report["metadata_license_shape"], {"id": "string", "title": "string"})
        self.assertEqual(report["metadata_license_semantic_value"], "mit")
        related = report["metadata_related_identifiers"]
        self.assertEqual((related["field_type"], related["item_count"]), ("list", 1))
        self.assertEqual(related["items"][0]["semantic_values"], {
            "relation": "isSupplementTo", "scheme": "url", "resource_type": "software",
        })
        self.assertEqual(related["items"][0]["field_types"]["server_detail"], {"normalized": "boolean"})
        self.assertTrue(related["items"][0]["identifier_matches_expected"])
        self.assertEqual(report["files"], [{"filename": "example.zip", "filesize": 42}])
        serialized = json.dumps(report)
        for forbidden in (
            "secret-bucket", "md5:secret", "owner", "download",
            diagnostic.EXPECTED_REPOSITORY_IDENTIFIER,
        ):
            self.assertNotIn(forbidden, serialized)

    def test_related_identifiers_safe_mismatch_and_malformed_shapes(self):
        mismatch = diagnostic.related_identifiers_report([{
            "identifier": "https://example.invalid/different",
            "relation": "isSupplementTo",
        }])
        self.assertFalse(mismatch["items"][0]["identifier_matches_expected"])
        self.assertNotIn("example.invalid", json.dumps(mismatch))
        malformed = (
            None,
            {},
            "not-a-list",
            ["not-an-object"],
            [{}],
            [{"identifier": 1, "relation": "isSupplementTo"}],
            [{"identifier": "x", "relation": None}],
            [{"identifier": "x", "relation": "unsafe value with spaces"}],
            [{"identifier": "x", "relation": "isSupplementTo", "scheme": {"unsafe": True}}],
        )
        for value in malformed:
            with self.assertRaises(diagnostic.Stop, msg=repr(value)):
                diagnostic.related_identifiers_report(value)

    def test_wrong_id_and_non_list_files_stop(self):
        with self.assertRaises(diagnostic.Stop):
            diagnostic.redacted_report({"id": 1, "metadata": {}}, [])
        with self.assertRaises(diagnostic.Stop):
            diagnostic.redacted_report({"id": 587120, "metadata": {}}, {})

    def test_workflow_static_security_boundary(self):
        workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "zenodo_sandbox_diagnostic.yml").read_text()
        script = MODULE_PATH.read_text()
        self.assertIn("environment: zenodo-sandbox", workflow)
        self.assertIn("secrets.ZENODO_SANDBOX_TOKEN", workflow)
        self.assertNotIn("curl", workflow)
        self.assertNotIn("set -x", workflow)
        for method in ('method="POST"', 'method="PUT"', 'method="PATCH"', 'method="DELETE"'):
            self.assertNotIn(method, script)
        self.assertNotIn("zenodo.org/api", script.replace("sandbox.zenodo.org/api", ""))
        self.assertEqual(diagnostic.ALLOWED_URLS, frozenset((diagnostic.DRAFT_URL, diagnostic.FILES_URL)))


if __name__ == "__main__":
    unittest.main()
