# audit-reframe(kimi): consistency audit of the reframed abstract + §1.3 opening

**Date:** 2026-06-14. **Commit under audit:** `e51b959`.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

This audit checks only the reframed *framing* (title/abstract/§1.3 opening of `paper/lsn-core.tex`) for quantitative drift and overstatement relative to the proved body theorems. Body math AUD1–AUD5 is taken as already clean.

## 7-row claim table

| Claim | Body theorem (`\label`, line) | Recomputed value (exact `Fraction`) | Verdict |
|---|---|---|---|
| **C1** Pairwise correlation `((1-2p)^2)/(p(1-p))·2^{j-2n}`, coefficient `4/3` at `p=1/4` | `lem:exact-corr`, l. 420 | `Fraction((1-2p)**2, p*(1-p))` · `Fraction(1, 2**(2*n-j))`. At `p=1/4`: `(1/2)^2 / (1/4·3/16) = (1/4)/(3/16) = 4/3`. | **MATCH** |
| **C2** All-ones subset moments have exact closed forms; fixed-size bundle deviates from unconstrained LPN by exactly `Θ(4^{-n})` | `thm:mj-closed`, l. 654; `thm:mj-general`, l. 672 | `m_j` formula verified symbolically; e.g. `n=3`: `m_2 = 284/4725`, unconstrained `1/16`, diff exact; `m_3 = 4/315`. Closed forms are exact rational identities; the `Θ(4^{-n})` deviation is the body’s stated asymptotic. | **MATCH** |
| **C3** Unconditional `Ω(2^n)` SQ lower bound via explicit symplectic spread | `thm:main-sq-uncond`, l. 490 | The theorem gives `Ω(2^t)` queries for `1 ≤ t ≤ n-1`; at `t = n-1` this is `Ω(2^n)`. | **MATCH** |
| **C4** `2^{2n-O(1)}` bound under a precisely stated extremality conjecture | `thm:main-sq-cond`, l. 530; `conj:pencil`, l. 518 | Body states exactly: assuming `conj:pencil`, any SQ algorithm with advantage `> 2/3` requires `q ≥ 2^{2n-O(1)}` queries. | **MATCH** |
| **C5** sympLPN off-diagonal exactly `-((1+τ)^{2n}-1)/(2^{2n}-1)`, versus `0` unconstrained; verify at `n=2,3` | `thm:symplpn-corr`, l. 568 | With `τ = (1-2p)^2`, at `p=1/4` (`τ=1/4`): `n=2 → -123/1280`; `n=3 → -183/4096`. Unconstrained off-diagonal is `0`. | **MATCH** |
| **C6** `2^{c_p n}`-query SQ bound at constant VSTAT strength | `cor:symplpn-sq`, l. 592 | `c_p = 1 - 2·log2(1+τ)` with `τ=(1-2p)^2`. At `p=1/4`: `c_p = 5 - 2·log2(5) ≈ 0.3561438102252753`. | **MATCH** |
| **C7** Transport invariant `C^⊤ M C = 0`; closes 3 of 4 cells + deterministic half of 4th; one open cell | `thm:transport-fullrank`, l. 890; `thm:transport-nearfull`, l. 913; `thm:deterministic-marginal-adaptive`, l. 1184; `open:marginal-adaptive`, l. 1238 | The body explicitly blocks public/fixed/conditionally-uniform adaptive and deterministic marginal-adaptive, and labels only randomized marginal-adaptive as open. | **MATCH** |

## “exactly” × 3 sharp check

- **C1 (pairwise correlation):** The body gives the formula as a literal exact identity with no `O(·)` or `o(1)` (`lem:exact-corr`, Eq. (2)). The abstract’s “exactly” is faithful. **PASS.**
- **C2 (moments / Θ(4^{-n})):** The *closed forms* for `m_j` are exact rational identities (`thm:mj-general`). The phrase “deviates … by exactly `Θ(4^{-n})`” reproduces the body’s asymptotic statement `m_j = (1/4)^j + Θ(4^{-n})`. No hidden error term was rounded away. **PASS** (with the caveat that `Θ(·)` is itself asymptotic notation; the exactness claim properly attaches to the closed forms).
- **C5 (sympLPN off-diagonal):** The body gives the off-diagonal as a literal exact identity (`thm:symplpn-corr`, l. 572). The abstract’s “exactly” is faithful. **PASS.**

## §1.3 positioning-phrase verdict

Phrase under audit: *“producing asymptotic-error-free correlations and moments where prior analyses give only bounds.”*

**Verdict: SUPPORTED** (by internal consistency only).

Our own text in §1.2 (l. 92) and `subsec:two-forms` (ll. 218–243) describes the concurrent works (KLP+25, PQS26, LPQR26) as proving hardness reductions, entropy-based barriers, and linear-reduction impossibility results in the `m = Θ(n)` regime, plus a bound for `m = ω(n)` that LPQR26 note is insufficient to fully rule out decodability. Nowhere does it attribute to them exact, asymptotic-error-free correlation/moment closed forms. The positioning phrase is therefore fair relative to our own citations.

## One-line overall verdict

**No MISMATCH and no OVERSTATEMENT found; the reframed abstract and §1.3 opening are quantitatively consistent with the proved body theorems.**

---

## Honesty labels (Sound Verifier)

- The table entries C1–C7 are **THEOREM** citations backed by the corresponding body statements.
- The fractional recomputations for C1/C5/C6 and the small-`n` moment checks for C2 are **EVIDENCE** (finite exact computations at the stated parameters).
- The positioning-phrase verdict is **EVIDENCE** based on inspection of our own `\cite` text and `subsec:two-forms`, not on external paper retrieval.
- The overall verdict is a **negative audit finding**: it does not prove security; it only states that the reframe does not drift beyond the body.
