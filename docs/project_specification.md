# A1 Project Specification

## 1. Document Metadata

```yaml
title: A1 Project Specification
document_id: A1-PROJECT-SPECIFICATION
version: 0.1.0
status: accepted
project_id: A1
scope: >
  Approved project requirements for the fof-locomotor-capacity-cohort target
  repository scaffold, public reproducibility boundary and future migration
  planning.
steward: NEEDS_VERIFICATION
review_authority: User / designated project owner
effective_date: 2026-08-10
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
project_mode_status: active
source_of_truth_state: partial; accepted target-repository context with unresolved source-repository and migration fields
activation_rule: active by Owner decision recorded in this Specification; bounded initial scope only
```

This accepted Project Specification records bounded A1 Project Mode activation.

## Owner Acceptance

OWNER DECISION - A1 PROJECT SPECIFICATION

```yaml
decision: ACCEPTED
artifact: docs/project_specification.md
decision_date: 2026-08-10
scope: >
  Accept docs/project_specification.md as the approved A1 Project
  Specification instance for fof-locomotor-capacity-cohort, based on the
  completed source-grounded Review and Validation.
unresolved_items_remain_unresolved: true
next_authorized_planning_step: >
  Prepare a read-only Project Mode activation review for a narrowly bounded
  initial A1 Project Mode.
git_hard_gate_action_authorized: false
```

The Specification is accepted with its explicitly recorded unresolved items
remaining unresolved and scoped to the work they affect.

The following remain WORK_PACKAGE_SCOPED_BLOCKERS and are not resolved by this
acceptance:

- source repository identity, revision and source paths;
- Migration Contract fields not explicitly resolved by later Owner decisions;
- migration strategy;
- dependency closure;
- migration privacy/provenance review;
- approved execution `allowed_paths`;
- protected analysis environment;
- Quarto availability in the intended validation environment;
- `renv` activation/lockfile status;
- chair-rise reverse-coding formula;
- publication/output scope and disclosure-review authority.

Review cadence and permanent steward mapping remain recorded non-blocking
limitations where applicable.

This acceptance confirms:

- `scientific_changes_allowed.value: false`;
- unresolved migration values remain `NEEDS_VERIFICATION`;
- unavailable validation capabilities do not constitute PASS;
- scoped unresolved items do not authorize affected work.

This acceptance does not authorize:

- Project Mode activation;
- source-repository access or inspection;
- migration or copying;
- migration-strategy selection;
- protected-data access;
- scientific or analytical changes;
- resolution or implementation of the chair-rise formula;
- publication or release;
- staging;
- commit;
- push;
- pull request;
- history rewrite;
- force operations.

No `NEEDS_VERIFICATION` item is converted into a verified fact by this
acceptance.

## 2. Project Identity

```yaml
project_identity:
  project_title: fof-locomotor-capacity-cohort
  project_identifier: A1
  project_purpose: >
    Govern the public target repository scaffold for a 12-month
    fear-of-falling and locomotor-capacity cohort analysis, preserving
    structural and rendering reproducibility with public materials while
    excluding restricted participant-level data from Git.
  project_owner_or_review_authority: User / designated project owner
  steward_or_maintaining_role: NEEDS_VERIFICATION
  intended_repository_or_workspace_relationship: public target scaffold repository
  visibility_boundary: public repository with restricted-data exclusion
  project_lifecycle_state: specification accepted; Project Mode active for bounded initial scope
  effective_date_or_activation_condition: active by Owner decision dated 2026-08-10
  review_cadence_or_trigger: NEEDS_VERIFICATION
```

## 3. Source-of-Truth Inputs

```yaml
source_of_truth_inputs:
  accepted_project_authority:
    - docs/project_context.md: accepted A1 Project Context instance
  verified_repository_authority:
    - README.md
    - AGENTS.md
    - docs/restricted_data_policy.md
    - docs/reproducibility_scope.md
    - data/README.md
    - .gitignore
    - DESCRIPTION
    - _quarto.yml
  faro1_knowledge_authority:
    - KB_INDEX.md
    - PROJECT_SPECIFICATION_TEMPLATE.md
    - SAFETY_PRIVACY_GUARDRAILS.md
    - TOOL_AND_AGENT_POLICY.md
    - EVIDENCE_REVIEW_AND_ACCEPTANCE.md
    - RESEARCH_REPOSITORY_PATTERNS.md
  verified_source_inspection_facts:
    - source_repository: Tupatuko2023/Python-R-Scripts
    - source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
    - source_path: Fear-of-Falling
    - evidence_basis: WP-A1-SOURCE-REPOSITORY-IDENTITY-INSPECT PASS
    - approval_scope: source identity, pinned revision and path for further bounded inspection and migration planning only
  unresolved_candidate_inputs:
    - migration strategy
    - protected analysis environment
```

Verified source inspection facts are binding only for source identity, revision
pinning and source path existence. They do not approve migration, copying,
artifact eligibility, dependency closure, privacy/provenance, migration strategy,
scientific equivalence or source-data safety. Unverified candidate inputs are not
binding project authority.

## 4. Scope and Non-Goals

```yaml
scope:
  included_work:
    - maintain and validate the public target-repository scaffold
    - document public structural and rendering reproducibility boundaries
    - preserve synthetic-data-only public validation
    - define future evidence needed for source-repository inspection and migration planning
  excluded_work:
    - unbounded source-repository access or inspection outside approved Work Packages
    - migration, copying or history rewriting
    - migration strategy selection
    - protected-data access
    - scientific or analytical changes
    - manuscript conclusions or statistical interpretation changes
    - Project Mode activation
    - staging, commit, push, pull request, release or publication
  project_deliverables:
    - accepted A1 Project Context
    - accepted A1 Project Specification
    - future source-inspection evidence package if separately approved
  non_goals:
    - numerical reproduction of restricted participant-level analyses in the public repository
    - inclusion of raw, pseudonymized or analysis-ready participant-level data in Git
    - deciding chair-rise reverse-coding formula
  accepted_assumptions:
    - the inspected public repository is a target scaffold repository
    - public validation uses synthetic data
  unresolved_assumptions:
    - source path contents and artifact eligibility
    - whether migration is required and under what contract
    - approved protected analysis environment
    - Quarto availability in the intended validation environment
  approved_operating_mode: bounded initial Project Mode active
  out_of_scope_requests_requiring_new_approval:
    - source-repository inspection
    - migration execution
    - protected-data handling
    - Git Hard Gate actions
```

## 5. Data, Privacy and Disclosure Constraints

```yaml
data_privacy_disclosure_constraints:
  permitted_data_categories:
    - clearly synthetic test data in data/synthetic/
    - public, non-restricted repository documentation and code
  prohibited_data_categories:
    - real participant-level data
    - raw data
    - pseudonymized participant-level data
    - participant identifiers
    - analysis-ready participant-level files
    - row-level model-frame datasets
    - secrets and credentials
    - unknown-sensitivity files
  permitted_input_locations:
    - data/synthetic/
    - inspected public repository files within the target repository
  prohibited_input_locations:
    - data/raw/
    - data/restricted/
    - secrets/
    - credentials/
    - source repositories unless separately approved for read-only inspection
  permitted_output_locations:
    - outputs/tables/ for reviewed aggregate or synthetic outputs
    - outputs/figures/ for reviewed aggregate or synthetic outputs
  publication_or_disclosure_review_requirements:
    - required before any public exposure beyond current repository scope
    - required for aggregate outputs before publication or release
  secret_handling_requirement: do not persist secrets in repository, prompts, logs or artifacts
  incident_or_uncertainty_escalation_route: stop affected scope and mark NEEDS_VERIFICATION
  unresolved_data_governance_items:
    - approved protected analysis environment
    - disclosure review authority and thresholds
    - original restricted-data access pathway
```

The public repository evidence supports a narrow claim that restricted participant-level data is prohibited from the public repository. Broader restricted-data existence, location or accessibility remains outside this Specification unless separately source-grounded.

## 6. Repository and Artifact Boundaries

```yaml
repository_artifact_boundaries:
  approved_repository_role: public target scaffold repository
  approved_top_level_artifact_classes:
    - repository documentation
    - R functions and tests for scaffold validation
    - synthetic fixture data
    - Quarto smoke-test structure
    - project context and project specification instance documents
  generated_output_policy: generated outputs require provenance and review before acceptance or publication
  supplementary_material_policy: NEEDS_VERIFICATION
  manuscript_or_report_publication_boundary: public scaffold supports structural/rendering reproducibility; final manuscript scope NEEDS_VERIFICATION
  archive_or_release_boundary: NEEDS_VERIFICATION
  files_or_directories_that_must_remain_out_of_scope:
    - data/raw/
    - data/restricted/
    - secrets/
    - credentials/
    - outputs/logs/
    - manuscript/_freeze/
    - manuscript/.quarto/
    - unverified participant-level data files
  review_requirement_before_public_exposure: required
```

Observed repository directories are not approved execution `allowed_paths` unless a later Owner decision authorizes a bounded work package.

## 7. Migration Contract

### Owner Migration Requirement Decision

OWNER DECISION - A1 MIGRATION REQUIREMENT

```yaml
decision: APPROVE MIGRATION REQUIREMENT
project: fof-locomotor-capacity-cohort / A1
decision_date: 2026-08-10
migration_contract_field:
  migration_required: yes
verified_source:
  repository: Tupatuko2023/Python-R-Scripts
  revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
  source_root: Fear-of-Falling
scope: >
  A1 requires a controlled source-to-target migration of the approved subset of
  analysis code and supporting non-restricted artifacts from the verified source.
purpose: >
  Establish the migration requirement so remaining artifact-selection,
  provenance, strategy-comparison and migration-planning work can proceed under
  FARO1 controls.
scientific_changes_allowed: false
git_hard_gate_action_authorized: false
```

This decision does not approve any specific artifact for copying, final
artifact disposition, migration strategy, full dependency closure,
privacy/provenance full PASS, source or target execution paths, target paths,
copying, migration execution, portability changes, scientific or analytical
changes, protected-data access, participant-level data movement,
generated-output migration, staging, commit, push, pull request, release,
publication, history rewrite or force operations.

### Owner Migration Strategy Decision

OWNER DECISION - A1 MIGRATION STRATEGY

```yaml
decision: APPROVE STRATEGY
project: fof-locomotor-capacity-cohort / A1
decision_date: 2026-08-10
approved_migration_strategy: provenance_preserving_copy
strategy_scope:
  core:
    - Fear-of-Falling/R-scripts/K50/K50.r
    - Fear-of-Falling/R/functions/reporting.R
    - Fear-of-Falling/R/functions/person_dedup_lookup.R
    - safe documentation/specification artifacts required for migration understanding and validation
    - Fear-of-Falling/renv.lock
    - safe manifest specifications excluding generated manifest CSVs
  conditional_not_approved_for_copying:
    - K50 downstream source scripts
    - broader R/functions/*.R
  deferred_or_excluded:
    - K40
    - K51/K52/K53
    - K51 override/linkage CSV
    - participant/raw data
    - data/
    - generated outputs
    - .RData
    - .rds
    - generated manifest CSVs
    - credential-like configuration
    - runtime/session/temp artifacts
verified_source:
  repository: Tupatuko2023/Python-R-Scripts
  revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
  source_root: Fear-of-Falling
rationale: >
  The approved candidate scope is small and bounded, source
  repository/revision/path provenance is known, full Git history has not been
  shown to be materially necessary for this scope, and
  provenance_preserving_copy provides the strongest current scope isolation from
  restricted data, generated artifacts, unrelated history and deferred branches.
required_provenance:
  - source repository
  - immutable source revision
  - source path
  - target path
  - migrated artifact role
  - material portability adaptations
  - validation state
scientific_changes_allowed: false
git_hard_gate_action_authorized: false
next_authorized_planning_step: WP-A1-MIGRATION-EXECUTION-READINESS
```

This strategy approval does not approve the final source copy allowlist,
conditional artifacts, target paths, execution `allowed_paths`, copying,
migration execution, portability changes, dependency additions, scientific or
analytical changes, protected-data access, participant-level-data movement,
generated artifact migration, staging, commit, push, pull request, release,
publication, history rewrite or force operations.

### Owner K50 Core Scope Extension Decision

OWNER DECISION - EXTEND A1 K50 CORE STRATEGY SCOPE

```yaml
decision: APPROVE SCOPE EXTENSION
project: fof-locomotor-capacity-cohort / A1
decision_date: 2026-08-10
approved_migration_strategy: provenance_preserving_copy
scope_extension:
  add_to_k50_core_strategy_scope:
    - Fear-of-Falling/R/functions/init.R
source_authority:
  repository: Tupatuko2023/Python-R-Scripts
  revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
rationale: >
  R/functions/reporting.R unconditionally sources R/functions/init.R, and
  bounded read-only review found init.R eligible as a safe transitive source-code
  dependency with no additional local source() dependencies.
approved_strategy_scope_status:
  init.R: included in K50-core strategy scope
recommended_structural_target_mapping:
  Fear-of-Falling/R/functions/init.R: R/functions/init.R
helper_layout_recommendation: preserve R/functions/ structure for K50 helpers
scientific_changes_allowed: false
git_hard_gate_action_authorized: false
next_authorized_planning_step: resume WP-A1-MIGRATION-EXECUTION-READINESS
```

This scope-extension decision does not approve copying, migration execution,
final target mappings, portability edits, runtime-generated manifest/output
artifacts, `manifest/manifest.csv`, output directories, final source allowlist,
target execution `allowed_paths`, dependency installation, scientific or
analytical changes, staging, commit, push, pull request, release, publication or
any Git Hard Gate action. Runtime-generated outputs and manifest CSV remain
`REGENERATE_OR_REFERENCE`.

```yaml
migration_contract:
  migration_required: yes
  migration_required_authority_state: >
    Owner Decision dated 2026-08-10 establishes that A1 requires a controlled
    source-to-target migration of an approved non-restricted subset. This does
    not approve artifacts, strategy, copying or execution.
  source_repository: Tupatuko2023/Python-R-Scripts
  source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
  source_paths:
    - Fear-of-Falling
  source_identity_status:
    value: verified
    evidence:
      - WP-A1-SOURCE-REPOSITORY-IDENTITY-INSPECT: PASS
    approved_meaning: source repository, immutable revision and source root are verified for bounded planning
  target_repository: Tupatuko2023/fof-locomotor-capacity-cohort
  target_paths:
    - NEEDS_VERIFICATION
  migration_strategy:
    value: provenance_preserving_copy
    approval_scope: minimal K50-centered core only
    approval_state: approved for planning; execution not authorized
    pattern_reference: RESEARCH_REPOSITORY_PATTERNS.md
    evidence:
      - WP-A1-MIGRATION-STRATEGY-COMPARISON: PASS
  artifact_selection:
    scope: candidate groups identified; migration approval remains NEEDS_VERIFICATION
    classification_reference: RESEARCH_REPOSITORY_PATTERNS.md
    evidence:
      - WP-A1-SOURCE-ARTIFACT-INVENTORY-AND-CLASSIFICATION: PASS
      - WP-A1-SOURCE-DEPENDENCY-CLOSURE: PASS WITH DEFECTS
      - WP-A1-SOURCE-PRIVACY-PROVENANCE-REVIEW: PASS WITH DEFECTS
    accepted_classifications:
      - candidate source/code/docs groups may remain candidates only
      - final migration-approved artifacts: NEEDS_VERIFICATION
    retained_candidate_groups:
      - K50 primary analysis source code
      - required K50 downstream source scripts
      - required R/functions/*.R helpers
      - R/functions/init.R as approved K50-core transitive dependency
      - applicable K40 source code
      - K51/K52/K53 source code where still candidate
      - safe documentation and specification files
      - renv.lock
      - safe manifest specifications
    excluded_classifications:
      - participant-level or raw source data
      - data/ and data/external/
      - ${DATA_ROOT}/paper_02/KAAOS_data.xlsx
      - K40 patient-level csv/rds outputs
      - K50 rds model/data outputs and model-frame artifacts
      - K15/K18 .RData artifacts
      - generated outputs, figures, tables and runlogs
      - generated manifest CSVs unless separately verified safe and necessary
      - config/database.yml
      - session, runtime, temporary and unknown binary artifacts
    generated_artifact_policy: REGENERATE_OR_REFERENCE
    participant_level_artifact_policy: EXCLUDE
    final_artifact_approval_state: NEEDS_VERIFICATION
  dependency_closure_status:
    value: PASS WITH DEFECTS
    evidence: WP-A1-SOURCE-DEPENDENCY-CLOSURE
    resolved_safe_dependencies:
      - K50 source code dependencies on R/functions/reporting.R
      - K50 source code dependencies on R/functions/person_dedup_lookup.R
      - K50 reporting dependency on R/functions/init.R
      - documented R package dependencies recorded in renv.lock
      - safe documentation/specification dependencies reviewed for planning
    generatable_upstream_dependencies:
      - K50 downstream generated tables, figures, diagnostics and receipts
      - generated manifest records where needed for provenance
    external_or_restricted_inputs:
      - data/external/KaatumisenPelko.csv
      - ${DATA_ROOT}/paper_02/KAAOS_data.xlsx
      - raw enrichment workbooks or equivalent restricted inputs used by K51/K52/K53
    remaining_needs_verification:
      - exact final A1 execution entrypoints
      - locomotor_capacity/z3/Composite_Z outcome construction and authoritative status
      - FI22_nonperformance_KAAOS availability and semantics
      - K51 override/linkage CSV sensitivity and disposition
      - generated/model-frame artifact handling
      - final execution allowlist and target mapping for approved K50-core files
  privacy_review_status:
    value: PASS WITH DEFECTS
    authority_reference: SAFETY_PRIVACY_GUARDRAILS.md
    evidence: WP-A1-SOURCE-PRIVACY-PROVENANCE-REVIEW
    participant_data_safety_state: source data are not safe for migration
    preserved_blockers:
      - participant-level and raw data dependencies
      - generated model/data artifacts
      - K51 override/linkage CSV
      - raw enrichment inputs
      - unknown/generated manifest CSVs
      - secret or credential-like configuration
  code_data_separability:
    value: PARTIALLY_SUPPORTED
    meaning: >
      Source code, documentation and dependency metadata appear separable for
      planning purposes. Real participant data and sensitive or generated
      artifacts remain external, excluded or unresolved, and several execution
      dependencies remain NEEDS_VERIFICATION.
  provenance_strategy:
    value: NEEDS_VERIFICATION
    source_grounded_facts:
      - canonical source repository is Tupatuko2023/Python-R-Scripts
      - immutable source revision is 8a4a4e37751a4416a6a875787a8173f621da91a9
      - repository-relative source root is Fear-of-Falling
      - candidate artifact roles and dependency relationships were reviewed at group level
    remaining_gaps:
      - authorship and rights review
      - formal legacy or superseded disposition for candidate groups
      - artifact-level provenance gaps that materially affect later migration selection
    non_requirements:
      - commit signing is not recorded as a universal provenance requirement
  portability_changes_allowed:
    value: NEEDS_VERIFICATION
    boundary_reference: RESEARCH_REPOSITORY_PATTERNS.md
  scientific_changes_allowed:
    value: false
    analytical_change_authorization: required-if-true
  required_validation:
    - git diff --check for repository edits
    - R tests when R code or validation behavior is affected
    - Quarto render when Quarto is available and render scope is affected
    - privacy and secret review for candidate changes
    - technical portability validation before migration execution
    - dependency validation before migration execution
    - privacy/provenance validation before accepting migrated artifacts
    - scientific/analytical parity validation before any reproduction claim
  expected_reference_results: NEEDS_VERIFICATION
  allowed_paths:
    - NEEDS_VERIFICATION
  forbidden_paths:
    - data/raw/
    - data/restricted/
    - secrets/
    - credentials/
    - NEEDS_VERIFICATION
  rollback_strategy: NEEDS_VERIFICATION
  owner_approval_gates:
    - source-repository inspection
    - migration strategy selection
    - migration execution
    - protected-data access
    - staging
    - commit
    - push
    - pull request
    - release
    - publication
```

These source repository, revision and path values are approved as verified
source identity and pinning facts for further bounded migration planning.
Artifact review, dependency closure and privacy/provenance review have been
recorded only at the partial states stated above. This Migration Contract does
not authorize migration, copying, history rewrite, strategy selection,
protected-data access, participant-level inspection, generated-artifact copying,
scientific or analytical changes, staging, commit, push, pull request, release
or publication.

## 8. Analysis and Output Requirements

```yaml
analysis_output_requirements:
  analysis_objective: >
    Public repository governance for a future fear-of-falling and
    locomotor-capacity cohort analysis pipeline; final analysis objectives
    and model specifications remain NEEDS_VERIFICATION.
  approved_analysis_inputs:
    - data/synthetic/synthetic_fixture.csv for structural validation only
  synthetic_fixture_policy: synthetic fixtures support structural and test validation only
  expected_tables_figures_reports_or_supplementary_outputs: NEEDS_VERIFICATION
  provenance_requirements_for_generated_outputs: required before acceptance or publication
  traceability_requirement_between_analysis_code_and_public_outputs: required when outputs are created
  limitations_that_must_be_reported:
    - public repository does not contain restricted participant-level data
    - full numerical reproducibility requires approved restricted environment
    - Quarto unavailable in current PATH
    - chair-rise reverse-coding formula unresolved
  outputs_requiring_separate_review_before_acceptance_or_publication:
    - tables
    - figures
    - rendered manuscripts
    - supplementary materials
```

This Specification does not modify manuscript conclusions, statistical interpretation, model formulas or clinical coding assumptions.

## 9. Tool, Agent and Environment Constraints

```yaml
tool_agent_environment_constraints:
  approved_runtime_environment_or_class: NEEDS_VERIFICATION
  observed_local_tools:
    - git available during inspection
    - Rscript available during inspection
  required_local_or_ci_validation_tools:
    - git
    - Rscript
    - quarto when render validation is in scope
  unavailable_tools_and_impact:
    - quarto CLI not found in current PATH; Quarto render cannot be claimed PASS in this environment
  agent_access_boundaries:
    - target repository read/write only within approved work packages
    - no protected-data access
    - no source-repository access without separate approval
  network_use_restrictions:
    - no network source inspection unless separately approved
  package_management_restrictions:
    - dependency installation or updates require separate approval when they change repository state
  git_commit_push_release_restrictions:
    - staging requires explicit Git Hard Gate
    - commit requires explicit Git Hard Gate
    - push requires explicit Git Hard Gate
    - pull request, release and publication require explicit Owner approval
  tool_or_environment_items_marked_NEEDS_VERIFICATION:
    - approved protected analysis environment
    - approved dependency update policy
    - Quarto availability in intended validation environment
    - `renv` activation and lockfile status
```

Tool availability does not imply permission.

## 10. Evidence, Review and Acceptance Requirements

```yaml
evidence_review_acceptance_requirements:
  minimum_evidence_required_for_project_changes:
    - source-grounded file inspection or command output
    - changed-file manifest for repository edits
    - relevant diff or no-index diff for untracked files
    - privacy and secret review
    - validation command results or explicit NOT RUN limitation
  required_review_categories:
    - scope and allowed files
    - source-of-truth classification
    - data/privacy boundary
    - tool/Git boundaries
    - migration-contract unresolved fields
    - activation blockers
  required_validation_categories:
    - structural/template completeness
    - contradiction and dependency review
    - git diff --check for edits
    - R tests when relevant
    - Quarto render when available and relevant
  acceptance_authority: User / designated project owner
  acceptable_PASS_FAIL_decision_scope: bounded work-package only
  defect_handling_expectations: blocking defects stop affected scope until corrected or explicitly deferred
  treatment_of_unavailable_validation_tools: report NOT RUN with reason and residual risk
  lifecycle_approval_requirement: Owner approval required for Project Specification acceptance
  commit_push_release_publication_approval_gates:
    - staging
    - commit
    - push
    - pull request
    - release
    - publication
```

Agent assertions are not objective evidence unless grounded in inspected files, command output, diffs, logs or recorded Owner decisions.

## 11. Activation, Suspension and Retirement

```yaml
activation_suspension_retirement:
  project_mode_status: active
  activation_prerequisite:
    - accepted Project Context
    - accepted Project Specification
    - Owner activation decision recorded for bounded initial scope
  activation_authority: User / designated project owner
  freshness_requirement: NEEDS_VERIFICATION
  conditions_that_block_activation:
    - Project Specification not accepted
    - source-of-truth conflict
    - unresolved activation authority
    - unresolved protected-data boundary for requested work
    - attempt to treat migration fields as approved when they remain NEEDS_VERIFICATION
  conditions_that_suspend_active_use:
    - evidence conflict
    - safety/privacy uncertainty affecting requested scope
    - stale or superseded project authority
  deactivation_or_retirement_criteria: NEEDS_VERIFICATION
  required_action_when_activation_state_uncertain: stop affected Project Mode use and mark NEEDS_VERIFICATION
```

## Owner Activation Decision

OWNER DECISION - ACTIVATE A1 PROJECT MODE

```yaml
decision: ACTIVATE
project: fof-locomotor-capacity-cohort / A1
decision_date: 2026-08-10
project_authorities:
  - accepted and validated docs/project_context.md
  - accepted and validated docs/project_specification.md
  - applicable FARO1 Knowledge routed through KB_INDEX.md
activation_scope:
  - read-only target-repository inspection
  - documentation and planning within separately approved bounded Work Packages
  - synthetic/public scaffold work within separately approved bounded Work Packages
  - validation using available and verified tools
  - preparation, Review and Validation of later bounded Work Packages and project artifacts
authorization_model:
  unrestricted_execution_authority_created: false
  bounded_work_packages_required_for_write_work: true
  git_hard_gate_action_authorized: false
scoped_unresolved_items_remain_unresolved: true
```

Project Mode activation does not create unrestricted execution authority. Write
work must remain inside separately approved bounded Work Packages / MacroGates
with explicit objective, allowed paths, operation classes, evidence requirements,
exclusions and stop conditions.

This activation does not authorize source-repository access or inspection,
source-to-target migration or copying, migration-strategy selection,
dependency-closure execution against a source repository, protected-data access,
participant-level-data handling, scientific or analytical changes, chair-rise
reverse-coding resolution or implementation, full numerical reproduction claims,
Quarto-render PASS claims while Quarto is unavailable, publication, release, pull
request, staging, commit, push, history rewrite, force operations, credential
access or any other Hard Gate action without separate explicit approval.

Existing `NEEDS_VERIFICATION` and Work-Package-scoped blockers remain unresolved
for their affected scopes. Activation does not promote them to verified facts or
authorize affected work.

Suspend the affected Project Mode scope on conflict between applicable
authorities, stale or superseded Project Context or Project Specification,
protected-data exposure, secret exposure, unknown-sensitivity exposure, proposed
work exceeding the activated boundary, MaterialBoundaryChange or insufficient
evidence for an affected Review, Validation or acceptance claim.

## 12. Source Inspection Planning

The following Migration Contract fields have been partially addressed by
completed bounded read-only source-inspection Work Packages where recorded
below. Remaining unresolved fields require separate future authority before they
can be used for migration approval or execution.

| Field | Current state | Evidence needed | Could source inspection resolve it? | Privacy/provenance precondition |
|---|---|---|---|---|
| `migration_contract.source_repository` | verified: `Tupatuko2023/Python-R-Scripts` | none for identity; artifact authority still unresolved | no for identity; yes for later contents | inspect metadata only; do not open unknown-sensitivity content |
| `migration_contract.source_revision` | verified: `8a4a4e37751a4416a6a875787a8173f621da91a9` | none for revision; artifact authority still unresolved | no for revision; yes for later contents | no protected content needed |
| `migration_contract.source_paths` | verified source root: `Fear-of-Falling` | artifact-level disposition remains incomplete | yes | stop on unknown sensitivity; no copying |
| `migration_contract.migration_required` | `yes` by Owner Decision dated 2026-08-10 | none for requirement; scoped contract fields remain unresolved | no | does not authorize copying or protected-data access |
| `migration_contract.migration_strategy.value` | `provenance_preserving_copy` for minimal K50-centered core by Owner Decision dated 2026-08-10 | execution readiness, exact allowlist, target paths and validation plan | partially | strategy approval is not copy or execution authority |
| `migration_contract.artifact_selection.scope` | candidate groups identified; approval still `NEEDS_VERIFICATION` | final artifact migration approval and excluded-path enforcement details | partially | classify before content exposure; stop on restricted data |
| `migration_contract.dependency_closure_status` | `PASS WITH DEFECTS` | named unresolved dependency branches | partially | inspect only necessary code paths |
| `migration_contract.privacy_review_status.value` | `PASS WITH DEFECTS` | blocker-specific resolution for unknown/restricted/generated artifacts | partially | fail-closed safety review required |
| `migration_contract.provenance_strategy` | `NEEDS_VERIFICATION` | authorship/rights review and formal legacy/superseded disposition | yes | metadata-first inspection |
| `migration_contract.expected_reference_results` | `NEEDS_VERIFICATION` | approved reference results or statement that none are available | partially | no participant-level outputs |
| `migration_contract.allowed_paths` | `NEEDS_VERIFICATION` | Owner-approved execution boundary | no | Owner decision required |

## 13. Open `NEEDS_VERIFICATION` Items

- Final artifact migration approval/disposition.
- Migration execution readiness for approved K50-core strategy.
- Unresolved dependency branches from dependency closure PASS WITH DEFECTS.
- Blocker-specific privacy/provenance resolution after PASS WITH DEFECTS.
- Authorship/rights review and formal legacy/superseded disposition.
- Approved execution `allowed_paths`.
- Approved protected analysis environment.
- Quarto availability in intended validation environment.
- `renv` activation and dependency-lock status.
- Chair-rise reverse-coding formula.
- Publication target, output scope and disclosure review authority.
- Project Specification review cadence.
- Steward or maintaining role.

## 14. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  routes-to -> PROJECT_SPECIFICATION_TEMPLATE.md for project specification structure

docs/project_context.md
  informs -> docs/project_specification.md

PROJECT_SPECIFICATION_TEMPLATE.md
  structures -> docs/project_specification.md

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> data, privacy, protected-data and publication requirements

TOOL_AND_AGENT_POLICY.md
  constrains -> tool, command, network, Git and agent boundaries

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> evidence, review, validation and acceptance gates

RESEARCH_REPOSITORY_PATTERNS.md
  informs -> migration patterns without authorizing execution
```

This Specification records bounded Project Mode activation. It does not approve source-repository inspection, migration, staging, commit, push, pull request, release or publication.
