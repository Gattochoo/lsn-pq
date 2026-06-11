# Codex P2 Positive-Basis ISD Screen

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-next-P1b-P2.md` P2
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment adds a capped positive-basis ISD-style screen:

1. collect positive labels `(a,b=1)`;
2. first test whether the full positive span already has rank `n` and is isotropic;
3. otherwise, sample `n` distinct positive points up to `max_attempts`;
4. keep only rank-`n` isotropic spans that match a Lagrangian in the public orbit;
5. score each valid candidate by label consistency over all samples.

This is not a new structural reduction. It is a finite-size attack screen with a required sanity check:
it should recover noiseless LSN, and then we measure whether constant-rate noise still permits useful
positive-basis recovery.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: GREEN, 13 tests passing.

New tests:

- `positive_basis_isd_recovers_noiseless_secret`;
- `positive_basis_isd_trial_runner_has_noiseless_sanity`.

## Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_isd_sweep -- \
  --n-start 3 \
  --n-end 5 \
  --ratios 4.0 \
  --p-values 0.0,0.25 \
  --trials 10 \
  --max-attempts 2000 \
  --seed 3235823838 \
  --output experiments/131-codex-p2-positive-basis-isd.json
```

Raw data: `experiments/131-codex-p2-positive-basis-isd.json`.

| n | m | p | trials | max attempts | successes | success rate | avg positives | avg valid candidates | avg best score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 256 | 0.00 | 10 | 2000 | 10 | 1.00 | 30.5 | 676.9 | 256.0 |
| 3 | 256 | 0.25 | 10 | 2000 | 8 | 0.80 | 80.6 | 186.4 | 192.1 |
| 4 | 1024 | 0.00 | 10 | 2000 | 10 | 1.00 | 65.0 | 636.3 | 1024.0 |
| 4 | 1024 | 0.25 | 10 | 2000 | 4 | 0.40 | 295.1 | 21.8 | 744.2 |
| 5 | 4096 | 0.00 | 10 | 2000 | 10 | 1.00 | 131.1 | 599.5 | 4096.0 |
| 5 | 4096 | 0.25 | 10 | 2000 | 0 | 0.00 | 1080.0 | 1.4 | 2669.2 |

## Interpretation

The sanity rail passes: at `p=0`, the attack recovers all measured `n=3,4,5` instances.

At constant-rate `p=1/4`, this is not uniformly dead at tiny `n`: `n=3` and `n=4` still show finite-size
success under a 2000-attempt cap. That is expected small-case behavior and must not be reported as a
break or as REDUCES.

The scaling signal points the other way. From `n=3` to `n=5`, the average number of valid isotropic
Lagrangian candidates found within the same 2000-attempt cap drops:

```text
n=3: 186.4
n=4:  21.8
n=5:   1.4
```

At `n=5`, the capped ISD screen finds almost no valid candidates and recovers `0/10`. This is consistent
with the noise-wall picture: positive labels are dominated by false positives, so choosing a clean
secret basis from positives becomes rapidly unlikely.

Honest status:

- **BROKEN:** no;
- **REDUCES / attack success beyond capped finite-size ISD:** no;
- **small-n artifact:** yes, `n=3,4` constant-rate successes are not family evidence;
- **OPEN evidence:** unchanged; this is an attack-family screen, not a proof.

## Next Step

Run an attempt-budget scaling check at `n=5,p=1/4` before moving to BKW:

- `max_attempts` in `{2k, 10k, 50k}` if runtime permits;
- report whether success grows sublinearly, polynomially, or remains effectively absent;
- stop and raise CLOSURE-GRADE only if a stable sub-`2^(2n)` recovery trend appears beyond small `n`.
