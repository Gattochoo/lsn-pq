# Codex LSN Reference Toy KAT Scaffold

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 4 first slice
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This increment starts the P3 reference-implementation/KAT track with a deliberately small toy
scaffold. It is **not** a production constant-time implementation and does **not** close L2. The
goal is narrower:

- create a separate `impl/lsn_ref` Rust crate;
- wire the existing LSN finite-field sampler and polar encoder/decoder into one deterministic
  toy KEM flow;
- generate one reproducible KAT JSON file;
- include a negative control where the same public key and ciphertext are decapsulated with the
  wrong Lagrangian secret.

Raw data:

- `experiments/152-codex-lsn-ref-toy-kat.json`

Implementation:

- `impl/lsn_ref/Cargo.toml`
- `impl/lsn_ref/src/lib.rs`
- `impl/lsn_ref/src/bin/lsn_toy_kat.rs`
- `impl/lsn_ref/tests/kat_baseline.rs`

## Toy Parameters

| field | value |
|---|---:|
| symplectic half-dimension `n` | 2 |
| public sample count | 64 |
| repetition | 3 |
| polar `N` | 16 |
| polar `K` | 8 |
| public noise rate | 0 |
| decoder design `p` | 0.0343 |

The parameters are intentionally tiny so that the KAT is easy to inspect. The `n=2` setting was
chosen because a wrong-secret negative control is visible at this toy density. A first attempted
`n=4` control was too sparse: both honest and wrong secrets often induce all-zero majority blocks,
which is a useful warning for future full KEM review rather than a production conclusion.

## RED/GREEN

1. Added tests referencing `ToyKemParams` and `toy_kat_vector`; RED failed on missing exports.
2. Implemented deterministic toy keygen/encaps/decaps flow; GREEN passed roundtrip.
3. Strengthened the negative control to use the same public key and ciphertext with a wrong secret;
   RED failed on missing `toy_wrong_secret_control`.
4. Implemented the control; initial `n=4` parameters did not fail, so the test was adjusted to the
   explicit toy `n=2` regime where the control is meaningful.
5. Added JSON writer test; RED failed on missing `toy_wrong_secret_control_to_json`, then GREEN
   passed.

## Command

```bash
cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --output experiments/152-codex-lsn-ref-toy-kat.json
```

## Result

Key fields from `experiments/152-codex-lsn-ref-toy-kat.json`:

```text
roundtrip_ok = true
wrong_secret_roundtrip_ok = false
encapsulated_key_hex =
  4292a13cfbbbffce0aa2e08bd03bd8b7accc004ab02b19e8ca018215c63335e0
wrong_secret_decapsulated_key_hex =
  3c1e9bcebbf8a947c8b655ea4ce7a5b06817429b83e2743a7f74c83a02eb4793
```

The JSON also records all seeds, public points, public labels, selected indices, message bits,
ciphertext syndrome bits, decoded bits, and both honest/wrong-secret Lagrangian point sets.

## Adjudication

- **KAT scaffold:** yes, for a toy reference flow.
- **Negative control:** yes, wrong secret on the same public key/ciphertext gives a different key.
- **Production constant-time implementation:** no.
- **Full LSN-KEM implementation:** no.
- **Security claim:** none.
- **Paper edit:** none.

## Next P3 Step

The next bounded step should be either:

1. replace toy hashing/PRG scaffolding with named, auditable interfaces while keeping deterministic
   KAT output; or
2. lift from `n=2` toy KAT to a still-small but less degenerate parameter set after deciding how the
   sparse membership-majority issue should be handled in the reference KEM model.

Do not describe this increment as closing L2. It only creates a reproducible starting point for the
reference/KAT track.
