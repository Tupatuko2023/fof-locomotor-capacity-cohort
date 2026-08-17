# A1 Project Context

## 1. Metadata

```yaml
project_context_id: A1-PROJECT-CONTEXT
version: 0.2.0
status: approved
document_evidence_state: validated
project_name: fof-locomotor-capacity-cohort
project_short_name: A1
project_phase: bounded Project Mode; K50 migration and scientific-phase closeout complete; post-release maintenance active
review_authority: User / designated project owner
```

## 2. Project Identity

```yaml
project_identity:
  project_name: fof-locomotor-capacity-cohort
  project_short_name: A1
  project_phase: bounded Project Mode; K50 migration and scientific-phase closeout complete; post-release maintenance active
  mission_or_goal: >
    Document a 12-month fear-of-falling and locomotor-capacity cohort
    analysis pipeline with public structural and rendering reproducibility
    while keeping restricted participant-level data out of Git.
```

The target repository now contains the bounded migrated K50 analysis core,
synthetic fixtures, structural tests, Quarto smoke-test structure, a public
traceability demonstration, release-candidate metadata and a draft-only Zenodo
Sandbox workflow. It does not contain protected analytical results or
participant-level data. Earlier scaffold-only descriptions are historical and
are superseded by the current-state record in Section 16.

## 3. Repository Context

```yaml
repository_context:
  primary_repository: Tupatuko2023/fof-locomotor-capacity-cohort
  primary_repository_role: public target scaffold repository
  related_repositories:
    - repository: Tupatuko2023/Python-R-Scripts
      source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
      source_path: Fear-of-Falling
      status: verified source identity and bounded K50 source for the completed provenance-preserving migration
  repository_relationship_summary: >
    The source identity, immutable revision and bounded K50 source paths are
    verified. The approved K50 core was migrated using provenance-preserving
    copy and has target-side provenance evidence. This does not approve or
    classify the remainder of the source repository.
```

## 4. Working Context

```yaml
working_context:
  expected_repository_root: target repository root
  approved_working_directories: []
  observed_candidate_working_areas:
    - R/
    - scripts/
    - data/synthetic/
    - manuscript/
    - outputs/tables/
    - outputs/figures/
    - tests/testthat/
    - docs/
  environment_identity: Termux/local workspace; permanent environment identity NEEDS_VERIFICATION
  platform_constraints:
    - quarto CLI not found in PATH during bootstrap inspection
    - renv scaffold only; renv/activate.R not present during R test startup
```

The observed candidate working areas are repository-structure facts only. They are not approved execution `allowed_paths`. Execution scope belongs to a later approved Project Specification.

## 5. Source Context

```yaml
source_context:
  approved_source_categories:
    - target repository README.md
    - target repository docs/restricted_data_policy.md
    - target repository docs/reproducibility_scope.md
    - target repository data/README.md
    - target repository .gitignore
    - target repository DESCRIPTION
    - target repository _quarto.yml
    - WP-A1-SOURCE-REPOSITORY-IDENTITY-INSPECT PASS: source identity, revision and path metadata only
  source_scope_summary: >
    Target-repository scaffold context plus bounded source identity metadata.
    Source repository content inspection, artifact classification, dependency
    closure, privacy/provenance review and migration execution have not been
    approved or performed.
  authority_or_precedence_references:
    - docs/project_context.md
    - docs/project_specification.md
    - docs/restricted_data_policy.md
    - docs/reproducibility_scope.md
```

Local development and governance materials are outside the runtime, test,
curated-bundle and release-tree boundary. The accepted public Project Context
and Project Specification are the repository-level authorities. Earlier Git
history remains public and is not rewritten.

## 6. Data Context

```yaml
data_context:
  applicable_classification_references:
    - docs/restricted_data_policy.md
    - data/README.md
    - docs/project_specification.md
  restricted_data_present: unknown
  participant_level_data_in_inspected_public_repository: no per inspected repository policy and scaffold evidence
  synthetic_data_available: yes
  explicit_data_exclusions:
    - real participant-level data
    - raw or pseudonymized participant data
    - participant identifiers
    - analysis-ready participant-level files
    - row-level model-frame data
    - secrets and credentials
    - unverified CSV/RDS/SAV data files
```

The inspected public repository policies prohibit restricted participant-level data and direct validation uses synthetic data. This context does not make a broader claim about the existence, location or accessibility of original restricted data beyond inspected repository evidence.

## 7. Publication Context

```yaml
publication_context:
  public_private_boundary: >
    Public scaffold repository for structural and rendering reproducibility
    with public materials; full numerical reproduction requires an approved
    restricted environment.
  publication_target_known: archival software release v0.1.0 published on GitHub 2026-08-15; Production Zenodo and DOI not published
  repository_role_relative_to_publication: >
    Supports transparent pipeline documentation and public reproducibility
    scaffolding, not final analytical results.
```

This context does not authorize publication, release, archive deposit, pull request creation or external disclosure.

## 8. Migration Context

```yaml
migration_context:
  migration_expected: yes; bounded K50 migration completed
  source_repository_relationship: source identity, pinned revision and bounded migrated source paths verified
  source_repository: Tupatuko2023/Python-R-Scripts
  source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
  source_path: Fear-of-Falling
  target_repository_relationship: public target scaffold repository verified
  migration_requirement_status: approved and completed for the bounded K50 core
  approved_migration_strategy: provenance_preserving_copy
  project_specification_reference: docs/project_specification.md
  migration_authority_reference: docs/project_specification.md
  migration_provenance_reference: docs/k50_migration_provenance.md
```

The bounded K50 migration and its provenance are complete. Broader source
inspection, artifact disposition and migration beyond that approved payload
remain outside this Context unless separately authorized.

## 9. Validation Environment Context

```yaml
validation_environment_context:
  available_environments:
    - git available during bootstrap inspection
    - Rscript available during bootstrap inspection
    - Ubuntu 26.04 PROOT approved for render validation
  known_unavailable_capabilities:
    - quarto CLI not found in native Termux PATH during bootstrap inspection
  environment_specific_limitations:
    - native Termux cannot perform Quarto render validation with its current PATH
    - inherited Termux PATH entries can select Termux R inside Ubuntu PROOT and must be isolated from the approved Ubuntu render runtime
    - chair-rise semantics are resolved for the bounded A1/K50 contract; broader use remains scope-bound
    - renv activation is not active because renv/activate.R was not present during R test startup
  approved_render_validation_environment:
    environment: Ubuntu 26.04 PROOT
    validation_status: APPROVED_FOR_RENDER_VALIDATION
    quarto_version: 1.9.38
    r_version: 4.5.2
    render_packages:
      knitr: 1.51
      rmarkdown: 2.30
    dependency_authority: DESCRIPTION
    active_renv: false
    runtime_isolation_requirement: R and Rscript must resolve from the Ubuntu runtime rather than inherited Termux paths
    environment_confusion_risk: Termux R 4.5.3 is not an approved Ubuntu render runtime
    required_evidence:
      - repository revision and render command
      - Ubuntu, Quarto, R and render-package versions
      - synthetic-only input declaration
      - output and side-effect manifest
      - render result and cleanup result
    expected_side_effects:
      - configured render output
      - ignored .quarto cache and temporary artifacts
    cleanup_expectation: generated render artifacts are classified and removed when not retained by an approved output policy
```

Tool availability does not imply permission. Ubuntu PROOT approval is limited
to synthetic-only render validation and does not authorize protected-data use,
dependency changes, publication or release.

## 10. Explicit Exclusions

```yaml
explicit_exclusions:
  out_of_scope_context:
    - no Project Mode activation
    - no Project Specification approval
    - no migration strategy selection
    - no source-repository access
    - no execution allowed_paths authorization
    - no protected-data access
    - no scientific or analytical changes
    - no staging, commit, push, pull request, release or publication authorization
```

## 11. Evidence Reviewed

Source-grounded evidence reviewed for this draft:

| Claim area | Source |
|---|---|
| Repository identity, scaffold status, missing migrated analysis/manuscript and no analytical results | `README.md` |
| Repository safety rules, allowed synthetic data and forbidden participant data | `docs/restricted_data_policy.md`; `data/README.md`; `docs/project_specification.md` |
| Restricted data exclusions and synthetic validation requirement | `docs/restricted_data_policy.md` |
| Public structural/render reproducibility and restricted-environment numerical reproducibility | `docs/reproducibility_scope.md` |
| Ignored restricted/raw data, secrets, credentials and prohibited file types | `.gitignore` |
| Package identity and R/testthat context | `DESCRIPTION` |
| Quarto project output and execution configuration | `_quarto.yml` |
| Accepted project boundary and governance requirements | `docs/project_context.md`; `docs/project_specification.md` |

## 12. Owner Acceptance

```yaml
owner_decision:
  decision: accepted
  artifact: docs/project_context.md
  scope: >
    Accepted as the approved A1 Project Context instance for
    fof-locomotor-capacity-cohort based on completed source-grounded Review
    and Validation.
  unresolved_items_remain_unresolved: true
  explicit_exclusions:
    - no Project Mode activation
    - no Project Specification creation or approval
    - no source-repository access or inspection
    - no migration authorization
    - no migration-strategy selection
    - no scientific or analytical changes
    - no protected-data access
    - no staging, commit, push, pull request, release or publication authorization
    - no history rewrite or force operation
  next_authorized_planning_step: Prepare a bounded proposal for WP-A1-PROJECT-SPECIFICATION-DRAFT
```

No unresolved `NEEDS_VERIFICATION` item is converted to a verified fact by this acceptance.

## 13. Project Mode Activation

OWNER DECISION - ACTIVATE A1 PROJECT MODE

```yaml
owner_decision:
  decision: activated
  project: fof-locomotor-capacity-cohort / A1
  decision_date: 2026-08-10
  project_authorities:
    - accepted and validated docs/project_context.md
    - accepted and validated docs/project_specification.md
  activation_scope:
    - read-only target-repository inspection
    - documentation and planning within separately approved bounded Work Packages
    - synthetic/public scaffold work within separately approved bounded Work Packages
    - validation using available and verified tools
    - preparation, Review and Validation of later bounded Work Packages and project artifacts
  unrestricted_execution_authority_created: false
  git_hard_gate_action_authorized: false
```

Project Mode is active only within the activation scope above. Write work still
requires separately approved bounded Work Packages / MacroGates with explicit
objective, allowed paths, operation classes, evidence requirements, exclusions
and stop conditions.

This activation does not authorize source-repository access or inspection,
migration, copying, migration-strategy selection, dependency-closure execution
against a source repository, protected-data access, participant-level-data
handling, scientific or analytical changes, chair-rise reverse-coding resolution
or implementation, full numerical reproduction claims, Quarto-render PASS claims
while Quarto is unavailable, publication, release, pull request, staging, commit,
push, history rewrite, force operations, credential access or any other Hard Gate
action without separate explicit approval.

Existing `NEEDS_VERIFICATION` and Work-Package-scoped blockers remain unresolved
for their affected scopes. Activation does not promote them to verified facts or
authorize affected work.

Suspend the affected Project Mode scope on authority conflict, stale or
superseded project authority, protected-data exposure, secret exposure,
unknown-sensitivity exposure, scope exceeding the activated boundary,
MaterialBoundaryChange or insufficient evidence for an affected Review,
Validation or acceptance claim.

## 14. Open `NEEDS_VERIFICATION` Items

- Source contents and artifact classification/disposition outside the bounded migrated K50 payload.
- Approved execution `allowed_paths` and `forbidden_paths`.
- Approved protected analysis environment.
- `renv` activation and dependency-lock status.
- Publication review authority and final manuscript/supplement scope.
- SCI-03C canonical meaning, due to a conflict between README and the normative closeout wording.
- SCI-SEM-COHORT scientific approval.
- RET-01 authoritative policy reference.
- Final root cause of the Zenodo workflow registration failure.

## 15. Dependencies and References

Repository-level dependency relationships:

```text
docs/project_context.md
  informs -> docs/project_specification.md

docs/restricted_data_policy.md and data/README.md
  constrain -> data, privacy and protected-data boundaries

docs/project_specification.md and docs/k50_migration_provenance.md
  govern -> migration scope, provenance and execution boundaries
```

This context is not an active Project Specification, Migration Contract, source-repository access authorization, migration authorization or Git Hard Gate record.

## 16. Canonical Current-State Alignment

This section is the active current-state record as of 2026-08-17. It
supersedes earlier bootstrap and planning statements only where they describe
an item below as unresolved or not yet performed. Historical Owner decisions
and migration-time evidence remain historical records and are not rewritten.

```yaml
current_state:
  target_repository_role: public research-software repository with a synthetic-only public validation boundary
  project_mode: active for bounded Work Packages; no standing Git or external-action authority
  migration_required: yes
  migration_strategy: provenance_preserving_copy
  bounded_k50_migration: completed and provenance-verified
  scientific_phase: CLOSED_WITH_DEFERRED_SCIENTIFIC_ITEMS
  chair_rise_semantics: resolved for the bounded A1/K50 contract
  dependency_authority: DESCRIPTION
  active_renv_environment: false
  native_termux_quarto: unavailable
  ubuntu_proot_quarto:
    version: 1.9.38
    status: available_and_smoke_tested
    validation_status: APPROVED_FOR_RENDER_VALIDATION
    ubuntu_version: 26.04
    r_version: 4.5.2
    knitr_version: 1.51
    rmarkdown_version: 2.30
    runtime_isolation_requirement: R and Rscript resolve from the Ubuntu runtime, not inherited Termux paths
    environment_confusion_risk: Termux R 4.5.3 is outside the approved Ubuntu render runtime
    evidence_policy: versions, repository revision, command, synthetic-only declaration, side-effect manifest, result and cleanup
  render_side_effect_policy: expected outputs and ignored caches are allowed when classified, bounded and safely cleanable; unexpected tracked source changes are not allowed
  target_license: MIT
  release_scope: v0.1.0 is a published independent synthetic-only research-software release, not a manuscript, supplement or scientific-results release
  formal_software_release: performed_on_github
  git_tag_v0_1_0:
    state: published_annotated
    target_commit: 63f00831c0c9cc5a8d7fad1c705922d1afe084af
  github_release:
    state: published
    published_at: 2026-08-15T08:48:49Z
    asset: fof-locomotor-capacity-cohort-0.1.0.zip
    asset_sha256: 9b70b06d6e7dd729a73f6fa20667f6610fbd4c029aa551ba3f0282b70c6fec81
  production_zenodo_record: not_created
  production_zenodo_authorized: false
  github_actions:
    registration_control_history: temporary registration diagnostic retired after workflow registration was validated
    zenodo_sandbox_workflow: registered_active_and_validated
  sandbox:
    phase: COMPLETE / VALIDATED
    draft_id: 587120
    draft_state: unpublished_unsubmitted
    pipeline_validation: end_to_end_pass
    metadata_readback: PASS
    bundle_upload_and_readback: PASS
    disposition: retained_as_validation_evidence_pending_later_explicit_decision
    formal_release: false
    production_zenodo: not_authorized
    bundle_boundary: explicit_allowlist_implemented_and_validated
  permanent_execution_allowed_paths: none
  local_development_and_governance_materials:
    release_boundary: local_only
    current_transition_state: excluded from the current tracked and release trees
    local_disposition: preserved outside the release boundary
    history: prior public Git history is retained without rewrite
    zenodo_bundle: excluded
```

The following remain open and are not promoted by this alignment:

- `SCI-03C: CONFLICT / NEEDS_VERIFICATION`. README and the normative
  closeout/specification currently assign incompatible meanings to this
  identifier. No canonical meaning is asserted pending Owner clarification.
- `SCI-SEM-COHORT`: scientific approval remains deferred.
- `SCI-03D`: remains `IMPLEMENTATION_SAFEGUARD_ONLY`.
- `RET-01`: remains `POLICY_REFERENCE_REQUIRED`.
- the approved protected analysis environment;
- final manuscript and supplement publication boundaries;
- steward and review cadence;
- AI-assistance disclosure.

This alignment makes no numerical-parity, clinical-validity, manuscript or
scientific-results publication, disclosure, retention, DOI or protected-data
claim beyond the bounded GitHub software-release facts recorded above.
