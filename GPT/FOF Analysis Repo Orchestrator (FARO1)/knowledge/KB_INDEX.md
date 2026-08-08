# FARO1 Knowledge Base Index

## 1. Document Metadata

```yaml
title: FARO1 Knowledge Base Index
document_id: FARO1-KB-INDEX
version: 0.1.0
status: approved
priority: P0
scope: Canonical manifest for the approved FARO1 Knowledge Base
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
```

Controlled values:

- `status`: `proposed`, `draft`, `reviewed`, `approved`, `active`, `superseded`, `retired`
- `priority`: `P0`, `P1`, `P2`
- `document_evidence_state`: `unverified`, `source-grounded`, `reviewed`, `validated`
- `claim_classification`: `verified-fact`, `source-derived-requirement`, `recommendation`, `architectural-inference`, `NEEDS_VERIFICATION`

The permanent organizational mapping for `steward` and `review_authority` is `NEEDS_VERIFICATION`.

## 2. Primary Responsibility

This document is the canonical FARO1 Knowledge Base manifest. It registers the approved Knowledge files and controls their routing, loading, dependencies and lifecycle metadata.

It is not a general policy, safety guardrail, project specification, session record or replacement for permanent FARO1 Instructions.

## 3. Scope and Exclusions

This manifest contains only Knowledge Base metadata and routing information. It must not contain:

- project-specific state;
- session state, transcripts or temporary work-package state;
- secrets, credentials or device details;
- participant data or protected research information;
- temporary branch names, commit identifiers or local paths;
- duplicated normative policy text;
- unapproved Knowledge files.

`PROJECT_SPECIFICATION.md` is a later Project Mode runtime document. It is not part of the permanent P0/P1/P2 Knowledge inventory and is not created here.

## 4. Global Precedence

Normative precedence is separate from loading order:

1. Permanent FARO1 Instructions and runtime constraints.
2. Applicable binding safety and policy requirements.
3. Approved project-specific requirements that do not conflict with levels 1-2.
4. Reference material, templates and recommendations.
5. Session evidence for factual state, subject to verification.

No Knowledge document, project instance, template, reference document or session evidence may override permanent Instructions or an applicable binding guardrail or policy.

## 5. Project Mode KB Loading Sequence

When entering Project Mode:

1. Load `KB_INDEX.md` first as the Knowledge Base entry source.
2. Verify that each registered file actually exists and is eligible for use.
3. Route the question to the file with the narrowest approved primary responsibility.
4. Load only required dependencies.
5. Stop on conflict, absence, stale status or unverifiable activation.

The manifest does not imply that a registered file exists. Existence and eligibility must be verified independently.

## 6. Knowledge File Registry

Registry field definitions:

| Field | Definition | Allowed values | Mandatory |
|---|---|---|---|
| `filename` | Exact approved filename | Controlled filename | Yes |
| `priority` | Inventory priority | `P0`, `P1`, `P2` | Yes |
| `role` | Functional document role | `manifest`, `policy`, `guardrail`, `evidence-governance`, `template`, `reference` | Yes |
| `primary_responsibility` | One responsibility of the document | Non-empty string | Yes |
| `load_condition` | Runtime loading condition | `always-kb-entry`, `always-safety`, `task-conditional`, `project-mode`, `template-only`, `project-instance-only` | Yes |
| `activation_rule` | Requirement for use | Non-empty string | Yes |
| `dependencies` | Required typed references | Approved filenames or permanent Instructions | Yes |
| `authority_level` | Normative role | `manifest`, `binding-policy`, `guardrail`, `template`, `reference` | Yes |
| `lifecycle_status` | Lifecycle state | Registry lifecycle values below | Yes |
| `document_evidence_state` | Validation state of the whole document | `unverified`, `source-grounded`, `reviewed`, `validated` | Yes |
| `steward` | Maintaining role | `FARO1 Knowledge Steward` | Yes |
| `review_authority` | Acceptance role | `User / designated project owner` | Yes |

All registry entries initially use `lifecycle_status: proposed` and `document_evidence_state: unverified`, except this manifest's metadata above.

| Filename | Priority | Role | Primary responsibility | Load condition | Activation rule | Dependencies | Authority | Lifecycle status | Document evidence state | Steward | Review authority |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| `KB_INDEX.md` | P0 | manifest | Register Knowledge files and control routing, loading, dependencies and lifecycle metadata | `always-kb-entry` | Load on Project Mode entry and verify manifest eligibility | Permanent FARO1 Instructions | `manifest` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `TOOL_AND_AGENT_POLICY.md` | P0 | policy | Define approved tool and agent boundaries | `task-conditional` | Load for a tool or agent decision | Permanent FARO1 Instructions | `binding-policy` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `SAFETY_PRIVACY_GUARDRAILS.md` | P0 | guardrail | Define safety, privacy and data restrictions | `always-safety` | Applicable to all Knowledge and project operations | Permanent FARO1 Instructions | `guardrail` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` | P0 | evidence-governance | Define evidence review and acceptance requirements | `task-conditional` | Load for evidence or acceptance decisions | Permanent FARO1 Instructions, `SAFETY_PRIVACY_GUARDRAILS.md` | `binding-policy` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `PROJECT_SPECIFICATION_TEMPLATE.md` | P0 | template | Define the structure and fields of a later project specification | `template-only` | Load only when drafting a project specification | `KB_INDEX.md` | `template` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `KNOWLEDGE_GOVERNANCE.md` | P1 | policy | Define Knowledge maintenance and lifecycle governance | `task-conditional` | Load for Knowledge maintenance or lifecycle decisions | `KB_INDEX.md`, `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`, `SAFETY_PRIVACY_GUARDRAILS.md`, `TOOL_AND_AGENT_POLICY.md` | `binding-policy` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `PROJECT_CONTEXT_TEMPLATE.md` | P1 | template | Define its own project-context template structure | `template-only` | Load only when its template structure is needed | `KB_INDEX.md`, `PROJECT_SPECIFICATION_TEMPLATE.md`, `SAFETY_PRIVACY_GUARDRAILS.md`, `TOOL_AND_AGENT_POLICY.md`, `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` | `template` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `RESEARCH_REPOSITORY_PATTERNS.md` | P1 | reference | Provide repository architecture patterns | `task-conditional` | Load for repository design questions | `KB_INDEX.md`, `PROJECT_CONTEXT_TEMPLATE.md`, `PROJECT_SPECIFICATION_TEMPLATE.md`, `SAFETY_PRIVACY_GUARDRAILS.md`, `TOOL_AND_AGENT_POLICY.md`, `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` | `reference` | `approved` | `validated` | `FARO1 Knowledge Steward` | `User / designated project owner` |
| `DECISION_LOG_TEMPLATE.md` | P2 | template | Define the structure of later decision records | `template-only` | Load only when a decision record is drafted | `KB_INDEX.md` | `template` | `proposed` | `unverified` | `FARO1 Knowledge Steward` | `User / designated project owner` |

## 7. Routing Policy

| Question category | Primary route | Load condition |
|---|---|---|
| Knowledge inventory, routing or dependencies | `KB_INDEX.md` | `always-kb-entry` |
| Safety, privacy or data handling | `SAFETY_PRIVACY_GUARDRAILS.md` | `always-safety` |
| Tool or agent permissions | `TOOL_AND_AGENT_POLICY.md` | `task-conditional` |
| Evidence review or acceptance | `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` | `task-conditional` |
| Knowledge maintenance or lifecycle | `KNOWLEDGE_GOVERNANCE.md` | `task-conditional` |
| Active project requirements | Verified `PROJECT_SPECIFICATION.md` | `project-mode` |
| Project specification structure | `PROJECT_SPECIFICATION_TEMPLATE.md` | `template-only` |
| Project context structure | `PROJECT_CONTEXT_TEMPLATE.md` | `template-only` |
| Repository architecture patterns | `RESEARCH_REPOSITORY_PATTERNS.md` | `task-conditional` |
| Decision-record structure | `DECISION_LOG_TEMPLATE.md` | `template-only` |

Overlapping questions route to the document with the narrowest explicit primary responsibility. Conflicting normative claims stop routing and invoke conflict handling.

## 8. Load Policy

- `always-kb-entry`: `KB_INDEX.md` is loaded first when entering Project Mode.
- `always-safety`: safety guardrails are always applicable.
- `task-conditional`: load only when the question requires the document.
- `project-mode`: load only for a verified active Project Mode instance.
- `template-only`: load for template structure, never as active project content.
- `project-instance-only`: load only for a verified project instance.

Files are not loaded merely because they are listed in this manifest. The file must exist, be eligible, and satisfy its activation rule.

## 9. Activation Rules

In Generic Mode, `KB_INDEX.md` does not activate project-specific state and `PROJECT_SPECIFICATION.md` is not loaded.

In Project Mode, `KB_INDEX.md` is loaded first. `PROJECT_SPECIFICATION.md` may be loaded only after its existence, approval, applicability and freshness have been verified. Its storage location is `NEEDS_VERIFICATION`.

Templates define structure only. They cannot be activated as project instances. Missing, stale, conflicting or unverifiable required sources block activation.

## 10. Lifecycle and Evidence

Lifecycle transitions:

```text
proposed -> draft -> reviewed -> approved -> active
active -> superseded
active -> retired
```

- `proposed`: planned but not drafted.
- `draft`: drafted but not accepted.
- `reviewed`: review completed, acceptance pending.
- `approved`: required acceptance decision recorded.
- `active`: approved and eligible for runtime loading under its rules.
- `superseded`: replaced by an approved successor.
- `retired`: no longer eligible for use.

The temporary roles are `FARO1 Knowledge Steward` and `User / designated project owner`. Permanent organizational role mapping is `NEEDS_VERIFICATION`.

Document validation state and claim classification are separate. A document uses `document_evidence_state`; individual claims may use `claim_classification`.

## 11. Maintenance Triggers

Review the manifest when any of the following occurs:

- FARO1 architecture changes.
- A policy, tool policy or safety requirement changes.
- Privacy requirements change.
- An evaluation fails.
- Routing is repeatedly ambiguous.
- An approved file is added, removed, renamed or replaced.

Knowledge-wide change governance belongs to `KNOWLEDGE_GOVERNANCE.md`, not to a Change History section in this manifest.

## 12. Conflict Handling

When sources conflict:

1. Stop the affected work.
2. Identify the conflicting sources and claims.
3. Do not silently reconcile them.
4. Mark the unresolved matter `NEEDS_VERIFICATION`.
5. Request a user decision when required.

Permanent Instructions and applicable binding guardrails remain controlling during the stop.

## 13. Dependency Graph

Typed relationships:

```text
Permanent FARO1 Instructions
  constrains -> KB_INDEX.md
  constrains -> TOOL_AND_AGENT_POLICY.md
  constrains -> SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md

KB_INDEX.md
  registers -> TOOL_AND_AGENT_POLICY.md
  registers -> SAFETY_PRIVACY_GUARDRAILS.md
  registers -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  registers -> PROJECT_SPECIFICATION_TEMPLATE.md
  registers -> KNOWLEDGE_GOVERNANCE.md
  registers -> PROJECT_CONTEXT_TEMPLATE.md
  registers -> RESEARCH_REPOSITORY_PATTERNS.md
  registers -> DECISION_LOG_TEMPLATE.md
  routes-to -> each registered file by primary responsibility
  conditionally-loads -> PROJECT_SPECIFICATION.md

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> acceptance decisions

PROJECT_SPECIFICATION.md
  derived-from -> PROJECT_SPECIFICATION_TEMPLATE.md

TOOL_AND_AGENT_POLICY.md
  conditionally-loads -> tool- or agent-specific execution context
```

`PROJECT_SPECIFICATION.md` is a later named runtime document, not a permanent inventory entry. Its storage location is `NEEDS_VERIFICATION`. No unnamed future instance document is introduced. The graph contains no circular normative dependency.

## 14. Reference and Validation Rules

Every approved Knowledge file must reference `KB_INDEX.md`. `KB_INDEX.md` must list every approved P0/P1/P2 file. References outside the approved architecture must be marked as external project inputs.

Validation checklist:

- [ ] Exactly one primary responsibility is stated.
- [ ] Metadata fields and controlled values are complete.
- [ ] All nine approved P0/P1/P2 files are registered.
- [ ] Global precedence is separate from loading and routing.
- [ ] `KB_INDEX.md` is the first Project Mode KB source.
- [ ] Routing uses the narrowest approved responsibility.
- [ ] Load and activation rules are distinct.
- [ ] Templates are not active project content.
- [ ] `approved` and `active` remain distinct.
- [ ] Dependency relationships are typed.
- [ ] No circular normative dependency exists.
- [ ] No project or session state is included.
- [ ] No secrets, participant data or protected information is included.
- [ ] Conflicts stop affected work and require `NEEDS_VERIFICATION`.
- [ ] Every approved file references `KB_INDEX.md`.
