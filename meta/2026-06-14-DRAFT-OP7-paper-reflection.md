# DRAFT — OP7 $n=2$ exact SD paper reflection

**For:** Claude (paper-body integration).  
**Source:** `experiments/192-KIMI-OP7-n2-exact-SD.py`,
`meta/2026-06-14-KIMI-OP7-n2-exact-SD.md`,
`experiments/output/192-op7-n2-exact-SD.json`.

## Claim to add

For $n=2$, the natural public symplectic-orbit transformation cannot produce
fresh independent samples for a rerandomized secret.  The exact statistical
distance between the transformed output and truly fresh samples is at least
$123/128 \approx 0.961$, with mean $309/320 \approx 0.966$ over all pairs
$S_1,S_2\in\mathrm{Sp}(4,\F_2)$.

## Suggested edits

### 1. Open Problem 7 (\Cref{sec:open}, item 7)

Replace

> \item \textbf{Sample freshness for rerandomized LSN.} Exact secret rerandomization is possible: applying a public symplectic matrix $S \in \mathrm{Sp}(2n)$ to the public part of each sample maps the secret $L$ to $S\cdot L$ while preserving labels. Does LSN admit a public transformation that yields \emph{fresh} (statistically independent) samples for the rerandomized secret? A positive answer would yield a tight multi-user security bound and improve the reduction in \Cref{subsubsec:kem-multiuser}. A negative answer would explain why the hybrid argument loses a factor $N$.

with

> \item \textbf{Sample freshness for rerandomized LSN.} Exact secret rerandomization is possible: applying a public symplectic matrix $S \in \mathrm{Sp}(2n)$ to the public part of each sample maps the secret $L$ to $S\cdot L$ while preserving labels. Whether LSN admits a public transformation that yields \emph{fresh} (statistically independent) samples for the rerandomized secret remains open for $n\ge 3$. For $n=2$ the natural symplectic-orbit transformation---using two public matrices $S_1,S_2$ to split one sample into two---is far from fresh: the exact statistical distance to independent samples is at least $123/128$ for every pair $S_1,S_2\in\mathrm{Sp}(4,\F_2)$, with average $309/320$ (Experiment~192). A positive answer for larger $n$ would yield a tight multi-user security bound; a fully general negative answer would explain why the hybrid argument loses a factor $N$.

### 2. Limitations item 4 (\Cref{subsec:limitations})

After

> \item[\textbf{Loose multi-user reduction.}] \Cref{subsubsec:kem-multiuser} uses a hybrid argument losing a factor $N$. A tight reduction would require sample freshness for a rerandomized secret. Exact secret rerandomization \emph{is} possible---applying a public symplectic matrix $S \in \mathrm{Sp}(2n)$ to the public part of each sample maps $L$ to $S\cdot L$ while preserving labels---but \emph{sample freshness} is blocked: because $\mathbf{1}_L$ is non-linear, one cannot generate independent fresh samples for the new secret from the old public samples alone without knowing $L$. In practice the margin is comfortable ($q\gtrsim 2^{114}$), but the bound is not tight.

append

> For $n=2$ this obstruction is exact: splitting one sample with two public symplectic matrices leaves statistical distance at least $123/128$ from fresh independent samples (Experiment~192).

### 3. Optional: new small remark after the KEM multi-user reduction paragraph

If a dedicated remark is desired:

> \begin{remark}[Empirical freshness barrier for $n=2$]
> The public symplectic orbit transformation that maps $(x,b)\mapsto (Sx,b)$ preserves labels but not sample independence.  Exact enumeration for $n=2$ shows that two samples produced from one original sample by $S_1,S_2\in\mathrm{Sp}(4,\F_2)$ have SD at least $123/128$ from two independent fresh samples (Experiment~192).  Thus even the optimal public transformation fails to refresh samples in the smallest case.
> \end{remark}

## Classification

Evidence-grade result (exact for $n=2$ only; $n\ge 3$ open).  No security claim.
