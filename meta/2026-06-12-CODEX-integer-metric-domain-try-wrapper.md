# CODEX integer metric domain try wrapper

Date: 2026-06-12

## Scope

This OFA-sized increment closes a remaining primitive-level panic surface in
the `ct-003` fixed SCL audit rail:

- `FixedSclIntegerMetricDomainCheck`
- `FixedSclIntegerMetricDeltaRun`
- `fixed_scl_integer_metric_domain_check`
- `fixed_scl_integer_metric_domain_failure_label`
- `try_fixed_scl_integer_metric_deltas`

The try wrapper validates a single public hard bit and integer magnitude before
calling `fixed_scl_integer_metric_deltas`. Invalid public inputs return terminal
sentinel deltas instead of panicking.

## Boundary

This is audit-only source scaffolding. It is not wired into `decode_scl`,
`decode_scl_fast`, or any active decoder path. The active decoder remains
`not_constant_time`.

No constant-time, production, security, PQ, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_integer_metric_domain_check_labels_single_round_inputs` failed
  because the primitive metric-domain APIs were absent.

GREEN:

- valid metric inputs map to `ok`;
- invalid hard bits map to `hard_bit`;
- negative magnitudes map to `magnitude`;
- invalid try-wrapper inputs return forbidden sentinel deltas rather than
  invoking the asserting primitive.

## Verification Target

- focused metric-domain tests;
- SCL audit JSON includes the primitive-level domain table and non-panicking
  wrapper;
- default `polar_validation` and `lsn_ref` verification before commit.
