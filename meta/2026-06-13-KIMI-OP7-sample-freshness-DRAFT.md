# OP7: Sample freshness for rerandomized LSN — DRAFT

**Date:** 2026-06-13.  
**Author:** Kimi.  
**Status:** DRAFT awaiting Claude adjudication.  
**Context:** `sec:open` item 7; follow-up to closed noise-side SA line (`6d7f73e`).

---

## 1. Problem statement (membership-LSN)

A sample from $D_L$ is $(x, b)$ with $x \sim U(\F_2^{2n})$, $e \sim \mathrm{Bernoulli}(p)$, and $b = \mathbf{1}_L(x) \oplus e$.

**Exact secret rerandomization.** For any public $S \in \mathrm{Sp}(2n)$, the map
\[
(x, b) \mapsto (Sx, b)
\]
produces a sample for the rerandomized secret $L' = S \cdot L$, because $\mathbf{1}_{S\cdot L}(Sx) = \mathbf{1}_L(x)$.

**Freshness question.** Given $t$ original samples from $D_L$, does there exist a public transformation $T$ (depending only on the public parts of the samples and on public coins, not on $L$) that outputs $k$ samples whose joint distribution is close to $k$ independent fresh samples from $D_{S\cdot L}$ for some public $S$?

More precisely, for a family $\mathcal{T}$ of public transformations, define
\[
\Delta(\mathcal{T}) := \min_{T \in \mathcal{T}} \; SD\bigl(T((x_1,b_1),\dots,(x_t,b_t)),\; (x'_1,b'_1),\dots,(x'_k,b'_k)\bigr),
\]
where the right-hand side consists of $k$ independent draws from $D_{S\cdot L}$ and $S$ is the symplectic matrix encoded by $T$ (or chosen independently).

- If $\Delta(\mathcal{T}) = o(1)$ for some natural $\mathcal{T}$, LSN admits a public freshness procedure.
- If $\Delta(\mathcal{T})$ stays bounded away from $0$ for all natural $\mathcal{T}$, sample freshness is blocked, explaining the $N$-fold loss in the multi-user hybrid.

## 2. First concrete family: symplectic orbit

The simplest candidate transformation uses $t=1$ sample and outputs $k$ points on the same symplectic orbit:
\[
T_{S_1,\dots,S_k}(x,b) = \bigl((S_1 x, b), (S_2 x, b), \dots, (S_k x, b)\bigr),
\]
where $S_i \in \mathrm{Sp}(2n)$ are public.

This rerandomizes the secret for each output sample to $L_i = S_i \cdot L$, but all $k$ outputs share the **same** query point $x$ (up to symplectic rotation) and the **same** noise bit $b$. Hence they are far from independent fresh samples, which would have independent $x'_i$ and independent noise $e'_i$.

## 3. Experimental plan for $n=2$

For $n=2$ we can enumerate everything exactly:

- All Lagrangian subspaces $L$ (15 subspaces; 90 isotropic matrices $A$ if bases are counted).
- All symplectic matrices $S \in \mathrm{Sp}(4, \F_2)$ (720 elements).
- For each $L$, sample $(x,b) \sim D_L$, apply $T_{S_1,S_2}$, and compare with two independent fresh samples from $D_{S_1 \cdot L}$ and $D_{S_2 \cdot L}$.
- Compute exact $SD$ by enumerating over $L$, $x$, $e$.

This gives an unconditional numerical answer for the symplectic-orbit family at $n=2$.

## 4. First result: symplectic-orbit family is far from fresh

`experiments/183-KIMI-OP7-symplectic-orbit-freshness.py` computes the exact $SD$ for $n=2$, $t=1$, $k=2$ by enumerating all Lagrangian subspaces and all symplectic matrices.

**Result:** over 200 random pairs $(S_1, S_2) \in \mathrm{Sp}(4, \F_2)^2$,
\[
SD = 0.960938 \quad \text{for every pair}.
\]

The transformed output $((S_1 x, b), (S_2 x, b))$ is essentially maximally far from two independent fresh samples. This is because:
- both output samples share the same query point $x$ up to symplectic rotation;
- both output samples share the exact same label bit $b$ (same noise realization).

Fresh samples, by contrast, have independent query points and independent noise bits.

## 5. Interpretation

This is **empirical evidence against public sample freshness** for the symplectic-orbit family. It supports the paper's claim that non-linearity of $\mathbf{1}_L$ blocks freshness, and explains why the multi-user hybrid loses a factor $N$.

The result is not a proof for all public transformations, but it rules out the most natural candidate family.

## 6. Caveats and next steps

- Only the symplectic-orbit family was tested; exotic public transformations remain possible in principle.
- $n=2$ is small; asymptotic behavior may differ (though the obstruction is structural and likely general).
- Next: test other natural families (e.g. affine symplectic shifts $x \mapsto Sx + t$, or linear combinations of multiple original samples) and formalize a conjecture.
