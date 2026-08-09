# FARO1 Research Repository Patterns

## 1. Document Metadata

```yaml
title: FARO1 Research Repository Patterns
document_id: FARO1-RESEARCH-REPOSITORY-PATTERNS
version: 0.2.0
status: approved
priority: P1
scope: Reusable research-repository architecture, reproducibility, code-migration and cross-repository evidence-intake patterns for FARO1-orchestrated research software work
steward: FARO1 Knowledge Steward
review_authority: User / designated project owner
effective_date: null
review_date_or_cadence: NEEDS_VERIFICATION
document_evidence_state: validated
primary_responsibility: Define reusable research-repository architecture, reproducibility, code-migration and evidence-intake patterns without defining project-specific repository state or execution authorization.
load_condition: task-conditional
authority_level: reference
activation_rule: Load for repository architecture, reproducibility-pattern or research-code migration-pattern questions. This reference does not authorize execution.
```

## 2. Primary Responsibility

This document defines reusable research-repository architecture, reproducibility, code-migration and cross-repository evidence-intake patterns for FARO1.

It does not define active project state, project-specific repository values, project-specific migration decisions, tool authorization, privacy classifications, evidence PASS/FAIL procedure, publication authorization, lifecycle governance, project context structure or project specification structure.

## 3. Scope

This reference applies when FARO1 needs reusable patterns for:

- research repository organization;
- reproducible analysis structure;
- source-to-target analysis-code migration planning;
- cross-repository evidence intake planning;
- artifact disposition during migration;
- dependency closure;
- provenance preservation;
- source pinning;
- upstream authority preservation;
- validation-state preservation;
- publication-safe artifact intake;
- partial readiness and independent blocker handling;
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
- Separate code migration from evidence intake.
- Separate portability changes from scientific or analytical changes.
- Preserve upstream scientific and technical authority unless a separate approved review changes it.
- Preserve partial validation states without flattening them to a single success flag.
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

This document does not require every research repository to be a manuscript repository, Quarto project, package, pipeline or compendium. It defines reusable architecture patterns and selection criteria. An approved project specification selects which patterns apply.

## 7. Reproducibility Patterns

Reusable reproducibility patterns include:

- documented execution entry points;
- deterministic script order where order matters;
- explicit local code dependencies;
- environment or dependency manifests appropriate to the project;
- synthetic fixtures for structural tests;
- generated-output regeneration instructions;
- provenance records for imported code or generated artifacts;
- provenance records for imported evidence when evidence is consumed without migrating code;
- explicit source versions or immutable references for upstream evidence;
- preservation of unresolved upstream validation states;
- validation commands appropriate to the repository pattern;
- clear separation of source logic, generated artifacts and protected data.

This document does not require a specific runtime manager, rendering engine, container system, package repository, continuous-integration provider or compliance framework. Those choices belong to project-specific requirements.

## 8. Cross-Repository Code Migration Pattern

The generic safe cross-repository research-code migration pipeline is:

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

Code migration moves or reconstructs code and its required dependencies. It may require portability adaptation and parity validation. Code migration must not be used as a shortcut for adopting upstream evidence, publication claims or scientific interpretation without the applicable evidence and scientific review.

## 9. Cross-Repository Evidence Intake Pattern

Cross-repository evidence intake is distinct from code migration.

Evidence intake applies when a target project consumes upstream authority, provenance, validation state or an evidence artifact while upstream implementation code, protected data or generated participant-level artifacts may remain in the upstream repository or controlled environment.

The generic evidence-intake pipeline is:

```text
IDENTIFY UPSTREAM AUTHORITY
  -> VERIFY SOURCE REPOSITORY OR SOURCE LOCATION
  -> PIN SOURCE COMMIT, VERSION OR IMMUTABLE REFERENCE
  -> IDENTIFY EVIDENCE ARTIFACT OR EVIDENCE REFERENCE
  -> PRESERVE UPSTREAM VALIDATION STATE
  -> DEFINE DOWNSTREAM CONSUMPTION CONTRACT
  -> REGISTER UNRESOLVED BLOCKERS
  -> CONNECT DOWNSTREAM CLAIMS OR RESULTS
  -> REVIEW + VALIDATION
```

Evidence intake must not silently transfer scientific or technical authority to the downstream repository. The downstream repository may consume an upstream contract, but it does not become the owner of upstream derivation, schema, construct validity or scientific interpretation unless an explicit approved authority change says so.

Evidence intake may be implemented with a registry, manifest, decision record, provenance note, specification section or another project-selected structure. This document does not require `source_registry.yaml`, `claim_registry.csv` or any universal evidence-intake filename.

## 10. Source-of-Truth and Authority Chain Pattern

Cross-repository work should preserve the authority chain behind code, evidence and claims.

| Authority layer | Owns |
|---|---|
| `Scientific Authority` | Interpretation, scientific role, analysis intent and construct meaning |
| `Technical Authority` | Derivation, schema, implementation provenance and producer behavior |
| `Downstream Consumption Contract` | How upstream evidence or code is consumed in the target repository |
| `Publication/Analysis Claim` | The downstream statement, result, table, figure or manuscript claim and its traceability |

Downstream consumption must not silently redefine upstream scientific authority or technical authority. If a downstream project needs to reinterpret, rederive, repair or replace upstream science, that is a separate scientific or analytical decision, not a portability or intake step.

## 11. Source Pinning Pattern

Evidence intake and code migration should pin the source sufficiently for review and reproducibility.

Minimum source-pinning evidence should include:

- repository identity or source-location identity;
- pinned commit, immutable version, release, archive digest or equivalent immutable reference;
- source path, evidence artifact or evidence reference;
- upstream authority role;
- downstream consumption role;
- validation state and unresolved validation categories;
- date or review context when relevant.

The implementation format is project-specific. A registry is one possible implementation pattern, not a universal requirement.

## 12. Evidence Status Preservation Pattern

Imported or consumed upstream evidence must retain its upstream validation taxonomy and unresolved states unless a separately reviewed downstream evidence review justifies a status change.

Do not flatten mixed validation states such as:

```text
code validation: PASS
reproducibility validation: PASS
criterion validation: NEEDS_VERIFICATION
predictive validation: NEEDS_VERIFICATION
```

into:

```text
validated: true
```

When evidence is partially validated, the target project should preserve the validated classes, unresolved classes, authority that produced them and downstream scope affected by each unresolved state.

## 13. Publication-Safe Artifact Intake Pattern

Publication-safe artifact intake is distinct from code migration and evidence intake.

Artifact intake should distinguish:

| Artifact type | Default handling |
|---|---|
| `publication_safe_aggregate` | Candidate for intake after provenance, privacy and claim-traceability review |
| `publication_safe_table_or_figure` | Candidate for intake when aggregate safety and claim linkage are established |
| `participant_level_artifact` | Stop and route to `SAFETY_PRIVACY_GUARDRAILS.md` |
| `generated_intermediate_artifact` | Prefer regeneration or reference-only handling unless explicitly approved |
| `unknown_artifact` | Mark `NEEDS_VERIFICATION` and stop affected path |

Publication-safe artifact intake does not imply permission to import participant-level data, generated participant-level derivatives or protected runtime inputs.

## 14. Partial Readiness and Independent Blocker Pattern

Research projects may contain independent contracts with different readiness states.

Example readiness shape:

```text
Contract A: READY
Contract B: BLOCKED
Project: PARTIALLY_READY
```

One upstream contract becoming ready must not mark the whole project, analysis, publication or migration as ready. Readiness should be scoped to the affected contract, artifact, analysis branch or claim.

This pattern supports targeted-stop behavior: an unresolved blocker stops the affected scope while independent, non-conflicting work may continue under its own authorization.

## 15. Artifact Classification Taxonomy

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

## 16. Dependency Closure Pattern

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

Evidence dependency closure should identify the upstream authority, pinned source, evidence artifact or reference, downstream consumption point, downstream claim or result, unresolved validation states and any protected-data boundary that prevents direct artifact movement.

## 17. Privacy and Provenance Pattern

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

For evidence intake, provenance should also preserve upstream authority role, source pinning, upstream validation taxonomy, downstream consumption contract and unresolved blockers. Privacy decisions remain owned by `SAFETY_PRIVACY_GUARDRAILS.md`.

## 18. Migration Strategy Selection

Migration strategy options include:

| Strategy | Use when | Key requirements |
|---|---|---|
| `history_preserving` | A bounded source subtree or file set has important authorship or historical provenance | Isolated plan, history-risk review, tool verification and explicit Git authorization |
| `provenance_preserving_copy` | A small set of artifacts can be copied with adequate source-grounded provenance | Provenance evidence, diff review, dependency closure and validation |
| `reconstruction` | Legacy code cannot be safely or portably migrated as-is | Explicit reconstruction scope, source references, parity or equivalence validation |

Tools such as history-filtering utilities may be examples for `history_preserving` extraction, but no tool is universally required by this document. Tool existence, version, capability, safety and suitability must be verified under `TOOL_AND_AGENT_POLICY.md` before use.

History rewrite, force-push, publication and external exposure remain hard-gated actions and require explicit authorization.

## 19. Portability vs Scientific Change Boundary

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

Evidence intake also does not authorize scientific or analytical change. Adopting, referencing or pinning upstream evidence must not reinterpret constructs, alter variable meaning, change model roles, revise claim wording or promote partial validation to full readiness without a separate approved review.

## 20. Validation and Parity Pattern

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

## 21. Rollback and Recovery Pattern

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

Evidence intake rollback or rejection may include removing a downstream reference, reverting a consumption contract, marking a claim unsupported, preserving an upstream blocker or rejecting an evidence artifact while leaving unrelated project state unchanged.

## 22. Explicit Exclusions

This reference does not make the following generic requirements:

- manuscript files in the target repository;
- manuscript repository status;
- Quarto projects;
- any specific rendering engine;
- any specific render configuration;
- any specific computational-freeze setting;
- source registries;
- claim registries;
- provenance manifests;
- containers;
- any specific package-manager repository or snapshot service;
- any specific history-filtering tool;
- `git-filter-repo`;
- regulated-compliance frameworks as automatic obligations;
- issue tracker or DevOps workflow;
- commit signing for every project;
- project-specific source or target repository identity;
- project-specific migration strategy;
- project-specific validation thresholds;
- publication, push, release or activation.

These may be project-selected implementations when required by an approved project specification or other applicable authority.

## 23. Decision Matrix

| Situation | Recommended pattern |
|---|---|
| A few independent scripts and history is not material | `provenance_preserving_copy` |
| Bounded source subproject and historical provenance is material | `history_preserving` extraction |
| Legacy code is not safely portable as-is | `reconstruction` plus parity validation |
| Upstream evidence is consumed without moving upstream code | Cross-repository evidence intake |
| Upstream validation state is mixed | Preserve validation taxonomy and unresolved states |
| One contract is ready and another is blocked | Partial readiness and targeted-stop handling |
| Publication-safe aggregate is needed | Publication-safe artifact intake after provenance and privacy review |
| Participant-level artifact is needed | Stop and apply `SAFETY_PRIVACY_GUARDRAILS.md` |
| Dependency closure is unclear | Stop and mark `NEEDS_VERIFICATION` |
| Data classification is unclear | Stop and apply `SAFETY_PRIVACY_GUARDRAILS.md` |
| Scientific logic changes | Separate analytical-change work package |
| Source provenance is unclear | Stop affected migration path |
| External publication or remote update is needed | External-action hard gate |

The matrix recommends patterns only. It does not authorize execution.

## 24. Dependencies and References

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

## 25. Validation Checklist

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
- [ ] Cross-repository code migration is distinct from evidence intake.
- [ ] Cross-repository evidence intake pattern is complete.
- [ ] Upstream scientific and technical authority are preserved.
- [ ] Source pinning does not require one registry format.
- [ ] Upstream validation states are preserved without flattening.
- [ ] Partial readiness and independent blockers are supported.
- [ ] Publication-safe artifact intake is distinct from participant-level artifact handling.
- [ ] Artifact taxonomy is a migration disposition taxonomy, not a privacy classification system.
- [ ] Dependency closure is required without mandating one implementation-specific data structure.
- [ ] Provenance requirements are source-grounded without requiring one file format.
- [ ] Migration strategy options are patterns, not automatic choices.
- [ ] Scientific and analytical changes are explicitly separated from portability changes.
- [ ] Evidence intake does not authorize scientific or analytical change.
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
- [ ] No source registry requirement.
- [ ] No claim registry requirement.
- [ ] No provenance manifest requirement.
- [ ] No specific rendering-engine requirement.
- [ ] No specific history-filtering-tool requirement.
- [ ] No `git-filter-repo` requirement.
- [ ] No container, package-snapshot, regulated-compliance, issue-tracker or commit-signing requirement.
- [ ] No secrets or participant data.
- [ ] No circular normative dependency.
- [ ] No Change History section.

`NEEDS_VERIFICATION` items:

- permanent repository-pattern review cadence;
- approved project-specific migration contract location;
- approved parity-validation standards by project type;
- full P1 activation prerequisites.
