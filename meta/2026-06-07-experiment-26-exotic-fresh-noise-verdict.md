# Experiment 26: Exotic Fresh-Noise Encoding Verdict — K2 DEAD

**Date**: 2026-06-07 22:31 KST
**Status**: **DEAD** — Exotic fresh-noise encoding does NOT preserve LPN-like hardness for LSN decoupling.
**File**: `lsn-experiments/26-kimi-exotic-fresh-noise-encoding.py`

---

## Objective

Screen K2 from the Codex handoff (OFA-359/360): Can non-i.i.d. or correlated public fresh-noise encoding provide a viable route for LSN decoupling?

**Required checks** (from Codex handoff):
1. **Usable noise**: Effective rate remains in cryptographic range, not near q→1/2
2. **Low leakage**: Low-weight TV leaks not visible at usable q
3. **Public/poly**: No hidden Lagrangian enumeration, no per-instance advice
4. **LPN-only hard step**: Any remaining hard step is explicitly ordinary LPN-style

**Three exotic encodings tested**:
- `correlated_pairs`: Adjacent pairs correlated via PRG
- `subset_sum`: Noise = XOR of random subset of public vectors
- `block_correlated`: Block-level shared noise component

---

## Results

### Noise Rate: PASS (All Encodings)

| Encoding | n=4, m=64 | n=5, m=125 | Usable? |
|----------|-----------|------------|---------|
| correlated_pairs | 0.319 ± 0.032 | 0.344 ± 0.044 | ✓ |
| subset_sum | 0.088 ± 0.175 | 0.088 ± 0.176 | ✓ |
| block_correlated | 0.084 ± 0.079 | 0.115 ± 0.097 | ✓ |

All encodings produce rates well below 0.5 (not near q→1/2). **Check 1 passes**.

### Hardness Preservation: FAIL (All Encodings)

**Simple decoder**: Correlation-based direction finder. For each coordinate direction, computes the difference in observed indicator rate between samples with dot=0 and dot=1. Picks the direction with maximum score.

| Encoding | Success Rate | Death? |
|----------|-------------|--------|
| correlated_pairs | **60%** (6/10) | ✗ FAIL |
| subset_sum | **80%** (8/10) | ✗ FAIL |
| block_correlated | **80%** (8/10) | ✗ FAIL |

A simple statistical decoder succeeds **60-80% of the time** against all exotic encodings. **Check 4 fails** — the exotic noise structure does NOT preserve LPN-like hardness; it actively helps the decoder.

---

## Death Mechanism: Exotic Structure Leakage

The exotic noise encodings introduce **publicly known correlations** that the decoder can exploit:

1. **Correlated pairs**: The pattern of which samples are correlated is public (deterministic from seed). The decoder can exploit the fact that certain pairs share noise components, increasing effective SNR for those pairs.

2. **Subset-sum**: The public vectors are known, and the subset selection is deterministic. The XOR structure creates algebraic dependencies that a simple correlation test can detect.

3. **Block-correlated**: Block boundaries are public, and samples within a block share noise. This creates a "super-sample" effect where the block-level component averages out sample noise.

**Root cause**: Public determinism + correlation structure = decoder knows where to look for signal. The exotic noise introduces **structure** that is orthogonal to the LSN structure, but the decoder can use standard statistical methods to detect the LSN signal *because* the noise structure is known and can be partially averaged out.

---

## Implications for K2

**Exotic fresh-noise encoding is NOT viable for LSN decoupling.**

The problem is fundamental: any public encoding of noise that introduces correlation structure will have that structure known to the decoder. The decoder can then use this knowledge to increase effective SNR. Private correlation (unknown to decoder) would help, but that requires hidden randomness, which defeats the purpose of public encoding.

**This is different from the i.i.d. noise case**: With i.i.d. Bernoulli noise, the decoder has no structural information about the noise and must fight pure randomness. With exotic noise, the decoder knows the noise structure and can exploit it.

---

## Open Question Status Update

### K2: Exotic Fresh-Noise Encoding → **CLOSED (DEAD)**

No viable exotic noise encoding found. All tested variants introduce structure that helps the decoder.

### Remaining Open Questions (from Codex handoff)

| Question | Status | Notes |
|----------|--------|-------|
| K1: Non-Fourier worst→avg | **OPEN** | Still highest priority |
| K2: Exotic fresh-noise | **DEAD** | This experiment |
| K3: Full SQ proof skeleton | **OPEN** | Requires theoretical work |
| K4: Quantum lane | **OPEN** | Only non-Clifford/period-finding |
| K5: Shared-branch hygiene | **OPEN** | Git work |

---

## Next Steps

1. **K1 remains the critical path**: Non-Fourier worst→average reduction for LSN. Theoretical approaches: combinatorial reduction, information-theoretic bounds, learning-theoretic lower bounds.

2. **K3 (SQ proof)**: Consider whether the exotic noise failure suggests a general principle: **any public noise structure is exploitable**. This might inform the SQ proof — the hardness of LSN may rely on the noise being *private* and *structureless*.

3. **No further exotic noise experiments needed**: The failure is structural and general. Moving to K1/K3 is the priority.

---

## Cross-Reference

- `docs/superpowers/specs/2026-06-07-kimi-to-codex-handoff.md` — Codex handoff (K2 origin)
- `docs/superpowers/specs/2026-06-07-experiment-23-weil-noise-preservation-verdict.md` — Weil noise (different failure mode)
- `lsn-experiments/26-kimi-exotic-fresh-noise-encoding.py` — This experiment script

---

*Verdict: K2 is dead. The exotic noise route is blocked by public structure leakage. Return to K1 (non-Fourier worst→avg) and K3 (SQ proof skeleton).*