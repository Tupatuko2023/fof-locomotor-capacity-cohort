# SCI-SEM-COHORT scientific decision package

Status: `NEEDS_SCIENTIFIC_AUTHORITY_DECISIONS`

This document is a decision framework, not an approved cohort specification.
It describes the current repository implementation without asserting that the
implemented choices are scientifically correct. It contains no participant
data, protected results, new calculations, or authority to execute against
protected inputs.

## Proposed population-stage vocabulary

The following labels are proposed only to separate the questions that require
authority. They are not yet approved scientific definitions.

1. `SOURCE_AUTHORIZED_COHORT`: the upstream cohort delivered through the
   authorized input snapshot.
2. `PERSON_RESOLVED_COHORT`: rows remaining after identifier normalization,
   identity lookup and person-level deduplication.
3. `PRIMARY_ANALYSIS_POPULATION`: the person-resolved rows satisfying the
   primary branch's complete-case requirements.
4. `SENSITIVITY_ANALYSIS_POPULATION`: the primary population further restricted
   by the completeness requirements of a named sensitivity branch.

## Decision 1 — Upstream eligibility

**Repository implementation.** K50 accepts an authoritative WIDE input or an
explicitly supplied input. The public repository validates input identity and
integrity but does not construct the original study cohort.

**Source-grounded fact.** The active structural contract is the WIDE 12-month
locomotor-capacity analysis. Public synthetic controls exercise only its
structure.

**Not established by the repository.** The authoritative source cohort,
recruitment frame, baseline eligibility, clinical inclusion/exclusion rules,
follow-up eligibility, and upstream exclusions are not specified here.

**Question for Scientific Authority.** What exact source population, input
snapshot authority, inclusion criteria, exclusion criteria, time origin and
follow-up requirements define `SOURCE_AUTHORIZED_COHORT`?

**Downstream impact.** Cohort-flow start and exclusion nodes, cohort
characteristics denominator, analysis-population description, and
generalizability boundary.

## Decision 2 — Identity resolution

**Repository implementation.** `prepare_k50_person_dedup()` requires a lookup
workbook with one uniquely resolvable identity field and bridge key. A matched
identity receives a verified person key. A non-matched, non-missing ID receives
an `id_fallback` key. Rows with missing normalized ID are excluded.

**Source-grounded fact.** The code fails closed when it cannot find exactly one
usable lookup sheet or bridge, or when a bridge value maps inconsistently.

**Not established by the repository.** The scientific and data-governance
authority of the lookup, the acceptable linkage method, and whether unmatched
IDs may remain through `id_fallback` are not approved.

**Questions for Scientific Authority and Data Steward.** Which identity lookup
and bridge are authoritative? May lookup-unmatched records remain under
`id_fallback`? If not, what is their required disposition? Is missing-ID
exclusion scientifically approved?

**Downstream impact.** Person counts, cohort-flow identity-resolution nodes,
duplicate handling and every downstream denominator.

## Decision 3 — Deduplication

**Repository implementation.** For a verified person, conflicting non-missing
FOF groups cause exclusion. Candidate selection then prioritizes branch
eligibility, outcome completeness, covariate completeness, number of observed
comparison fields and deterministic canonical-ID order. A top tie with
different signatures is treated as ambiguous and excluded.

**Source-grounded fact.** This ordering and ambiguous-person exclusion are
deterministic and implemented in `R/functions/person_dedup_lookup.R`.

**Not established by the repository.** No Scientific Authority record states
that completeness-based selection is the correct scientific duplicate rule or
that excluding every ambiguous verified person is acceptable.

**Question for Scientific Authority.** Approve, reject or replace each
deduplication priority and the exclusion of FOF-conflicting or otherwise
ambiguous verified-person records. If replacement is required, provide the
ordered rule and tie policy.

**Downstream impact.** `PERSON_RESOLVED_COHORT`, exclusion counts, selection
bias, model denominators and reproducibility of cohort flow.

## Decision 4 — Primary analysis population

**Repository implementation.** In the active WIDE locomotor-capacity branch,
the primary model requires non-missing baseline and 12-month locomotor capacity,
FOF status, age, sex and BMI after person resolution. The fitted model is
`locomotor_capacity_12m ~ locomotor_capacity_0 + FOF_status + age + sex + BMI`.

**Source-grounded fact.** This is the current complete-case filter and model
formula implemented by K50.

**Not established by the repository.** The repository does not establish that
complete-case restriction is the approved missing-data strategy, define its
target estimand, or approve the resulting selection/generalizability
implications.

**Question for Scientific Authority.** Is this exact complete-case rule the
canonical `PRIMARY_ANALYSIS_POPULATION`? What target estimand and interpretation
apply after conditioning on two observed outcomes and complete covariates? If
not approved, specify the missing-data and population rule.

**Downstream impact.** Primary-effect table and figure, cohort characteristics,
missingness presentation, denominator annotations and manuscript methods.

## Decision 5 — Sensitivity populations

**Repository implementation.** The Z3 fallback starts from the primary
complete-case population and additionally requires non-missing `z3_0` and
`z3_12m`. The FI22 branch starts from the primary requirements and additionally
requires non-missing `FI22_nonperformance_KAAOS`.

**Source-grounded fact.** Z3 is currently labeled
`fallback_sensitivity`; FI22 is `fi22_sensitivity`. Their canonical synthetic
artifacts validate bytes and provenance only.

**Not established by the repository.** The scientific role, estimand,
comparability to the primary population, and manuscript/supplement placement of
either branch are not approved. SCI-03C-A and SCI-03C-B also remain undecided.

**Question for Scientific Authority.** Are the branch-specific completeness
rules approved? What scientific question and estimand does each branch answer?
How should population differences be reported? The Z3 publication role must
also be reconciled with the eventual SCI-03C-A and SCI-03C-B decisions.

**Downstream impact.** Z3 and FI22 sensitivity tables, population-flow branches,
denominator comparisons, interpretation and main-versus-supplement placement.

## Required decision record

The consolidated Scientific Authority response must, for each decision above,
record `APPROVE`, `REJECT` or `REPLACE`; the exact approved wording or rule; the
authority and approval reference; effective repository revision; affected
population stages; and any required code, documentation, protected-validation
or disclosure follow-up. Silence or partial review must remain
`NEEDS_VERIFICATION`.
