# K50 WIDE structural synthetic fixture

`k50_wide_structural_fixture.csv` is a wholly synthetic fixture for structural,
integrity, fail-closed and rendering tests. It is not participant-derived and
must not be used for numerical, distributional, clinical or scientific claims.

The `FI22_nonperformance_KAAOS` values `3, 1, 4, 2` are deterministic test
sentinels only. They do not represent the real FI22 distribution, scale,
cut-off, direction, clinical meaning or a scientifically approved analysis
result. Their only purpose is to exercise the optional `--fi22 on` sensitivity
branch without adding a scientific interpretation.

The fixture is bound to `k50_wide_authoritative_test_control.lock`. Any byte
change requires corresponding MD5 and SHA-256 updates and must retain the
`synthetic_wide_test_control` role and `SYN-K50-WIDE-` snapshot namespace.

Synthetic execution must use `--synthetic-wide-test-control` together with an
explicit empty `--synthetic-output-dir`. It must never select a production
input, production lock or the canonical local K50 output directory.
