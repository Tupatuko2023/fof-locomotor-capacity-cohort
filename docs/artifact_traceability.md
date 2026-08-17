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
