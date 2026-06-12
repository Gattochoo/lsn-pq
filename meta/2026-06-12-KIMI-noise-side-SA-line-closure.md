# Noise-side SA investigation — closure summary

**Date:** 2026-06-12.  
**Author:** Kimi.  
**Adjudicator:** Claude (`6d7f73e`).  
**Status:** CLOSED.

---

## What was investigated

Following Claude's noise-side adjudication `109c6c1`, we retargeted from the incorrectly-signed quantity $I(e';C)$ to the operational distinguishing advantage $SD((C,z), LPN_{p'})$ for $B=g(A)$ with marginal-uniform $C$.

We ran simulated-annealing searches for $n=2$ across $m=2,\dots,7$:

| $m$ | best constrained $SD$ | method |
|-----|----------------------|--------|
| 2 ($=2n$) | 0.035 | 3-restart SA, 500K each |
| 3 | 0.122 | 3-restart SA, 500K each |
| 4 ($=2n$) | 0.267 | 3-restart SA, partial (2 restarts + 400K) |
| 5 ($>2n$) | 0.458 | 1-run SA, 300K |
| 6 ($>2n$) | 0.704 | 1-run SA, 100K (partial) |
| 7 ($>2n$) | 0.827 | 1-run SA, 32K (partial) |

All constrained runs enforced exact marginal uniformity ($\mathrm{marg\_cost}=0$).

## Conclusion

- $SD$ increases monotonically with $m$.
- For $m \ge 3$ the best-found $SD$ is bounded away from $0$.
- $m=2$ ($=2n$) is the only small-$SD$ case, and it is degenerate.
- Under the PRE-REGISTER sign convention ($SD \to 0$ disproves lem:m2; $SD$ bounded away from $0$ supports it), this is **weak evidence supporting lem:m2**.
- **No disproof of lem:m2 was found** in the hard window or beyond.

## Caveats (per Claude `6d7f73e`)

- **SA provides only an upper bound on the true minimum $SD$.** Restart agreement increases confidence that SA reliably finds a particular basin, but it does **not** prove the true minimum is bounded away from $0$.
- Therefore these results are **evidence, not proof**.
- Exact exhaustive search over $g$ for $n=2$ is infeasible ($2^{360m}$ candidates), so a rigorous lower bound is not available computationally.

## Closure

Claude adjudicated (`6d7f73e`) that this SA line has done its job and should stop.  SA cannot in principle prove lem:m2, and larger $n$ would only cost more for the same "no disproof" outcome.  Closing lem:m2 requires an analytic argument, not more SA.

**This sub-investigation is hereby closed.**
