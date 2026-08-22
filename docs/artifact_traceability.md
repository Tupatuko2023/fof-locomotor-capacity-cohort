# Public artifact registry and traceability scaffold

## Scope

The public artifact registry is a metadata-only safety scaffold. It does not
contain a manuscript inventory, participant data, protected paths, research
results, or publication decisions. The canonical registry starts empty, and
adding an entry does not approve an analysis, disclosure, or publication.

The scaffold separates three state dimensions:

- `artifact_status` describes generation and technical validation;
- `disclosure_state` describes independent disclosure review;
- `publication_status` describes independent publication approval.

An aggregate artifact is not public merely because it has been generated.

## Files and validation

The canonical files are:

- `config/artifacts/artifact_registry.json`;
- `config/artifacts/artifact_registry.schema.json`;
- `scripts/validation/validate_artifact_registry.py`.

Validate the registry from the repository root:

```sh
python scripts/validation/validate_artifact_registry.py \
  config/artifacts/artifact_registry.json
```

The validator uses only the Python standard library. It applies the schema's
required-field, type, enum, digest and path rules plus semantic checks that are
not conveniently expressed in JSON Schema, including supersession cycles,
state invariants, secret-pattern rejection and placeholder eligibility. It
fails closed and reports only an error code and metadata path, never a rejected
value.

## Artifact identity

The candidate identifier convention is:

```text
A1-<TYPE>-<ROLE>-<NN>
```

This is a naming rule only. No A1 artifact IDs or final inventory are approved
by this scaffold. Synthetic tests use the reserved `TEST-` prefix. Lifecycle
state is stored separately from identity so approval does not silently change
cross-references.

## State boundaries

Artifact status values distinguish design candidates, synthetic candidates,
synthetic validation, protected generation and protected validation. Terminal
or hold states include quarantine, supersession and withdrawal.

Disclosure and publication use separate enums. For protected or formerly
protected material, publication approval is invalid until disclosure approval
has an evidence reference and locks an exact artifact SHA-256. Publication
approval requires its own decision reference. Published bytes require a
published SHA-256.

Provisional entries cannot be publication-approved or published. Synthetic
artifacts require a synthetic disclaimer and cannot be cited as research
results.

## Protected/public boundary

Participant-level material, model frames, residuals, row-level predictions,
identifiers, credentials and protected absolute paths are forbidden in the
public registry. Protected inputs may be represented only by the abstract
classification `PROTECTED_PARTICIPANT_INPUT_REQUIRED`. A protected execution
reference must be an opaque approval identifier, not a filesystem path.

Protected generated artifacts must not declare a public candidate output path.
Their exact bytes stay in protected staging until technical validation and
independent disclosure review are complete. Any changed bytes form a new
artifact revision and require a new review chain.

## Provenance chain

For a materialized artifact, traceability is:

```text
analysis contract
  -> generator path, full Git revision and generator SHA-256
  -> abstract input classification and approved snapshot reference
  -> execution reference
  -> artifact SHA-256
  -> validation receipt
  -> disclosure decision and locked SHA-256
  -> publication decision
  -> manuscript reference
```

Design candidates may name a planned generator without pretending that an
artifact exists. Once the generator status is `EXISTS`, its repository-relative
path, full Git revision and SHA-256 are mandatory.

## Placeholder contract

The future cross-reference syntax is:

```text
{{artifact:<ARTIFACT_ID>|use=<USE_CLASS>}}
```

Allowed use classes are:

- `research_result`;
- `supplement_evidence`;
- `synthetic_demo`;
- `repository_provenance`.

Placeholder validation is opt-in until an approved manuscript exists:

```sh
python scripts/validation/validate_artifact_registry.py \
  path/to/registry.json --placeholders path/to/synthetic-placeholder-fixture.qmd
```

An unknown, inactive or malformed reference fails. A `research_result`
reference requires publication approval and, for protected material,
disclosure approval. `PUBLIC_SYNTHETIC` material can be used only for synthetic
demonstration, not as a research result.

## Synthetic contract tests

All fixture content is artificial metadata under the `TEST-` namespace. The
tests cover empty and candidate registries, synthetic validation, artificial
approval-state metadata, forbidden result fields, identifier and credential
patterns, unsafe paths, missing provenance, invalid state transitions,
supersession cycles and placeholder boundaries.

Run them with:

```sh
python -m unittest discover -s tests -p 'test_artifact_registry.py'
```

The fixtures do not encode cohort sizes, estimates, p-values, confidence
intervals or any other research-result values.

## Public synthetic QC/provenance bundle

`A1-SUPPLEMENT-QC-PROVENANCE-01` is a provisional, synthetic-only technical
bundle contract. It is not an accepted manuscript supplement or a report of
study findings. The implementation uses only the approved synthetic WIDE
control and does not transform production receipts, decision logs, modeled
cohort exports or raw `sessionInfo()` output into public artifacts.

Generate the bundle into a new or empty directory:

```sh
python scripts/demo/build_qc_provenance_bundle.py --output-dir outputs/demo/qc-provenance
```

Validate the generated directory independently:

```sh
python scripts/validation/validate_qc_provenance_bundle.py \
  outputs/demo/qc-provenance/A1-SUPPLEMENT-QC-PROVENANCE-01
```

The contract requires exactly eight files. Five bounded evidence payloads are
hashed by `payload_manifest.json`. `validation_receipt.json` binds that exact
payload-manifest digest to the validator path and validator SHA-256.
`bundle_manifest.json` then binds the exact eight-name allowlist and the hashes
of all seven other files. The canonical registry artifact SHA-256 is the
SHA-256 of the exact `bundle_manifest.json` bytes. An archive or other transfer
container has a separate transport hash and cannot replace this identity.

JSON is canonicalized as UTF-8 without BOM, LF terminated, compact, with
lexicographically sorted object keys and fixed member ordering. Timestamps are
intentionally omitted from canonical identity. The bounded runtime metadata
records a stable runtime profile and generator provenance; it does not contain
raw environment, filesystem or session dumps.

The implementation lifecycle ceiling is `SYNTHETIC_CANDIDATE`. Promotion to
`SYNTHETIC_VALIDATED` requires a separately accepted canonical revision,
artifact hash and stable validation-receipt reference. Disclosure remains
`NOT_APPLICABLE_SYNTHETIC`, publication remains `NOT_APPROVED`, and the
manuscript destination remains `NEEDS_VERIFICATION`.

## Synthetic validation promotion infrastructure

The `SYNTHETIC_CANDIDATE -> SYNTHETIC_VALIDATED` transition is a
filesystem-backed, fail-closed evidence gate. A validated registry entry must
bind an exact artifact revision and SHA-256 to a canonical promotion receipt
and receipt SHA-256. The receipt separately binds generator, synthetic
input/control, execution identity, validator, validation checks and supporting
evidence.

The common receipt schema is
`config/artifacts/synthetic_promotion_receipt.schema.json`. The filesystem
validator is `scripts/validation/validate_synthetic_promotion.py`. It supports
`SINGLE_FILE_TABLE_V1` and `QC_PROVENANCE_BUNDLE_V1` without changing the
promotion meaning between profiles. For the bundle profile, the promoted
artifact hash is the exact `bundle_manifest.json` hash; the bundle's internal
validation receipt remains supporting evidence.

The validator requires at least one explicit repository-relative
`--canonical-root` argument. Both the artifact and its promotion receipt must
be regular, non-symlink files below an approved root. This mechanism does not
approve a root by itself.

```text
CANONICAL_STORAGE_POLICY: NEEDS_OWNER_DECISION
```

No current A1 entry is promoted by the infrastructure implementation. Promotion
does not establish numerical reproduction, protected execution validation,
disclosure approval, publication approval, manuscript placement or scientific
interpretation. Synthetic validated entries remain provisional, carry the
synthetic disclaimer and keep publication status `NOT_APPROVED`.

## Decisions outside this scaffold

The following remain outside the registry implementation and require their
respective authorities:

- the final A1 manuscript artifact inventory and destinations;
- scientific meaning, estimands, interpretation, SCI-03C and cohort semantics;
- protected environment, operators and input authorization;
- disclosure thresholds, aggregate egress and retention;
- journal selection, manuscript structure and publication approval;
- any real-data-derived synthetic dataset;
- any software release, Zenodo deposit or DOI action.

The registry is a control surface for recording later decisions. It does not
make those decisions.
