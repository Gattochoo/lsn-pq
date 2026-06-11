# OP8 Obstruction Note — Final DRAFT

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (final per DIRECTIVE-KIMI-op8-final.md; replaces `2026-06-12-KIMI-op8-bridge-attempt.md`).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## §0. Pinned interface summary (no re-derivation)

All items below are quoted or directly inferred from the pinned sources (`2026-06-12-CLAUDE-klp25-formal-theorem-pins.md`, `2026-06-12-CLAUDE-klp25-definition-pins.md` §1).

| | **OUR membership-LSN** | **THEIR stabilizer-decoding LSN (KLP+25)** |
|---|---|---|
| **Public structure** | None. | Matrix $[A \mid B]$: $A \in \F_2^{2n \times n}$ with pairwise symplectically orthogonal columns spanning a Lagrangian; $B \in \F_2^{2n \times k}$ isotropic, jointly full-rank with $A$. The concatenated $[A \mid B]$ is **not** isotropic (dimension $n+k > n$). |
| **Secret** | Lagrangian $L \in \Lagr(2n)$. Entropy $\Theta(n^2)$ bits (Eq.~`eq:lagr-count`). | Logical string $y \in \F_2^k$ ($k \ge 1$). Entropy $k$ bits. |
| **Sample format** | Noisy membership bit: $b = \mathbf{1}_L(a) \oplus e$, with $a \sim \mathrm{Unif}(\F_2^{2n})$, $e \sim \mathrm{Bernoulli}(p)$ i.i.d. per label. | Noisy codeword: $w = [A \mid B] \cdot [r; y] + e \in \F_2^{2n}$, with $r \sim \mathrm{Unif}(\F_2^n)$ junk, $e$ = symplectic representation of depolarizing noise. |
| **Junk / free register** | None. | $r \in \F_2^n$ (random, independent per sample in $\mathrm{LSN}^m$). |
| **Freshness per sample** | Fresh $(a_i, e_i)$ for each label. | **LSN** (no superscript): single sample $(A,B,r,e)$. **$\mathrm{LSN}^m$**: fresh $(A_i,B_i,r_i,e_i)$ per sample; only $y$ is fixed. |
| **External hardness** | Our SQ lower bounds (§Barriers). | Thm 6.6 (KLP+25): constant-rate Decision LPN $\le$ **single-sample Search LSN**$(k,n,p)$ with probability $\ge 1/2^k + 1/\mathrm{poly}(n)$. |

**Key pinned fact for §3:** KLP+25's Lemma 6.5 (p.65) explicitly states that naive secret$\to$secret embedding is infeasible due to dimension mismatch (e.g. $n$-bit secret into $k=1$ LSN secret), and they **bypass this via junk embedding**: "Our basic strategy is to embed the sympLPN data $(A,z)$ into the junk matrix and vector of one of the samples." This is an in-paper counterexample to the inference "dimension/type mismatch $\Rightarrow$ obstruction". Our membership-LSN has **no junk register**, so any embedding must use other degrees of freedom.

---

## §1. Direction 2 (THEIR $\le$ OUR), source = single-sample Search LSN

**Why this source matters:** Thm 6.6 pins the external hardness to single-sample Search LSN. A reduction designer may therefore treat this as the hardness-bearing variant.

### Information-budget wall

Our membership-LSN interface requires secret entropy $\Theta(n^2)$ bits (Eq.~`eq:lagr-count`) divided by at most 1 bit per noisy label $\Rightarrow$ **$m = \Omega(n^2)$ noisy labels required**.

A single-sample LSN instance carries only **$2n$ bits** of $y$-correlated data: the noisy codeword $w = [A \mid B][r;y] + e$. Rerandomisation of the same $w$ (e.g. applying a public symplectic transform $S$ to obtain a new query point $a = Sw$) is a deterministic function of $w$; it cannot manufacture statistically independent noise. Producing $m \gg 2n$ i.i.d.-noise membership labels from $2n$ bits is the **same correlated-noise wall as OP9 / `lem:m2`** (the fixed $2n$-bit symplectic noise vector $e$ of their problem is literally the "fixed noise" obstacle of OP9).

**★ Honesty note (mandatory):** This unification means "single-sample OP8 reduces to the *same unproven lemma* as OP9" — i.e. both would be resolved if one could prove that a fixed $2n$-bit noise vector cannot supply $\Omega(n^2)$ independent noisy membership labels. It is **not** a proof of either statement. `lem:m2` is unproven, which is exactly why OP9 remains open.

---

## §2. Direction 2 (THEIR $\le$ OUR), source = $\mathrm{LSN}^\mathrm{poly}$ (multi-sample)

Fresh noise $e_i$ per sample **collapses** the information-budget wall: each sample provides a fresh $2n$-bit noise vector, so $m$ labels can in principle be supplied by $m$ samples. The remaining obstruction is **frame alignment**:

- $y$ arrives in **different public frames** $[A_i \mid B_i]$ per sample.
- Our target requires **one fixed hidden Lagrangian** $L$.
- Any natural map that aligns frames uses only public data ($[A_i \mid B_i]$) $\Rightarrow$ yields a public Lagrangian $\Rightarrow$ membership becomes publicly decidable $\Rightarrow$ hiding fails.

**Critical caveat (mandatory):** This blocks *natural* maps only; it is **not an impossibility proof**. The design space for $\mathrm{LSN}^\mathrm{poly} \to$ membership-LSN is genuinely open. The rev1 phrase "BROKEN likely" was overconfident and is retracted.

---

## §3. Embedding locus analysis (forced by Lemma 6.5)

KLP+25's authors explicitly write that "the usual strategy [secret$\to$secret] is infeasible in our case, as the dimensions are completely mismatched" and they **embed into junk instead**. Our membership-LSN has **no junk register**, so we must examine the remaining loci where their data could embed. For each locus we ask: "If we embed their $(y, w)$ here, how does the map live or die?"

### (i) Query points $a_i$

Our definition requires $a_i \sim \mathrm{Unif}(\F_2^{2n})$ marginally. For a fixed $y$, their noisy codeword $w = [A \mid B][r;y] + e$ is uniform over the $n$-dimensional coset $\mathrm{colspan}(A) + B y$ (not over all of $\F_2^{2n}$), since $r$ varies only over $\F_2^n$ while $y$ is fixed. Thus **marginal uniformity over $\F_2^{2n}$ fails already at the single-sample level**: $w$ is confined to a set of size $2^n$ inside $2^{2n}$ ($n=2$: $4/16$; $n=3$: $8/64$). Full-rankness of $[A \mid B]$ guarantees uniformity only when $[r;y]$ is jointly uniform.

However, the membership label $\mathbf{1}_L(a_i)$ must correlate with $y$. For a fixed secret Lagrangian $L$, the label depends only on $L$. To recover $y$ from $L$, we need $L = L(y)$, which forces us into locus (iii). Moreover, if the reduction algorithm must choose $L$ without knowing $y$ in advance, the query distribution must simultaneously serve all possible $y$ — a joint uniformity condition that is stricter than marginal uniformity and is not automatically satisfied by their sampling procedure.

### (ii) Label noise $e_i$

Our model requires Bernoulli$(p)$ i.i.d. noise per label. Their single-sample model provides one $2n$-bit noise vector $e$. Mapping each label's noise to a coordinate (or function) of $e$ makes the label noise **deterministically correlated** across labels, since $e$ is fixed per sample. This is exactly the correlated-noise wall of §1 / OP9.

In the multi-sample setting, fresh $e_i$ per sample can supply fresh noise per label. But then the reduction must map multi-sample structure to a single secret Lagrangian, returning us to the frame-alignment wall of §2.

### (iii) Partial structure of the secret Lagrangian

Can we set $L = L(y; \mathrm{coins})$ where only some directions of $L$ depend on $y$?

**Entropy accounting:** $y$ carries $k$ bits; $L$ carries $\Theta(n^2)$ bits. The remaining $\Theta(n^2) - k$ bits must be filled by $\mathrm{coins}$ (randomness independent of $y$). For $L(y; \mathrm{coins})$ to be uniformly distributed over $\Lagr(2n)$ for fixed $y$, the coins would need to encode $\Theta(n^2)$ bits of uniform Lagrangian structure — but then $L$ is essentially independent of $y$, and a solver recovering $L$ learns almost nothing about $y$.

Conversely, if $L$ is concentrated on a small set conditioned on $y$ (e.g. all Lagrangians containing a fixed isotropic subspace $W(y)$), the marginal distribution of $L$ is far from uniform over $\Lagr(2n)$. The solver's success probability on non-uniform secrets is not covered by our SQ lower bounds, which assume uniform $L$. Even if we accept non-uniformity, extracting $y$ from $L$ requires inverting $L(y; \mathrm{coins})$. If coins are public, $L(y)$ is public given $y$ and the reduction adversary learns nothing. If coins are secret, they add entropy that the solver must also recover, worsening the information budget of §1.

### (iv) Absence of junk — summary

In KLP+25, the junk register $r \in \F_2^n$ provides $n$ bits of free randomness per sample to hide sympLPN structure. Our membership-LSN has no analogous freedom: the query point is either adversarial or uniform, and the secret $L$ has no auxiliary register.

The junk-absence is **not an obstruction by itself**, but it forces all embedding attempts into the narrow channels of (i)–(iii). (i) is marginally satisfiable but fails at joint uniformity; (ii) hits the correlated-noise wall in the single-sample regime; (iii) faces an entropy-uniformity tradeoff. Thus Lemma 6.5's bypass route is **unavailable** to us, and the remaining routes each carry their own walls.

---

## §4. Direction 1 (OUR $\le$ THEIR)

**Mirror obstruction (code visibility).** To build their instance from ours we need a public matrix $[A \mid B]$ with $\mathrm{colspan}(A) \approx L$, but $L$ is secret. Any natural map that produces $[A \mid B]$ from the public parameters of our problem reveals $L$. This is the symmetric counterpart of §2's frame-alignment wall: their problem *requires* public structure that encodes our secret.

As in §2, this blocks natural maps only; a clever reduction might generate $[A \mid B]$ without revealing $L$ (e.g. using a pseudorandom generator with $L$ as seed). No impossibility proof is known.

---

## §5. Verdict table (variant $\times$ direction)

| Direction | Source variant | Wall / obstruction | Verdict |
|---|---|---|---|
| **THEIR $\le$ OUR** | Single-sample Search LSN (hardness carrier, Thm 6.6) | Information-budget wall: $2n$ bits of $y$-correlated data vs $\Omega(n^2)$ labels required. Same wall as OP9 `lem:m2`. | **Blocks natural maps.** Reduces to the **same open lemma** as OP9. |
| **THEIR $\le$ OUR** | $\mathrm{LSN}^\mathrm{poly}$ (multi-sample) | Frame-alignment wall: $y$ in fresh public frames per sample vs fixed hidden Lagrangian. | **Blocks natural maps.** Design space **OPEN**. |
| **OUR $\le$ THEIR** | — | Code-visibility (mirror): public $[A \mid B]$ needs $\mathrm{colspan}(A) \approx L$, but $L$ secret. | **Blocks natural maps.** |
| Single-sample Decision$\to$Search | — | KLP+25 themselves leave this open (§5.2, p.45): "it is an open question as to whether the equivalence holds with a single sample." | **OPEN** (external confirmation of subtlety). |

**Forbidden vocabulary enforced:** No "impossible", no "BROKEN", no probability-of-failure claims. Only "blocks natural maps", "OPEN", "reduces to the same open lemma".

---

## §6. Proposed text for the paper (English; Claude to verify & integrate)

### For `subsec:two-forms` (positioning item, upgraded)

> The two LSN formulations differ in interface, not merely in syntax. KLP+25's stabilizer-decoding LSN provides a noisy codeword in a public frame $[A \mid B]$ with a $k$-bit secret logical string $y$; our membership-LSN provides noisy membership bits for a secret Lagrangian $L$ with no public structure. The external hardness result (constant-rate LPN $\le$ Search LSN, Thm 6.6 of KLP+25) attaches to the single-sample variant, where an information-budget wall---shared with Open Problem 9---blocks natural reductions to our interface: a single noisy codeword carries $2n$ bits of $y$-correlated data, while our interface needs $\Omega(n^2)$ noisy labels. In the multi-sample variant, fresh noise per sample collapses this wall, leaving a frame-alignment obstruction: $y$ arrives in different public frames per sample, while our target requires a single fixed hidden Lagrangian. Neither obstruction is an impossibility proof; the design space for embedding their data into our interface remains open, and the absence of a junk register in membership-LSN forces any such embedding into the narrow channels of query distribution, label noise, or partial Lagrangian structure.

### For `sec:open`, OP8 item (upgraded)

> **Membership-LSN $\leftrightarrow$ stabilizer-decoding LSN bridge.** Relate our membership formulation (secret Lagrangian, no public matrix) to the LSN of KLP+25 (public stabilizer matrix $[A \mid B]$ with a Lagrangian $A$-block, noisy-codeword samples, secret logical string). The external hardness (constant-rate LPN $\le$ Search LSN, Thm 6.6) is pinned to the single-sample variant. A reduction THEIR $\le$ OUR would need to embed a $k$-bit secret $y$ into our $\Theta(n^2)$-bit secret Lagrangian $L$ without a junk register---KLP+25's Lemma 6.5 bypasses dimension mismatch via junk embedding, which our formulation lacks. Single-sample source hits an information-budget wall (same open lemma as OP9); multi-sample source hits frame alignment. Direction 1 (OUR $\le$ THEIR) is blocked by code visibility. No impossibility claim; all directions remain open.

---

## Gate check

- **No closure claim:** All verdicts are "blocks natural maps" or "OPEN", never "impossible".
- **No break:** Obstruction analysis does not disclose scheme weakness.
- **No security claim:** We do not claim LSN hardness.
- **No `paper/` edits:** This document is meta-only; §6 is proposed text for Claude integration.
- **No numbers fabricated:** This is a structural analysis; no numerical claims are made.
- **KLP+25 pins cited:** All definitions and theorems are referenced to the pinned source documents.

No closure; no break; no security claim. OPEN = LSN.
