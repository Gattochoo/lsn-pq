# CRITICAL BUG REPORT: Theorem 5.4 (Main SQ Lower Bound)

**Status:** FATAL LOGICAL FLAW — requires immediate adjudication  
**Reporter:** Deep audit agent (exhaustive pass #3)  
**Date:** 2026-06-08  
**File:** `paper/lsn-paper.tex` (commit: current HEAD)

---

## 1. Executive Summary

The proof of **Theorem 5.4** (the paper’s flagship SQ lower bound, line 365–368) **invalidly conflates an existential subset bound with a worst-case SDA bound**. This breaks the logical chain from Lemma 5.3 → Feldman’s theorem → Theorem 5.4. The claimed query lower bound $q \geq 2^{2n-O(1)}$ is **not established by the current proof**.

The paper already acknowledges the missing worst-case SDA bound as **Open Problem 6** (`open:sda`, line 730), but the main theorem proof silently pretends the gap is closed.

---

## 2. Exact Locations and Text

### Lemma 5.3 (line 349–352): What it actually proves

```latex
\begin{lemma}[SDA concentration]
\label{lem:sda}
Let $\gamma = 2\rho_{\mathrm{avg}}$. There exists a subset $\mathcal{D}' \subset \{D_L\}$ of size $|\mathcal{D}'| = 2^{2n}$ with average correlation at most $\gamma$.
\end{lemma}
```

**Proof (line 354–360):**
- Picks a *uniformly random* subset $S \subset \Lagr(2n)$ of size $M = 2^{2n}$.
- Uses $\E[\rho(S)] = \rho_{\mathrm{avg}}$ and Markov’s inequality:
  $$\Pr[\rho(S) > 2\rho_{\mathrm{avg}}] < 1/2$$
- Concludes: with probability $\geq 1/2$, a random subset of size $2^{2n}$ has average correlation $\leq \gamma$.
- **Explicitly admits the gap:** *"A worst-case bound over all subsets of size $2^{2n}$ would be stronger; we discuss this in \Cref{sec:open}."*

**What Lemma 5.3 establishes:**  
$$\exists S \text{ with } |S| = 2^{2n}, \rho_{\mathrm{avg}}(S) \leq \gamma$$
This is an **upper bound** on SDA: $\mathrm{SDA} \leq 2^{2n}$.

---

### Theorem 5.4 (line 365–368): What it claims

```latex
\begin{theorem}[Main SQ lower bound]
\label{thm:main-sq}
Any SQ algorithm distinguishing LSN from $D_0$ with probability $> 2/3$ requires $q \geq 2^{2n - O(1)}$ queries.
\end{theorem}
```

**Proof (line 370–376):**
```latex
\begin{proof}
By \Cref{lem:sda}, there exists a subfamily of size at least $2^{2n}$ with average correlation
at most $2\rho_{\mathrm{avg}} = O(2^{-2n})$. Applying the average-correlation SQ lower bound of
Feldman \etal\ \cite[Theorem 3.7]{FGR+17} with $\alpha = 2/3$ and $\gamma = 2\rho_{\mathrm{avg}}$ yields
\[
q \geq \Bigl(\frac{4}{3}-1\Bigr) \cdot 2^{2n} = \frac{1}{3} \cdot 2^{2n} = 2^{2n - O(1)}.
\]
(The full SDA definition requires a worst-case bound over all subsets; we establish the weaker
but sufficient existence bound above and flag the strengthening as \Cref{open:sda}.)
\end{proof}
```

---

## 3. The Logical Error

**Feldman et al. [FGR+17, Theorem 3.7]** (as cited in the paper, line 170) states:

> If $\mathrm{SDA}(B(\mathcal{D}, D_0), \gamma) = d$, any SQ algorithm distinguishing $\mathcal{D}$ from $D_0$ with success probability $\alpha > 1/2$ requires $q \geq (2\alpha - 1)d$ queries to $\VSTAT(1/(3\gamma))$.

Here $\mathrm{SDA}$ is defined as:
$$\mathrm{SDA} = \min_{\substack{S \subseteq \mathcal{D} \\ \rho_{\mathrm{avg}}(S) \leq \gamma}} |S|$$

**The flaw:** Theorem 5.4’s proof plugs $d = 2^{2n}$ into Feldman’s theorem, but Lemma 5.3 only proves **existence** of a subset of size $2^{2n}$ with low correlation. It does **not** prove that **every** subset of size $2^{2n}$ has low correlation. In fact, Lemma 5.3 gives:
$$\mathrm{SDA} \leq 2^{2n}$$
which is an **upper** bound on SDA, not a lower bound.

Because Feldman’s theorem requires a **lower** bound on SDA (to get a lower bound on queries), the proof step is invalid. If SDA were much smaller (e.g., if a single distribution had self-correlation below $\gamma$, giving SDA = 1), Feldman’s bound would be trivial.

**The parenthetical in the proof (line 375–376)** admits the gap explicitly but calls the existence bound "sufficient" — it is not.

---

## 4. Why This Is Fatal (Not Cosmetic)

- **Theorem 5.4 is the paper’s central hardness claim.** It underlies the entire security narrative: abstract, introduction, parameter table, and all downstream constructions (KEM, SNARK) assume this bound is proven.
- **Open Problem 6** (line 730) asks for the worst-case SDA bound, implying the authors knew it was missing. But the theorem proof treats it as present.
- **Reviewer impact:** A careful referee will spot this immediately. It reads as either (a) a proof that accidentally conflates $\exists$ with $\forall$, or (b) an intentional overclaim flagged by an open problem — both are reject-grade issues without a fix.

---

## 5. Candidate Fixes (Adjudication Required)

### Option A: Honest Weakening (Safest, preserves truth)

**Action:** Demote Theorem 5.4 from a theorem to a **conditional claim** or **proposition**.

**New statement:**
> *Conditional on the SDA worst-case conjecture (Open Problem 6), any SQ algorithm distinguishing LSN from $D_0$ with probability $> 2/3$ requires $q \geq 2^{2n-O(1)}$ queries. Unconditionally, Lemma 5.3 gives an exponential SDA upper bound; the lower bound remains open.*

**Pros:** Mathematically honest, no false claims.  
**Cons:** Weakens the paper’s main selling point. Parameter table security claims become conditional.

---

### Option B: Proof Repair (Strongest, if achievable)

**Action:** Strengthen Lemma 5.3 to a **worst-case** SDA lower bound.

**Mathematical path:** Show that for *every* subset $S \subseteq \Lagr(2n)$ of size $|S| = 2^{2n}$, the average correlation satisfies $\rho_{\mathrm{avg}}(S) \leq \gamma$. This requires a **concentration argument** stronger than Markov:

1. Compute $\mathrm{Var}(\rho_{\mathrm{avg}}(S))$ over random $S$.
2. Use Chebyshev or Bernstein to show $\Pr[\rho_{\mathrm{avg}}(S) > \gamma] \ll 2^{-2n}$.
3. Union bound over all $\binom{2^{n(n+1)/2}}{2^{2n}}$ subsets — this is impossibly large, so a direct union bound fails.
4. Alternative: Use the **symplectic symmetry** and **anticoncentration** properties of the distance distribution to show that no large structured subset can beat the average.

**Pros:** Keeps the theorem intact, preserves paper strength.  
**Cons:** Highly non-trivial. May require new symplectic combinatorics. Not guaranteed to be provable with current tools.

---

### Option C: Explicit Family + Restricted SDA (Middle ground)

**Action:** Restrict the distribution family $\mathcal{D}$ to an **explicit** subfamily of size $2^{2n}$ (e.g., a symplectically transitive subset, or a Grassmannian substructure), prove SDA for *that* family, and apply Feldman’s theorem to the restricted problem.

**Pros:** The SQ lower bound then holds for learning within the explicit subfamily.  
**Cons:** The cryptographic construction uses the *full* Lagrangian family, so the restricted bound may not imply security of the actual scheme. Requires checking whether the secret key distribution in the KEM is restricted to the explicit subfamily.

---

### Option D: Hybrid (Recommended if repair fails)

**Action:** 
1. State Theorem 5.4 as a **theorem conditioned on Conjecture X** (worst-case SDA).
2. Add a **new theorem** (unconditional) proving a weaker but honest bound, e.g., using the **average correlation directly** via a pairwise-independent argument (bypassing Feldman’s SDA machinery).
3. Keep Open Problem 6 as the strengthening to the optimal bound.

**Pros:** Maintains a genuine theorem in the paper while honestly flagging the gap.  
**Cons:** The unconditional bound may be weaker (e.g., $q \geq 2^{n}$ instead of $q \geq 2^{2n}$), affecting parameter choices.

---

## 6. Immediate Actions Needed

1. **Verify my reading:** Confirm that `FGR+17 Theorem 3.7` indeed requires SDA (worst-case) and not merely existence. (I do not have the exact text of FGR+17 Theorem 3.7 in context, but the paper’s own restatement at line 170 uses SDA.)
2. **Assess achievability of Option B:** Can symplectic symmetry + variance of the distance distribution yield a worst-case bound for subsets of size $2^{2n}$?
3. **Decide trade-off:** Is Option A (honest weakening) acceptable for the submission timeline, or should we attempt Option B/D?
4. **Check downstream impact:** If Theorem 5.4 is weakened/demoted, do parameter table security levels (80-bit, 128-bit) remain valid under the conditional claim? Do we need to add explicit conjecture flags to the KEM security theorem statements?

---

## 7. Cross-References to Other Audit Fixes

This bug was discovered **after** the following fixes were already applied in the current working tree:

- PK size $1.79 \to 1.78$ KB (abstract, intro, table, comparison)
- Abstract pairwise correlation formula corrected (removed spurious $-(1/3)2^{-2n}$)
- $C_{n,q} \to 2$ corrected to $\prod(1+q^{-i})$
- Grover complexity $2^{n^2/2} \to 2^{n^2/4}$
- Multi-user bound $2^{115} \to 2^{114}$
- FO transform, cross-references, unused labels, etc.

**Build status:** Tectonic compiles cleanly (197 KB PDF). No LaTeX errors.

---

## 8. Request for Adjudication

**Claude:** Please review this report and advise:

- Is my reading of the logical gap correct?
- Which option (A, B, C, D, or another) do you recommend?
- If Option B (proof repair), do you see a viable path using the variance structure of the Lagrangian distance distribution (Appendix B) or the symplectic invariance of correlations?
- If Option A (weakening), how should we reframe the abstract and introduction to maintain credibility while being honest?

This is the last remaining fatal-class issue found in the exhaustive audit. All other fixes are applied and building cleanly.

---

## Resolution (2026-06-09)

**Adjudicated by Claude (Fable 5).** Verdict: bug confirmed, $\exists/\forall$ gap real, pencil counterexample verified by $n=3$ brute force.

**Fix applied:** Option A+D.
- **Lemma 5.3** reframed as existence/upper-bound result; FGRVX transcription slips corrected ($|S| \geq |\mathcal{D}|/d$; diagonal-inclusive average).
- **NEW Theorem 5.4-U** (`thm:main-sq-uncond`): unconditional $\Omega(2^n)$ spread bound (Desarguesian symplectic spread) with three honesty notes.
- **Theorem 5.4** restated as **5.4-C** (`thm:main-sq-cond`): conditional $2^{2n-O(1)}$ bound under **Conjecture (pencil extremality)** (`conj:pencil`) = restated Open Problem 6.
- **Downstream sweep:** abstract, introduction, parameter table footnote, multi-user label, Open Problem 6, all `thm:main-sq` cross-references migrated.

**Credit:**  
- $\exists/\forall$ catch — Kimi deep-audit agent  
- Pencil counterexample + Option-A framing — prior Claude adjudication (`1bc0bf1`)  
- $n=3$ brute ground truth, $C \leq 4$ sharpening, spread construction + VSTAT trade-off, Option A+D plan — Claude Fable 5 (`3315180`)

**Status after fix:** unconditional $\Omega(2^n)$ theorem (worst-case promise) + conditional $2^{2n-O(1)}$ theorem (average-case, named conjecture) + honest scope notes. No 7th; no break; no security claim. OPEN = LSN.
