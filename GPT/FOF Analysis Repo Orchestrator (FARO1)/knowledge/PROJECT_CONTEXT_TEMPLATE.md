# FARO1 Project Context Template

## 1. Document Metadata

```yaml
title: FARO1 Project Context Template
document_id: FARO1-PROJECT-CONTEXT-TEMPLATE
version: 0.1.0
status: approved
priority: P1
scope: Template structure and required fields for project context documents used by FARO1 Project Mode
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define the contextual facts and relationships that FARO1 needs to interpret an activated project correctly.
load_condition: template-only
authority_level: template
activation_rule: Load only when drafting, reviewing or validating project context structure. This template is not an active project context.
```

## 2. Primary Responsibility

This document defines the template structure for project context documents used by FARO1.

It does not define an active project, project requirements, project authorization, repository architecture patterns, migration strategy, tool permissions, privacy classifications, evidence acceptance procedure, Knowledge lifecycle governance, decision-log structure or session state.

## 3. Scope

This template applies when FARO1 needs a structured project context document describing the environment, sources, repository relationships, data boundaries, publication boundary, migration context or validation environment needed to interpret a project correctly.

It covers:

- project identity and mission context;
- repository and workspace relationships;
- source and authority context;
- data and privacy context by reference;
- publication and external-exposure context;
- migration existence and source/target relationship context;
- validation environment context;
- explicit exclusions for values that belong elsewhere.

It is a template only. A completed project context document must be separately reviewed before it is treated as project context.

## 4. Project Context vs Project Specification

Project Context answers:

```text
In what environment, source set and repository relationships does FARO1 operate?
```

Project Specification answers:

```text
What is approved for this project, under what requirements, boundaries and acceptance criteria?
```

A completed project context may state that a source repository relationship exists, that a publication boundary is known, or that a migration requirement is expected. It must not approve the work, define acceptance criteria, choose a migration strategy, set allowed paths for execution, or replace a completed project specification.

Example boundary:

```text
PROJECT_CONTEXT:
source_repository_relationship: exists
relationship_summary: <source repository provides analysis code to be assessed for possible migration>

PROJECT_SPECIFICATION:
source_repository: <approved URI or identifier>
source_commit: <approved commit>
source_paths: <approved paths>
migration_strategy: <approved strategy>
allowed_paths: <approved paths>
required_validation: <approved validation>
```

## 5. Project Context vs Repository Patterns

Project Context records relevant project relationships and environmental facts.

Repository Patterns define reusable repository architecture and implementation patterns that may inform project design.

Project Context may record:

- whether migration is expected;
- known source and target repository relationships;
- migration requirement status;
- a pointer to the applicable project specification or repository-pattern reference.

Project Context must not define:

- migration strategy selection rules;
- history-rewrite method;
- file-classification taxonomy;
- dependency-closure algorithm;
- scientific parity procedure;
- repository architecture patterns.

## 6. Required Context Fields

A completed project context document must include:

```yaml
project_identity:
  project_name: NEEDS_VERIFICATION
  project_short_name: NEEDS_VERIFICATION
  project_phase: NEEDS_VERIFICATION
  mission_or_goal: NEEDS_VERIFICATION

repository_context:
  primary_repository: NEEDS_VERIFICATION
  primary_repository_role: NEEDS_VERIFICATION
  related_repositories: []
  repository_relationship_summary: NEEDS_VERIFICATION

working_context:
  expected_repository_root: <project-defined>
  approved_working_directories: []
  environment_identity: NEEDS_VERIFICATION
  platform_constraints: []

source_context:
  approved_source_categories: []
  source_scope_summary: NEEDS_VERIFICATION
  authority_or_precedence_references: []

data_context:
  applicable_classification_references: []
  restricted_data_present: unknown
  synthetic_data_available: unknown
  explicit_data_exclusions: []

publication_context:
  public_private_boundary: NEEDS_VERIFICATION
  publication_target_known: unknown
  repository_role_relative_to_publication: NEEDS_VERIFICATION

migration_context:
  migration_expected: unknown
  source_repository_relationship: NEEDS_VERIFICATION
  target_repository_relationship: NEEDS_VERIFICATION
  migration_requirement_status: NEEDS_VERIFICATION
  project_specification_reference: NEEDS_VERIFICATION

validation_environment_context:
  available_environments: []
  known_unavailable_capabilities: []
  environment_specific_limitations: []
```

Placeholder values must be replaced, removed or marked `NEEDS_VERIFICATION` in a completed project context document.

## 7. Optional Context Fields

A completed project context document may include:

- project aliases or external identifiers;
- related workspaces;
- approved local non-secret configuration categories;
- external-service relationships;
- known package or runtime environment families;
- CI or validation environment names;
- source repository relationship history at a high level;
- known publication or archive surfaces;
- links to approved project specifications or decision records;
- explicit out-of-scope repositories or workspaces.

Optional fields must not become implicit authorization. If an optional context value affects permissions, protected data, publication, migration method, validation acceptance or project requirements, the applicable owner document or project specification must control the decision.

## 8. Source and Authority Context

A completed project context document must identify source categories needed to interpret the project. Eligible source categories may include:

| Source category | Context value |
|---|---|
| Approved Knowledge document | Filename and relevant scope |
| Approved project specification | Filename or identifier |
| Approved repository policy | File, repository or authority |
| Approved data-governance source | Authority and applicable restriction |
| Approved publication source | Boundary, target or review authority |
| Approved environment source | Runtime, workspace or environment authority |
| Source material pending review | Identifier and `NEEDS_VERIFICATION` status |

Unverified sources must not be treated as binding project authority. Conflicting sources must stop the affected context decision and be marked `NEEDS_VERIFICATION`.

## 9. Repository and Workspace Context

A completed project context document must describe repository and workspace relationships without prescribing repository architecture.

It should identify:

- primary repository identity;
- primary repository role;
- related repositories and their relationship type;
- source repository relationship, if any;
- target repository relationship, if any;
- expected repository root as a project-defined role, not a local absolute path;
- approved working directories by role;
- forbidden or out-of-scope repository areas, if known;
- external-service or remote relationships, if known.

This template must not include local absolute paths. Personal home directories, device-specific mount points or temporary shell session paths belong to local runtime context, not permanent Knowledge.

## 10. Data and Privacy Context

A completed project context document must identify applicable data and privacy context by reference to approved authorities. It must not duplicate canonical safety classifications.

It may state:

```yaml
data_context:
  applicable_classification_references:
    - SAFETY_PRIVACY_GUARDRAILS.md
  restricted_data_present: yes | no | unknown
  participant_level_data_in_repository: no | unknown
  synthetic_data_available: yes | no | unknown
  explicit_data_exclusions:
    - <category or path role, not sensitive content>
```

It must not include participant-level data, direct identifiers, secrets, credentials, row-level examples, sensitive filesystem layouts, real storage locations or data values.

When data sensitivity, provenance or authority is uncertain, the affected context item remains `NEEDS_VERIFICATION` and the applicable safety policy controls.

## 11. Publication and External Exposure Context

A completed project context document should identify known publication and external-exposure boundaries:

- public/private repository boundary;
- publication target, if known;
- repository role relative to publication;
- release or archive boundary, if known;
- external services or hosted artifacts, if known;
- review authority for publication or disclosure, if known.

This section does not authorize publication, release, upload, archive deposit, pull request creation or external disclosure. External actions remain governed by the applicable tool, safety and evidence policies and by project-specific authorization.

## 12. Migration Context

A completed project context document may identify whether migration is expected and how repositories relate.

Allowed fields include:

```yaml
migration_context:
  migration_expected: yes | no | unknown
  source_repository_relationship: NEEDS_VERIFICATION
  target_repository_relationship: NEEDS_VERIFICATION
  migration_requirement_status: none | proposed | expected | approved | NEEDS_VERIFICATION
  project_specification_reference: NEEDS_VERIFICATION
  repository_patterns_reference: NEEDS_VERIFICATION
```

This section must not select or require a migration strategy. It must not require `git-filter-repo`, history rewriting, direct copy, reconstruction, dependency-closure algorithms, file-classification taxonomies or scientific parity procedures.

Migration strategy belongs to the applicable project specification and repository-pattern guidance. Tool authorization belongs to `TOOL_AND_AGENT_POLICY.md`. Safety and privacy handling belongs to `SAFETY_PRIVACY_GUARDRAILS.md`. Evidence and validation acceptance belongs to `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

## 13. Validation Environment Context

A completed project context document should identify known validation environments and limitations:

```yaml
validation_environment_context:
  available_environments:
    - <environment name or role>
  known_unavailable_capabilities:
    - <capability and impact>
  environment_specific_limitations:
    - <limitation and residual risk>
```

This section may record that a capability is available or unavailable. It must not infer permission from availability and must not convert an unavailable validation tool into PASS. Tool use and unavailable-validation behavior remain governed by `TOOL_AND_AGENT_POLICY.md` and `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

## 14. Explicit Exclusions

This template must not contain:

- active project requirements;
- project approval decisions;
- active project state;
- session state;
- local absolute paths;
- real participant-level data;
- secrets or credentials;
- privacy classification tables;
- tool or command policy;
- evidence PASS/FAIL procedure;
- repository architecture patterns;
- migration strategy rules;
- file-classification taxonomy;
- dependency-closure algorithm;
- scientific parity procedure;
- manuscript, Quarto, Docker, Posit Package Manager, GxP, FDA or SLSA assumptions;
- Change History section.

## 15. Completed Project Context Skeleton

The following skeleton may be copied when drafting a completed project context document:

```markdown
# Project Context

Metadata:

project_context_id: NEEDS_VERIFICATION
version: 0.1.0
status: draft
document_evidence_state: source-grounded
project_name: NEEDS_VERIFICATION
project_short_name: NEEDS_VERIFICATION
project_phase: NEEDS_VERIFICATION
review_authority: NEEDS_VERIFICATION

Project Identity:

mission_or_goal: NEEDS_VERIFICATION
project_scope_summary: NEEDS_VERIFICATION

Repository Context:

primary_repository: NEEDS_VERIFICATION
primary_repository_role: NEEDS_VERIFICATION
related_repositories: []
repository_relationship_summary: NEEDS_VERIFICATION

Working Context:

expected_repository_root: <project-defined>
approved_working_directories: []
environment_identity: NEEDS_VERIFICATION
platform_constraints: []

Source Context:

approved_source_categories: []
source_scope_summary: NEEDS_VERIFICATION
authority_or_precedence_references: []

Data Context:

applicable_classification_references: []
restricted_data_present: unknown
synthetic_data_available: unknown
explicit_data_exclusions: []

Publication Context:

public_private_boundary: NEEDS_VERIFICATION
publication_target_known: unknown
repository_role_relative_to_publication: NEEDS_VERIFICATION

Migration Context:

migration_expected: unknown
source_repository_relationship: NEEDS_VERIFICATION
target_repository_relationship: NEEDS_VERIFICATION
migration_requirement_status: NEEDS_VERIFICATION
project_specification_reference: NEEDS_VERIFICATION
repository_patterns_reference: NEEDS_VERIFICATION

Validation Environment Context:

available_environments: []
known_unavailable_capabilities: []
environment_specific_limitations: []

Explicit Exclusions:

out_of_scope_context: []
```

## 16. Review Requirements

Before accepting a completed project context document, review must verify:

- every required context field is present;
- placeholder values are replaced, removed or marked `NEEDS_VERIFICATION`;
- source and authority references are inspectable;
- repository relationships are described without prescribing architecture patterns;
- migration context records relationships and status only;
- data and privacy context references the safety authority without duplicating classifications;
- tool and validation environment context does not infer permission from availability;
- publication context does not authorize external exposure;
- no project requirements or acceptance criteria are introduced;
- no project or session state is embedded in the template document;
- no secrets, participant data or local absolute paths are present.

## 17. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  registers -> PROJECT_CONTEXT_TEMPLATE.md
  routes-to -> PROJECT_CONTEXT_TEMPLATE.md for project context structure questions

PROJECT_SPECIFICATION_TEMPLATE.md
  constrains -> boundary between project context and project requirements

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> data, privacy, protected-data and publication context

TOOL_AND_AGENT_POLICY.md
  constrains -> tool, command, environment and external-action context

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> review, validation and acceptance evidence for project context

RESEARCH_REPOSITORY_PATTERNS.md
  owns -> repository architecture and migration pattern guidance when approved
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `PROJECT_SPECIFICATION_TEMPLATE.md` owns project specification structure.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the evidence review and acceptance authority.
- `RESEARCH_REPOSITORY_PATTERNS.md`, when approved, owns repository architecture and migration pattern guidance.

Proposed or absent files must not be represented as active runtime Knowledge sources.

## 18. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P1`.
- [ ] Status `approved`.
- [ ] Evidence state `validated`.
- [ ] Load condition `template-only`.
- [ ] Authority level `template`.
- [ ] Project context structure is defined.
- [ ] Project Context vs Project Specification boundary is explicit.
- [ ] Project Context vs Repository Patterns boundary is explicit.
- [ ] Required context fields are defined.
- [ ] Optional context fields are defined.
- [ ] Source and authority context is defined.
- [ ] Repository and workspace context is defined without prescribing architecture patterns.
- [ ] Data and privacy context is defined without duplicating safety classifications.
- [ ] Publication and external-exposure context does not authorize publication.
- [ ] Migration context records relationships and status without owning migration strategy.
- [ ] Validation environment context does not infer permission from tool availability.
- [ ] No active project values.
- [ ] No FOF/A1 project values.
- [ ] No local absolute paths.
- [ ] No session state.
- [ ] No manuscript assumption.
- [ ] No Quarto requirement.
- [ ] No `git-filter-repo` requirement.
- [ ] No Docker, Posit Package Manager, GxP, FDA or SLSA assumption.
- [ ] No file-classification taxonomy.
- [ ] No dependency-closure algorithm.
- [ ] No scientific parity procedure.
- [ ] No duplicate P0 policy content.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent project context storage location;
- completed project context approval requirements;
- relationship to future active project context documents;
- full P1 activation prerequisites.
