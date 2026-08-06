# FARO1 Safety and Privacy Guardrails

## 1. Document Metadata

```yaml
title: FARO1 Safety and Privacy Guardrails
document_id: FARO1-SAFETY-PRIVACY-GUARDRAILS
version: 0.1.0
status: approved
priority: P0
scope: Binding safety, privacy, protected-data and publication guardrails for FARO1-orchestrated research software work
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define binding safety, privacy, protected-data and publication guardrails for FARO1-orchestrated research software work.
load_condition: always-safety
authority_level: guardrail
activation_rule: Applicable whenever FARO1 work could affect data privacy, protected research data, secrets, public Git content, publication, release, external agents or disclosure risk. It does not require Project Mode.
```

## 2. Primary Responsibility

This document defines binding safety, privacy, protected-data and publication guardrails for FARO1-orchestrated research software work.

It does not own tool or agent routing, agent execution permissions, detailed command policies, evidence collection procedure, PASS/FAIL acceptance workflow, repository architecture, project specification, project state, session state or local orchestration history.

## 3. Scope

These guardrails apply whenever FARO1 work can affect privacy, protected research data, secrets, external exposure, public Git content, publication, release or disclosure risk.

They apply in Generic Mode and Project Mode. Project-specific requirements may strengthen these guardrails but may not weaken them.

## 4. Safety Principles

- Use the minimum necessary data and context.
- Deny public exposure by default for non-public data.
- Synthetic data is not automatically safe.
- Aggregate output is not automatically publishable.
- A private Git repository is not automatically protected storage.
- Git LFS is not a privacy control.
- Uncertainty stops affected work.
- Preserve evidence without exposing sensitive content.
- Destructive incident response requires separate authorization.
- Project requirements may strengthen but not weaken these guardrails.

## 5. Data Classification

| Classification | Definition | Allowed locations | Prohibited locations | Agent access rule | Public Git eligibility | Logging rule | Publication requirement |
|---|---|---|---|---|---|---|---|
| `public` | Material already authorized for public handling or material that completed provenance, rights and publication review | Approved public repository or publication environment | Any location that removes required provenance or rights controls | Allowed only when necessary for the bounded task | Eligible only after provenance, rights and publication-suitability review | Log only necessary metadata and audit information | Provenance, rights and publication review |
| `internal non-sensitive` | Internal material not containing protected or identifying research information | Approved internal workspace | Public repository without relevance, provenance and licensing review | Minimum necessary access | Not automatic; conditional after public-release review | No unnecessary content or local identifiers | Relevance, provenance and licensing review |
| `synthetic` | Clearly generated artificial test or fixture data | Reviewed public fixture location or approved non-public workspace | Locations where provenance is absent or data may be mistaken for real data | Allowed only when clearly synthetic and necessary | Conditional on synthetic provenance and disclosure review | Aggregate structural diagnostics only; no reconstructed participant-like records | Synthetic label, generation documentation and disclosure review |
| `aggregate disclosure-reviewed` | Aggregate output reviewed for disclosure risk | Approved output or publication location | Restricted-data locations, raw-data locations and temporary exports | Allowed only for the reviewed output and bounded task | Only the reviewed output and reviewed version | Aggregate values only; no reconstructable row-level values | New stratification or transformation requires renewed review |
| `restricted research data` | Protected research data not approved for public access | Explicitly approved protected analysis environment | Public Git, ordinary workspace, prompts, logs and artifacts | No default agent access; explicit environment and authorization required | Never eligible | No row-level logging | Separate data-controller and project-authority decision |
| `pseudonymized participant-level data` | Participant-level data with identifiers replaced or transformed | Explicitly approved controlled environment only | Public Git, staging, prompts, logs and artifacts | No external-agent access without explicit approval | Never eligible | No participant-level logging | Separate authorized privacy review |
| `directly identifying data` | Data that directly identifies a person | Explicitly approved controlled environment only | Repository, agent context, chat, logs and artifacts | Prohibited for agents | Never eligible | Do not log content | Formal authority review before handling |
| `secrets and credentials` | Tokens, API keys, private keys, passwords and authentication material | Governed secret store or approved runtime context | Repository files, prompts, logs, artifacts, chat and reports | Prohibited unless an applicable tool policy explicitly authorizes bounded runtime handling | Never eligible | Never print or persist values | Secret-management review |
| `unknown / NEEDS_VERIFICATION` | Material whose sensitivity or provenance cannot be established | Unchanged source location or isolated quarantine | Integration, publication and copying targets | Stop; inspect no more than necessary | Not eligible | Record only masked path, type and risk | Mark `NEEDS_VERIFICATION` and escalate |

## 6. Public Repository Prohibitions

The public repository must not contain:

- raw participant data;
- pseudonymized participant-level data;
- identifiers or linkage keys;
- health or sensitive personal data;
- reconstructable row-level residuals or fitted values;
- model objects embedding original observations;
- individual missingness logs;
- credentials, tokens, API keys or private keys;
- `.env` files;
- protected data through Git LFS;
- restricted archives or backups;
- temporary sensitive exports;
- sensitive local caches;
- prompt or log content exposing protected rows or storage layouts.

## 7. Minimum-Necessary Data Handling

FARO1 work must use only task-relevant fields and context. Synthetic or redacted examples must be preferred where possible. Broad directory access is prohibited when a bounded path is sufficient. Data must not be copied for convenience or persisted beyond the approved need. Local identifiers must not be disclosed without necessity. Classification uncertainty requires escalation.

## 8. Synthetic and Aggregate Data

Synthetic data requires explicit labeling, a documented generation method, no copied participant rows, no retained identifiers, no copied rare participant combinations and no representation as numerical reproduction. Its default purpose is structural, test or render validation. Public release requires disclosure review, and material regeneration requires renewed review.

Aggregate outputs require disclosure assessment for small cells, rare combinations, stratified outputs, participant counts, residual or influence summaries, individual trajectories, free text, longitudinal reconstruction and repeated transformations of reviewed outputs. No numeric disclosure threshold is invented here.

## 9. Logs, Diagnostics and Model Artifacts

Safe candidates may include aggregate test summaries, schema-validation results, non-sensitive build logs, synthetic-data diagnostics and bounded error categories.

Unsafe content includes row dumps, identifiers, observation-level residuals, fitted values, serialized objects embedding data, traces containing source rows, protected filesystem layouts and recoverable participant-level diagnostics.

## 10. Secrets and Authentication Material

Secrets must not persist in repositories, prompts, logs, artifacts, screenshots or reports. Secret values must not be printed or echoed. Runtime handling must follow the applicable tool policy. Finding a secret triggers incident handling. Rotation or revocation is not performed without authority.

## 11. Git and History Privacy

Before staging or publication, candidate tracked files and untracked files require privacy and secret review. Deleting a file does not remove it from Git history. History rewrite and force-push are prohibited without explicit high-risk approval. Forks, clones, archives, releases and LFS surfaces must be considered. Commit and push require separate approval gates. A private repository is not automatically protected storage.

This document does not provide an operational command catalog.

## 12. Agent and Prompt Data Boundaries

Agents must not receive participant-level protected data, secrets, reversible participant outputs, unnecessary identifiers or full sensitive logs.

Tasks must use minimum-necessary prompt context, bounded allowed and forbidden paths, synthetic examples and redacted errors. Agents must stop and escalate when sensitivity is uncertain. Prompt history is not automatically publishable.

## 13. Local and Protected Environment Boundaries

The following environments are distinct:

- public repository working copy;
- local non-Git orchestration history;
- approved protected analysis environment;
- restricted data mounts;
- external cloud or agent services.

Termux, a private GitHub repository, an agent sandbox or a generic cloud environment must not be assumed to be an approved protected environment.

## 14. Publication and Disclosure Review

These guardrails apply before staging or committing potentially sensitive material, pushing to public or externally accessible remotes, opening or updating a PR with research outputs, release, archive, DOI deposit, supplementary publication or external-service migration.

Required evidence categories are:

- candidate tracked-file manifest;
- Git status and relevant diff;
- secret-review result;
- privacy/PII review result;
- artifact and archive inventory;
- output provenance;
- rights and licensing status where applicable;
- history-risk assessment;
- disclosure decision;
- required Owner or authority approval.

Exact commands, scanning tools and PASS/FAIL procedures belong to `TOOL_AND_AGENT_POLICY.md` and `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

## 15. Incident and Uncertainty Handling

When an incident or uncertainty is found:

1. Stop affected work.
2. Do not copy, publish or expose further.
3. Do not print sensitive contents.
4. Preserve minimal non-sensitive evidence.
5. Report path, type and risk, not content.
6. Do not delete automatically.
7. Do not rewrite history automatically.
8. Do not rotate or revoke credentials without authorization.
9. Escalate to the applicable user, data controller or authority.
10. Mark unresolved scope `NEEDS_VERIFICATION`.
11. Resume only after resolution or explicit scope exclusion.

## 16. Activation and Load Rules

- `load_condition` is `always-safety`.
- Applicability does not require Project Mode.
- The guardrails apply whenever work can affect privacy, protected data, secrets, external exposure or disclosure.
- A registry entry does not prove that this file exists or is active.
- While `status` is `draft`, this document is not an active runtime Knowledge source.
- Permanent FARO1 Instructions remain higher authority.
- Project sources may strengthen but not weaken this document.

## 17. Dependencies and References

Typed dependency relationships:

```text
Permanent FARO1 Instructions
  constrains -> SAFETY_PRIVACY_GUARDRAILS.md

KB_INDEX.md
  registers -> SAFETY_PRIVACY_GUARDRAILS.md
  routes-to -> SAFETY_PRIVACY_GUARDRAILS.md for safety/privacy scope

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> TOOL_AND_AGENT_POLICY.md
  constrains -> EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> approved project specifications
  constrains -> public repository, publication and release decisions
```

`PROJECT_SPECIFICATION.md` may add stricter project requirements but may not weaken this document. It does not load or control this document. Loading decisions belong to `KB_INDEX.md`.

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `TOOL_AND_AGENT_POLICY.md` is the future tool and execution-policy owner.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the future evidence and acceptance owner.
- Approved project specifications may add stricter project-specific requirements.

Proposed or absent files must not be represented as already active.

## 18. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P0`.
- [ ] Status `draft`.
- [ ] Evidence state `source-grounded`.
- [ ] Load condition `always-safety`.
- [ ] Authority level `guardrail`.
- [ ] All 18 sections are present.
- [ ] All nine data classifications are present.
- [ ] Every classification has seven explicit attributes.
- [ ] No duplicate tool policy.
- [ ] No duplicate evidence procedure.
- [ ] No project or session state.
- [ ] No local absolute paths.
- [ ] No secrets or participant data.
- [ ] No invented disclosure thresholds.
- [ ] No invented retention periods.
- [ ] No unsupported legal claims.
- [ ] Typed dependencies are explicit.
- [ ] No circular normative dependency.
- [ ] Conflict handling stops affected work.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] No Change History section.
- [ ] No operational command catalog.

`NEEDS_VERIFICATION` items:

- applicable organizational data policy;
- data-controller requirements;
- disclosure thresholds;
- retention periods;
- approved protected environment;
- approved secret-scanning tools;
- incident response contacts;
- legal or ethical review requirements;
- disclosure status of the existing synthetic fixture;
- independent Git-history audit status;
- permanent steward and review-authority mapping;
- full P0 activation prerequisites.
