# Claude adjudication — batch 2 (rework): fixes ACCEPT; 90/89 data re-read — δ∝m·2^{−n} observation + public-vs-secret-B model split

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** `eb2de58` (paper+C1), `2aa8f90` (89), `a58e58a` (90).
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 1. ACCEPT — the two text fixes (verbatim per my replacement wording)
- lem:enrichment-sq closing sentence ✓ (model conflation gone). C1 pin ✓ (finite-field caveat +
  motivation-only sentence; line-40/42 contradiction resolved).

## 2. Experiment 90 (sub-floor n=5) — design ✓, but the data say MORE than the header reads

Re-derived from the run (baseline 2^{−5} = 0.03125, χ²/sample = κ2^{−n} = 1/24):

```text
 m   fresh-mean  δ = fresh/base − 1   m·χ²    δ/(m·χ²)
  8    0.0410        0.31             0.33      0.94
 12    0.0424        0.36             0.50      0.71
 16    0.0467        0.49             0.67      0.74
 20    0.0494        0.58             0.83      0.70
 24    0.0546        0.75             1.00      0.75
```

**Fresh-point enrichment is NOT ≈ baseline** (the script's interpretation line mis-predicts its
own data); it grows ≈ linearly with m at rate δ ≈ (0.7–0.9)·m·κ·2^{−n}. That is exactly the
**hardness-consistent scaling**: δ = Ω(1) requires m = Ω(2^n); at KEM parameters (n=65,
m=22528): δ ≈ 2^{−50} — negligible. And pair_fresh ≤ fresh at every m (pair heuristic adds
nothing — confirmed in the proper regime now). **Required next:** (i) state the δ ∝ m·2^{−n}
observation explicitly with the fit; (ii) n-scaling check (n=4 vs n=5 at matched m·2^{−n}) before
any paper sentence; (iii) fix the interpretation lines in the script header/footer to match the
data. Graph-Lagrangian prior restriction: note it (43% of all Lagrangians) — acceptable for the probe.

## 3. Experiment 89 (A3b redesign) — family fixed ✓; one wart + one genuine model insight

- **Wart:** A's columns appear to be sampled from L without a basis guarantee — avg rank(BA)
  ≈ 4.49 < 5 at q=1 traces back to rank-deficient A (random 5 vectors from a 2^5-point
  Lagrangian are a basis w.p. ≈ 0.30). Use a random BASIS of L; rerun. Degenerate instances
  pollute every column of the table.
- **★ Model insight (from the q=1 endpoint):** at q=1, B is usually full-rank ⇒ the transport
  theorem catches every REALIZATION (minR(E) → 0.5 ≈ Gram ≡ 0) — while the MARGINAL output BA
  is uniform. No contradiction: the detector needs B. Hence **A3b must be split by B-visibility**:
  - **Public-B model** (reduction's matrix is known): per-realization transport applies at ALL q
    — the random-B escape does not exist here; residual = mid-rank strip only.
  - **Secret-B model** (only the marginal output matters — this is LPQR/D.2's model per the
    pinned quantifier): matrix part can be uniformized, the open bridge is the label-signal vs
    BA-uniformity trade-off. minR(E) is NOT a viability metric here; closeness-of-marginal +
    label-signal-given-BA are.
  The coverage chart should label each row with its model. This materially sharpens the A3b
  target: the bridge question lives ONLY in the secret-B model.
- "Trade-off" language remains premature at n=5 (bias falls only 0.14→0.05 — piling-up is a
  constant-factor effect at small n). Keep as shape-check data.

## 4. Action list (next pass)
1. 89: random-basis A fix + rerun; relabel metrics by model (public-B vs secret-B); chart row labels.
2. 90: δ∝m·2^{−n} fit + n-scaling; fix script interpretation lines.
3. A3b lemma #1 (Krawtchouk affine-coset bias) — unchanged, still the right next theorem target.
4. Coverage sentence in the paper for the D.2-quantifier + model-split yields (one paragraph, after 1–2).

No 7th; no break; no security claim. OPEN = LSN.
