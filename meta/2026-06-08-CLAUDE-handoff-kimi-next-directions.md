# Kimi research handoff — next directions after K3/P1–P5/A1–A2

**From:** Claude (math / adjudicator). **To:** Kimi. **Date:** 2026-06-08.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; OPEN = LSN; no
security claim). If any task ever *claims* a worst→avg success or a 7th-source: treat as ≈0,
re-verify 10× adversarially, alert the user immediately.

---

## 0. Where we are (read first)

```text
SECRET-RECOVERY layer   :  ≡ LPN-grade.  CLOSED.   (lane-G#1 degree-1 ⊕ lane-I/OFA-349 degree-2 x-free)
DISTRIBUTIONAL layer    :  where 7th lives.  OPEN =  LSN ⊀ LPN.
   · linear class       :  IMPOSSIBLE (external, Lu–Poremba–Quek–Ramkumar App. D)
   · polynomial class   :  BLOCKED (P3)
   · adaptive class     :  OPEN  ← the only in-house lever on 7th
   · source novelty     :  CONJECTURE (symplectic / self-dual / x-free structure)
worst→avg (foundation)  :  natural routes CLOSED (P1 + transport-floor + encode all-or-nothing). Not the 7th axis.
K3 security bug + over-claim : FIXED & verified (7b3aef3c). K3 proof-completeness items: still pending (§1).
```

**The pivotal fact (seed `00a7620b`):** the **SQ lower bound is not the 7th-distinguisher** —
LPN/LWE have SQ bounds too, and sympLPN secret-recovery is ≡ LPN-grade. So finishing the SQ proof
is **rigor/credibility**, not 7th progress. Keep "rigor work" and "7th-axis work" separate below.

---

## 1. PRIORITY 1 (rigor, tractable) — finish K3 as a clean, complete SQ theorem

**Why:** it is the paper's backbone and removes the "incomplete proof" weakness. Codex already
localized every remaining gap (OFA-388/389/391/394–396). This is mostly careful write-up + a
correct citation, not new mathematics.

**Tasks**
- **T1.1 — Lemma 3.1 via the likelihood-ratio object** (not raw support; OFA-388 finding 5).
  Use Codex OFA-389: against the noise-only background `D0` (`x` uniform, `y∼Bern(p)`), a pair with
  `dim(L∩L')=j` has `corr_base = 2^j/2^{2n}`, calibrated `corr_p = corr_base·(1−2p)²/(p(1−p))`
  (`=4/3·corr_base` at `p=1/4`). Write this as a proven lemma.
- **T1.2 — Exact `ρ_avg`** with the **corrected** count (`E[2^j]→2`, already fixed in
  `30-k3`). Floors are `≈2n−1` (OFA-391), not the old buggy values.
- **T1.3 — Invoke the statistical-dimension theorem** (Feldman et al.) with that `ρ_avg`/`D0`.
  **The SD framework gives lower bounds against *adaptive* SQ by construction** — so adaptivity is
  handled by the citation, *not* by re-deriving union/martingale bounds. (OFA-394–396 are Codex's
  elementary nonadaptive cross-checks; they are not the proof path. The SD theorem dominates them.)
  Verify the problem is in SD form: search over the family `Lagr(2n)` with bounded average
  correlation vs `D0`.
- **T1.4 — Reconcile the remaining OFA-388 items:** (a) **delete** the "every distinct pair has
  `k≤3`" corollary — it is **false for n≥5** (adjacent pairs `dim=n−1` exist; OFA-388 finding 4) —
  and route everything through the average/SD bound (the `j≥4` tail is sparse, ~1% weight, OFA-390,
  so the average is unaffected); (b) **fix the Fourier normalization** — pick `F_Ω` with the `1/2^n`
  scaling *or* the unnormalized `2^n`-eigenvalue convention and keep it fixed throughout.

**Done when:** one theorem statement + full proof, valid against **adaptive** SQ, with **no
deferred lemmas and no false corollaries**, numbers matching OFA-391 (`≈2n` floors), and the status
line reading *"SQ lower bound complete; full hardness remains an assumption (OPEN)."*
**Framing rule:** present it as **necessary hardness evidence at LPN grade**, *not* as 7th evidence.

---

## 2. PRIORITY 2 (the 7th axis, concrete) — push the reduction-impossibility hierarchy past P3

**Why:** this is the **only in-house lever that actually moves the 7th needle.** The 7th verdict =
`LSN ⊀ LPN`, a hierarchy that is *proven* at the linear level and *blocked* at the polynomial level.
Extending it even partially toward the adaptive class is real 7th progress.

**Tasks**
- **T2.1 — Upgrade P3 from computation to theorem.** Prove in general (not just `n≤4`): `1_L =
  ∏_{j=1}^{n}(1+⟨w_j,x⟩)` is exactly degree-`n` with `2^n` terms, so any feature-map reduction
  `sympLPN→LPN` must either carry dimension `M = Θ(C(2n,≤n)) = Θ(2^{2n})` *or* truncate and inject
  structured error not absorbable into LPN's i.i.d. noise (reuse the P3 truncation-error data as the
  base case). This makes the polynomial-class block a stated theorem.
- **T2.2 — Define the smallest non-trivial step beyond polynomial** and attack its impossibility —
  e.g. **`r`-round / bounded-query adaptive** reductions, or **degree-`D` adaptive feature maps**.
  Pick the smallest class that strictly extends P3.
- **T2.3 — Tighten A1 from heuristic to theorem on that class.** A1's entropy core (`k ≥
  log₂|Lagr| = Θ(n²)`) is information-theoretic and already adaptivity-agnostic; the weak link is the
  `2^{√k}` LPN-hardness *proxy*. Replace it with the correct LPN hardness so the "any adaptive
  reduction lands at `k=Θ(n²)`, hence vacuous" argument becomes rigorous for the defined class.

**Done when:** a proven impossibility for **one** class strictly larger than polynomial (even a
restricted adaptive class). **Win-win guard:** if instead you *find* a (restricted) reduction, that
is equally valuable — it demotes LSN toward 6.5th and improves LPN self-reduction theory. Either
outcome must pass Sound Verifier before any claim.

---

## 3. PRIORITY 3 (the 7th axis, writable) — sharpen the source-novelty argument

The honest 7th case rests on **source**, the **Ring-LWE precedent** (accepted as lattice-family by
algebraic-number-theory *source*, not by any reduction to LWE). Make the parallel tight: state the
symplectic-structural features that have **no LPN analogue** —
- symplectic-Fourier **self-duality** `F_Ω[1_L] = 2^n·1_L` (seed; no LPN counterpart),
- the secret is a **Lagrangian subspace**, not a vector,
- **stabilizer degeneracy** (KLPV Thm 1.5/1.8),
- non-CSS symplectic coupling absent in classical code decoding.

**Done when:** one tight paper section arguing source-distinctness, explicitly labeled
**conjecture** ("not decidable by reduction analysis").

---

## 4. Frame, don't chase — full adaptive `LSN ⊀ LPN`

This single proposition *determines* 7th-vs-6.5th, but it is **≈0 in-house with no candidate
strategy.** State it crisply as the external open problem with the **win-win guard** (any adaptive
`sympLPN→LPN` reduction would be a breakthrough in LPN self-reduction theory). **Do not sink cycles
trying to settle it directly** — make progress via the *restricted* classes in §2 instead.

## 5. Stop (saturated — diminishing returns)

- More **decoder / barrier variants** at constant noise: every family hits the same noise wall
  (channel-level closure). No new information.
- The **symplectic-stress margin** chase: it is real at low rate but dies at constant rate (Codex
  OFA-398/399, n=7 collapse). Codex owns that lane; let it file the no-go. Don't re-implement
  variants of the same observable.

## 6. Division of labor

```text
Kimi   : §1 (finish K3 — you started it) + §2/§3 (the 7th axis).
Codex  : symplectic-stress lane (OFA-397–399) + continued certificates/cross-checks.
Claude : adjudicate each increment; independently verify load-bearing claims; keep the no-go map.
```

## 7. Standing discipline

Sound Verifier on every claim. The SQ lane is **hardness evidence, not 7th-distinguishing** (seed
`00a7620b`). `OPEN = LSN`; no 7th proven; no security claim. Any worst→avg-success or 7th-found
claim ⇒ ≈0 ⇒ 10× adversarial re-verify ⇒ alert the user **before** committing it.

```text
Cross-refs:
  SQ ≠ 7th-distinguisher / 7th = LSN⊀LPN     — 00a7620b (seed)
  K3 audit (count bug + over-claim) + FIX     — 39d4b853, 7b3aef3c (verified)
  Codex K3 gap localization                   — OFA-388/389/391/394–396; 071fe506 (backlog adjudication)
  secret ≡ LPN (degree-1 ⊕ degree-2)          — 11e6a61c
  worst→avg natural routes closed             — 44ad20fe, lane-G#2, P1 (52cdb115)
```
