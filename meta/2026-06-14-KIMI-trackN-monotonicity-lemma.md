# Track N — matched-rate SD is non-decreasing in m (fixed n)

**Date:** 2026-06-14  
**Track:** N (experiment numbers 216–219)  
**Script:** `experiments/216-KIMI-trackN-monotonicity-lemma.py`  
**Outputs:**
- `experiments/output/216-trackN-monotonicity-lemma.json`
- `experiments/output/216-trackN-n2.json`
- `experiments/output/216-trackN-n3.json`

**Context:** defensive cryptanalysis for public publication; no real-world targets.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. **OPEN = LSN.**

---

## 0. PRE-REGISTER interpretation guards (mandatory)

1. **Comparison distribution.** All SDs are to **matched-rate** LPN$_{p_{\rm eff}(n)}$ with
   $$
   p_{\rm eff}(n)=\frac{1-(3/4)^{2n}}{2}.
   $$
   No comparison to LPN$_{1/4}$ is made.
2. **Scaling axis.** We study **$m$ increasing at fixed $n$** (the axis of lem:m2). No fixed-small-$m$ conclusion is drawn.
3. **Usability of the LPN target.** $p_{\rm eff}(n)\to 1/2$ as $n\to\infty$, so the target itself approaches trivial noise-$1/2$ LPN.  The SD numbers measure whether the correlation introduced by marginal-adaptive $B$ is detectable inside a vacuous LPN regime; they do **not** imply a practical distinguisher for standard LPN.

---

## 1. Projection lemma and monotonicity theorem (THEOREM)

Let $n$ be fixed and let

- $P_{\rm out}^{(m)}$ be the distribution of $(C,y)=(BA,\,B(Ax+e))$ with $A\sim\mathrm{Unif}(\mathrm{Lagr}(2n,\mathbb F_2))$, $x\sim\mathrm{Unif}(\mathbb F_2^n)$, $e\sim\mathrm{Bernoulli}(1/4)^{2n}$, and $B\sim\mathrm{Unif}(\mathbb F_2^{m\times 2n})$ drawn **fresh per $A$**;
- $P_{\rm lpn}^{(m)}$ be the matched-rate LPN$_{p_{\rm eff}(n)}$ distribution over $\mathbb F_2^{m\times n}\times\mathbb F_2^m$;
- $\Pi_m$ be the deterministic channel that drops the last row of $(C,y)$.

**Projection lemma.** The first-$m$-rows marginal of $P_{\rm out}^{(m+1)}$ equals $P_{\rm out}^{(m)}$, and the first-$m$-rows marginal of $P_{\rm lpn}^{(m+1)}$ equals $P_{\rm lpn}^{(m)}$.

*Proof.* The rows of $B$ are i.i.d. and independent of everything else except through the shared $(A,x,e)$.  Conditional on $(A,x,e)$, the $(m+1)$ output rows are i.i.d. copies of the one-row map $r\mapsto (rA,\,r(Ax+e))$.  Hence the first $m$ rows have exactly the same joint law as the $m$-row reduction.  For the LPN side, the $(m+1)$ samples are i.i.d. rows $(c_i,\langle c_i,x\rangle+e_i)$; dropping the last row leaves $m$ i.i.d. rows with the same secret $x$ and per-coordinate noise $p_{\rm eff}(n)$, i.e. $P_{\rm lpn}^{(m)}$. ∎

**Monotonicity theorem.** Define $\mathrm{SD}(m)=\mathrm{SD}(P_{\rm out}^{(m)},P_{\rm lpn}^{(m)})$. Then for every $m\ge 1$,
$$
\mathrm{SD}(m)\le \mathrm{SD}(m+1).
$$

*Proof.* By the projection lemma, $\Pi_m(P_{\rm out}^{(m+1)})=P_{\rm out}^{(m)}$ and $\Pi_m(P_{\rm lpn}^{(m+1)})=P_{\rm lpn}^{(m)}$.  Statistical distance satisfies the data-processing inequality under any channel: $\mathrm{SD}(\Pi_m(P),\Pi_m(Q))\le \mathrm{SD}(P,Q)$.  Applying this with $P=P_{\rm out}^{(m+1)}$ and $Q=P_{\rm lpn}^{(m+1)}$ gives the claim. ∎

**Strictness.** Strict inequality is observed in every exact table below, but it is **not** claimed as a theorem.

---

## 2. Exact cross-check (EVIDENCE)

The script verifies the sufficient-statistic reduction against from-scratch enumeration for small $(n,m)$ and then cross-checks monotonicity on the largest available exact tables.

### Self-checks (direct vs sufficient-statistic)

| $n$ | $m$ | status |
|----:|----:|:------:|
| 2 | 2,3,4 | OK |
| 3 | 3,4 | OK |

### $n=2$ exact SD (matched rate $p_{\rm eff}=175/512$)

| $m$ | exact SD | decimal | source |
|----:|---------:|--------:|:-------|
| 2 | $36575/524288$ | 0.069761 | experiments/200 |
| 3 | $695896635/4294967296$ | 0.162026 | experiments/200 |
| 4 | $277825754675/1099511627776$ | 0.252681 | experiments/200 |
| 5 | $11668368577886825/36028797018963968$ | 0.323862 | experiments/202 |
| 6 | $27663233753869930405/73786976294838206464$ | 0.374907 | experiments/202 |
| 7 | $62110524507069812281095/151115727451828646838272$ | 0.411013 | experiments/202 |
| 8 | $16905825785074125865887285/38685626227668133590597632$ | 0.437005 | experiments/202 |
| 12 | $2670376973898429557749111289348052212525/5444517870735015415413993718908291383296$ | 0.490471 | this script |
| 16 | $776580527746517716721610547003155688886535620657255/1496577676626844588240573268701473812127674924007424$ | 0.518904 | this script |
| 24 | … | 0.567854 | experiments/202 |
| 32 | … | 0.613360 | experiments/202 |
| 48 | … | 0.691341 | this script |

All 12 points are strictly increasing.

### $n=3$ exact SD (matched rate $p_{\rm eff}=3367/8192$)

| $m$ | exact SD | decimal | source |
|----:|---------:|--------:|:-------|
| 2 | $60016775/2415919104$ | 0.024842 | experiments/200 |
| 3 | $27456165227309/422212465065984$ | 0.065029 | experiments/200 |
| 4 | $2606451312633458017/20752587082923245568$ | 0.125596 | experiments/200 |
| 5 | $1948309423583462892421105/10880332376531662572355584$ | 0.179067 | experiments/200 |
| 6 | $154465747684542391975435825813/713053462628379038341895553024$ | 0.216626 | experiments/200 |
| 7 | $2809657129253759292702122144354957/11682667931703362164193616740745216$ | 0.240498 | this script |
| 8 | … | 0.255124 | this script |
| 9 | … | 0.264112 | this script |
| 10 | … | 0.269815 | this script |
| 11 | … | 0.273674 | this script |
| 12 | … | 0.276540 | this script |

All 11 points are strictly increasing.

### Monotonicity check result

```json
{
  "2": {"m_range": [2, 48], "num_points": 12, "monotone": true, "strict": true},
  "3": {"m_range": [2, 12], "num_points": 11, "monotone": true, "strict": true}
}
```

### Wall note

The values at $n=2$, $m=64$ and $m=80$ are **not** recomputed here.  The $O(m^7)$ sufficient-statistic enumeration (the same wall Track L is engineered to push) exceeds the 300 s foreground limit at $m=50$.  The monotonicity theorem does not depend on those points; when Track L produces $m=64,80$ exact values (experiments 204–209), the same check can be appended automatically.

---

## 3. Limit corollary

**THEOREM.** For each fixed $n$, $\lim_{m\to\infty}\mathrm{SD}(m)$ exists because the sequence is bounded in $[0,1]$ and monotone non-decreasing.

**EVIDENCE / OPEN.** The entropy heuristic (the correlated noise in the reduction output carries at most $2n+n$ bits of structure, while the LPN target is a product distribution over $m$ rows) suggests the limit is $1$ at fixed $n$.  This is **not proved** here; it is recorded as evidence only.

At the largest computed points:
- $n=2$, $m=48$: $1-\mathrm{SD}\approx 0.308659$;
- $n=3$, $m=12$: $1-\mathrm{SD}\approx 0.723460$.

---

## 4. Standing guards

- **L1 exact arithmetic.** Every probability is kept as a `fractions.Fraction`; JSON stores string fractions.  The sufficient-statistic reduction uses the single integer common denominator $q_{\rm den}\cdot N\cdot(2N)^m\cdot D^m$.
- **L2 J-twist duality.** The row-type inner product is the standard $\mathbb F_2$ pairing $\langle w,\tau\rangle$; no dual-space twist is introduced.
- **L3 query-class hygiene.** Conclusions are about statistical distance only; no unrestricted Feldman/SQ inference is made.
- **L4 never transform the comparison distribution.** The projection channel $\Pi_m$ is applied to **both** $P_{\rm out}^{(m+1)}$ and $P_{\rm lpn}^{(m+1)}$; the comparison distribution is never bijected alone.

---

## 5. Deliverables and status

| file | purpose |
|------|---------|
| `experiments/216-KIMI-trackN-monotonicity-lemma.py` | theorem/proof + exact cross-check script |
| `experiments/output/216-trackN-monotonicity-lemma.json` | merged summary with claim labels and guards |
| `experiments/output/216-trackN-n2.json` | $n=2$ exact table up to $m=48$ |
| `experiments/output/216-trackN-n3.json` | $n=3$ exact table up to $m=12$ |
| `meta/2026-06-14-KIMI-trackN-monotonicity-lemma.md` | this note |

**Claim labels:**
- Projection lemma: **THEOREM**.
- Monotonicity theorem: **THEOREM**.
- Monotonicity on exact tables: **EVIDENCE** (finite exact computation; strictness observed but not proven in general).
- Existence of $\lim_{m\to\infty}\mathrm{SD}(m)$: **THEOREM**.
- Limit equals $1$: **EVIDENCE / OPEN**.
- lem:m2 status: **OPEN**.
