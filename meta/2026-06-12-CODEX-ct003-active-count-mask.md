# CODEX note: ct-003 active count mask

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment removes the source-level `candidate.active != 0` comparison from
`FixedSclPathBuffer::active_count`.

## RED/GREEN

RED:

- Added `fixed_scl_active_count_source_uses_masked_active_bits`.
- The focused test failed on the existing `candidate.active != 0` expression.

GREEN:

- Replaced the comparison with `candidate.active & 1` summation.
- Existing active-count, child-write, compact, and fixed-i64 noisy smoke tests
  pass.

## Interpretation

This is a narrow source-level cleanup in the fixed-i64 SCL audit rail. It keeps
`active_count` as an inspection/test helper and does not change decoder
selection.

Limits:

- no generated-code, optimizer, timing, branch-predictor, or cache audit;
- remaining fixed-path comparisons still need public/secret classification;
- `decode_scl`/`decode_scl_fast` remain active non-constant-time decoders;
- N=2048 KAT/BLER gates are not run here;
- no inventory status change and no production constant-time, PQ, security, or
  7th-source claim.

## Next Step

Continue ct-003 by classifying remaining fixed-path comparisons, or add a
fixed-i64 high-noise negative control before larger-N comparison.
