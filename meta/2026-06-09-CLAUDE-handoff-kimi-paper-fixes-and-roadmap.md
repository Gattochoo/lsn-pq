# Kimi handoff — paper fixes (E1–E3) + forward roadmap

**From:** Claude (adjudicator). **To:** Kimi. **Date:** 2026-06-09.
**Ref:** `2026-06-09-CLAUDE-adjudication-kimi-A1A4-and-paper.md` (`d1972019`).
**Context:** A1–A4 are all done well; the paper is disciplined. Part A = the small paper fixes to
apply now. Part B = recommended next work, prioritized. **Discipline:** Sound Verifier; OPEN = LSN;
if anything ever *claims* a worst→avg success or a 7th-source, treat as ≈0, re-verify 10×, alert
the user first.

---

## PART A — paper fixes to apply now (`lsn-paper-draft.tex`)

**E1 [real error] — Table 1 search-space exponent.** Line ~55: `2^{n²+O(n)} → 2^{n²/2+O(n)}`.
Reason: `|Lagr(2n)| = ∏_{i=1}^n(2^i+1)`, so `log₂|Lagr| ≈ n(n+1)/2 ≈ n²/2` (e.g. `n=41 → 862`,
not `1681`). The asymptotic `SD = 2^{Ω(n²)}` is unchanged (only the explicit figure was wrong).
*(Also scan the rest of the corpus for any other "`2^{n²+O(n)}`" / "`≈n²`" Lagrangian-count and fix
to `n²/2`; the K3 doc and A1 may have the same slip.)*

**E2 [consistency] — §7 Table, 128-bit row.** `n=64 → n=65`. `n=64` gives `log₂q_min ≈ 2·64−0.6 =
127.4` (short of 128); `n=65 → 129.4` clears it, and matches B1 / the F_q table.

**E3 [consistency] — Lemma 5.2 (Exact Correlation).** It uses `(1-2p)²`, but the corrected K3 /
OFA-389 use the noise-only-`D_0` factor `(1-2p)²/(p(1-p))`. Either (a) harmonize Lemma 5.2 to `D_0`,
or (b) state explicitly that §4's `⟨·,·⟩` is taken w.r.t. the **uniform** base. Pick one and use it
in K3, the paper, and F_q §3.1 consistently. (Asymptotics unaffected.)

**Minor:**
- §5 (Quantum): "K4 = CLOSED" → "all *tested* quantum attacks blocked; **no** quantum-security
  proof." Rewrite/relocate the garbled "BKW `2^{n²/b}`" bullet (BKW is a *classical* LPN algorithm).
- §8 P3: "sympLPN→LPN (non-linear)" → "**beyond polynomial feature maps**" (the polynomial class is
  *blocked* by P3; only the adaptive/algebraic class is open).
- §1.3 line 63: "the *quantum* extra beyond classical LPN" → "the **symplectic** extra" (`S_A=0` is a
  classical algebraic constraint).
- Author line `(Claude, Codex, Kimi)`: AI-as-author is a venue-policy choice — flag for the human
  author to decide attribution before any submission.

**Done when:** E1–E3 applied; one noise-factor convention used everywhere; minors addressed.

---

## PART B — recommended next work (prioritized)

### R1 [theory, highest leverage] — make the SDA argument referee-tight

Your self-assessment correctly flags that the statistical-dimension step rests on a *probabilistic
existence* argument and an average (not worst-case) correlation. Close this — it is the paper's load
-bearing theorem and the most likely referee objection.
- **Concrete:** state the bound via Feldman's **average-correlation** statistical dimension (SDA),
  which is *designed* to use `ρ_avg` and absorb a sparse high-correlation tail — so the `j≥4` /
  adjacent-pair tail (count `~10³` ppm, weight `~1.12%`, OFA-390) is handled *by the theorem*, not by
  a hand-wave "negligible." Verify the SDA preconditions explicitly and drop the existence argument.
- **If you want a stronger statement:** prove a *high-probability* correlation bound — for a `1−o(1)`
  fraction of Lagrangian pairs, `|⟨D_L,D_{L'}⟩| ≤ O(2^{-2n})` — via the exact q-binomial tail
  (OFA-390 numbers). That upgrades "average" to "typical," which referees prefer.
- **Done when:** the main theorem cites the correct SDA variant, the tail is handled inside the
  theorem, and no "there exists a subfamily" step remains.

### R2 [validation, the single biggest gap] — Python experiments (leave Rust/circuits to Codex, 06-11)

Your assessment names "zero experimental validation" as the project's largest weakness. Two
Python-level experiments are high-value and within reach now:
- **R2a — LSN sample-complexity curve.** At `n = 3,4,5` (brute/ML decoder, `p=1/4`), measure the
  number of samples needed for recovery and check it tracks the `~2^{2n}` floor. This *empirically
  grounds* the hardness claim that the paper currently only asserts asymptotically.
- **R2b — polar Monte-Carlo.** Simulate the concatenated code (`r=7`, `N=2048`, BSC) and measure the
  empirical block-error rate; confirm it is consistent with the `2^{-80}` design point. *(I already
  verified the Arıkan–Bhattacharyya bound analytically — `2^{-80}/2^{-148}` — so this is
  confirmation, not discovery; but a sim closes the "unverified assumption" objection.)*
- **Done when:** two committed scripts + a short results note; the paper can cite real numbers.
- *Hand to Codex (returns 06-11):* Rust KEM reference impl, SNARK circuit (validate P5's `O(n²)`
  constraints), KAT vectors. Don't block on these.

### R3 [the honest 7th case] — sharpen "the symplectic structure is reduction-inert"

This is where the 7th claim actually lives (A5), and it is *writable* now (vs. the adaptive-reduction
impossibility, which is ≈0 in-house). Make the Ring-LWE-precedent argument tight:
- Formalize that `S_A=0` is **public and x-free** (lane-I / OFA-349 / my §3: secret-recovery ≡ LPN),
  so the symplectic structure **cannot be the lever of any reduction to LPN** — it adds no
  x-information for an attacker and no usable handle for a reductionist.
- Frame exactly as Ring-LWE (accepted as lattice-family by *source*, not by reduction): LSN's source
  (symplectic self-duality `F_Ω[1_L]=2^n1_L`, Lagrangian-subspace secret, stabilizer degeneracy) has
  no LPN analogue. Label it **conjecture** (source novelty is not decidable by reduction analysis).
- **Done when:** one tight paper subsection that a skeptic reads as "the 7th case rests on source +
  blocked-reductions + SQ evidence," not on a forthcoming impossibility proof.

### R4 [paper completeness] — expand the two thin sections + proper LaTeX

- **Quantum (§5/§7):** currently thin (and partly garbled). Add a concrete statement of what is and
  is *not* covered: Weil/Fourier-sampling collapse (cite the experiment), HSP-non-applicability, and
  an explicit "no quantum lower bound is claimed; quantum hardness is conjectural, as for LWE/LPN."
- **Primitives (§ on B1/P5):** give B1's corrected parameters and the (now clean) decisional-LSN
  IND-CPA hop; for P5 state honestly "circuit constraint count `O(n²)`, not yet implemented."
- Finish the **LaTeX** conversion (the `.tex` is skeletal; your assessment notes Markdown-not-LaTeX).

### R5 [do NOT do]

- **Do not chase "adaptive degree-2 SQ"** — K3 already governs all SQ; it is subsumed, not open
  (your revised T2.2 §6 says this correctly).
- **Do not attempt to *close* the adaptive-reduction / `LSN⊀LPN` question in-house** — it is ≈0 and
  is the standing external open problem. Keep it as P1/P3 open; route 7th-energy into R3 (source) and
  R1 (rigor), which actually move the paper.

---

## Priority order

```text
1. PART A  (E1–E3 paper fixes)         — now; mechanical; blocking for the draft
2. R1      (SDA referee-tightness)     — the main-theorem gap; highest leverage
3. R3      (source-inertness subsection)— the honest 7th case; writable now
4. R2      (Python validation)         — biggest weakness; grounds the claims
5. R4      (quantum/primitives + LaTeX) — completeness
   R5: don't chase adaptive-deg-2 SQ or try to close LSN⊀LPN in-house.
```

No 7th; no break; no security claim. **OPEN = LSN.**
