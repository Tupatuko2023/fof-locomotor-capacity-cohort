# FARO1 Decision Log Template

## 1. Document Metadata

```yaml
title: FARO1 Decision Log Template
document_id: FARO1-DECISION-LOG-TEMPLATE
version: 0.1.0
status: approved
priority: P2
scope: Template structure and required fields for later FARO1 decision records
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define the structure of later decision records.
load_condition: template-only
authority_level: template
activation_rule: Load only when drafting, reviewing or validating decision-record structure. This template is not an active decision record.
```

## 2. Primary Responsibility

This document defines the template structure and required fields for later FARO1 decision records.

It does not approve decisions, define active project requirements, create project state, define Knowledge lifecycle governance, set evidence PASS/FAIL rules, authorize tools or Git actions, define safety classifications, prescribe repository architecture or modify manuscript conclusions or statistical interpretation.

## 3. Template Use

Use this template when a FARO1 work package, project specification, Knowledge change, approval gate or unresolved governance question needs a structured decision record.

A completed decision record must be source-grounded, reviewed and accepted under the applicable authority before it can be treated as evidence of a decision. This template cannot be activated as a decision instance and cannot substitute for Owner approval.

Placeholder values must be replaced, removed or marked `NEEDS_VERIFICATION` before a completed decision record is accepted.

## 4. Decision Record vs Other Documents

A decision record answers:

```text
What decision was made, by whom, under what evidence, scope, constraints and follow-up requirements?
```

It must not replace:

- `KB_INDEX.md` for Knowledge registry, routing or dependency truth;
- `KNOWLEDGE_GOVERNANCE.md` for lifecycle, versioning, compatibility, retirement or registry-alignment rules;
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` for evidence review, acceptance gates or PASS/FAIL semantics;
- `SAFETY_PRIVACY_GUARDRAILS.md` for safety, privacy, protected-data or publication guardrails;
- `TOOL_AND_AGENT_POLICY.md` for command, tool, agent, network, Git or publication authorization rules;
- `PROJECT_CONTEXT_TEMPLATE.md` for project context structure;
- `PROJECT_SPECIFICATION_TEMPLATE.md` for project requirements structure;
- `RESEARCH_REPOSITORY_PATTERNS.md` for repository architecture or migration-pattern guidance.

## 5. Required Metadata Fields

A completed decision record must begin with canonical metadata:

```yaml
decision_id: NEEDS_VERIFICATION
title: NEEDS_VERIFICATION
version: 0.1.0
status: draft
decision_class: NEEDS_VERIFICATION
decision_date: NEEDS_VERIFICATION
decision_authority: NEEDS_VERIFICATION
steward: NEEDS_VERIFICATION
scope: NEEDS_VERIFICATION
document_evidence_state: source-grounded
related_work_package: NEEDS_VERIFICATION
related_project_or_kb_document: NEEDS_VERIFICATION
supersedes: []
superseded_by: null
review_date_or_cadence: NEEDS_VERIFICATION
```

Allowed `status` values for completed decision records are:

- `draft`;
- `reviewed`;
- `accepted`;
- `deferred`;
- `superseded`;
- `retired`.

Allowed `decision_class` values are:

- `owner-approval`;
- `technical-review`;
- `validation-result`;
- `lifecycle-transition`;
- `scope-decision`;
- `deferral`;
- `rejection`;
- `NEEDS_VERIFICATION`.

## 6. Required Decision Fields

A completed decision record must define:

- decision summary;
- decision authority and basis for authority;
- decision scope;
- explicit exclusions;
- affected files, documents, artifacts or work packages;
- source-of-truth inputs reviewed;
- evidence reviewed;
- constraints that controlled the decision;
- defects, unresolved items or accepted limitations;
- required follow-up actions;
- expiration, review trigger or retirement condition;
- downstream actions that remain separately gated.

If any required value is unknown or outside the available authority, it must be marked `NEEDS_VERIFICATION`.

## 7. Owner Approval and Gate Fields

When a decision record documents Owner approval, lifecycle acceptance, activation, staging, commit, push, pull request, release, publication or another approval gate, it must state:

```yaml
approval_gate:
  gate_type: NEEDS_VERIFICATION
  decision: accepted | rejected | deferred | NEEDS_VERIFICATION
  authority: NEEDS_VERIFICATION
  approved_scope:
    - NEEDS_VERIFICATION
  explicit_exclusions:
    - NEEDS_VERIFICATION
  conditions:
    - NEEDS_VERIFICATION
  not_authorized:
    - staging
    - commit
    - push
    - pull_request
    - release
    - publication
```

A decision record must not imply authorization for any gate that is not explicitly included in its approved scope.

## 8. Evidence Fields

A completed decision record must list evidence without duplicating the evidence policy:

```yaml
evidence:
  reviewed_files: []
  reviewed_diffs_or_manifests: []
  validation_commands: []
  review_checklists: []
  owner_or_authority_inputs: []
  limitations:
    - NEEDS_VERIFICATION
  evidence_state: source-grounded | reviewed | validated | NEEDS_VERIFICATION
```

Evidence references must be inspectable at the level required by `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`. Agent assertions, summaries or ungrounded claims must not be recorded as accepted evidence by themselves.

## 9. Safety and Privacy Fields

When the decision could affect data, privacy, protected research information, secrets, public Git content, release, publication, external services or disclosure risk, the completed decision record must include:

```yaml
safety_privacy_review:
  authority_reference: SAFETY_PRIVACY_GUARDRAILS.md
  candidate_scope_reviewed: NEEDS_VERIFICATION
  restricted_data_or_secret_risk: NEEDS_VERIFICATION
  public_exposure_risk: NEEDS_VERIFICATION
  unresolved_safety_items:
    - NEEDS_VERIFICATION
```

The decision record must not contain participant-level data, row-level examples, secrets, credentials, sensitive filesystem layouts or protected data values.

## 10. Tool and Git Fields

When the decision could affect commands, automation, agents, network use, staging, commit, push, pull request, release or publication, the completed decision record must include:

```yaml
tool_git_review:
  authority_reference: TOOL_AND_AGENT_POLICY.md
  tool_scope_reviewed: NEEDS_VERIFICATION
  git_or_external_action_requested: yes | no | NEEDS_VERIFICATION
  git_or_external_action_authorized: yes | no | NEEDS_VERIFICATION
  separate_gates_remaining:
    - NEEDS_VERIFICATION
```

Tool availability must not be recorded as permission. Git and external publication actions require explicit scope-specific authorization.

## 11. Decision Record Skeleton

The following skeleton may be copied when drafting a completed decision record:

```markdown
# Decision Record

## 1. Metadata

## 2. Decision Summary

## 3. Authority and Scope

## 4. Source-of-Truth Inputs

## 5. Evidence Reviewed

## 6. Constraints Applied

## 7. Decision

## 8. Explicit Exclusions

## 9. Defects, Limitations and `NEEDS_VERIFICATION` Items

## 10. Follow-Up Actions and Remaining Gates

## 11. Dependencies and References
```

The skeleton is structure only. It is not an accepted decision until completed, reviewed and accepted by the applicable authority.

## 12. Explicit Exclusions

This template must not contain:

- active project decisions;
- project requirements or project state;
- session state;
- local absolute paths;
- participant-level data or protected research information;
- secrets or credentials;
- duplicated safety classification tables;
- duplicated tool or command policy;
- duplicated evidence PASS/FAIL procedure;
- Knowledge lifecycle rules beyond the fields needed to record a lifecycle decision;
- repository architecture patterns;
- migration strategy rules;
- manuscript conclusions or statistical interpretation;
- Change History section.

## 13. Review Requirements

Before accepting a completed decision record, review must verify:

- every required field is present or explicitly marked `NEEDS_VERIFICATION`;
- decision authority is identified and sufficient for the stated scope;
- evidence references are source-grounded and inspectable;
- explicit exclusions prevent accidental authorization of broader gates;
- safety and privacy constraints are compatible with `SAFETY_PRIVACY_GUARDRAILS.md`;
- tool and Git constraints are compatible with `TOOL_AND_AGENT_POLICY.md`;
- evidence treatment is compatible with `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`;
- Knowledge lifecycle decisions are compatible with `KNOWLEDGE_GOVERNANCE.md`;
- registry or routing claims, if any, are compatible with `KB_INDEX.md`;
- no project or session state is embedded in this template document;
- no secrets, participant data or local absolute paths are present.

## 14. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  registers -> DECISION_LOG_TEMPLATE.md
  routes-to -> DECISION_LOG_TEMPLATE.md for decision-record structure questions

DECISION_LOG_TEMPLATE.md
  structures -> later completed decision records

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> completed decision records that affect data, privacy, protected data, secrets, public exposure, release or publication

TOOL_AND_AGENT_POLICY.md
  constrains -> completed decision records that affect tools, commands, agents, network use, Git or external actions

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> completed decision records for evidence, review, validation, acceptance and Owner approval gates

KNOWLEDGE_GOVERNANCE.md
  constrains -> completed decision records for Knowledge lifecycle, registry alignment, deprecation, retirement, supersession and migration decisions
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the evidence review and acceptance authority.
- `KNOWLEDGE_GOVERNANCE.md` is the Knowledge lifecycle and maintenance authority.

Completed decision records are project, governance or work-package evidence artifacts. They are not automatically part of the permanent Knowledge inventory.

## 15. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P2`.
- [ ] Status `approved` after Owner approval.
- [ ] Evidence state `validated` after structural validation passes.
- [ ] Load condition `template-only`.
- [ ] Authority level `template`.
- [ ] Template-only status is explicit.
- [ ] Required decision metadata fields are defined.
- [ ] Decision class values are defined.
- [ ] Required decision fields are defined.
- [ ] Owner approval and gate fields are defined without authorizing omitted gates.
- [ ] Evidence fields reference evidence policy without duplicating PASS/FAIL semantics.
- [ ] Safety and privacy fields reference guardrails without duplicating classifications.
- [ ] Tool and Git fields reference tool policy without duplicating command policy.
- [ ] Completed decision records are distinct from this template.
- [ ] No active project values.
- [ ] No FOF/A1 project values.
- [ ] No local absolute paths.
- [ ] No session state.
- [ ] No secrets or participant data.
- [ ] No duplicated neighboring Knowledge responsibility.
- [ ] No circular normative dependency.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent decision-record storage location;
- permanent decision-record approval authority;
- permanent decision-record retention and retirement requirements;
- relationship between decision records and future active project specifications;
- full P2 activation prerequisites.
