#!/usr/bin/env python3
"""Build a fail-closed, explicitly allowlisted public cohort ZIP."""
from __future__ import annotations

import argparse
import hashlib
import posixpath
from pathlib import Path, PurePosixPath
import re
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile
import xml.etree.ElementTree as ET

ALLOWLIST = (
    "CHANGELOG.md", "CITATION.cff", "DESCRIPTION", "LICENSE", "README.md",
    "_quarto.yml", "fof-locomotor-capacity-cohort.Rproj",
    "R/functions/init.R", "R/functions/person_dedup_lookup.R",
    "R/functions/reporting.R", "R/transform_locomotor_indicators.R",
    "scripts/01_generate_synthetic_fixture.R", "scripts/K50/K50.r",
    "scripts/demo/run_public_traceability.R", "data/README.md",
    "data/synthetic/k50_long_structural_fixture.csv",
    "data/synthetic/k50_long_structural_fixture_schema.md",
    "data/synthetic/k50_synthetic_dedup_lookup_fixture_schema.md",
    "data/synthetic/k50_synthetic_dedup_lookup_root/paper_02/KAAOS_data_sotullinen.xlsx",
    "data/synthetic/k50_wide_authoritative_test_control.lock",
    "data/synthetic/k50_wide_structural_fixture.csv",
    "data/synthetic/synthetic_fixture.csv",
    "manuscript/public_traceability_demo.qmd", "manuscript/smoke_test.qmd",
    "tests/testthat.R", "tests/testthat/test_k50_synthetic_wide_test_control.R",
    "tests/testthat/test_public_traceability_demo.R",
    "tests/testthat/test_transform_locomotor_indicators.R",
    "docs/k50_migration_provenance.md", "docs/project_specification.md",
    "docs/reproducibility_scope.md", "docs/restricted_data_policy.md",
    "docs/v0.1.0_release_runbook.md",
)
GENERATED = ("manifest.txt", "SHA256SUMS")
XLSX_PATH = ALLOWLIST[18]
FORBIDDEN_PREFIXES = ("GPT/", ".git/", "outputs/", "data/raw/", "data/restricted/", "secrets/", "credentials/")
FORBIDDEN_NAMES = {"AGENTS.md", ".env", ".RData", ".Rhistory"}
FORBIDDEN_SUFFIXES = {".rds", ".rda", ".rdata", ".sqlite", ".db", ".mdb", ".accdb", ".parquet", ".feather", ".sav", ".dta", ".sas7bdat", ".zip", ".tar", ".gz", ".7z", ".env", ".key", ".pem", ".p12", ".pfx"}
SECRET_RE = re.compile(rb"(?i)(authorization\s*:\s*bearer\s+\S+|(?:github|ghp|zenodo|aws)[_-]?(?:access[_-]?)?(?:token|key|secret)\s*[=:]\s*\S+|-----BEGIN [A-Z ]*PRIVATE KEY-----|aws_access_key_id\s*[=:]\s*\S+|aws_secret_access_key\s*[=:]\s*\S+|(?:secret|token|password)\s*[=:]\s*['\"]?[^\s'\"$<{]{4,})")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
XLSX_MEMBERS = {"[Content_Types].xml", "_rels/.rels", "docProps/core.xml", "docProps/app.xml", "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/worksheets/sheet1.xml"}
XLSX_ROWS = [("id", "ssn")] + [(f"SYN-K50-{i:03d}", f"SYNLOOKUPKEY{i:03d}") for i in range(1, 5)]
XLSX_SHA256 = "86d90c707bf5fc927fddfc86dc19067440feda36e17beb6e0f8ba3d16c260058"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/package/2006/relationships"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_member(name: str) -> None:
    p = PurePosixPath(name)
    if not name or p.is_absolute() or ".." in p.parts or "\\" in name:
        raise ValueError(f"unsafe archive path: {name}")
    if name in FORBIDDEN_NAMES or name.startswith(FORBIDDEN_PREFIXES):
        raise ValueError(f"forbidden path: {name}")
    if PurePosixPath(name).suffix.lower() in FORBIDDEN_SUFFIXES and name != XLSX_PATH:
        raise ValueError(f"forbidden file suffix: {name}")

def validate_xlsx(path: Path) -> None:
    if sha256(path) != XLSX_SHA256:
        raise ValueError("synthetic XLSX does not match the approved deterministic fixture")
    with zipfile.ZipFile(path) as book:
        names = book.namelist()
        if len(names) != len(set(names)) or set(names) != XLSX_MEMBERS:
            raise ValueError("synthetic XLSX OOXML member contract mismatch")
        for info in book.infolist():
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("synthetic XLSX contains a symlink member")
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        sheets = workbook.findall(".//m:sheet", NS)
        if len(sheets) != 1 or sheets[0].get("name") != "Taul1" or sheets[0].get("state", "visible") != "visible":
            raise ValueError("synthetic XLSX sheet contract mismatch")
        rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        relationships = [(x.get("Id"), x.get("Type"), x.get("Target"), x.get("TargetMode")) for x in rels]
        expected_rel = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet", "worksheets/sheet1.xml", None)]
        if relationships != expected_rel: raise ValueError("synthetic XLSX relationship contract mismatch")
        sheet = ET.fromstring(book.read("xl/worksheets/sheet1.xml"))
        if sheet.findall(".//m:cols/m:col[@hidden='1']", NS) or sheet.findall(".//m:row[@hidden='1']", NS):
            raise ValueError("synthetic XLSX contains hidden rows or columns")
        if sheet.findall(".//m:f", NS): raise ValueError("synthetic XLSX contains formulas")
        rows = []
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            cells=[]
            for cell in row.findall("m:c", NS):
                text=cell.find("m:is/m:t", NS)
                if cell.get("t") != "inlineStr" or text is None: raise ValueError("synthetic XLSX cell encoding mismatch")
                cells.append(text.text or "")
            rows.append(tuple(cells))
        if rows != XLSX_ROWS: raise ValueError("synthetic XLSX value/schema contract mismatch")
        core = ET.fromstring(book.read("docProps/core.xml")); app = ET.fromstring(book.read("docProps/app.xml"))
        core_values=[(x.text or "") for x in core]; app_values=[(x.text or "") for x in app]
        if core_values != ["synthetic-fixture-generator", "synthetic-fixture-generator"] or app_values != ["synthetic-fixture-generator"]:
            raise ValueError("synthetic XLSX metadata contract mismatch")
        all_text=b" ".join(book.read(n) for n in names)
        if re.search(rb"\b\d{6}[-+A]\d{3}[0-9A-Y]\b", all_text, re.I): raise ValueError("participant-derived identifier pattern detected")

def validate_sources(root: Path, allowlist=ALLOWLIST) -> None:
    if tuple(allowlist) != ALLOWLIST or len(set(allowlist)) != len(allowlist):
        raise ValueError("allowlist differs from approved exact manifest")
    for name in allowlist:
        validate_source_file(name, root / name)
    markdown = {
        name: (root / name).read_text(encoding="utf-8")
        for name in allowlist if PurePosixPath(name).suffix.lower() == ".md"
    }
    validate_markdown_link_closure(markdown, set(allowlist))
    validate_xlsx(root / XLSX_PATH)

def validate_markdown_link_closure(markdown: dict[str, str], members: set[str]) -> None:
    for source, content in markdown.items():
        for match in MARKDOWN_LINK_RE.finditer(content):
            destination = match.group(1).strip()
            if destination.startswith("<") and ">" in destination:
                destination = destination[1:destination.index(">")]
            else:
                destination = destination.split(maxsplit=1)[0]
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme.lower() not in {"http", "https", "mailto"}:
                    raise ValueError(f"unsupported Markdown link scheme in {source}: {destination}")
                continue
            if not parsed.path:
                continue
            path = unquote(parsed.path)
            if path.startswith(("/", "\\")) or "\\" in path:
                raise ValueError(f"unsafe Markdown link in {source}: {destination}")
            target = posixpath.normpath((PurePosixPath(source).parent / path).as_posix())
            safe_member(target)
            if target not in members:
                raise ValueError(f"Markdown link target is outside the curated bundle: {source} -> {target}")

def validate_source_file(name: str, path: Path) -> None:
    safe_member(name)
    if not path.exists(): raise FileNotFoundError(name)
    if path.is_symlink() or not path.is_file(): raise ValueError(f"not a regular non-symlink file: {name}")
    if SECRET_RE.search(path.read_bytes()): raise ValueError(f"secret-like content detected: {name}")

def build(root: Path, output_dir: Path) -> tuple[Path, str]:
    validate_sources(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = output_dir / "fof-locomotor-capacity-cohort-0.1.0.zip"
    hashes = [(sha256(root / name), name) for name in ALLOWLIST]
    manifest = "".join(f"{name}\n" for name in ALLOWLIST).encode()
    sums = "".join(f"{digest}  {name}\n" for digest, name in hashes).encode()
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ALLOWLIST: archive.write(root / name, name)
        archive.writestr("manifest.txt", manifest)
        archive.writestr("SHA256SUMS", sums)
    verify_archive(bundle)
    digest = sha256(bundle)
    (output_dir / "bundle.sha256").write_text(f"{digest}  {bundle.name}\n", encoding="utf-8")
    return bundle, digest

def verify_archive(bundle: Path) -> None:
    expected = set(ALLOWLIST + GENERATED)
    with zipfile.ZipFile(bundle) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)) or set(names) != expected: raise ValueError("archive manifest mismatch")
        for info in infos:
            safe_member(info.filename)
            if (info.external_attr >> 16) & 0o170000 == 0o120000: raise ValueError("symlink in archive")
        if archive.read("manifest.txt").decode().splitlines() != list(ALLOWLIST): raise ValueError("embedded manifest mismatch")
        markdown = {
            name: archive.read(name).decode("utf-8")
            for name in ALLOWLIST if PurePosixPath(name).suffix.lower() == ".md"
        }
        validate_markdown_link_closure(markdown, set(names))
        recorded = dict(line.split("  ", 1)[::-1] for line in archive.read("SHA256SUMS").decode().splitlines())
        for name in ALLOWLIST:
            if hashlib.sha256(archive.read(name)).hexdigest() != recorded.get(name): raise ValueError(f"checksum mismatch: {name}")
        with tempfile.TemporaryDirectory() as tmp:
            archive.extractall(tmp)
            extracted = {p.relative_to(tmp).as_posix() for p in Path(tmp).rglob("*") if p.is_file()}
            if extracted != expected: raise ValueError("re-extracted manifest mismatch")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    bundle, digest = build(args.root.resolve(), args.output_dir.resolve())
    print(f"BUNDLE_SAFETY=PASS bundle={bundle.name} sha256={digest}")

if __name__ == "__main__": main()
