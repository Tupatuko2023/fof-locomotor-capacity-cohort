# FARO1 Knowledge Governance

## 1. Document Metadata

```yaml
title: FARO1 Knowledge Governance
document_id: FARO1-KNOWLEDGE-GOVERNANCE
version: 0.1.0
status: approved
priority: P1
scope: Knowledge maintenance, versioning, lifecycle, compatibility, deprecation and migration governance for the FARO1 Knowledge Base
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define Knowledge maintenance and lifecycle governance.
load_condition: task-conditional
authority_level: binding-policy
activation_rule: Load for Knowledge maintenance, versioning, lifecycle transition, compatibility, deprecation, retirement, replacement, migration or registry-alignment decisions.
```

## 2. Primary Responsibility

This document defines Knowledge maintenance and lifecycle governance for the FARO1 Knowledge Base.

It does not define the canonical registry, routing or dependency manifest; those belong to `KB_INDEX.md`. It does not define evidence acceptance gates; those belong to `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`. It does not define safety classifications, tool policy, project specification structure, repository architecture patterns, project context structure or decision-log structure.

## 3. Scope

This policy applies when FARO1 work creates, reviews, updates, supersedes, retires, renames, migrates or revalidates Knowledge documents.

It covers:

- Knowledge document ownership and stewardship;
- versioning policy;
- lifecycle transitions;
- compatibility expectations;
- change classification;
- maintenance triggers;
- deprecation, supersession and retirement;
- migration and registry alignment;
- periodic review expectations;
- governance evidence requirements.

Project-specific runtime state is outside this document.

## 4. Precedence

Knowledge governance decisions follow this precedence:

1. Permanent FARO1 Instructions and runtime constraints.
2. `KB_INDEX.md` for registry, routing and manifest truth.
3. `SAFETY_PRIVACY_GUARDRAILS.md` for safety and privacy constraints.
4. `TOOL_AND_AGENT_POLICY.md` for tool and agent execution boundaries.
5. `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` for evidence and acceptance gates.
6. This Knowledge governance policy.
7. Approved project-specific requirements that do not conflict with levels 1-6.

When governance sources conflict, stop the affected change and mark the unresolved point `NEEDS_VERIFICATION`.

## 5. Governance Principles

- `KB_INDEX.md` is the only canonical Knowledge file registry.
- Knowledge changes must preserve one primary responsibility per document.
- Governance changes must be source-grounded and reviewable.
- Lifecycle status and document evidence state remain distinct.
- Approval does not imply activation unless activation is separately authorized.
- Templates remain templates and must not become project instances.
- Proposed or absent documents must not be represented as active Knowledge.
- Compatibility risks must be made explicit before approval.
- Deprecation and retirement must not silently remove needed routing or safety coverage.
- Project or session state must not be added to permanent Knowledge documents.

## 6. Governance Roles

Temporary governance roles are:

| Role | Responsibility |
|---|---|
| `FARO1 Knowledge Steward` | Maintains Knowledge structure, proposes changes and preserves governance consistency |
| `User / designated project owner` | Provides required approval decisions and acceptance authority |

Permanent organizational mappings for governance roles are `NEEDS_VERIFICATION`.

A steward may prepare a change, review evidence and recommend a lifecycle transition. The review authority must approve changes that alter lifecycle status, authority, routing, dependencies, deprecation, retirement or activation eligibility.

## 7. Knowledge Inventory Control

The approved Knowledge inventory is controlled by `KB_INDEX.md`.

Adding a Knowledge document requires:

- registry entry in `KB_INDEX.md`;
- stated primary responsibility;
- priority, role, load condition, activation rule and authority level;
- dependencies and typed relationship;
- lifecycle status;
- document evidence state;
- steward and review authority;
- conflict and overlap review.

Removing, renaming or replacing a Knowledge document requires an explicit governance work package and registry alignment. A file must not be treated as approved merely because it exists in the Knowledge directory.

## 8. Versioning Policy

Knowledge documents use semantic versioning at the document level:

- major version: incompatible change to responsibility, authority, activation, lifecycle meaning or normative behavior;
- minor version: compatible addition of policy, structure, requirement or template field;
- patch version: wording clarification, typo correction or non-normative cleanup that preserves behavior.

Version increments must match the actual change. If compatibility impact is uncertain, mark the change `NEEDS_VERIFICATION` and do not approve the version update until resolved.

Version number changes do not replace lifecycle review or Owner approval.

## 9. Change Classification

Knowledge changes must be classified before approval:

| Change class | Description | Minimum governance response |
|---|---|---|
| `editorial` | Non-normative wording or formatting change | Diff review and evidence note |
| `clarification` | Makes an existing rule more explicit without changing behavior | Scope and compatibility review |
| `compatible-extension` | Adds requirements or fields without weakening existing behavior | Dependency, routing and overlap review |
| `behavior-changing` | Changes authority, required behavior, activation, acceptance or obligations | Full review and Owner approval |
| `breaking` | Invalidates existing consumers, project assumptions or approved workflows | Migration plan and Owner approval |
| `deprecation` | Marks a document, field or rule for replacement or removal | Successor or mitigation plan |
| `retirement` | Removes eligibility for future use | Registry alignment and residual-risk review |

Unknown classification blocks acceptance until resolved or explicitly deferred by the review authority.

## 10. Lifecycle Governance

Lifecycle transitions follow the values registered in `KB_INDEX.md`:

```text
proposed -> draft -> reviewed -> approved -> active
active -> superseded
active -> retired
```

Governance requirements:

- `proposed` requires registry planning only.
- `draft` requires file creation or substantive draft content.
- `reviewed` requires completed review evidence.
- `approved` requires recorded Owner or review-authority acceptance.
- `active` requires approval plus activation eligibility under the document's activation rule.
- `superseded` requires an approved successor or explicit replacement decision.
- `retired` requires a retirement decision and residual-risk review.

Lifecycle transitions must be reflected consistently in document metadata and, when applicable, the `KB_INDEX.md` registry.

## 11. Evidence State Governance

Document evidence states remain separate from lifecycle status:

- `unverified`: not yet reviewed against requirements.
- `source-grounded`: supported by inspected sources, draft evidence or implementation evidence.
- `reviewed`: reviewed and defect state known.
- `validated`: review and validation gates passed for the stated scope.

Evidence state must not be upgraded without evidence reviewed under `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

`validated` does not imply `active`. `approved` does not imply `validated` unless the required validation gate has also passed.

## 12. Compatibility and Migration

Before approving a behavior-changing or breaking Knowledge change, review must identify:

- affected Knowledge documents;
- affected routing decisions;
- affected project specifications or project instances;
- affected prompts, tools or agent workflows;
- migration requirement;
- compatibility risk;
- rollback or recovery option;
- required Owner decision.

Migration instructions must avoid project or session state unless they are stored in an approved project-specific document.

## 13. Deprecation, Supersession and Retirement

Deprecation announces planned replacement or removal while preserving current eligibility unless otherwise stated.

Supersession means an approved successor replaces the document or rule for future use. Supersession requires:

- successor identity;
- reason for replacement;
- compatibility assessment;
- migration requirement;
- registry update;
- review authority approval.

Retirement means the document or rule is no longer eligible for use. Retirement requires:

- reason for retirement;
- affected routing or dependency review;
- residual-risk statement;
- registry update;
- review authority approval.

Deprecated, superseded or retired content must not be silently used as active authority.

## 14. Maintenance Triggers

Knowledge review is required when:

- `KB_INDEX.md` changes;
- Permanent FARO1 Instructions change;
- a safety, tool, evidence or project-specification rule changes;
- a routing ambiguity recurs;
- a conflict is identified between Knowledge documents;
- an activation rule fails;
- a project specification cannot be validated against Knowledge requirements;
- a document becomes stale, incomplete or misleading;
- a proposed P1/P2 document is drafted or accepted;
- publication, release or external exposure requirements change.

Maintenance trigger review must be scoped to the affected documents unless a broader dependency review is required.

## 15. Registry Alignment

Registry alignment is required after a Knowledge document lifecycle or evidence state changes.

Registry alignment must verify:

- filename unchanged or intentionally changed;
- priority unchanged or intentionally changed;
- primary responsibility matches the approved document;
- load condition and activation rule match approved use;
- dependencies match approved typed relationships;
- authority level is correct;
- lifecycle status matches document status where applicable;
- document evidence state matches document metadata;
- steward and review authority remain correct or are marked `NEEDS_VERIFICATION`.

Only the affected registry entry should change unless a broader registry work package is approved.

## 16. Governance Work Package Requirements

Knowledge governance work packages must state:

- work package name;
- target document or registry entry;
- allowed files;
- allowed changes;
- forbidden changes;
- expected evidence;
- validation commands or review method;
- Owner approval requirement;
- stop condition.

For high-risk changes, the work package must include compatibility, migration and rollback considerations.

## 17. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  registers -> KNOWLEDGE_GOVERNANCE.md
  routes-to -> KNOWLEDGE_GOVERNANCE.md for Knowledge maintenance or lifecycle decisions

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> Knowledge governance evidence, review and acceptance decisions

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> Knowledge governance changes that affect privacy, protected data, secrets, public exposure or publication

TOOL_AND_AGENT_POLICY.md
  constrains -> tools, commands, agents and Git actions used for Knowledge governance

KNOWLEDGE_GOVERNANCE.md
  constrains -> Knowledge maintenance, lifecycle, versioning, compatibility, deprecation, retirement and migration decisions
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the evidence review and acceptance authority.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.

Proposed or absent files must not be represented as active runtime Knowledge sources.

## 18. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P1`.
- [ ] Status `approved`.
- [ ] Evidence state `validated`.
- [ ] Load condition `task-conditional`.
- [ ] Authority level `binding-policy`.
- [ ] Knowledge maintenance and lifecycle governance are defined.
- [ ] `KB_INDEX.md` remains the canonical registry owner.
- [ ] Versioning policy is explicit.
- [ ] Change classification is explicit.
- [ ] Lifecycle transition rules are explicit.
- [ ] Evidence state governance is explicit.
- [ ] Compatibility and migration requirements are explicit.
- [ ] Deprecation, supersession and retirement rules are explicit.
- [ ] Registry alignment requirements are explicit.
- [ ] Work package requirements are explicit.
- [ ] Evidence acceptance process is not duplicated.
- [ ] Safety and privacy classifications are not duplicated.
- [ ] Tool policy is not duplicated.
- [ ] Project specification structure is not duplicated.
- [ ] Repository architecture guidance is not duplicated.
- [ ] No project or session state.
- [ ] No local absolute paths.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent organizational steward mapping;
- permanent review-authority mapping;
- permanent compatibility policy authority;
- permanent migration approval authority;
- permanent deprecation and retirement authority;
- P1 activation prerequisites.
