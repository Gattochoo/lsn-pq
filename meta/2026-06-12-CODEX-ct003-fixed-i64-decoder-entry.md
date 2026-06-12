# CODEX note: ct-003 fixed-i64 decoder entry point

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment starts implementation, not another audit-only classifier. It
adds a real fixed-buffer SCL decoder entry point:

```rust
decode_scl_fixed_i64<const N: usize, const L: usize, const CHILD_CAP: usize>
```

The function consumes the existing `PolarCode` and LLR slice, expands all
fixed path slots into a fixed child buffer, scores candidates with integer
metric deltas, and compacts through the existing fixed-schedule top-L selector.

## RED/GREEN

RED:

- Added `noiseless_fixed_i64_scl_roundtrip_recovers_info_bits`.
- The focused test failed to compile because `decode_scl_fixed_i64` did not
  exist.

GREEN:

- Added `decode_scl_fixed_i64`.
- Added bounded LLR-to-integer magnitude conversion.
- The focused test passes for `N=16`, `K=8`, `L=8`, `CHILD_CAP=16` on a
  noiseless roundtrip.

## Interpretation

This is the first ct-003 implementation hook: the fixed SCL work is now
callable as a decoder, not only as a shape-audit prototype.

Limits:

- it is not wired into default `decode_scl` or `decode_scl_fast`;
- it has not been checked against N=2048/K=256/r=7 KAT;
- it has not run BLER equivalence or high-noise negative controls;
- source still contains branches in fixed-buffer helper code;
- no generated-code, timing, cache, production constant-time, PQ, security, or
  7th-source claim is made;
- ct-inventory is intentionally not changed in this increment.

## Next Step

Extend the fixed-i64 entry point from a noiseless small roundtrip to byte-exact
comparison against the existing SCL rail on deterministic noisy small fixtures,
then scale toward the paper-r7 KAT and BLER gate before any inventory change.
