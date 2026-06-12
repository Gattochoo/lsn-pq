# CODEX ct-003: fixed-i64 decoder reuses scratch buffers across public rounds

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

`decode_scl_fixed_i64` now allocates its integer LLR and partial-sum scratch arrays once per decoder invocation, before the public `phi` loop, and reuses those fixed-size arrays across public bit rounds. The recursion remains integer-only after the initial channel quantization, and this step preserves the existing fixed child expansion and expand-then-compact prototype shape.

## RED/GREEN

- RED: added `fixed_i64_decoder_reuses_scratch_buffers_across_public_rounds`, which failed while the scratch arrays were declared inside the public `phi` loop.
- GREEN: moved `llr_scratch` and `partial_scratch` declarations before the `for phi in 0..N` loop.

## Adjudication

This is still an implementation/audit rail only. It does not make a production constant-time, security, PQ, or 7th-source claim. The active decoder remains marked `not_constant_time` until a full data-oblivious schedule, memory-access review, and platform-level timing story exist.
