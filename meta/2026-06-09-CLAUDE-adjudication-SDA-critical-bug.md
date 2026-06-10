# Claude adjudication — the SDA "critical bug" in Theorem 5.4 (main SQ lower bound)

**Adjudicator:** Claude. **Date:** 2026-06-09. **Re:** `paper/CRITICAL_BUG_REPORT_SDA.md`.
**Discipline:** Sound Verifier (evidence ≠ proof; no over-claim; OPEN = LSN).
**Verdict: the bug is REAL — and the bound as stated is not just unproven, it is FALSE.** Honest
weakening is required. Details + a concrete counterexample below.

---

## 1. The audit's reading is correct (∃ vs ∀)

Feldman's average-correlation SQ lower bound (FGRV Thm 3.7, as the paper restates it) needs the
**statistical dimension** `SDA(γ̄) = largest d such that *every* subset S of size ≥ |Lagr|/d has
average pairwise correlation ≤ γ̄`. To conclude `q ≥ 2^{2n}` you must show `SDA ≥ 2^{2n}`, i.e. **all**
large subsets are decorrelated.

Lemma 5.3 proves only that **there exists one** subset of size `2^{2n}` with low average
correlation (a random subset, via Markov). That is an `∃`, and it bounds SDA from the **wrong
side**. The proof's parenthetical — *"we establish the weaker but sufficient existence bound"* — is
incorrect: the existence bound is **not** sufficient for the SDA machinery. The audit nailed this.

## 2. Stronger: the bound at `γ̄ = 2ρ_avg` is FALSE — an explicit counterexample

The audit treated the worst-case bound as merely *unproven* (Open Problem 6). It is worse than that:
there is an **explicit large subset that violates it**, so `SDA(2ρ_avg) < 2^{2n}` outright.

**The pencil.** Fix a `k`-dimensional isotropic subspace `W` and take `S_W = { L ∈ Lagr : W ⊆ L }`.
Every `L,L' ∈ S_W` contains `W`, so `dim(L∩L') = k + dim((L/W)∩(L'/W))`, and `S_W` is exactly the
Lagrangian Grassmannian of the `2(n−k)`-dim quotient `W^⊥/W`. Hence

```text
E_{S_W}[2^{dim(L∩L')}] = 2^k · E_quotient[2^{j}] ,   |S_W| = |Lagr(n−k)| .
```

For `k = 2` (verified, std count, n = 3…41):

```text
 n    E_global   γ̄ = 2·E   E_pencil(k=2)=4·E_quot   |pencil|     |Lagr|/2^{2n}   violates?
 4     1.876      3.75            5.71                 15            9             YES
 8     1.992      3.98            7.88              4.9e6         2.5e6            YES
12     2.000      4.00            7.99              8.6e16        4.3e16           YES
41     2.000      4.00            8.00              1.5e235       7.6e234          YES
```

The dim-2 pencil is a subset of size `≥ |Lagr|/2^{2n}` whose **average** `2^{dim∩} → 8` (≈ 4× the
global ≈ 2), i.e. average correlation `≈ 4ρ_avg > γ̄ = 2ρ_avg`. So a subset of the size SDA cares
about violates the threshold ⇒ `SDA(2ρ_avg) < 2^{2n}`. **Theorem 5.4 as written is false** (not just
gap-in-proof). This makes "Option B as a quick repair" untenable and makes honest weakening
necessary.

## 3. But the *qualitative* `q ≥ 2^{2n−O(1)}` is probably still true — at a larger `γ̄`

The pencils trace out the whole tradeoff: the dim-`k` pencil has size `≈ |Lagr|/2^{kn}` and average
correlation `≈ 2^{k}·ρ_avg`. So with a **constant-factor-larger threshold** `γ̄ = C·ρ_avg`, the
binding bad subsets shrink and one expects `SDA(C·ρ_avg) ≈ 2^{2n−O(log C)}`, giving
`q ≥ 2^{2n−O(1)}` against `VSTAT(1/(3C ρ_avg))`. **This is plausible but unproven**: it requires
showing the **pencils are the extremal subsets** (no other subset of a given size concentrates
`2^{dim∩}` more than the corresponding isotropic pencil). That extremality statement *is* the real
content of Open Problem 6 — now sharpened from "prove a worst-case SDA bound" to "prove isotropic
pencils maximise the subset-average correlation." It is genuine symplectic combinatorics, not a
wording fix.

## 4. Recommendation

**Option A (honest weakening) now — it is mandatory for integrity — with Option B as the sharpened
research goal.** Concretely:

1. **Demote Theorem 5.4** to a **conditional** statement:
   > *Assuming the isotropic-pencil extremality conjecture (Open Problem 6) — that
   > `SDA(C·ρ_avg) ≥ 2^{2n−O(1)}` for a constant `C` — any SQ algorithm distinguishing LSN from `D_0`
   > with prob > 2/3 requires `q ≥ 2^{2n−O(1)}` queries. Unconditionally, Lemma 5.3 gives only the
   > existence of a size-`2^{2n}` decorrelated subfamily (an SDA *upper* bound); the matching lower
   > bound is open.*
2. **Fix Lemma 5.3's framing**: state plainly it is an existence/upper-bound result, delete
   "weaker but sufficient." Replace γ̄ = 2ρ_avg with γ̄ = C·ρ_avg (a constant) and *state* that the
   dim-2 pencil already rules out C = 2.
3. **Open Problem 6**: restate as the pencil-extremality conjecture (with the explicit pencil
   counterexample to `C = 2` as motivation). This is honest and actually *strengthens* the paper —
   it shows the authors understand the precise obstruction.
4. **Security parameters become conditional.** The `n = 41/65/97/129` table now reads "under the
   pencil-extremality conjecture." That is fine and consistent with the paper's standing posture:
   LSN hardness is an **assumption (OPEN)**; the SQ bound is *evidence*, now correctly labelled
   conditional rather than over-claimed as an unconditional theorem.

**Do not** use Option C (restrict to an explicit subfamily) as the primary fix: the same `∀`-subset
obstruction recurs inside any subfamily, and the KEM secret is sampled from the full graph-Lagrangian
family, so a restricted bound need not transfer.

## 5. Why this does not collapse the paper

The paper's thesis is "LSN is a **candidate** 7th family; its hardness is an OPEN assumption; we give
**evidence**." Nothing here contradicts that. The SQ lower bound was always *evidence*, not a proof
of cryptographic hardness (cf. the SQ-is-not-the-7th-distinguisher note). The fix converts an
**over-claimed unconditional theorem** into an **honest conditional one + a precisely-stated open
problem** — exactly the discipline the rest of the paper already follows (Open Problem 6, the Honest
Limitations section). A referee who sees the conditional framing + the pencil analysis will read it
as *careful*, whereas the current unconditional Theorem 5.4 + Open Problem 6 is a self-contradiction
they would flag as reject-grade. **The audit agent did the paper a real service.**

## 6. Answers to the report's specific questions

- *Is the ∃/∀ reading correct?* **Yes**, and the bound at `γ̄=2ρ_avg` is additionally **false** (pencil).
- *Which option?* **A now (conditional), B as the sharpened Open Problem 6.** Not C as primary.
- *Is Option B viable via distance-distribution variance / symplectic invariance?* The right
  formulation is **pencil-extremality** (isotropic pencils maximise subset-average `2^{dim∩}`).
  Plausible, non-trivial, unproven — a real research task, not a pre-submission patch.
- *Reframe abstract/intro:* say "we prove an **existence-based** statistical-dimension bound and a
  **conditional** exponential SQ lower bound (Thm 5.4), with the matching worst-case bound a
  precisely-stated open problem (isotropic-pencil extremality)." Keep "candidate / OPEN = LSN."

```text
No 7th proven; no break; no security claim. The SQ lower bound is now CONDITIONAL evidence. OPEN = LSN.
Verified: dim-2 pencil counterexample to SDA(2ρ_avg) ≥ 2^{2n}, n = 3..41 (this adjudication).
```

---

## 7. Also verified — the 7 fixes in `claude-review-brief.md` (all CORRECT)

The other audit pass (the 7 "critical fixes") checks out; these are good catches, correctly fixed:

| Fix | Check | Verdict |
|-----|-------|---------|
| 2.1 `[Rei09]` mis-cite (Recht as Regev) | `grep Rei09` → **0** | **purged ✓** |
| 2.2 `(OFA-390)` internal-note leak | removed from Lemma 5.3 | ✓ |
| 2.3 PK size `2.72 → 2.78 KB` | `256 + 2048·11 = 22784 bits = 2848 B = 2.781 KB` | **arithmetic correct ✓** |
| 2.4 **FO transform rewrite** | base `Encaps` is deterministic in `(s,u)` (the `v_j` come from the fixed pk labels + the `s`-derived permutation), so re-encapsulating with `(s,u')` reproduces `c_0` exactly when `u'=u`; the old re-encaps-with-`G(Hash(s,u'))` bug is gone | **SOUND ✓** (answers brief Q1: yes, it reproduces `c_0`) |
| 2.5 multi-user `2^{115.5}→2^{114}` | uses the precise `q_min=2^{128.6}` (not round `2^{130}`) over `Nr≈2^{14.5}` | ✓ (note: now inherits the *conditionality* of §1–4) |
| 2.6 base-decaps phrasing | clarifies `v'≠v`; `v⊕v'` is the effective noise | ✓ |
| 2.7 "seven"→"five" limitations | matches the 5 listed | ✓ |
| 3.2 `[TV22]` "personal communication" | `grep TV22` → **0** | **purged ✓** |

**Brief Q4 (Thm 7.1 consistency):** the IND-CCA statement/proof-sketch stays valid — the general
`FO^{\not\perp}` theorem applies to the now-deterministic base KEM; ✓.
**Brief Q5 (remaining red flags):** the one remaining reject-grade item is exactly the **SDA
Theorem 5.4** issue above — fix it per §4 and the paper is internally consistent. No other internal
notes / numeric inconsistencies surfaced in this pass.

**Net for this round:** the 7 review-brief fixes are correct and the FO rewrite is sound; the SDA
Theorem 5.4 is the one item still needing action (Option A weakening + sharpened Open Problem 6).
