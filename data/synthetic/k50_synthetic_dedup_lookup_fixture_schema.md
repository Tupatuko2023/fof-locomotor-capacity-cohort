# K50 Synthetic Dedup Lookup Fixture

## Purpose

This fixture provides the smallest wholly synthetic workbook needed to exercise the existing K50 person-dedup lookup path without accessing protected source data or changing deduplication semantics.

It is for structural smoke testing only. It is not participant-derived, not scientifically representative, and not suitable for analytical, linkage, numerical, or clinical interpretation.

## Files

- Workbook: `data/synthetic/k50_synthetic_dedup_lookup_root/paper_02/KAAOS_data_sotullinen.xlsx`
- Documentation: `data/synthetic/k50_synthetic_dedup_lookup_fixture_schema.md`

The nested `paper_02/KAAOS_data_sotullinen.xlsx` path mirrors the path that the current code constructs under `DATA_ROOT`. The root is synthetic and must be supplied explicitly in a process-local environment when used for smoke testing.

## Generation Method

The workbook was generated locally as a minimal OOXML `.xlsx` file with one visible worksheet and fixed synthetic cell values. No participant-level files, restricted data, real workbook rows, real identifiers, real linkage keys, cohort distributions, dates, or source-data paths were used.

## Structural Contract From Code

The current K50 dedup lookup code expects:

- File format: Excel workbook readable by `readxl`.
- Resolved path: `file.path(DATA_ROOT, "paper_02", "KAAOS_data_sotullinen.xlsx")`.
- Sheet detection: exactly one sheet/read-spec combination must contain one supported identity column and one bridge key compatible with the canonical input.
- Supported identity column names after lowercase normalization: `hetu`, `sotu`, `ssn`, or `socialsecuritynumber`.
- Bridge key: either exactly one shared bridge-like column name with the canonical input, or the alias pair canonical `id` to lookup `nro`.
- Bridge-like names include `id`, names ending in `_id`, `nro`, names ending in `_nro`, or names containing `participant`, `record`, `study`, `subject`, or `person`.
- Missing bridge or identity values are dropped before the lookup is used.
- Distinct bridge/identity pairs are retained.
- A bridge value must not map to multiple identity values.
- Unmatched analysis rows are allowed and fall back to `id:` person keys.

The code does not require a specific workbook row count beyond at least one non-missing bridge/identity pair. This fixture uses four rows so every ID in `k50_long_structural_fixture.csv` can match structurally.

## Fixture Schema

| Column | Type | Role | Synthetic pattern |
|---|---|---|---|
| `id` | character | bridge key shared with K50 canonical input | `SYN-K50-001` through `SYN-K50-004` |
| `ssn` | character | supported identity column name for existing lookup code | `SYNLOOKUPKEY001` through `SYNLOOKUPKEY004` |

## Artificial Row Rationale

The workbook has four data rows:

- `SYN-K50-001` maps to `SYNLOOKUPKEY001`
- `SYN-K50-002` maps to `SYNLOOKUPKEY002`
- `SYN-K50-003` maps to `SYNLOOKUPKEY003`
- `SYN-K50-004` maps to `SYNLOOKUPKEY004`

These rows are the minimum needed to match all four synthetic IDs in the existing LONG fixture while avoiding artificial duplicate-person outcomes, conflict cases, or cohort-like prevalence patterns.

## Safety Notes

- The `ssn` column name is used only because it is an existing supported structural identity-column name in the code.
- The `ssn` values are artificial tokens, not real social security numbers or realistic linkage keys.
- The fixture contains no hidden study data, participant rows, protected paths, names, dates, secrets, or source workbook content.
- Duplicate-person and ambiguity scenarios are intentionally not represented in this fixture. Those would require a separate approved structural test case because they exercise selection behavior rather than only lookup injection.

## Intended Smoke Setup

Use a process-local synthetic `DATA_ROOT` only:

```sh
DATA_ROOT="$(pwd)/data/synthetic/k50_synthetic_dedup_lookup_root" \
Rscript scripts/K50/K50.r --shape LONG --outcome locomotor_capacity --data data/synthetic/k50_long_structural_fixture.csv
```

This setup points the existing path resolver at the synthetic workbook without changing join, dedup, fallback, or selection semantics.
