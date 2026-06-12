# CODEX integer metric domain labels

Date: 2026-06-12

## Scope

This OFA-sized increment makes the primitive integer metric-domain failure table
explicit in Rust:

- `FixedSclIntegerMetricDomainFailureLabel`
- `FIXED_SCL_INTEGER_METRIC_DOMAIN_FAILURE_LABELS`
- `fixed_scl_integer_metric_domain_failure_label`

The table mirrors the audit JSON `integer_metric_domain_failure_codes` surface
for single-round metric inputs while keeping it distinct from the schedule-level
domain label table.

## Boundary

This is audit-only source scaffolding. It does not change `decode_scl`,
`decode_scl_fast`, or any active decoder path. The active decoder remains
`not_constant_time`.

No constant-time, production, security, PQ, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_integer_metric_domain_failure_labels_cover_primitive_codes` failed
  because the primitive label table/type were absent.

GREEN:

- primitive labels cover `ok`, `hard_bit`, and `magnitude`;
- primitive label lookup returns `"unknown"` for out-of-table codes;
- existing primitive metric-domain and SCL audit tests still pass.

## Verification Target

- focused primitive label/domain tests;
- full `polar_validation` and `lsn_ref` verification before commit;
- no `paper/` edits staged.
