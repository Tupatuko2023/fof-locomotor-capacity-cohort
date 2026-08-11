# K50 Core Migration Provenance

## Purpose

This document records source provenance for the bounded K50-core migration into
`Tupatuko2023/fof-locomotor-capacity-cohort`. It is an artifact correspondence
record, not an analysis plan, scientific specification, validation report, or
publication approval.

## Upstream Source

- Repository: `Tupatuko2023/Python-R-Scripts`
- Immutable revision: `8a4a4e37751a4416a6a875787a8173f621da91a9`
- Source root: `Fear-of-Falling`
- Repository-level license evidence: the pinned upstream revision contains an
  MIT License with copyright attributed to Tomi Korpi (2025).

The migration strategy is `provenance_preserving_copy`. This strategy applies
only to the approved, bounded K50-core scope represented below.

## Artifact Correspondence

The migration commit is
`3ef80195e03bca3b20519af215b79532dfc3f893` (`Migrate K50 core analysis code`).
Its parent is `20d0399a9b2450c4830c6212af5a5b25269be796`, and its file manifest contains
exactly the four target paths in this table.

| Upstream source path | Target path | Correspondence and adaptation state | Evidence |
| --- | --- | --- | --- |
| `Fear-of-Falling/R-scripts/K50/K50.r` | `scripts/K50/K50.r` | Provenance-preserving copy. The migration-commit version is byte-identical to the pinned source. Later target commits make bounded non-semantic portability and synthetic structural-test adaptations: target output locations in `7a6f6e3b309ff5e10aa1964d0a06adf59c0efc6b`, and a target-specific synthetic WIDE test-control path in `c38986095c58196d6b626638848d6d75ab8e77d0`. Production lock integrity and authority semantics remain outside the synthetic test-control authority. | Pinned-source SHA-256 and migration-version SHA-256 both `8a7f8b2cdf1c8d543616047166a6e48406a39ecabea96c28441790b336d2fbee`; Git diffs for the two later commits; synthetic tests PASS 12/12 and repository R tests PASS 18/18. |
| `Fear-of-Falling/R/functions/reporting.R` | `R/functions/reporting.R` | Provenance-preserving copy with formatting-only whitespace normalization; no functional adaptation was identified. | Pinned-source SHA-256 `96940f3141aa7a30882a7eeb34ac6ed24727d4763371c955fc8b7b931c82ad64`; target SHA-256 `ec0373862cfcd2ab27986962dfa04332a973b0d70ddd8fdcffd4bebc7ab8cb3a`; inspected diff contains whitespace changes only. |
| `Fear-of-Falling/R/functions/person_dedup_lookup.R` | `R/functions/person_dedup_lookup.R` | Verbatim copy; the current target remains byte-identical to the pinned source. | Pinned-source and current-target SHA-256 both `83364843e6c4dccf281217b0c08cf91f92c30d5939811de95ef956a8dc347f5b`. |
| `Fear-of-Falling/R/functions/init.R` | `R/functions/init.R` | Provenance-preserving copy with formatting-only whitespace normalization at migration, followed by a non-semantic target portability adaptation in `7a6f6e3b309ff5e10aa1964d0a06adf59c0efc6b` that redirects K50 tables and manifest records to the target repository's approved output layout. | Pinned-source SHA-256 `c4a4f75b2abdb452b0ff76338237d65691ab55645db060e0ae53d4ad303c9ddc`; migration-version diff is whitespace-only; later Git diff changes `R-scripts/<label>/outputs` and `manifest/manifest.csv` to `outputs/tables/<label>` and `outputs/logs/<label>_manifest.csv`. |

The later commits above are implementation and structural-validation evidence;
they do not expand the four-file K50-core migration manifest.

## Authority Boundary

Upstream documentation remains upstream scientific or technical authority
unless an A1 Owner decision separately and explicitly adopts it. This record
does not import or approve upstream scientific interpretations, analysis-plan
authority, thesis scope, validation claims, outcome definitions, or manuscript
conclusions. Pinned upstream documents may be consulted as source evidence
without becoming downstream project authority.

Current local copies under `docs/source/Fear-of-Falling/**` are not part of this
provenance record or the approved migration payload. This Work Package does not
approve those copies for Git publication.

## Rights And Provenance Boundary

The pinned upstream repository provides repository-level MIT License evidence,
the immutable source revision, and the exact source paths recorded above. The
target repository's license remains unapproved, and artifact-level authorship
or rights questions are not represented as fully resolved by this record.

## Privacy Boundary

No participant-level or pseudonymized data, generated model or data artifacts,
restricted inputs, credentials, secrets, protected source artifacts, or
generated upstream outputs are part of this record or the four-file migration
payload. This record contains only repository-relative source and target paths
needed for provenance.

## Validation State

- Technical source-to-target provenance: verified for the four mappings above.
- Migration commit identity and manifest: verified from target Git history.
- Synthetic WIDE validation: structural validation only.
- Repository R tests: PASS 18/18 as supporting technical evidence.
- Quarto: `NOT RUN - unavailable`.
- Numerical or scientific parity: `NOT ESTABLISHED`.
- Upstream scientific interpretations and validation claims: not adopted by
  this record.
