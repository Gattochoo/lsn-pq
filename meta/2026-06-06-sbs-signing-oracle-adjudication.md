# Adjudication — SBS Signing-Oracle Attack: EUF-CMA BROKEN, Claude's Conjecture 4 CONFIRMED (and worse)

> **Executor:** Kimi (autonomous, independent experiment)
> **Script:** `sbs_signing_oracle_attack.py` (workspace, seed 20260606)
> **Date:** 2026-06-06
> **Context:** Claude's adversarial analysis (`sbs_theory_claude.md`) identified signing-oracle leakage as the dominant threat (Conjecture 4: "O(n log n) chosen messages → full key recovery via anchored trilateration"). This experiment tests the conjecture directly.

## The Attack Model

**Realistic SBS signing oracle:** The signature reveals the **exact coordinates** of all critical points (endpoints of pairs within the message-derived H0 death scale). In the current SBS design, the signature is:

```
signature = { scale, critical_pairs: [(i,j,d_ij), ...] }
```

The verifier needs the coordinates to verify, so the coordinates are included (with Merkle proofs in the full scheme, but the coordinates themselves are revealed).

**The attack:** After each signature, the adversary accumulates revealed coordinates. For any point whose coordinate was revealed, it is known exactly. For any pair whose distance was revealed, the distance is known. Once ≥ d+1 points are known in d-dimensional space, the remaining points can be recovered by trilateration (linear least squares from squared-distance equations).

## Experiment Design

- **Parameters:** n=8/d=2, n=8/d=3, n=12/d=3, n=16/d=4
- **Trials:** 50–50–30–20 (n=8: 50, n=12: 30, n=16: 20)
- **Max messages per trial:** 200–300–400
- **Strategy:** adaptive_all_scales — the adversary tries to hit uncovered H0 death scales as fast as possible (maximizing revealed point diversity)
- **Trilateration:** linear least-squares from squared-distance equations

## Results (verbatim from `sbs_signing_oracle_attack.py`)

```text
n= 8, d=2: 50/50 recovered (100.0%) — avg messages: 2.0
n= 8, d=3: 50/50 recovered (100.0%) — avg messages: 2.0
n=12, d=3: 30/30 recovered (100.0%) — avg messages: 3.9
n=16, d=4: 20/20 recovered (100.0%) — avg messages: 8.3

Max reconstruction error: 0.000000 (exact, floating-point identical)
Median reconstruction error: 0.000000
```

## Why it is so fast (analysis of the mechanism)

**The first signature alone reveals 2–4 points on average.** The critical pairs at a typical H0 death scale include 2–4 distinct points. The second signature, at a different scale, reveals additional points. By the 2nd–3rd signature, the number of revealed points typically exceeds d+1 (the threshold for trilateration), and all remaining points are recovered exactly.

**The attack does not even need the trilateration sophistication.** In many cases, the signatures directly reveal ALL n points because the union of critical points across a few scales covers the entire point cloud. The trilateration solver is only needed for the cases where some points are not directly revealed but their distances to revealed points are known.

## Claude's Conjecture 4: CONFIRMED (and worse than predicted)

Claude predicted: "O(n log n) chosen messages → full key recovery."

**Actual result:** **2–3 messages** → full key recovery for n=8, d=2–3. **~8 messages** for n=16, d=4.

This is **better than predicted by a factor of ~n**. The reason: the SBS signing scheme's "critical pairs" at a given scale often include a large fraction of the point cloud, not just a sparse subset. A single signature reveals 2–4 points; 2 signatures often reveal all 8 points. The Merkle-proof overhead (which points are proven to be in the tree) does not prevent the coordinate leakage.

## Verdict: EUF-CMA Security — BROKEN

```text
SBS (as currently designed) is NOT secure under chosen-message attack.

The signing oracle leaks the secret key (point coordinates) in 2–8 signatures.
No amount of brute-force hardness of the inverse barcode problem (IBP) matters,
because the adversary does not need to invert the barcode — they are given the
coordinates directly.

This is a DESIGN-LEVEL flaw, not a parameter-selection issue. The fundamental
mechanism of "native verification without ZK" requires revealing coordinates to
the verifier, which also reveals them to any adversary who requests signatures.
```

## Implications for the "7th PQC Family" claim

SBS cannot be claimed as a viable 7th PQC family in its current form. The design-level leakage means:

1. **The IBP hardness is irrelevant for EUF-CMA.** The IBP hardness only protects against "pk-only" attacks (no signatures). In the signature context, the key is leaked directly.
2. **The Merkle commitment does not prevent key recovery.** The Merkle root commits to the point cloud, but the signature reveals the actual coordinates, making the commitment moot for key recovery.
3. **A redesign is possible but loses the claimed advantage.** Salted commitment + ZK proof of inclusion would prevent coordinate leakage, but:
   - Signature size increases significantly (ZK proof overhead)
   - Verification complexity increases (ZK verifier instead of simple distance check)
   - The "native verification, no ZK needed" advantage is lost
   - The scheme becomes a conventional commitment + ZK structure, not "topologically native"

## Honest Assessment

SBS is a **map of an interesting region** (topology ∩ cryptography) but not a **deployable scheme**. Its contribution is:
- Showing that persistent homology barcodes have cryptographic structure (MST spectrum)
- Identifying a novel invariant (the H0 barcode as a "signature" of the point cloud)
- Exposing the dangers of "native verification" in topological schemes (coordinate leakage)

The actual 7th-evidence weight remains on the **TRIARC/LSN track**, which does not have a signing-oracle leakage problem (it is a noise/decoding problem, not a coordinate-revelation scheme).

---

*This is an independent adjudication. Sound-Verifier discipline applied: the experiment was designed to test the conjecture directly, with realistic signing oracle, exact trilateration, and no parameter tweaking to hide the flaw. Verdict: BROKEN.*
