# FARO1 Evidence Review and Acceptance

## 1. Document Metadata

```yaml
title: FARO1 Evidence Review and Acceptance
document_id: FARO1-EVIDENCE-REVIEW-AND-ACCEPTANCE
version: 0.2.0
status: approved
priority: P0
scope: Binding evidence review, validation, acceptance, approval-gate and rollback principles for FARO1-orchestrated research software work
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define evidence review and acceptance requirements for FARO1-orchestrated research software work.
load_condition: task-conditional
authority_level: binding-policy
activation_rule: Load for decisions about evidence sufficiency, review completeness, validation results, PASS/FAIL classification, Owner approval gates, rollback requirements or acceptance readiness.
```

## 2. Primary Responsibility

This document defines evidence review and acceptance requirements for FARO1-orchestrated research software work.

It does not define safety, privacy or protected-data classifications; those belong to `SAFETY_PRIVACY_GUARDRAILS.md`. It does not define tool permissions, command authorization, package policy, network policy or agent delegation; those belong to `TOOL_AND_AGENT_POLICY.md`. It does not define project requirements, repository architecture or project specification structure.

## 3. Scope

This policy applies when FARO1 work determines whether a work package, document, code change, generated artifact, validation result or review result is ready for acceptance.

It covers:

- acceptable evidence categories;
- evidence sufficiency;
- review minimums;
- validation minimums;
- PASS, PASS WITH DEFECTS and FAIL decisions;
- Owner approval gates;
- evidence limitations;
- rollback and correction principles.

Project-specific requirements may add stricter acceptance criteria but may not weaken this policy or binding safety and tool policies.

## 4. Precedence

Evidence and acceptance decisions follow this precedence:

1. Permanent FARO1 Instructions and runtime constraints.
2. `SAFETY_PRIVACY_GUARDRAILS.md`.
3. `TOOL_AND_AGENT_POLICY.md`.
4. This evidence review and acceptance policy.
5. Approved project-specific requirements.
6. Task-specific user instructions that do not conflict with levels 1-5.

When evidence sources, acceptance criteria or authority claims conflict, stop the affected decision and mark the unresolved point `NEEDS_VERIFICATION`.

## 5. Evidence Principles

- Evidence must be task-relevant, current enough for the decision and reproducible where practical.
- Evidence must distinguish observed facts from inference, recommendation and unresolved uncertainty.
- Evidence must identify the command, file, review source or user decision that supports the claim.
- An agent's assertion, summary or report of success is not objective evidence by itself. It may support review only when grounded in inspected files, preserved command output, recorded decisions, diffs, test results, manifests, logs or another source-grounded artifact.
- If an agent claim cannot be tied to inspectable source-grounded evidence, the affected claim remains `NEEDS_VERIFICATION` and must not support PASS.
- A successful command is not sufficient evidence for acceptance when required review categories remain incomplete.
- A missing or unavailable validation tool must be reported as a limitation, not converted into PASS.
- Unreviewed generated output is not accepted evidence for publication or release.
- Acceptance must not rely on secret values, participant-level content or unknown-sensitivity material.
- Uncertainty about evidence sufficiency stops the affected acceptance decision.

## 6. Acceptable Evidence Categories

Acceptable evidence may include:

| Evidence category | Eligible use | Minimum requirement |
|---|---|---|
| File inspection | Confirm metadata, structure, content, scope or dependencies | Cite the reviewed file and relevant lines or sections |
| Git status and diff | Confirm changed files, intended scope and whitespace validity | Report status and relevant diff summary without exposing restricted content |
| Validation command result | Confirm tests, renders, checks or scripts completed | Report command, outcome and material warnings or limitations |
| Review checklist | Confirm required review categories were considered | State each required category as PASS, PASS WITH DEFECTS, FAIL or NOT RUN |
| Owner decision | Record acceptance or direction from the review authority | Capture decision, document or work package, scope and exclusions |
| Dependency review | Confirm dependency direction and absence of circular normative dependency | Identify the typed edges reviewed |
| Defect log | Track known defects and corrections | Include defect ID, severity, location, expected rule, observed issue and required correction |

Evidence must be sufficient for the specific decision. A category is not required merely because it exists in this table.

## 7. Evidence Quality States

Evidence quality states are:

- `not-run`: required or planned evidence was not collected.
- `unverified`: evidence exists but has not been checked against the acceptance criteria.
- `source-grounded`: evidence is tied to an inspected source, command output or recorded decision.
- `reviewed`: evidence was checked by a review step and defects, limits or uncertainty were recorded.
- `validated`: evidence passed the required review and validation gates for the stated scope.
- `NEEDS_VERIFICATION`: evidence is missing, conflicting, stale, ambiguous or outside the agent's authority to accept.

`NEEDS_VERIFICATION` is not an approval state and does not authorize continuation of the affected acceptance decision.

## 8. Review Minimums

Review and Validation are distinct mandatory gates and are not interchangeable. Review assesses whether the implementation, scope, evidence, dependencies, defects, safety constraints and acceptance criteria match the approved work package.

Under an active MacroGate defined by `TOOL_AND_AGENT_POLICY.md`, Review and Validation may be performed by the agent as technical gates within the same bounded work package without separate human interaction for each technical sub-step.

Review and Validation remain distinct gates. Each must produce source-grounded evidence appropriate to its own purpose, and PASS at one gate does not imply PASS or Acceptance at another gate.

Final Acceptance, lifecycle approval, activation, staging, commit, push, pull request, release, publication and other Owner Approval Gates remain separate explicit decisions.

Before acceptance, the review must check the narrowest applicable set of categories:

- requested scope and allowed files;
- primary responsibility and scope boundaries for Knowledge documents;
- metadata and controlled values;
- dependencies and typed edge direction;
- overlap with adjacent Knowledge responsibilities;
- changed-file manifest;
- relevant diff or full content for untracked files;
- safety, privacy and secret risk result at the appropriate level;
- validation results and limitations;
- known defects and their resolution status;
- explicit approval authority and exclusions.

For untracked files, ordinary `git diff` may be insufficient. Use a no-index diff, full line-numbered content or another source-grounded equivalent.

## 9. Validation Minimums

Validation applies artifact-appropriate checks, commands, tests, renders, inspections or other verification methods to determine whether the defined acceptance criteria are actually satisfied. A successful Review does not replace Validation, and successful Validation does not replace Review.

Validation must be appropriate to the changed artifact:

- Markdown Knowledge files require structural, metadata, dependency, duplication and whitespace review.
- Code changes require relevant tests and static checks where available.
- Generated analysis outputs require provenance and review appropriate to their sensitivity and intended use.
- Repository publication candidates require changed-file, secret, privacy and history-risk review.
- Unavailable validation tools must be reported with reason and residual risk.

Validation commands and tool authorization are governed by `TOOL_AND_AGENT_POLICY.md`. Safety, privacy and disclosure requirements are governed by `SAFETY_PRIVACY_GUARDRAILS.md`.

## 10. Decision Classes

Review decisions use the following classes:

| Decision | Meaning | Acceptance effect |
|---|---|---|
| `PASS` | Required evidence is sufficient and no blocking defect remains | Eligible for the next explicit gate |
| `PASS WITH DEFECTS` | Evidence is sufficient to continue review, but non-blocking or bounded defects remain | Not eligible for final approval unless the approval scope explicitly accepts the defects |
| `FAIL` | Required evidence is missing, conflicting, invalid or a blocking defect remains | Stop the affected work until corrected or explicitly deferred |
| `DEFER` | Decision is intentionally postponed by the authorized reviewer | No approval or activation occurs |
| `NOT RUN` | A relevant validation was not executed | Must include reason and residual risk |
| `NEEDS_VERIFICATION` | The agent cannot establish the required fact or authority | Stop the affected decision pending resolution |

PASS at one gate does not imply approval at another gate.

## 11. Defect Handling

Defects must be recorded with:

- defect ID;
- severity;
- file and lines or bounded location;
- expected rule;
- observed text or behavior;
- required correction;
- resolution status.

Severity classes:

- `Blocking`: prevents acceptance or safe continuation.
- `Major`: materially weakens policy, implementation, validation or review reliability.
- `Minor`: bounded correction needed; acceptance may continue only if the approval scope permits.
- `Informational`: non-blocking note or residual risk.

In-scope defect fixes may continue within the same MacroGate when they remain inside the approved bounded work package and do not constitute a `MaterialBoundaryChange` under `TOOL_AND_AGENT_POLICY.md`.

If a fix requires broader policy changes, another document, new authority, external exposure, protected-data access or another MaterialBoundaryChange, stop the affected work and request the required authorization.

## 12. Owner Approval Gates

Owner approval is required for:

- lifecycle approval of Knowledge documents;
- activation of an approved document;
- acceptance of unresolved defects;
- staging, commit, push, pull request, release or publication actions;
- high-risk Git actions;
- destructive rollback or cleanup;
- scope changes that broaden access, authority or content exposure.

An Owner decision must state:

- decision class;
- document, work package or artifact;
- approval scope;
- required corrections, if any;
- explicit exclusions such as no activation, staging, commit, push, pull request, release or publication.

Approval is not transferable to a broader scope unless explicitly stated.

## 13. Lifecycle Acceptance

Knowledge document lifecycle acceptance must keep lifecycle status and evidence state distinct.

Minimum evidence for Knowledge document approval includes:

- complete canonical metadata;
- exactly one primary responsibility;
- correct priority, load condition and authority level;
- required references to `KB_INDEX.md`;
- correct typed dependencies;
- no circular normative dependency;
- no duplicated neighboring responsibility;
- no project or session state;
- no secrets, participant data or protected information;
- completed review with defects resolved, accepted or deferred by explicit authority.

Approval records the acceptance decision. Activation requires a separate activation rule and authorization when applicable.

## 14. Rollback and Correction Principles

Rollback is a controlled correction decision, not an automatic reaction.

When accepted work later proves incorrect:

1. Stop affected downstream use.
2. Identify the accepted decision, evidence and affected files or artifacts.
3. Classify the problem and residual risk.
4. Preserve minimal non-sensitive evidence.
5. Propose the narrowest correction or rollback.
6. Obtain required authorization for destructive or publication-affecting actions.
7. Validate the corrected state.

Git history rewrite, force-push, release deletion, secret rotation and protected-data incident response require separate explicit authorization and must follow applicable safety and tool policies.

## 15. Evidence Reporting

Evidence reports should be concise but must include enough detail for independent review.

Reports should include:

- work package or decision name;
- files reviewed or changed;
- material commands and results;
- PASS/FAIL/NOT RUN outcomes;
- defects and resolution mapping;
- limitations and residual risk;
- approval status and next gate.

Reports must not include secret values, participant-level content or unnecessary sensitive local context.

## 16. Non-Acceptance Conditions

Acceptance must not be granted when:

- required evidence is missing without an explicit deferral;
- evidence conflicts and the conflict is unresolved;
- a blocking defect remains;
- the approval authority is unclear;
- the work exceeds authorized scope;
- safety, privacy or tool-policy gates are unresolved;
- generated artifacts are unreviewed for their intended use;
- validation output is stale, unavailable or irrelevant and no limitation is recorded;
- the acceptance would silently approve activation, staging, commit, push, pull request, release or publication without explicit scope.

## 17. Dependencies and References

Typed dependency relationships:

```text
Permanent FARO1 Instructions
  constrains -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md

KB_INDEX.md
  registers -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  routes-to -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md for evidence or acceptance decisions

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md

TOOL_AND_AGENT_POLICY.md
  constrains -> command, tool, network, Git and agent evidence collection

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> evidence sufficiency, review decisions, acceptance gates and rollback decisions
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.
- Approved project specifications may add stricter project-specific acceptance criteria.

Proposed or absent files must not be represented as active runtime Knowledge sources.

## 18. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P0`.
- [ ] During draft review, `status` is `draft` and `document_evidence_state` is `source-grounded`.
- [ ] Before lifecycle approval is recorded, the document has passed content Review and Validation and received explicit Owner approval.
- [ ] After lifecycle alignment, `status` is `approved` and `document_evidence_state` is `validated`, with the corresponding `KB_INDEX.md` registry entry aligned.
- [ ] Load condition `task-conditional`.
- [ ] Authority level `binding-policy`.
- [ ] Evidence categories are defined without becoming a tool policy.
- [ ] Agent assertions are not treated as objective evidence without inspectable source-grounded support.
- [ ] Review and Validation are defined and applied as distinct, non-substitutable gates.
- [ ] PASS, PASS WITH DEFECTS, FAIL, NOT RUN and NEEDS_VERIFICATION are defined.
- [ ] Review minimums are explicit.
- [ ] Validation minimums are explicit.
- [ ] Owner approval gates are explicit.
- [ ] Rollback principles are explicit.
- [ ] Safety and privacy classifications are not duplicated.
- [ ] Tool permissions and command authorization are not duplicated.
- [ ] Project specification structure is not duplicated.
- [ ] Repository architecture guidance is not duplicated.
- [ ] No project or session state.
- [ ] No local absolute paths.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] `SAFETY_PRIVACY_GUARDRAILS.md` constrains this document.
- [ ] `TOOL_AND_AGENT_POLICY.md` constrains evidence collection.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent organizational steward mapping;
- permanent review-authority mapping;
- permanent acceptance authority roles;
- accepted validation cadence;
- approved defect severity definitions;
- approved rollback authority mapping;
- full P0 activation prerequisites.
