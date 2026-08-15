# SCI-03C protected execution package preparation

Status: `SYNTHETIC_ONLY`; protected execution is **not authorized**.

## Scientific purpose and decision boundary

This package prepares aggregate evidence for comparing `ANY_COMPONENT`,
`MIN_2_OF_3`, and `REQUIRE_3_OF_3`. It does not select a rule, change K32 or
K50, access participant data, produce scientific results, or authorize egress.
SCI-03C-A (coverage threshold) and SCI-03C-B (temporal application) remain
Scientific Owner decisions. SCI-03D remains a separate 0.40 producer gate.

## Aggregate-output contract

Only the following disclosure-controlled CSV tables are proposed for egress.
Every row contains `disclosure_status`; suppressed counts, denominators,
percentages, shares, and derived gate results are blank.

| Table | Exact fields |
|---|---|
| `coverage_distribution.csv` | `scope`, `fof_group`, `timepoint`, `components_observed`, `denominator_n`, `n`, `pct`, `disclosure_status` |
| `component_missingness.csv` | `scope`, `fof_group`, `timepoint`, `component`, `missing`, `denominator_n`, `n`, `pct`, `disclosure_status` |
| `paired_transition.csv` | `scope`, `fof_group`, `components_observed_baseline`, `components_observed_12m`, `denominator_n`, `n`, `pct`, `disclosure_status` |
| `rule_eligibility.csv` | `scope`, `fof_group`, `window`, `rule`, `denominator_n`, `n`, `pct`, `disclosure_status` |
| `k50_population.csv` | `scope`, `fof_group`, `rule`, `stage`, `denominator_n`, `n`, `pct`, `disclosure_status` |
| `sci03d_comparison.csv` | rule-eligibility fields plus `nonmissing_share`, `producer_gate`, `producer_gate_result`, `disclosure_status` |

Allowed enumerations are:

- `scope`: `OVERALL`, `FOF_STRATIFIED`;
- `timepoint`: `baseline`, `12m`;
- `window`: `baseline`, `12m`, `paired`;
- `components_observed`: integer 0 through 3;
- `rule`: `ANY_COMPONENT`, `MIN_2_OF_3`, `REQUIRE_3_OF_3`;
- `stage`: `SOURCE_PAIRED`, `COVERAGE_ELIGIBLE`, `K50_COMPLETE_CASE`;
- `disclosure_status`: `RELEASED`, `PRIMARY_SUPPRESSED`, `SECONDARY_SUPPRESSED`.

No ID, row-level availability flag, component value, model frame, coefficient,
prediction, residual, or free text from the input is an output field.

The internal, non-egress input adapter must construct exactly one row per
`subject_key` and `timepoint`, with fields `subject_key`, `timepoint`,
`fof_group`, `gait_available`, `chair_available`, `balance_available`, and
`k50_covariates_complete`. These rows and flags are participant-level material
and must never leave the approved environment. Mapping source variables into
this internal contract requires separate scientific and data-governance review.

## Parameterized disclosure design

`small_cell_threshold` is a mandatory positive integer supplied by the
disclosure authority. Its institutional value is `AUTHORITY_TO_DEFINE`.

The candidate algorithm primary-suppresses each positive count below the
authority-supplied threshold. As a conservative secondary control, it suppresses
every other count and derived percentage in the same logical partition. This
prevents recovery from partition totals but may suppress more information than
necessary. Cross-table differencing, denominator release, zero-cell handling,
and any less conservative complementary-suppression algorithm require explicit
disclosure-authority approval. No output may leave the environment merely
because this technical function completed.

The synthetic dry run requires an explicitly named `synthetic-test-threshold`.
That value tests parameter flow only and is not a proposed institutional rule.

## Code candidate

The candidate files are:

- `R/functions/sci03c_aggregate_evidence.R`;
- `scripts/SCI03C/run_synthetic_dry_run.R`;
- `tests/testthat/test_sci03c_aggregate_evidence.R`.
- `config/sci03c/protected_execution_manifest.template`;
- `config/sci03c/runtime_manifest.template`;
- `config/sci03c/audit_receipt.schema`.

The approval record must pin their Git object IDs or SHA-256 checksums. The
repository revision at approval time must also be recorded. Preparation-time
revision identifiers are evidence, not authorization.

## Runtime proposal

The implementation uses base R only. Approval must pin the OS, R version,
package/library state, locale, timezone, and seed. The dry-run receipt records
the observed values. The protected runner and protected input adapter remain a
separate approval-bound implementation: this public entrypoint is deliberately
synthetic-only.

## Proposed execution paths

Allowed:

- read-only approved input location inside the protected environment;
- immutable approved code checkout;
- protected temporary workspace;
- protected output-staging directory;
- protected audit-log location.

Forbidden:

- this public repository for participant data or protected outputs;
- `data/`, `data/synthetic/`, `outputs/`, Git, prompts, console logs, or source
  code as participant-data destinations;
- network, clipboard, removable-media, or unapproved cloud egress;
- any path containing secrets or credentials in an artifact or receipt.

Concrete paths are `ENVIRONMENT_ADMINISTRATOR_TO_DEFINE` and must be allowlisted
before protected execution.

## Audit-receipt schema

The protected receipt must contain only:

- package and execution identifiers;
- operator authorization reference, never personal credentials;
- UTC execution timestamp;
- environment approval reference;
- repository revision and script checksums;
- runtime pins, locale, timezone, and seed;
- input snapshot/checksum reference that reveals no participant information;
- rule definitions and authority-supplied disclosure parameters;
- reconciliation results per table;
- disclosure reviewer decision and approval reference;
- output filenames and checksums;
- retention-policy reference and deletion-verification status.

It must not contain participant identifiers, rows, cell values, file paths that
reveal identities, secrets, credentials, or raw error payloads.

## Synthetic dry run

Run into a temporary directory, not the repository output tree:

```sh
Rscript scripts/SCI03C/run_synthetic_dry_run.R \
  --output-dir /approved/synthetic/temp/path \
  --synthetic-test-threshold AUTHORIZED_TEST_INTEGER
```

Acceptance requires schema equality, count reconciliation, paired counts not
exceeding either timepoint, monotonic eligibility (`ANY >= 2/3 >= 3/3`), no
identifier columns in outputs, suppression behavior tests, and a receipt marked
`mode=SYNTHETIC_ONLY` and `protected_execution_authorized=NO`.

## Institutional approval checklist

| Required decision | Current value |
|---|---|
| Protected environment | `AUTHORITY_TO_DEFINE` |
| Data controller/steward | `AUTHORITY_TO_DEFINE` |
| Authorized operators | `AUTHORITY_TO_DEFINE` |
| Scientific purpose/schema approval | `NEEDS_VERIFICATION` |
| Small-cell threshold | `AUTHORITY_TO_DEFINE` |
| Secondary-suppression approval | `NEEDS_VERIFICATION` |
| Disclosure review authority | `AUTHORITY_TO_DEFINE` |
| Approved code revision/checksums | `NEEDS_VERIFICATION` |
| Allowed/forbidden concrete paths | `NEEDS_VERIFICATION` |
| Runtime pins | `NEEDS_VERIFICATION` |
| Audit-log location/access | `AUTHORITY_TO_DEFINE` |
| RET-01 retention/deletion policy | `AUTHORITY_TO_DEFINE` |
| Aggregate egress authority | `AUTHORITY_TO_DEFINE` |
| Owner approval | `NEEDS_VERIFICATION` |

Required approvers are the Data Controller/Steward, Scientific Authority,
Disclosure Authority, Environment Administrator, and Project Owner. Protected
execution remains `NO` until the consolidated approval record is complete.
