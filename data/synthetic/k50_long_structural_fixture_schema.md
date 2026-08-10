# K50 LONG Structural Synthetic Fixture

## Purpose

`k50_long_structural_fixture.csv` is a wholly synthetic LONG-shape fixture for K50 schema and data-loading smoke checks only. It is not participant-derived, not scientifically representative, and not suitable for analytical, numerical, or clinical interpretation.

## Generation Method

The fixture was hand-authored with simple artificial placeholder values. No participant-level files, restricted data, source-data rows, marginal distributions, missingness patterns, dates, linkage keys, or real identifiers were used.

## Scope

Initial scope is LONG only. WIDE is deferred because the migrated K50 WIDE path uses an authoritative input lock and should not be weakened or bypassed for synthetic testing.

Later schema/data-loading checks should use explicit input, for example:

```sh
Rscript scripts/K50/K50.r --shape LONG --outcome locomotor_capacity --data data/synthetic/k50_long_structural_fixture.csv
```

That command shape is documented for interface planning only. Full K50 execution is not claimed by this fixture because the migrated code currently also requires the external person-dedup lookup workbook during runtime.

## Schema

| Variable | Required | Type | LONG role | Synthetic meaning |
|---|---:|---|---|---|
| `id` | yes | character | grouping and paired time structure | synthetic identifier only |
| `time` | yes | integer-like numeric | K50 LONG time gate, expected `0` and `12` | synthetic visit marker |
| `FOF_status` | yes | integer-like binary | predictor and FOF gate, expected `0` and `1` | synthetic category |
| `age` | yes | numeric | covariate | structural placeholder |
| `sex` | yes | character/factor-like | covariate | synthetic category |
| `BMI` | yes | numeric | covariate | structural placeholder |
| `locomotor_capacity` | yes | numeric | primary LONG outcome for planned smoke | synthetic structural placeholder, not validated |
| `z3` | yes for `locomotor_capacity` branch | numeric | mandated fallback/sensitivity field | synthetic structural placeholder, not validated |
| `Composite_Z` | optional for this fixture | numeric | legacy bridge field if explicitly enabled | synthetic structural placeholder, not validated |
| `FI22_nonperformance_KAAOS` | optional unless `--fi22 on` | numeric | FI22 sensitivity field | synthetic structural placeholder, not validated |
| `tasapainovaikeus` | optional | character | carried by K50 transmute when present | synthetic category |

## Row Count Rationale

The fixture has eight rows: four synthetic IDs and two rows per ID for time `0` and `12`. This is the smallest deliberately simple shape that exercises paired LONG structure and both `FOF_status` categories without attempting to mimic a cohort.

## Safety Notes

- No real participant rows or identifiers are included.
- No real linkage keys, dates, local storage paths, or free-text clinical material are included.
- Numeric values are artificial placeholders and must not be interpreted as valid measurements.
- The fixture does not resolve FI22, z3, Composite_Z, chair-rise, missing-data, deduplication, model, or analytical parity questions.
