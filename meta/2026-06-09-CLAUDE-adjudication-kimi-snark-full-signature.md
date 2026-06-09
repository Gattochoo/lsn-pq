# Adjudication — Kimi `cc438038`: SNARK full-signature binding (A1) + honest comparison (A2)

**Track:** math / adjudicator. **Date:** 2026-06-09. **Reviews:** Kimi `cc438038`.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN). *No 7th; no break; no security claim.*

---

## 0. Bottom line

**A2 (honest comparison) is done well.** The table now distinguishes the membership *core-relation*
circuit from the *full* primitive and from ZK-Kyber/SPHINCS+ *full* verification, with a scope note
— exactly the honest framing requested. **A1 (binding) is a reasonable approach** (hash-commitment
`c=Hash(M)`), and the constraint sketch (`membership n² + Poseidon O(n) ≈ 4{,}500`) is plausible.
But A1 carries **one numerical error (I fixed it)** and **two design-soundness gaps** that must be
addressed before any "full primitive" claim is final. The core hardness story is unchanged
(security still rests on LSN, now *also* on hash preimage-resistance — see §2). `n=42→41` fixed.

## 1. Done well (verified)

- **A2 — comparison table.** Relabeled "LSN-SNARK membership (core-relation)" + new "LSN-SNARK full
  (+hash)" row + "ZK-Kyber/SPHINCS+ full KEM/sig verif." + scope sentence ("binding overhead is
  comparable across schemes"). This is the equal-footing comparison I asked for. ✓
- **`n=42 → 41`** in the verified counts (matches the 80-bit parameter). ✓
- **Hash-commitment approach** (`c=Hash(M)`, Poseidon, prove opening + membership) is a standard,
  legitimate commit-and-prove binding. The `O(n)` hash cost (`~300–500` constraints for `~9` field
  elements at `n=65`) is in the right ballpark.

## 2. Issues

**[FIXED — numerical] "100× smaller than SHA-256" was wrong.** The full primitive `~4{,}500–4{,}700`
vs one SHA-256 block `~25{,}000` is **~5×**, not 100× (`25000/4700 = 5.3`). I corrected it to
"about 5× smaller than a single SHA-256 block… roughly 1{,}000× smaller than ZK-Kyber" (the
ZK-Kyber `1000×` is fine: `millions / 4700 ≈ 1000`).

**[FLAG — assumption set] The hash commitment introduces a *second* hardness assumption.** With
`c=Hash(M)` in `pk`, a forgery requires producing some `M'` with `Hash(M')=c` (and membership), so
unforgeability hardness is `min(LSN-search, hash-preimage)`. The scheme is therefore **not "secure
purely from LSN"** — it also needs **preimage resistance of `Hash`**. This is fine *if* the hash
output is sized so that hash-preimage ≥ the LSN level (e.g. a `≥256`-bit hash, so quantum preimage
`2^{128}` ≥ LSN at `n=65`), but the paper must **state the hash assumption** and that LSN is the
intended bottleneck. (Today the SNARK text still says "still `O(n²)`, security from LSN.")

**[FLAG — soundness sketch] The full-signature relation is under-specified.** The circuit proves
"`Hash(M)=c` ∧ `x∈L_M`," but *what is `x`*? If `x` is a Fiat–Shamir challenge from the message, then
a random `x` lies in `L_M` (density `2^{-n}`) only with probability `2^{-n}`, so the **legitimate
signer cannot satisfy `x∈L_M`** for a random challenge. So the membership-against-challenge picture
as written does not yield a functional signature. A real construction must specify the binding to
the message and to the `m` public samples (e.g. prove `M` consistent with a *challenged subset* of
the public `(x_i,y_i)`, or use a different message-binding) — which can change the full-circuit
count. **Until this is pinned down, the `~4{,}500` "full primitive" figure is a lower-bound sketch,
not the established cost of a sound signature.** Recommend labeling it "(illustrative; full EUF-CMA
construction in progress)."

## 3. Net + actions for Kimi

```text
A2 honest comparison      : DONE (equal-footing table + scope). Good.
n=42→41                   : DONE.
A1 hash-commitment binding: reasonable APPROACH; circuit sketch ~4,500 plausible.
  - "100× vs SHA-256"     : FIXED here → ~5×.
  - assumption set        : state that unforgeability = min(LSN, hash-preimage); size the hash so LSN
                            is the bottleneck; drop "security purely from LSN" for the signature.
  - soundness spec        : pin down what x∈L_M is checked against (message/sample binding); the
                            legitimate signer cannot meet x∈L_M for a random FS challenge. Until then
                            label the full count "illustrative; full EUF-CMA in progress."
```

The membership-circuit result and the compact-secret-key bonus remain the real, solid wins. The
hardness story for LSN itself is untouched (OPEN). No 7th; no break; no security claim. **OPEN = LSN.**

```text
Credit:
  full-signature binding (hash commitment) + honest comparison table  — Kimi (cc438038)
  100×→5× fix + assumption-set / soundness-spec flags                  — this adjudication
```
