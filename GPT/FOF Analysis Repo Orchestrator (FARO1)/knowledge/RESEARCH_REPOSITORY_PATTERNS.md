# FARO1 Research Repository Patterns

## 1. Document Metadata

```yaml
title: FARO1 Research Repository Patterns
document_id: FARO1-RESEARCH-REPOSITORY-PATTERNS
version: 0.1.0
status: approved
priority: P1
scope: Reusable research-repository architecture, reproducibility and code-migration patterns for FARO1-orchestrated research software work
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define reusable research-repository architecture, reproducibility and code-migration patterns without defining project-specific repository state or execution authorization.
load_condition: task-conditional
authority_level: reference
activation_rule: Load for repository architecture, reproducibility-pattern or research-code migration-pattern questions. This reference does not authorize execution.
```

## 2. Primary Responsibility

This document defines reusable research-repository architecture, reproducibility and code-migration patterns for FARO1.

It does not define active project state, project-specific repository values, project-specific migration decisions, tool authorization, privacy classifications, evidence PASS/FAIL procedure, publication authorization, lifecycle governance, project context structure or project specification structure.

## 3. Scope

This reference applies when FARO1 needs reusable patterns for:

- research repository organization;
- reproducible analysis structure;
- source-to-target analysis-code migration planning;
- artifact disposition during migration;
- dependency closure;
- provenance preservation;
- portability adaptation;
- scientific or analytical change boundaries;
- rollback and recovery pattern selection.

Project-specific requirements, approved paths, source repositories, target repositories, migration strategy decisions and validation thresholds belong to an approved project specification or other authorized project-level source.

## 4. Repository Pattern Principles

- Inspect before modifying or migrating.
- Prefer the smallest repository pattern that supports reproducibility, review and maintenance.
- Keep source-grounded provenance for material repository changes.
- Keep protected data and secrets out of public repository history.
- Separate reusable patterns from project-specific decisions.
- Separate portability changes from scientific or analytical changes.
- Treat uncertain dependency, provenance, permission or data classification as `NEEDS_VERIFICATION`.
- Preserve P0 hard gates for Git publication, history rewrite, force-push, release, activation and external exposure.

Patterns are recommendations unless adopted by an approved project specification or explicit work package.

## 5. Ownership Boundaries

This document may recommend repository and migration patterns. It must not authorize the tools, data access or external actions needed to execute them.

Ownership boundaries:

| Topic | Owner |
|---|---|
| Tool, command, Git, network and agent authorization | `TOOL_AND_AGENT_POLICY.md` |
| Safety, privacy, protected data, secrets and disclosure | `SAFETY_PRIVACY_GUARDRAILS.md` |
| Evidence sufficiency, review, validation and acceptance | `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` |
| Project context structure | `PROJECT_CONTEXT_TEMPLATE.md` |
| Project-specific requirements and approved choices | `PROJECT_SPECIFICATION_TEMPLATE.md` or approved project specification |
| Knowledge lifecycle and governance | `KNOWLEDGE_GOVERNANCE.md` |

If a repository pattern conflicts with a binding P0 policy or approved project requirement, the affected decision stops and is marked `NEEDS_VERIFICATION`.

## 6. Research Repository Architecture Patterns

Common research repository patterns include:

| Pattern | Use when | Cautions |
|---|---|---|
| `analysis-package` | Shared functions, tests and reusable analysis code are central | Requires package metadata and test discipline |
| `analysis-pipeline` | Ordered scripts or jobs produce outputs from approved inputs | Must preserve execution order and dependency clarity |
| `research-compendium` | Code, documentation, synthetic fixtures and reproducibility metadata are bundled | Must not imply real data belongs in the repository |
| `manuscript-adjacent-analysis` | Repository supports report or publication outputs | Does not require manuscript files to be stored in the repository |
| `validation-fixture-repository` | Synthetic or public fixtures support structural testing | Fixtures must be clearly synthetic or public and provenance-reviewed |
| `migration-staging-repository` | A temporary isolated workspace is needed for migration assessment | Must not be treated as approved protected storage by default |

Pattern selection is project-specific. A repository may combine patterns when the combination is explicitly reviewed and does not create conflicting ownership or data-handling assumptions.

## 7. Reproducibility Patterns

Reusable reproducibility patterns include:

- documented execution entry points;
- deterministic script order where order matters;
- explicit local code dependencies;
- environment or dependency manifests appropriate to the project;
- synthetic fixtures for structural tests;
- generated-output regeneration instructions;
- provenance records for imported code or generated artifacts;
- validation commands appropriate to the repository pattern;
- clear separation of source logic, generated artifacts and protected data.

This document does not require a specific runtime manager, rendering engine, container system, package repository, continuous-integration provider or compliance framework. Those choices belong to project-specific requirements.

## 8. Safe Code Migration Pattern

The generic safe research-code migration pipeline is:

```text
INSPECT SOURCE
  -> CLASSIFY CANDIDATE ARTIFACTS
  -> RESOLVE DEPENDENCY CLOSURE
  -> PRIVACY + PROVENANCE REVIEW
  -> SELECT MIGRATION STRATEGY
  -> BOUNDED MIGRATION WORK PACKAGE
  -> PORTABILITY ADAPTATION
  -> SCIENTIFIC / ANALYTICAL PARITY CHECK
  -> REVIEW + VALIDATION
  -> EXTERNAL-ACTION HARD GATE
```

No migration should begin with copying files, rewriting history or pushing to a remote. Migration begins with source inspection, artifact classification, dependency closure and privacy/provenance review.

The selected migration strategy must be explicitly justified and authorized by the applicable project-level decision. A pattern recommendation is not execution approval.

## 9. Artifact Classification Taxonomy

The following taxonomy is a migration disposition taxonomy, not a privacy classification system:

| Classification | Meaning | Default disposition |
|---|---|---|
| `REQUIRED_FOR_ANALYSIS` | Needed to run or understand approved analysis logic | Candidate for migration after dependency, privacy and provenance review |
| `REQUIRED_FOR_PUBLICATION` | Needed for an approved publication or reporting output | Candidate only when publication boundary allows it |
| `TRANSITIVE_DEPENDENCY` | Required by a required artifact | Candidate if closure and safety checks pass |
| `GENERATED_ARTIFACT` | Reproducible output or build product | Prefer regeneration unless project approval requires preservation |
| `RESTRICTED_DATA` | Data or artifact requiring restricted handling | Stop and apply `SAFETY_PRIVACY_GUARDRAILS.md` |
| `LEGACY_OR_SUPERSEDED` | Replaced, obsolete or exploratory material | Exclude unless explicitly approved |
| `OUT_OF_SCOPE` | Not needed for the approved objective | Exclude |
| `NEEDS_VERIFICATION` | Unclear role, provenance, dependency or safety state | Stop affected migration path pending resolution |

`RESTRICTED_DATA` in this taxonomy is a disposition warning. Canonical data classifications and handling rules remain owned by `SAFETY_PRIVACY_GUARDRAILS.md`.

## 10. Dependency Closure Pattern

Migration planning must establish the transitive closure required for the selected objective.

Dependency closure should identify:

- local code dependencies;
- local configuration dependencies;
- local fixture or test dependencies;
- generated artifacts that are inputs to later steps;
- package or runtime dependencies relevant to validation;
- external file references;
- environment assumptions that affect execution;
- missing, ambiguous or out-of-scope dependencies.

A directed graph may be useful, but this document does not require one specific data structure. The requirement is a reviewable, source-grounded dependency closure result.

If closure is incomplete, stale, contradictory or impossible to inspect, the affected migration path is `NEEDS_VERIFICATION`.

## 11. Privacy and Provenance Pattern

Before migration execution, candidate artifacts require privacy and provenance review.

Minimum provenance evidence should include:

- source repository identity or source location;
- source revision, commit or version when applicable;
- source path;
- target path or target role;
- selected migration strategy;
- artifact classification and disposition;
- material portability adaptations;
- validation evidence or planned validation;
- reviewer or Owner decision when required.

The evidence may be a manifest, table, decision record, review report or another source-grounded artifact. This document does not require a universal filename, JSON schema or serialization format.

If data sensitivity, source provenance, license, rights or publication eligibility is uncertain, stop the affected migration path and route to the applicable owner.

## 12. Migration Strategy Selection

Migration strategy options include:

| Strategy | Use when | Key requirements |
|---|---|---|
| `history_preserving` | A bounded source subtree or file set has important authorship or historical provenance | Isolated plan, history-risk review, tool verification and explicit Git authorization |
| `provenance_preserving_copy` | A small set of artifacts can be copied with adequate source-grounded provenance | Provenance evidence, diff review, dependency closure and validation |
| `reconstruction` | Legacy code cannot be safely or portably migrated as-is | Explicit reconstruction scope, source references, parity or equivalence validation |

Tools such as history-filtering utilities may be examples for `history_preserving` extraction, but no tool is universally required by this document. Tool existence, version, capability, safety and suitability must be verified under `TOOL_AND_AGENT_POLICY.md` before use.

History rewrite, force-push, publication and external exposure remain hard-gated actions and require explicit authorization.

## 13. Portability vs Scientific Change Boundary

Portability or infrastructure changes may include:

- replacing local absolute paths with approved project-relative paths;
- adapting repository layout without changing analysis semantics;
- updating non-semantic configuration needed for the target repository;
- adjusting synthetic fixture paths;
- documenting environment assumptions;
- adapting build or validation entry points without changing analytical logic.

Migration or portability work does not automatically authorize scientific or analytical changes.

Scientific or analytical changes include changes to:

- statistical formulas;
- variable definitions;
- cohort inclusion or exclusion criteria;
- transformation semantics;
- missing-data handling;
- model specification;
- analytically meaningful random seeds;
- scientific interpretation;
- analysis results or conclusions.

If a scientific or analytical change is needed, treat it as a `MaterialBoundaryChange`: stop the affected migration path, request separate analytical-change authorization and require appropriate parity, equivalence or review evidence.

## 14. Validation and Parity Pattern

Validation should match the migration strategy and artifact risk.

Possible validation patterns include:

- changed-file and changed-scope review;
- dependency-closure review;
- syntax or static checks;
- unit or smoke tests;
- render or build checks when relevant;
- synthetic-fixture execution;
- provenance review;
- privacy and secret review;
- parity or equivalence comparison for migrated analysis behavior;
- human review for scientific or analytical changes.

Parity validation is required when migration claims analytical equivalence and suitable reference results exist. If reference results, tools or environments are unavailable, report the limitation and residual risk under `EVIDENCE_REVIEW_AND_ACCEPTANCE.md`.

Passing technical commands does not replace privacy review, evidence review or Owner approval.

## 15. Rollback and Recovery Pattern

Migration planning should define a rollback or recovery option before execution.

Rollback and recovery may include:

- preserving source references and source revisions;
- keeping migration work isolated until reviewed;
- documenting candidate changes before external action;
- maintaining a reversible target-branch or patch strategy;
- excluding uncertain artifacts rather than importing them;
- recording limitations and rejected artifacts;
- stopping before external-action hard gates when evidence is incomplete.

Destructive cleanup, history rewrite, force-push, release deletion, secret rotation and protected-data incident response require separate explicit authorization.

## 16. Explicit Exclusions

This reference does not make the following generic requirements:

- manuscript files in the target repository;
- any specific rendering engine;
- any specific render configuration;
- any specific computational-freeze setting;
- containers;
- any specific package-manager repository or snapshot service;
- any specific history-filtering tool;
- regulated-compliance frameworks as automatic obligations;
- issue tracker or DevOps workflow;
- commit signing for every project;
- project-specific source or target repository identity;
- project-specific migration strategy;
- project-specific validation thresholds;
- publication, push, release or activation.

These may be project-selected implementations when required by an approved project specification or other applicable authority.

## 17. Decision Matrix

| Situation | Recommended pattern |
|---|---|
| A few independent scripts and history is not material | `provenance_preserving_copy` |
| Bounded source subproject and historical provenance is material | `history_preserving` extraction |
| Legacy code is not safely portable as-is | `reconstruction` plus parity validation |
| Dependency closure is unclear | Stop and mark `NEEDS_VERIFICATION` |
| Data classification is unclear | Stop and apply `SAFETY_PRIVACY_GUARDRAILS.md` |
| Scientific logic changes | Separate analytical-change work package |
| Source provenance is unclear | Stop affected migration path |
| External publication or remote update is needed | External-action hard gate |

The matrix recommends patterns only. It does not authorize execution.

## 18. Dependencies and References

Typed dependency relationships:

```text
KB_INDEX.md
  registers -> RESEARCH_REPOSITORY_PATTERNS.md
  routes-to -> RESEARCH_REPOSITORY_PATTERNS.md for repository architecture and migration pattern questions

PROJECT_CONTEXT_TEMPLATE.md
  constrains -> project context and source/target relationship boundary

PROJECT_SPECIFICATION_TEMPLATE.md
  constrains -> project-specific requirements, approved choices and acceptance limits

SAFETY_PRIVACY_GUARDRAILS.md
  constrains -> data, privacy, protected-data, secret and disclosure aspects of repository patterns

TOOL_AND_AGENT_POLICY.md
  constrains -> tools, commands, Git operations, history rewrite, network use and external actions

EVIDENCE_REVIEW_AND_ACCEPTANCE.md
  constrains -> review, validation, evidence sufficiency and acceptance decisions
```

References:

- `KB_INDEX.md` is the manifest and routing authority.
- `PROJECT_CONTEXT_TEMPLATE.md` owns project context structure.
- `PROJECT_SPECIFICATION_TEMPLATE.md` owns project specification structure.
- `SAFETY_PRIVACY_GUARDRAILS.md` is the safety, privacy and protected-data authority.
- `TOOL_AND_AGENT_POLICY.md` is the tool, command and agent-boundary authority.
- `EVIDENCE_REVIEW_AND_ACCEPTANCE.md` is the evidence review and acceptance authority.

Proposed or absent files must not be represented as active runtime Knowledge sources.

## 19. Validation Checklist

- [ ] Exactly one primary responsibility.
- [ ] Complete canonical metadata.
- [ ] Priority `P1`.
- [ ] Status `approved`.
- [ ] Evidence state `validated`.
- [ ] Load condition `task-conditional`.
- [ ] Authority level `reference`.
- [ ] Repository architecture patterns are reusable and non-project-specific.
- [ ] Reproducibility patterns avoid mandatory project-specific tooling.
- [ ] Safe code migration pipeline is complete.
- [ ] Artifact taxonomy is a migration disposition taxonomy, not a privacy classification system.
- [ ] Dependency closure is required without mandating one implementation-specific data structure.
- [ ] Provenance requirements are source-grounded without requiring one file format.
- [ ] Migration strategy options are patterns, not automatic choices.
- [ ] Scientific and analytical changes are explicitly separated from portability changes.
- [ ] P0 hard gates remain intact.
- [ ] Guardrails boundary is preserved.
- [ ] Tool Policy boundary is preserved.
- [ ] Evidence Policy boundary is preserved.
- [ ] Project Context boundary is preserved.
- [ ] Project Specification boundary is preserved.
- [ ] No active project values.
- [ ] No FOF/A1 project values.
- [ ] No local absolute paths.
- [ ] No session state.
- [ ] No manuscript requirement.
- [ ] No specific rendering-engine requirement.
- [ ] No specific history-filtering-tool requirement.
- [ ] No container, package-snapshot, regulated-compliance, issue-tracker or commit-signing requirement.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent repository-pattern review cadence;
- approved project-specific migration contract location;
- approved parity-validation standards by project type;
- full P1 activation prerequisites.
