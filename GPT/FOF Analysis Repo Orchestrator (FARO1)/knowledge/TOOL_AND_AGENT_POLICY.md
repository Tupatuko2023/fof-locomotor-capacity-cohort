# FARO1 Tool and Agent Policy

## 1. Document Metadata

```yaml
title: FARO1 Tool and Agent Policy
document_id: FARO1-TOOL-AND-AGENT-POLICY
version: 0.1.0
status: approved
priority: P0
scope: Binding tool, command, automation and agent-boundary policy for FARO1-orchestrated research software work
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define approved tool and agent boundaries for FARO1-orchestrated research software work.
load_condition: task-conditional
authority_level: binding-policy
activation_rule: Load for decisions about tool use, command execution, automation, external agents, delegated work, sandbox boundaries, network access, package installation, Git operations or runtime handling of authentication context.
```

## 2. Primary Responsibility

This document defines approved tool, command, automation and agent boundaries for FARO1-orchestrated research software work.

It does not define safety, privacy or protected-data classifications; those belong to `SAFETY_PRIVACY_GUARDRAILS.md`. It does not define evidence acceptance criteria, PASS/FAIL review workflow or Owner acceptance procedure; those belong to `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

## 3. Scope

This policy applies when FARO1 work uses or authorizes:

- shell commands;
- repository inspection tools;
- file editing tools;
- package managers;
- render, test or analysis tools;
- network-enabled tools;
- Git and GitHub tools;
- subagents or external automation;
- tools that may access authentication context;
- tools that may create, modify, publish or remove repository content.

Project-specific requirements may restrict these rules further but may not weaken this policy or any binding safety guardrail.

## 4. Precedence

Tool and agent decisions follow this precedence:

1. Permanent FARO1 Instructions and runtime constraints.
2. Binding safety and privacy guardrails.
3. This tool and agent policy.
4. Approved project-specific requirements.
5. Task-specific user instructions that do not conflict with levels 1-4.

When instructions conflict, stop the affected action and mark the unresolved point `NEEDS_VERIFICATION`.

## 5. Tool-Use Principles

- Use the narrowest tool that can complete the bounded task.
- Inspect before editing.
- Prefer read-only commands for orientation.
- Prefer structured tools over ad hoc parsing when available.
- Verify tool existence, task-relevant capability and version where relevant before using the tool or accepting its output as evidence. If verification is not possible, stop the affected action and mark the capability `NEEDS_VERIFICATION`.
- Do not broaden filesystem, network or credential access for convenience.
- Do not route sensitive, unknown or unnecessary content to external tools.
- Do not continue a tool action after its safety classification becomes uncertain.
- Preserve user changes unless explicitly authorized to modify them.
- Treat generated files, caches, logs and screenshots as possible disclosure surfaces.

## 6. Approved Read-Only Tool Classes

The following read-only tool classes are generally eligible when bounded to the task:

| Tool class | Eligible use | Boundary |
|---|---|---|
| Repository listing | Identify relevant files and directories | Do not enumerate unrelated sensitive locations |
| Text search | Locate symbols, references, tests or policies | Use bounded paths where practical |
| File viewing | Read relevant source, documentation, tests or manifests | Do not open participant data, secrets or unknown sensitive files |
| Git inspection | Review status, diff, branch, remotes or history metadata | Do not expose sensitive diff content in prompts or reports |
| Test discovery | Identify available local tests and render targets | Do not generate or inspect real participant data |
| Environment inspection | Verify tool availability and non-secret runtime settings | Do not print secrets, tokens or credential-bearing variables |

Read-only status does not remove privacy obligations. If a file or output may contain restricted research data, secrets or unknown sensitivity, stop and apply `SAFETY_PRIVACY_GUARDRAILS.md`.

## 7. Approved Write Tool Classes

Write operations are eligible only when they are necessary for the approved task and stay within allowed paths.

| Tool class | Eligible use | Boundary |
|---|---|---|
| File editing | Create or modify scoped repository files | Do not modify unrelated files or protected data |
| Formatting | Apply established project formatting to changed files | Do not reformat unrelated files |
| Test output generation | Create approved synthetic or aggregate outputs | Do not create participant-level outputs |
| Render output generation | Render approved documents or smoke tests | Outputs must be reviewed before publication |
| Package lock updates | Update dependency metadata when required by the task | Requires review of changed dependency files |

Write tools must not create `.env`, `.RData`, `.Rhistory`, unverified CSV/RDS/SAV data files, secrets, protected participant data or local machine state in the repository.

## 8. Shell and Command Policy

Commands must be scoped, reproducible and explainable. Prefer direct commands over interactive sessions. Use non-interactive flags where available.

Allowed command purposes include:

- repository status and diff inspection;
- source and documentation search;
- tests and smoke renders;
- synthetic fixture generation;
- linting, formatting and validation;
- package inspection;
- bounded dependency installation or update when explicitly needed.

Commands are not eligible when they:

- delete, overwrite or rewrite history without explicit high-risk authorization;
- print secrets or protected participant-level content;
- copy unknown or restricted data into the repository;
- upload repository content or artifacts without approval;
- run unreviewed remote scripts;
- modify global user configuration without explicit user authorization;
- bypass sandbox, permission or review controls.

If a command needs elevated permissions, network access or access outside the current writable scope, the request must state the reason and the bounded action.

If permission scope, authorization, allowed path or execution authority is ambiguous, stop the affected action and mark the issue `NEEDS_VERIFICATION`. Permission must not be inferred from tool availability, repository contents, prior general approval or agent capability.

## 9. Package Manager and Dependency Policy

Package managers may be used for:

- installing dependencies required by the existing project;
- updating a package when explicitly requested or required for compatibility;
- inspecting installed package versions;
- running package-defined scripts that are relevant to the task.

Package manager use must not:

- install unrelated tooling into the repository;
- run unreviewed post-install behavior against protected data;
- alter global configuration without explicit authorization;
- hide dependency changes from review;
- introduce packages that duplicate established project tooling without a documented reason.

Dependency changes require review of manifest and lockfile diffs where such files exist.

## 10. Git and GitHub Tool Policy

Git inspection is allowed when bounded to the task. Staging, committing, pushing, opening pull requests, rewriting history, deleting branches, creating releases or publishing artifacts require explicit user authorization unless permanent runtime instructions provide a narrower approved workflow.

Before any Git publication action, the candidate changes must be reviewed for:

- intended files only;
- no secrets;
- no participant data;
- no prohibited file types;
- no unintended generated artifacts;
- no unrelated user changes.

History rewrite, force-push, tag deletion and release deletion are high-risk actions and require explicit high-risk authorization.

## 11. Network and External Service Policy

Network-enabled tools may be used only when the task requires current external information, package retrieval, remote repository access, publication or external validation.

External services must not receive:

- restricted research data;
- pseudonymized or directly identifying participant-level data;
- secrets or credentials, except through an approved bounded authentication mechanism;
- unknown-sensitivity files;
- unnecessary local paths, logs or environment details.

When external information is used as evidence, record the source at the appropriate level of detail without copying restricted or copyrighted content beyond allowed limits.

## 12. Agent Delegation Policy

Subagents or external agents may be used only for bounded tasks with clearly defined inputs, outputs and forbidden content.

Delegated agents must not receive:

- participant-level protected data;
- secrets;
- full sensitive logs;
- unrestricted repository context;
- authority to publish, commit, push, delete or rewrite history unless explicitly authorized.

The controlling FARO1 agent remains responsible for integrating results, checking conflicts, verifying changed files and applying applicable safety and evidence rules. Agent output is not accepted merely because an agent produced it.

## 13. Authentication and Secret Handling

Tools may use existing authenticated runtime context only when the task requires it and the tool boundary is understood. Secret values must not be printed, copied, committed, summarized or exposed to another agent.

If a tool reveals a secret or credential-like value:

1. Stop the affected work.
2. Do not repeat or quote the value.
3. Preserve only masked, non-sensitive evidence.
4. Escalate under `SAFETY_PRIVACY_GUARDRAILS.md`.

Secret rotation, revocation and history cleanup require separate authorization.

## 14. Data and Artifact Boundaries

Tools must read analysis data only from approved synthetic or explicitly authorized locations. In the public research repository, participant-level real data is not an approved tool input.

Generated artifacts must be classified before publication or commit. Aggregate outputs, rendered manuscripts, figures, tables, logs, caches and model artifacts require review appropriate to their content and provenance.

Synthetic fixtures must remain clearly labeled as synthetic and generated. They must not be represented as numerical reproduction of restricted research data.

## 15. Validation Commands

When repository files are changed, validation must include the repository-required checks unless the user explicitly narrows the task or a required tool is unavailable:

```text
git diff --check
Rscript -e 'testthat::test_dir("tests/testthat")'
quarto render manuscript/smoke_test.qmd
```

If a validation command cannot be run, report the reason and the residual risk. Passing commands do not replace privacy, evidence or Owner acceptance requirements.

## 16. Prohibited Actions

The following actions are prohibited without explicit separate authorization:

- using real participant-level data in the public repository;
- opening or printing secrets;
- committing prohibited data types;
- copying restricted data into prompts, logs or artifacts;
- destructive cleanup after a suspected incident;
- rewriting Git history;
- force-pushing;
- publishing releases or archives;
- granting broad filesystem, network or credential access to an agent;
- installing persistent global tooling unrelated to the task;
- bypassing project validation after edits.

Some actions remain prohibited even with ordinary task authorization when they conflict with binding safety or privacy guardrails.

## 17. Dependencies and References

Typed dependency relationships:

```text
Permanent FARO1 Instructions
  constrains -> TOOL_AND_AGENT_POLICY.md

KB_INDEX.md
  registers -> TOOL_AND_AGENT_POLICY.md
  routes-to -> TOOL_AND_AGENT_POLICY.md for tool and agent decisions

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> TOOL_AND_AGENT_POLICY.md

TOOL_AND_AGENT_POLICY.md
  conditionally-loads -> tool- or agent-specific execution context
  constrains -> command, automation, package, network, Git and agent-delegation decisions
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the future evidence review and acceptance authority.

Proposed or absent files must not be represented as active runtime Knowledge sources.

## 18. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P0`.
- [ ] Status `approved`.
- [ ] Evidence state `validated`.
- [ ] Load condition `task-conditional`.
- [ ] Authority level `binding-policy`.
- [ ] Tool and agent boundaries are defined.
- [ ] Tool existence and task-relevant capability verification are required before use or evidentiary reliance.
- [ ] Permission ambiguity stops affected work and is marked `NEEDS_VERIFICATION`.
- [ ] Safety and privacy classifications are not duplicated.
- [ ] Evidence acceptance workflow is not duplicated.
- [ ] Git, package, network and shell boundaries are explicit.
- [ ] Agent delegation boundaries are explicit.
- [ ] No project or session state.
- [ ] No local absolute paths.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] `KB_INDEX.md` is referenced correctly.
- [ ] `SAFETY_PRIVACY_GUARDRAILS.md` constrains this document.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent organizational steward mapping;
- permanent review-authority mapping;
- approved external-agent providers;
- approved secret-scanning tools;
- approved dependency update policy;
- approved GitHub publication workflow;
- approved protected analysis environment;
- full P0 activation prerequisites.
