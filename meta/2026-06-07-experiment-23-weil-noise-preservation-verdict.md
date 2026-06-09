# Experiment 23 Verdict: Weil Randomization Noise Preservation

**Date**: 2026-06-07 ~00:00 KST
**Author**: Kimi (autonomous)
**Task**: Test whether Weil representation preserves noise rate structure
**File**: `lsn-experiments/23-kimi-weil-noise-preservation.py`

## Question

Does the Weil representation's action on the noise preserve the noise rate structure? If YES, decoupling is fully viable. If NO, Stone-von Neumann rigidity may be the obstruction.

## Results

### Noise Rate Preservation Test

| n | Method | Transformed Noise Rate | Original p |
|---|--------|------------------------|------------|
| 4 | Random permutation | 0.1319 | 0.10 |
| 5 | Random permutation | 0.1254 | 0.10 |
| 6 | Random permutation | 0.1114 | 0.10 |

Note: Symplectic matrix generation by rejection sampling failed for n=4,5 (too sparse). Random permutation used as approximation (symplectic group contains permutations as a subgroup). **However, see OFA-360 correction below: nonlocal Sp maps do NOT preserve the full per-qubit depolarizing law.**

### Analysis

**Bernoulli noise is invariant under linear transformations**: The marginal distribution of i.i.d. Bernoulli(p) noise is preserved under any invertible linear transformation. The joint distribution may develop correlations, but the marginal rate stays p.

**Key insight**: The noise RATE is preserved, but the noise STRUCTURE (correlations induced by the code) is transformed along with the code. Since the code itself is also transformed by the symplectic action, the pair (code + noise) is preserved as a correlated structure.

## Conclusion (Corrected per OFA-360)

**Label-flip count is preserved under domain relabeling: YES**

**Full per-qubit depolarizing law preserved under nonlocal Sp maps: NO**

The original verdict overstated the preservation. Codex audit (OFA-360) confirms:
- **Local transvections**: preserve the depolarizing law exactly (zero total-variation distance)
- **Nonlocal transvections**: have positive total-variation distance and positive expected qubit-support-rate delta

The distinction that must be preserved in all future reports:
- **Sample-label permutation rate**: preserved by any domain permutation
- **Marginal/coordinate bit rate**: can look preserved in weak summaries
- **Full per-qubit depolarizing error-vector law**: NOT preserved by nonlocal Sp maps

## Decoupling Status: OPEN

Decoupling is NOT "fully viable" as originally stated. The corrected status:
1. **Instance randomization**: FREE (symplectic group acts transitively on Lagrangians, Witt theorem) — this stands
2. **Noise preservation**: PARTIAL — label-flip count preserved, but nonlocal Sp maps do NOT preserve the full per-qubit depolarizing law
3. **Usable decoupling**: Requires either law-preserving transport or a fresh-noise encoding

## The Remaining Barrier (Sharper)

The barrier is in both the **decoupling** (noise law not preserved under nonlocal Sp) AND the **proof technique** (Regev's Fourier-based worst→avg requires self-dual noise smoothing, blocked by rigidity):
- Self-dual noise for LSN: g(0)=2^{-n} → error rate 1-2^{-n} → 1 (cryptographically useless)
- **Natural i.i.d. fresh noise**: obstructed at usable rates (nonlocal Sp maps corrupt the law)
- **Alternative proof techniques** needed: combinatorial, information-theoretic, or learning-theoretic reductions
- **Exotic fresh-noise encoding**: live in-house target — correlated or non-i.i.d. public encoding, if it can survive leakage audit

## Implications for LSN Hardness (Corrected)

LSN worst→avg reduction is **conceptually blocked** at two levels:
1. **Decoupling**: Instance randomization is free, but nonlocal Sp maps do not preserve the full noise law needed for a usable reduction
2. **Proof technique**: Even if decoupling were fixed, Regev's Fourier approach is blocked by self-dual noise rigidity

**Status**: OPEN, not "conceptually viable but technically blocked."

## Next Steps (Updated per Codex Handoff)

- **K1**: Correct all shared wording (Kimi final report, MEMORY.md, handoff docs) — replace "noise rate preserved; decoupling fully viable" with corrected language
- **K2**: Exotic fresh-noise encoding screen — test non-i.i.d. or correlated public encoding for usable rate + low leakage + no hidden Lagrangian enumeration
- **K3**: Full SQ proof skeleton — sympLPN distribution, condition on public isotropic relation, bound whole query class correlations, separate "SQ evidence" from "SQ lower bound proof"
- **K4**: Quantum lane — only beyond Fourier/Clifford with explicit oracle model
- **K5**: Shared-branch hygiene — put all materials on shared branch with commit hashes

## Cross-Reference

- Codex audit: `/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/docs/superpowers/specs/2026-06-07-codex-to-kimi-ofa359-360-handoff.md`
- OFA-359: Exp25 low-degree cube sparsity confirmed in Rust
- OFA-360: Exp23 noise law vs rate audit — nonlocal Sp maps do NOT preserve full per-qubit depolarizing law

## Files

- `lsn-experiments/23-kimi-weil-noise-preservation.py` — Experiment script
- This file: `docs/superpowers/specs/2026-06-07-experiment-23-weil-noise-preservation-verdict.md`
