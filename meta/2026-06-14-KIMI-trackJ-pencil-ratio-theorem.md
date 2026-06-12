# Track J — pencil-ratio theorem for all $(n,k)$ (231)

**Date:** 2026-06-14. **Actor:** Kimi. **Status:** DRAFT for Claude adjudication.  
**Files:** `experiments/231-KIMI-trackJ-pencil-ratio-theorem.py`, `experiments/output/231-KIMI-trackJ-pencil-ratio-theorem.json`.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## Interpretation guard (PRE-REGISTER)

Before interpreting the numbers as bearing on `conj:pencil`:

1. **Comparison distribution / matched normalisation.** The statistic is the raw integer intersection size $|L \cap L'| = 2^{\dim(L \cap L')}$.  The paper's correlation $\langle D_L, D_{L'}\rangle$ contains the common factor $(1-2p)^2/(p(1-p)) \cdot 2^{-2n}$, which cancels in every ratio to $\rho_{\mathrm{avg}}$.  All ratio claims below are therefore ratio-scale invariant and matched.
2. **m-vs-n scaling.** `conj:pencil` asserts that every subset $\mathcal{D}'$ with $|\mathcal{D}'| \ge |\operatorname{Lagr}(2n,\F_2)|/2^{2n-c}$ has average correlation at most $5\rho_{\mathrm{avg}}$.  We record, for every $n$ and $k$, whether the $k$-pencil meets the $c=0$ threshold.
3. **Noise-rate guard.** This is a structural geometric statistic; no output-noise-rate comparison is involved.

**Convention:** diagonal-inclusive averages, matching `thm:distance` and Track D.  That is,
\[
\bar\rho(S) = \frac{1}{|S|^2}\sum_{L,L'\in S} 2^{\dim(L\cap L')}.
\]

---

## J1 — $n=4$ verification by quotient construction (EVIDENCE)

For the standard $k$-dimensional isotropic subspace $W = \langle e_1,\dots,e_k\rangle$, the pencil
\[
S_W = \{ L \in \operatorname{Lagr}(2n,\F_2) : W \subseteq L \}
\]
is built by enumerating $\operatorname{Lagr}(W^{\perp_\Omega}/W) \cong \operatorname{Lagr}(2(n-k),\F_2)$ and lifting each quotient Lagrangian back to $V$.  No enumeration of the full $\operatorname{Lagr}(8,\F_2)$ is required.

The script computes the diagonal-inclusive average correlation of each pencil and compares it with the pre-registered predictions.

| $k$ | $|S_W|$ | $\bar\rho(S_W)$ | ratio to $\rho_{\mathrm{avg}}$ | predicted |
|----:|--------:|----------------:|-------------------------------:|----------:|
| 1 | 135 | $32/9$ | $17/9$ | $17/9$ |
| 2 | 15  | $32/5$ | $17/5$ | $17/5$ |
| 3 | 3   | $32/3$ | $17/3$ | $17/3$ |
| 4 | 1   | $16$   | $17/2$ | $17/2$ |

All four predictions match exactly.  **Label:** EVIDENCE (constructive verification; the general proof is J2).

---

## J2 — THEOREM: exact pencil ratio for all $(n,k)$

### Statement
For every $n \ge 1$ and every $1 \le k \le n$,
\[
\operatorname{ratio}(n,k)
\;:=\;
\frac{\bar\rho(S_W)}{\rho_{\mathrm{avg}}}
\;=
\frac{2^n+1}{2^{n-k}+1},
\]
for any $k$-dimensional isotropic $W$.

### Proof
1. **Quotient geometry.** Let $Q = W^{\perp_\Omega}/W$, a non-degenerate symplectic space of dimension $2(n-k)$.  For $L,L' \in S_W$ with quotient images $\bar L, \bar L' \in \operatorname{Lagr}(Q)$,
   \[
   \dim(L \cap L') = k + \dim(\bar L \cap \bar L').
   \]
   Hence
   \[
   \bar\rho(S_W) = 2^k \cdot C_{n-k},
   \]
   where $C_m = \E[2^{\dim(\bar L \cap \bar L')}]$ is the diagonal-inclusive average over $\operatorname{Lagr}(2m,\F_2)$.

2. **Closed form of $C_n$.** From `thm:distance`,
   \[
   C_n = \frac{1}{|\operatorname{Lagr}(2n,\F_2)|}
         \sum_{j=0}^{n} {n \brack j}_2 \, 2^{(n-j)(n-j+1)/2} \, 2^{j}.
   \]
   Substituting $j = n-\ell$ and using ${n \brack n-\ell}_2 = {n \brack \ell}_2$ gives
   \[
   C_n = \frac{2^n}{|\operatorname{Lagr}(2n,\F_2)|}
         \sum_{\ell=0}^{n} {n \brack \ell}_2 \, 2^{\ell(\ell-1)/2}.
   \]
   The $q$-binomial theorem at $q=2$ states
   \[
   \sum_{\ell=0}^{n} {n \brack \ell}_2 \, 2^{\ell(\ell-1)/2}
   = \prod_{i=0}^{n-1}(1+2^i)
   = 2\prod_{i=1}^{n-1}(2^i+1).
   \]
   Since $|\operatorname{Lagr}(2n,\F_2)| = \prod_{i=1}^{n}(2^i+1)$, we obtain
   \[
   C_n = \frac{2^{n+1}}{2^n+1}.
   \]

3. **Assemble the ratio.**
   \[
   \operatorname{ratio}(n,k)
   = \frac{2^k C_{n-k}}{C_n}
   = \frac{2^k \cdot 2^{n-k+1}/(2^{n-k}+1)}{2^{n+1}/(2^n+1)}
   = \frac{2^n+1}{2^{n-k}+1}.
   \]

### Script verification
`experiments/231-KIMI-trackJ-pencil-ratio-theorem.py` checks:
- $C_n$ from `thm:distance` equals $2^{n+1}/(2^n+1)$ for $n=1\dots 8$.
- The $q$-binomial identity used in step 2 for $n=1\dots 8$.
- The full ratio formula against the quotient construction for $1\le k\le n\le 5$.

All checks pass.  **Label:** THEOREM.

---

## J3 — Corollary: exact pencil thresholds for `conj:pencil` (COROLLARY/DRAFT)

The exact ratio immediately gives the limiting behaviour:
\[
\lim_{n\to\infty} \operatorname{ratio}(n,k) = 2^k.
\]
In particular:
- $k=1$ pencils have ratio $\to 2$ from below.
- $k=2$ pencils have ratio
  \[
  \frac{2^n+1}{2^{n-2}+1} = 4 - \frac{3}{2^{n-2}+1},
  \]
  so they approach $4\rho_{\mathrm{avg}}$ from below.  **Any `conj:pencil` threshold strictly below $4\rho_{\mathrm{avg}}$ is therefore ruled out by $k=2$ pencils.**
- $k\ge 3$ pencils have ratio $\to 2^k \ge 8$, but their size is
  \[
  |S_W| = |\operatorname{Lagr}(2(n-k),\F_2)| = \prod_{i=1}^{n-k}(2^i+1),
  \]
  which falls below the $c=0$ scale threshold $|\operatorname{Lagr}(2n,\F_2)|/2^{2n}$ for every $n\ge 3$ (checked exactly in the JSON table for $n\le 12$).  They are therefore irrelevant at the conjectured scale.

### Draft motivation paragraph for `paper/lsn-core.tex`

> For a $k$-dimensional isotropic core $W$, the exact diagonal-inclusive average correlation of the pencil $S_W$ is $\bar\rho(S_W)=2^k C_{n-k}$, where $C_m = 2^{m+1}/(2^m+1)$ is the global diagonal-inclusive average over $\operatorname{Lagr}(2m,\F_2)$.  Consequently the pencil ratio is $\operatorname{ratio}(n,k) = \rho(S_W)/\rho_{\mathrm{avg}} = (2^n+1)/(2^{n-k}+1)$.  In particular, the $k=1$ pencil ratio tends to $2$ from below, while the $k=2$ pencil ratio tends to $4$ from below; hence any threshold below $4\rho_{\mathrm{avg}}$ is automatically unsafe from pencils.  For $k\ge 3$ the ratio tends to $2^k\ge 8$, but $|S_W| = |\operatorname{Lagr}(2(n-k),\F_2)|$ falls below the `conj:pencil` scale $|\operatorname{Lagr}(2n,\F_2)|/2^{2n}$ for every $n\ge 3$, so the only scale-relevant pencils are $k=1$ and $k=2$.  The conjectured $5\rho_{\mathrm{avg}}$ bound therefore survives all pencils and is forced to be strictly larger than $4\rho_{\mathrm{avg}}$ by the $k=2$ family.

**Label:** COROLLARY/DRAFT.

---

## Files and reproducibility

- `experiments/231-KIMI-trackJ-pencil-ratio-theorem.py` — reproducible script.
- `experiments/output/231-KIMI-trackJ-pencil-ratio-theorem.json` — exact rational outputs as strings.

Run: `python3 experiments/231-KIMI-trackJ-pencil-ratio-theorem.py`.

---

## Standing guards observed

- **(L1) Exact arithmetic.** Every ratio and average is a `fractions.Fraction`; JSON stores rationals as strings.
- **(L2) Duality care.** The quotient construction uses $W^{\perp_\Omega}/W$, the symplectic perpendicular (the $J$-twisted Gram dual).  No Euclidean dual is invoked.
- **(L3) Query-class hygiene.** All claims are statements about Lagrangian geometry; no unrestricted SQ/Feldman inference is made.

---

No closure; no break; no security claim.  `conj:pencil` remains OPEN.
