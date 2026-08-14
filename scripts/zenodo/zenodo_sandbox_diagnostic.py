#!/usr/bin/env python3
"""Read-only, redacted diagnostic for one approved Zenodo Sandbox draft."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


ORIGIN = "https://sandbox.zenodo.org"
DRAFT_ID = "587120"
DRAFT_URL = f"{ORIGIN}/api/deposit/depositions/{DRAFT_ID}"
FILES_URL = f"{DRAFT_URL}/files"
ALLOWED_URLS = frozenset((DRAFT_URL, FILES_URL))
EXPECTED_REPOSITORY_IDENTIFIER = "https://github.com/Tupatuko2023/fof-locomotor-capacity-cohort"
SEMANTIC_KEYS = ("relation", "scheme", "resource_type", "resource-type", "type")
SAFE_SEMANTIC_VALUE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,63}")


class Stop(RuntimeError):
    pass


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Stop("redirect refused for authenticated diagnostic GET")


def default_opener(request, timeout):
    return build_opener(RejectRedirects()).open(request, timeout=timeout)


def authenticated_get(url, token, opener=default_opener):
    if url not in ALLOWED_URLS:
        raise Stop("request URL is outside the diagnostic allowlist")
    request = Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
    try:
        with opener(request, 60) as response:
            if response.geturl() != url:
                raise Stop("response URL differs from the approved request URL")
            payload = response.read()
    except Stop:
        raise
    except HTTPError as error:
        raise Stop(f"Sandbox diagnostic GET stopped with HTTP {error.code}") from None
    except (URLError, TimeoutError, json.JSONDecodeError):
        raise Stop("Sandbox diagnostic GET failed closed") from None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        raise Stop("Sandbox diagnostic response was not JSON") from None


def json_shape(value):
    if isinstance(value, dict):
        return {key: json_shape(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [json_shape(value[0])] if value else []
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    return "string"


def license_semantic_value(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("id", "identifier", "name", "title"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
    return None


def related_identifiers_report(value):
    if not isinstance(value, list):
        raise Stop("diagnostic related_identifiers was not a list")
    safe_items = []
    expected_hash = hashlib.sha256(EXPECTED_REPOSITORY_IDENTIFIER.encode()).hexdigest()
    for item in value:
        if not isinstance(item, dict):
            raise Stop("diagnostic related_identifiers item was not an object")
        identifier = item.get("identifier")
        relation = item.get("relation")
        if not isinstance(identifier, str) or not isinstance(relation, str):
            raise Stop("diagnostic related_identifiers required field was not a string")
        semantic_values = {}
        for key in SEMANTIC_KEYS:
            if key not in item:
                continue
            semantic = item[key]
            if not isinstance(semantic, str) or not SAFE_SEMANTIC_VALUE.fullmatch(semantic):
                raise Stop("diagnostic related_identifiers semantic field was unsafe")
            semantic_values[key] = semantic
        actual_hash = hashlib.sha256(identifier.encode()).hexdigest()
        safe_items.append({
            "key_names": sorted(item),
            "field_types": {key: json_shape(item[key]) for key in sorted(item)},
            "semantic_values": semantic_values,
            "identifier_type": "string",
            "identifier_matches_expected": actual_hash == expected_hash,
        })
    return {
        "field_type": "list",
        "item_count": len(safe_items),
        "items": safe_items,
    }


def redacted_report(draft, files):
    if str(draft.get("id")) != DRAFT_ID:
        raise Stop("diagnostic response draft ID mismatch")
    if not isinstance(files, list):
        raise Stop("diagnostic files response was not a list")
    metadata = draft.get("metadata")
    if not isinstance(metadata, dict):
        raise Stop("diagnostic metadata was not an object")
    license_value = metadata.get("license")
    related_identifiers = related_identifiers_report(metadata.get("related_identifiers"))
    safe_files = []
    for item in files:
        if not isinstance(item, dict):
            raise Stop("diagnostic file entry was not an object")
        safe_files.append({
            "filename": item.get("filename"),
            "filesize": item.get("filesize"),
        })
    return {
        "draft_id": DRAFT_ID,
        "submitted": draft.get("submitted"),
        "published": draft.get("published"),
        "state": draft.get("state"),
        "status": draft.get("status"),
        "modified": draft.get("modified"),
        "metadata_license_shape": json_shape(license_value),
        "metadata_license_semantic_value": license_semantic_value(license_value),
        "metadata_related_identifiers": related_identifiers,
        "metadata_key_names": sorted(metadata),
        "file_count": len(safe_files),
        "files": safe_files,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    token = os.environ.get("ZENODO_SANDBOX_TOKEN")
    if not token:
        raise Stop("ZENODO_SANDBOX_TOKEN is required")
    draft = authenticated_get(DRAFT_URL, token)
    files = authenticated_get(FILES_URL, token)
    report = redacted_report(draft, files)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("SANDBOX_DIAGNOSTIC=PASS requests=2 methods=GET redaction=PASS")


if __name__ == "__main__":
    main()
