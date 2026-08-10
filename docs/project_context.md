# A1 Project Context

## 1. Metadata

```yaml
project_context_id: A1-PROJECT-CONTEXT
version: 0.1.0
status: accepted
document_evidence_state: validated
project_name: fof-locomotor-capacity-cohort
project_short_name: A1
project_phase: MVP scaffold; Project Mode active for bounded initial scope
review_authority: User / designated project owner
```

## 2. Project Identity

```yaml
project_identity:
  project_name: fof-locomotor-capacity-cohort
  project_short_name: A1
  project_phase: MVP scaffold; Project Mode active for bounded initial scope
  mission_or_goal: >
    Document a 12-month fear-of-falling and locomotor-capacity cohort
    analysis pipeline with public structural and rendering reproducibility
    while keeping restricted participant-level data out of Git.
```

The inspected target repository currently contains a safe reproducibility scaffold, synthetic test data, R test code and Quarto smoke-test structure. The repository documentation states that real analysis code and the manuscript have not yet been migrated and that analytical results are not included.

## 3. Repository Context

```yaml
repository_context:
  primary_repository: Tupatuko2023/fof-locomotor-capacity-cohort
  primary_repository_role: public target scaffold repository
  related_repositories:
    - repository: Tupatuko2023/Python-R-Scripts
      source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
      source_path: Fear-of-Falling
      status: verified source identity, pinned revision and source path for further bounded inspection and migration planning only
  repository_relationship_summary: >
    The candidate source repository identity, inspected immutable revision and
    repository-relative source path have been verified for further bounded
    inspection and migration planning. Migration requirement, source path
    contents, artifact eligibility, dependency closure, privacy/provenance,
    migration strategy and copying permission remain NEEDS_VERIFICATION.
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
    - target repository AGENTS.md
    - target repository docs/restricted_data_policy.md
    - target repository docs/reproducibility_scope.md
    - target repository .gitignore
    - target repository DESCRIPTION
    - target repository _quarto.yml
    - FARO1 Knowledge Base baseline 885c6e0
    - WP-A1-SOURCE-REPOSITORY-IDENTITY-INSPECT PASS: source identity, revision and path metadata only
  source_scope_summary: >
    Target-repository scaffold context plus bounded source identity metadata.
    Source repository content inspection, artifact classification, dependency
    closure, privacy/provenance review and migration execution have not been
    approved or performed.
  authority_or_precedence_references:
    - KB_INDEX.md
    - PROJECT_CONTEXT_TEMPLATE.md
    - SAFETY_PRIVACY_GUARDRAILS.md
    - TOOL_AND_AGENT_POLICY.md
    - EVIDENCE_REVIEW_AND_ACCEPTANCE.md
    - PROJECT_SPECIFICATION_TEMPLATE.md
    - RESEARCH_REPOSITORY_PATTERNS.md
```

Untracked migration notes in `GPT/` may contain candidate source-repository claims, but they are not accepted project authority in this context.

## 6. Data Context

```yaml
data_context:
  applicable_classification_references:
    - SAFETY_PRIVACY_GUARDRAILS.md
    - AGENTS.md
    - docs/restricted_data_policy.md
    - data/README.md
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
  publication_target_known: unknown
  repository_role_relative_to_publication: >
    Supports transparent pipeline documentation and public reproducibility
    scaffolding, not final analytical results.
```

This context does not authorize publication, release, archive deposit, pull request creation or external disclosure.

## 8. Migration Context

```yaml
migration_context:
  migration_expected: NEEDS_VERIFICATION
  source_repository_relationship: source identity, pinned revision and source path verified for further bounded inspection and migration planning only
  source_repository: Tupatuko2023/Python-R-Scripts
  source_revision: 8a4a4e37751a4416a6a875787a8173f621da91a9
  source_path: Fear-of-Falling
  target_repository_relationship: public target scaffold repository verified
  migration_requirement_status: NEEDS_VERIFICATION
  project_specification_reference: NEEDS_VERIFICATION
  repository_patterns_reference: RESEARCH_REPOSITORY_PATTERNS.md
```

No migration strategy is selected. No source repository content inspection, artifact classification, dependency closure, privacy/provenance review or migration execution has been approved by this context.

## 9. Validation Environment Context

```yaml
validation_environment_context:
  available_environments:
    - git available during bootstrap inspection
    - Rscript available during bootstrap inspection
  known_unavailable_capabilities:
    - quarto CLI not found in PATH during bootstrap inspection
  environment_specific_limitations:
    - Quarto render cannot be validated in the current PATH
    - chair-rise reverse-coding formula remains NEEDS_VERIFICATION
    - renv activation is not active because renv/activate.R was not present during R test startup
```

Tool availability does not imply permission. Unavailable validation tools are limitations, not PASS evidence.

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
| Agent safety rules, allowed synthetic data, forbidden participant data and validation commands | `AGENTS.md` |
| Restricted data exclusions and synthetic validation requirement | `docs/restricted_data_policy.md` |
| Public structural/render reproducibility and restricted-environment numerical reproducibility | `docs/reproducibility_scope.md` |
| Ignored restricted/raw data, secrets, credentials and prohibited file types | `.gitignore` |
| Package identity and R/testthat context | `DESCRIPTION` |
| Quarto project output and execution configuration | `_quarto.yml` |
| Project Context template boundary and required fields | `PROJECT_CONTEXT_TEMPLATE.md` |
| Safety, tool, evidence and migration boundaries | FARO1 Knowledge Base baseline `885c6e0` |

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
    - applicable FARO1 Knowledge routed through KB_INDEX.md
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

- Source path contents and artifact classification/disposition.
- Whether migration is required for A1 and under what approved contract.
- Project Specification storage location and approval scope.
- Approved execution `allowed_paths` and `forbidden_paths`.
- Approved protected analysis environment.
- Quarto CLI availability in the intended validation environment.
- `renv` activation and dependency-lock status.
- Chair-rise reverse-coding formula.
- Publication target and publication review authority.

## 15. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  routes-to -> PROJECT_CONTEXT_TEMPLATE.md for project context structure

PROJECT_CONTEXT_TEMPLATE.md
  structures -> docs/project_context.md

PROJECT_SPECIFICATION_TEMPLATE.md
  constrains -> boundary between project context and project requirements

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> data, privacy, protected-data and publication context

TOOL_AND_AGENT_POLICY.md
  constrains -> tool, command, environment and external-action context

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> review, validation and acceptance evidence

RESEARCH_REPOSITORY_PATTERNS.md
  informs -> migration-context boundaries without authorizing execution
```

This context is not an active Project Specification, Migration Contract, source-repository access authorization, migration authorization or Git Hard Gate record.
