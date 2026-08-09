# FARO1 Project Specification Template

## 1. Document Metadata

```yaml
title: FARO1 Project Specification Template
document_id: FARO1-PROJECT-SPECIFICATION-TEMPLATE
version: 0.2.0
status: approved
priority: P0
scope: Template structure and required fields for a later FARO1 project specification
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define the structure and fields of a later project specification.
load_condition: template-only
authority_level: template
activation_rule: Load only when drafting, reviewing or validating the structure of a project specification. This template is not an active project specification.
```

## 2. Primary Responsibility

This document defines the required structure, fields and template-level rules for a later FARO1 project specification.

It does not define an active project, project state, session state, research conclusions, repository architecture patterns, evidence acceptance procedure, safety classifications, tool policy or Knowledge lifecycle governance.

## 3. Template Use

Use this template to draft a project-specific `PROJECT_SPECIFICATION.md` or an equivalent approved project specification document when Project Mode requires one.

The completed project specification must be source-grounded, reviewed and approved before it can be treated as project authority. This template cannot be activated as a project instance and cannot substitute for project approval.

Template instructions are written as requirements for the completed project specification. Placeholder values must be replaced, removed or marked `NEEDS_VERIFICATION` before approval.

## 4. Required Metadata Block

A completed project specification must begin with canonical metadata:

```yaml
title: NEEDS_VERIFICATION
document_id: NEEDS_VERIFICATION
version: 0.1.0
status: draft
project_id: NEEDS_VERIFICATION
scope: NEEDS_VERIFICATION
steward: NEEDS_VERIFICATION
review_authority: NEEDS_VERIFICATION
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: source-grounded
project_mode_status: proposed
source_of_truth_state: NEEDS_VERIFICATION
activation_rule: NEEDS_VERIFICATION
```

The completed project specification must not use placeholder values for approved runtime activation unless the unresolved value is explicitly accepted as non-blocking by the review authority.

## 5. Required Project Identity Fields

The completed project specification must define:

- project title;
- project identifier;
- project purpose;
- project owner or review authority;
- steward or maintaining role;
- intended repository or workspace relationship;
- public, internal or restricted visibility boundary;
- project lifecycle state;
- effective date or activation condition;
- review cadence or review trigger.

If any identity field is unknown, it must be marked `NEEDS_VERIFICATION`.

## 6. Source-of-Truth Requirements

The completed project specification must list the approved source-of-truth inputs that support project requirements.

Eligible source categories may include:

| Source category | Required description |
|---|---|
| Owner decision | Decision, date if known, scope and exclusions |
| Approved protocol or plan | Identifier, version and controlled location |
| Approved repository policy | File or policy name and applicable scope |
| Approved data-governance source | Authority and applicable restriction |
| Approved publication or output plan | Scope, rights status and review authority |
| Approved environment source | Runtime or analysis environment and authority |
| Approved Knowledge document | Filename, status and relevant responsibility |

Unverified sources must not be treated as binding project authority. Conflicting sources must stop the affected project specification decision and be marked `NEEDS_VERIFICATION`.

## 7. Project Scope Fields

The completed project specification must define:

- included work;
- excluded work;
- project deliverables;
- non-goals;
- accepted assumptions;
- unresolved assumptions;
- approved operating mode;
- out-of-scope requests that require a new approval.

Scope must be specific enough to prevent accidental activation of unrelated tasks or repositories.

## 8. Data and Privacy Fields

The completed project specification must identify applicable data and privacy constraints without redefining the canonical safety classifications.

Required fields:

- permitted data categories for the project;
- prohibited data categories for the project;
- permitted input locations;
- prohibited input locations;
- permitted output locations;
- publication or disclosure review requirements;
- secret-handling requirement;
- incident or uncertainty escalation route;
- unresolved data-governance items.

`SAFETY_PRIVACY_GUARDRAILS.md` remains the safety and privacy authority. The project specification may strengthen but must not weaken those guardrails.

## 9. Repository and Artifact Fields

The completed project specification must define repository and artifact boundaries relevant to the project:

- approved repository role;
- approved top-level artifact classes;
- generated-output policy;
- supplementary-material policy;
- manuscript or report publication boundary;
- archive or release boundary;
- files or directories that must remain out of scope;
- review requirement before public exposure.

This template does not prescribe repository architecture patterns. Repository design references belong to the appropriate approved reference document or project-specific source.

## 10. Migration Contract Fields

When the project includes source-to-target migration, the completed project specification must define a project-specific Migration Contract.

The Migration Contract instantiates approved project choices. It must not copy migration pattern logic, privacy classifications, tool policy or evidence PASS/FAIL procedure from other Knowledge documents.

Required fields:

```yaml
migration_contract:
  migration_required: yes | no | NEEDS_VERIFICATION
  source_repository: NEEDS_VERIFICATION
  source_revision: NEEDS_VERIFICATION
  source_paths:
    - NEEDS_VERIFICATION
  target_repository: NEEDS_VERIFICATION
  target_paths:
    - NEEDS_VERIFICATION
  migration_strategy:
    value: NEEDS_VERIFICATION
    pattern_reference: RESEARCH_REPOSITORY_PATTERNS.md
  artifact_selection:
    scope: NEEDS_VERIFICATION
    classification_reference: RESEARCH_REPOSITORY_PATTERNS.md
    accepted_classifications:
      - NEEDS_VERIFICATION
    excluded_classifications:
      - NEEDS_VERIFICATION
  dependency_closure_status: NEEDS_VERIFICATION
  privacy_review_status:
    value: NEEDS_VERIFICATION
    authority_reference: SAFETY_PRIVACY_GUARDRAILS.md
  provenance_strategy: NEEDS_VERIFICATION
  portability_changes_allowed:
    value: NEEDS_VERIFICATION
    boundary_reference: RESEARCH_REPOSITORY_PATTERNS.md
  scientific_changes_allowed:
    value: false
    analytical_change_authorization: required-if-true
  required_validation:
    - NEEDS_VERIFICATION
  expected_reference_results: NEEDS_VERIFICATION
  allowed_paths:
    - NEEDS_VERIFICATION
  forbidden_paths:
    - NEEDS_VERIFICATION
  rollback_strategy: NEEDS_VERIFICATION
  owner_approval_gates:
    - NEEDS_VERIFICATION
```

`migration_strategy.value` records the project-approved strategy. This template does not choose a strategy or define strategy-selection logic. Strategy patterns belong to `RESEARCH_REPOSITORY_PATTERNS.md`.

`privacy_review_status` records the project-specific review state under `SAFETY_PRIVACY_GUARDRAILS.md`. It must not redefine safety classifications or weaken fail-closed privacy handling.

`required_validation` records the project-required validation set under `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`. It must not redefine PASS/FAIL semantics.

Migration permission does not authorize scientific or analytical change. If `scientific_changes_allowed.value` is anything other than `false`, the completed project specification must reference a separate approved analytical-change scope or work package. Analytical changes must not be hidden inside portability changes.

Tool selection, history rewrite, network use, staging, commit, push, release, publication and external exposure remain governed by `TOOL_AND_AGENT_POLICY.md`, applicable safety guardrails and explicit Owner approval gates.

## 11. Analysis and Output Fields

When the project includes analysis work, the completed project specification must define:

- analysis objective at the level appropriate for repository governance;
- approved analysis inputs;
- synthetic, fixture or mock-data policy;
- expected tables, figures, reports or supplementary outputs;
- provenance requirements for generated outputs;
- traceability requirement between analysis code and public outputs;
- limitations that must be reported;
- outputs requiring separate review before acceptance or publication.

The project specification must not alter manuscript conclusions or statistical interpretation unless the user explicitly authorizes that scope.

## 12. Tool, Agent and Environment Fields

The completed project specification must define project-specific tool, agent and environment constraints only where stricter or more specific than the general policy.

Required fields:

- approved runtime environment or environment class;
- required local or CI validation tools;
- unavailable tools and impact;
- agent access boundaries;
- network-use restrictions;
- package-management restrictions;
- Git, commit, push or release restrictions;
- tool or environment items marked `NEEDS_VERIFICATION`.

`TOOL_AND_AGENT_POLICY.md` remains the tool and agent authority. The project specification may not infer permission from tool availability.

## 13. Evidence and Acceptance Fields

The completed project specification must define project-specific evidence and acceptance requirements:

- minimum evidence required for project changes;
- required review categories;
- required validation categories;
- acceptance authority;
- acceptable PASS / FAIL decision scope;
- defect handling expectations;
- treatment of unavailable validation tools;
- lifecycle approval requirement;
- commit, push, release and publication approval gates.

`EVIDENCE_REVIEW_AND_ACCEPTANCE.md` remains the evidence and acceptance authority. Project-specific criteria may strengthen but must not weaken it.

## 14. Activation and Deactivation Fields

The completed project specification must define:

- activation prerequisite;
- who or what may activate Project Mode;
- freshness requirement;
- conditions that block activation;
- conditions that suspend active use;
- deactivation or retirement criteria;
- required action when activation state is uncertain.

Activation uncertainty must stop Project Mode use for the affected scope and be marked `NEEDS_VERIFICATION`.

## 15. Project Specification Skeleton

The following skeleton may be copied when drafting a completed project specification:

```markdown
# Project Specification

## 1. Document Metadata

## 2. Project Identity

## 3. Source-of-Truth Inputs

## 4. Scope and Non-Goals

## 5. Data, Privacy and Disclosure Constraints

## 6. Repository and Artifact Boundaries

## 7. Migration Contract

## 8. Analysis and Output Requirements

## 9. Tool, Agent and Environment Constraints

## 10. Evidence, Review and Acceptance Requirements

## 11. Activation, Suspension and Retirement

## 12. Open `NEEDS_VERIFICATION` Items

## 13. Dependencies and References
```

The skeleton is structure only. It is not approved project content until completed, reviewed and accepted.

## 16. Exclusions

This template must not contain:

- active project requirements;
- participant-level data or protected research information;
- secrets or credentials;
- project or session state;
- local absolute paths;
- temporary branch, commit or device state;
- manuscript conclusions or statistical interpretation;
- duplicated safety classification tables;
- duplicated tool or command policy;
- duplicated evidence acceptance procedure;
- repository architecture pattern guidance;
- project-specific migration source, revision, path or strategy values;
- Knowledge lifecycle governance.

## 17. Review and Validation Rules

Before approving a completed project specification, review must verify:

- all required fields are present or explicitly marked `NEEDS_VERIFICATION`;
- every binding project requirement is source-grounded;
- no placeholder value is silently accepted;
- safety and privacy constraints are compatible with `SAFETY_PRIVACY_GUARDRAILS.md`;
- tool and agent constraints are compatible with `TOOL_AND_AGENT_POLICY.md`;
- evidence and acceptance constraints are compatible with `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`;
- migration contract fields are present when source-to-target migration is in scope;
- migration contract choices are compatible with `RESEARCH_REPOSITORY_PATTERNS.md`;
- migration permission does not silently authorize scientific or analytical changes;
- activation rules are explicit;
- unresolved items are classified and bounded;
- no project or session state is present in this template document.

Validation must be appropriate to the completed specification and must include structural, metadata, dependency and contradiction review.

## 18. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  registers -> PROJECT_SPECIFICATION_TEMPLATE.md
  routes-to -> PROJECT_SPECIFICATION_TEMPLATE.md for project specification structure questions

PROJECT_SPECIFICATION_TEMPLATE.md
  structures -> PROJECT_SPECIFICATION.md

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> completed project specifications

TOOL_AND_AGENT_POLICY.md
  constrains -> completed project specifications for tool, command, network, Git and agent boundaries

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> completed project specifications for evidence, review and acceptance requirements

RESEARCH_REPOSITORY_PATTERNS.md
  informs -> completed project specifications for repository architecture and migration-pattern choices
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the evidence review and acceptance authority.
- `RESEARCH_REPOSITORY_PATTERNS.md` owns repository architecture and migration-pattern guidance.

The future `PROJECT_SPECIFICATION.md` is a project instance document, not part of this permanent Knowledge inventory unless separately approved.

## 19. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P0`.
- [ ] Status `approved`.
- [ ] Evidence state `validated`.
- [ ] Load condition `template-only`.
- [ ] Authority level `template`.
- [ ] Template-only status is explicit.
- [ ] Required project metadata fields are defined.
- [ ] Required source-of-truth fields are defined.
- [ ] Required scope fields are defined.
- [ ] Required data and privacy fields are defined without duplicating safety classifications.
- [ ] Required repository and artifact fields are defined without prescribing architecture patterns.
- [ ] Required migration contract fields are defined without duplicating migration patterns.
- [ ] Migration strategy is a project-specific value with a repository-pattern reference.
- [ ] Migration privacy review status references Guardrails without redefining privacy classifications.
- [ ] Migration validation references Evidence Policy without redefining PASS/FAIL semantics.
- [ ] Migration contract does not authorize scientific or analytical changes by default.
- [ ] Required analysis and output fields are defined without adding project-specific conclusions.
- [ ] Required tool, agent and environment fields are defined without duplicating tool policy.
- [ ] Required evidence and acceptance fields are defined without duplicating acceptance procedure.
- [ ] Activation and deactivation fields are explicit.
- [ ] No active project content.
- [ ] No A1 or FOF project values.
- [ ] No project-specific repository URLs, commit SHAs, paths or selected migration strategy.
- [ ] No project or session state.
- [ ] No local absolute paths.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent organizational steward mapping;
- permanent review-authority mapping;
- permanent project specification storage location;
- permanent Project Mode activation authority;
- permanent project-source approval requirements;
- full P0 activation prerequisites.
