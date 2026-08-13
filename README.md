# fof-locomotor-capacity-cohort

## Overview

This repository contains public research software and synthetic
reproducibility-support materials for a 12-month cohort study of fear of falling
(FOF) and locomotor capacity in older adults. It provides the migrated K50
analysis core, synthetic fixtures, structural tests, and a public
analysis-to-output traceability demo. It supports the analysis workflow
associated with the study but is not itself a report of the study or its
findings.

The repository supports inspection and testing of the public software
workflow. It does not distribute protected participant-level data or protected
analytical results.

## Scope and claim boundary

Public validation uses wholly synthetic fixtures. These fixtures are designed
for software, schema, integrity, and rendering checks; they are not intended to
represent the study cohort or reproduce its results.

The current repository-level A1/K50 claim is limited to:

> A1/K50 conforms to the specified analysis contracts at the structural and
> implemented-workflow level, with z3 coverage, final cohort semantics, and
> scientific approval of the 0.40 producer threshold explicitly deferred.

This claim does not establish numerical parity, exact numerical reproduction,
effect equivalence, full scientific validation, or clinical validity. It does
not authorize publication or disclosure of protected study results. The
normative decision and claim-boundary record is
[docs/project_specification.md](docs/project_specification.md#14-a1k50-scientific-phase-closeout).

## A1/K50 status

The A1/K50 scientific phase is
`CLOSED_WITH_DEFERRED_SCIENTIFIC_ITEMS — PUBLISHED`. Here, `PUBLISHED` is an
internal project-status label recording that the closeout documentation was
published to the repository. It does not mean that the study, manuscript,
software release, or DOI has been published. Technical execution met the
current internal closeout criteria. The protected scientific review was
completed with explicitly deferred scientific items.
`PARITY-OBJECTIVE-01` uses Option A: structural and methodological conformity
plus protected scientific review.

The remaining deferred register is:

- `SCI-03C`: final z3 component-coverage semantics remain a deferred scientific
  decision; the repository does not establish a final scientific
  interpretation of that coverage;
- `SCI-SEM-COHORT`: final scientific definitions governing cohort construction
  and deduplication remain deferred;
- `SCI-03D`: the 0.40 producer threshold is currently
  `IMPLEMENTATION_SAFEGUARD_ONLY`; its scientific adoption remains deferred;
- `RET-01`: retention remains `POLICY_REFERENCE_REQUIRED`.

These items are not blockers under the repository's current internal closeout
criteria; they remain explicitly deferred scientific decisions. Numerical
reference and tolerance work (`SCI-REF` and `SCI-TOL`) remains inactive under
Option A.

## Public synthetic traceability demo

Run the public end-to-end demonstration from the repository root in a supported
environment with R and Quarto:

```bash
Rscript scripts/demo/run_public_traceability.R
```

The command validates the approved synthetic WIDE fixture and integrity lock,
then regenerates exactly four files under `outputs/demo/`:

- `traceability_qc.csv` — machine-readable structural QC status;
- `traceability_qc.png` — synthetic QC checklist figure;
- `public_traceability_demo.html` — dedicated Quarto report;
- `traceability_receipt.json` — machine-readable provenance receipt.

These files are generated workflow demonstrations, not committed research
results. They are ignored by Git and can be regenerated from the tracked
entrypoint, Quarto source, synthetic fixture, and integrity control.

## Repository structure

```text
fof-locomotor-capacity-cohort/
├── R/
│   ├── functions/                         # K50 support and reporting functions
│   └── transform_locomotor_indicators.R   # Public synthetic transformation
├── scripts/
│   ├── K50/K50.r                          # Migrated K50 analysis entrypoint
│   ├── demo/run_public_traceability.R     # Public synthetic traceability demo
│   └── 01_generate_synthetic_fixture.R
├── data/
│   ├── README.md
│   └── synthetic/                         # Synthetic fixtures and controls only
├── manuscript/
│   ├── public_traceability_demo.qmd
│   └── smoke_test.qmd
├── tests/testthat/
│   ├── test_k50_synthetic_wide_test_control.R
│   ├── test_public_traceability_demo.R
│   └── test_transform_locomotor_indicators.R
├── outputs/
│   ├── figures/
│   └── tables/
└── docs/
    ├── project_specification.md
    ├── k50_migration_provenance.md
    ├── reproducibility_scope.md
    └── restricted_data_policy.md
```

Local orchestration material, protected runtime artifacts, and regenerated
demo output are not part of the public software release scope.

## Installation and dependencies

`DESCRIPTION` is the dependency authority. The project does not currently use
an active `renv` environment or target-specific `renv.lock` file.

Install the declared R dependencies from an approved package source. The
current dependency set includes the packages in `Imports` and `Suggests` in
`DESCRIPTION`. Quarto is additionally required for rendering.

## Validation

Generate the small general-purpose synthetic fixture if needed:

```bash
Rscript scripts/01_generate_synthetic_fixture.R
```

Run the complete R test suite from the repository root:

```bash
Rscript -e 'testthat::test_dir("tests/testthat")'
```

Run the public traceability contract test directly:

```bash
Rscript -e 'testthat::test_file("tests/testthat/test_public_traceability_demo.R")'
```

Render the smoke test with Quarto:

```bash
quarto render manuscript/smoke_test.qmd
```

Quarto validation has been demonstrated in an Ubuntu PRoot environment where R
and Quarto share a compatible runtime. A native environment may be used when it
provides the dependencies declared in `DESCRIPTION` and a working Quarto CLI.
All public validation remains synthetic-only.

## Data availability

Protected cohort data are not distributed in this repository. The public
repository contains synthetic fixtures only. Access to the underlying research
data is governed separately by the responsible data authority and applicable
ethical, legal, and institutional approvals. The public software repository
does not grant or promise access to those data.

See [docs/restricted_data_policy.md](docs/restricted_data_policy.md) and
[docs/reproducibility_scope.md](docs/reproducibility_scope.md) for the public
data and reproducibility boundaries.

## License

The target repository is licensed under the MIT License; see
[LICENSE](LICENSE). Provenance-bound K50 material retains its applicable Tomi
Korpi (2025) MIT attribution. The migration and adaptation history is recorded
in [docs/k50_migration_provenance.md](docs/k50_migration_provenance.md). This
software license does not authorize access to or disclosure of protected study
data or results.

## Citation

[CITATION.cff](CITATION.cff) is the current software citation metadata
authority. The release-facing draft identifies Tomi Korpi as the software
creator and version `0.1.0` as the planned first archival software release.

No Zenodo DOI has yet been published. The cohort software is intended to have a
separate archival software record from the dissertation, subject to later
Sandbox testing, release review, explicit human publication approval, and DOI
verification.

## Release status

Version `0.1.0` is a release-candidate metadata draft prepared for internal and
BMC Geriatrics/domain-expert review. It is not yet a Git tag, GitHub Release,
Zenodo record, or published DOI.
