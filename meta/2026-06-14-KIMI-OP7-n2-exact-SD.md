# OP7 $n=2$ exact SD — symplectic-orbit sample freshness

**Date:** 2026-06-14  
**Script:** `experiments/192-KIMI-OP7-n2-exact-SD.py`

## Question

Can a public symplectic transformation turn one LSN sample into two fresh
independent samples for a rerandomized secret?  Formally, choose $L$ uniformly,
draw one sample $(x,b)\sim D_L$ with $b=\mathbf 1_L(x)+e$, $e\sim\operatorname{Bernoulli}(1/4)$,
and apply two public symplectic matrices $S_1,S_2$ to obtain
$(S_1 x,b)$ and $(S_2 x,b)$.  Compare this joint distribution to two independent
fresh samples from $D_{S_1 L}$ and $D_{S_2 L}$.

## Reduction to $T = S_1^{-1}S_2$

Because everything is transformed by $S_1^{-1}$, the statistical distance depends
only on $T=S_1^{-1}S_2$.  The transformed distribution has support only on keys
$(u,b,Tu,b)$ with identical noise bit, while the fresh distribution has two
independent noise bits.

## Exact results

| Statistic | Value | Float |
|-----------|------:|------:|
| Number of $T\in\mathrm{Sp}(4,\F_2)$ | 720 | — |
| Minimum SD | $123/128$ | $0.9609375$ |
| Maximum SD | $371/384$ | $0.9661458$ |
| Mean SD | $309/320$ | $0.965625$ |
| Median SD | $309/320$ | $0.965625$ |

## Interpretation

Even the best choice of public symplectic pair leaves SD $\ge 123/128\approx0.961$.
The two output samples are therefore far from independent fresh samples.  This
is because the original single noise bit $e$ is shared between both outputs:
$b$ is identical, while fresh samples would have independent noise bits.  The
public symplectic map preserves this correlation, so it cannot create freshness.

For $n=2$ the answer to OP7 is **negative**: no public symplectic orbit
transformation yields fresh samples.

## Relation to Experiment 183

Experiment 183 sampled 200 random symplectic pairs and reported a best SD of
$0.961$ (float).  The exact enumeration here confirms that the true minimum is
$123/128=0.9609375$ and that the random sample was essentially optimal.
