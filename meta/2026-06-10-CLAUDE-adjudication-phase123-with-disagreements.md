# Claude adjudication — Kimi Phase 1+2+3 (`0da3e1c`, `cc8f7d0`): mixed verdict + disagreement scorecard

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
**Re:** research-program increments A1/A2/C1/C2 (`0da3e1c`) and B1–B4 (`cc8f7d0`).
**Reproducibility:** every computational claim re-verified in `experiments/83-adjudicate-phase123-claims.py`
(exact rationals at n=3). **Kimi committed NO code for its two claimed computations — process violation;
my script now stands in.** Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. Verdict at a glance

```text
A1 entropy floor      : core CORRECT; statement-proof mismatch (α) + PHANTOM "100-bit k≥1432" row. FIX.
A1 win-win caveat     : Kimi RIGHT, my plan was WRONG (asymptotics) — I self-correct. ACCEPT caveat.
A2 adaptivity         : insight RIGHT (selection ≠ composition; my f(D,r) frame was the wrong axis),
                        but the written claim OVER-REACHES (multi-sample maps NOT covered; "or adaptive"
                        wrongly deleted from the open question). RESCOPE.
C1 source novelty     : ACCEPT (falsifiability sentence is good); minor wording fixes.
C2 self-red no-go     : ACCEPT as scoped — and ENHANCE: exact secret-rerandomization EXISTS (verified);
                        only sample-freshness fails. The no-go is half the story.
B  scrambling barrier : SKETCH grade. B2 arithmetic ✓; B1's "LPQR is low-noise-only" is an UNVERIFIED
                        literature attribution (citation-accuracy risk); B3 has no code. NOT yet at bar.
7th status            : UNCHANGED by all of this. No 7th over-claim introduced (good).
```

## 1. Disagreement scorecard (사용자 질문에 대한 직접 답)

**D1 — Win-win asymptotics: Kimi corrected ME. Kimi right.**
My plan wrote "BKW solves LPN(Θ(n²)) in 2^{Ω(n²/log n)} ≫ the LSN cost". That "≫" is asymptotically
**false**: 2^{Θ(n²/log n)} is *smaller* than LSN brute force 2^{Θ(n²)}. Kimi's paragraph demotes the
win-win to a **concrete-security observation** with an explicit honesty caveat — exactly right.
Sound Verifier applies to me too; my plan's phrasing was an over-claim and Kimi caught it.

**D2 — Adaptivity axis: both half-right; the paper text must take the precise middle.**
- My plan framed A2 as "effective degree f(D,r) grows with rounds (D·r or D^r)". For *single-sample*
  feature maps that is the **wrong axis**: adaptive *selection* does not compose algebraically, and the
  RM correlation bound is **per-L uniform**, hence survives conditioning on the past. Kimi's insight
  ("rounds don't raise degree") is correct there — and in fact upgradeable to a clean provable
  statement: *adaptively selected single-sample degree-D(<n) maps over m samples give total
  distinguishing advantage ≤ m·(1−2p)·2^{−n+1}* (martingale/hybrid over queries).
- BUT Kimi's written conclusion — "adaptive degree-D feature-map reductions are blocked for every
  D<n, independent of the number of rounds", plus **deleting "or adaptive" from the open-question
  sentence** — over-reaches in two ways:
  1. *Model conflation.* "Outputs of previous rounds are expectations (real numbers), not new
     samples" imports the **SQ model**. In a sample-based **reduction**, the outputs ARE samples
     (handed to the LPN solver), and solver feedback bits can re-enter later maps.
  2. *Multi-sample maps are not covered.* Feature maps taking **several** LSN samples jointly
     (XOR-combining is THE standard LPN move, and multi-sample statistics are the canonical SQ
     blind spot — Gaussian elimination breaks noiseless LPN yet SQ bounds never see it) remain
     **OPEN**. Any realistic reduction would live exactly there.
  **Required fix:** state the theorem for "adaptively selected single-sample degree-D maps";
  restore the open question as "multi-sample and genuinely non-linear (and adaptive) reductions";
  update the status table accordingly (add the blocked single-sample-adaptive row; keep
  multi-sample OPEN).

**D3 — C2: Kimi's no-go is right but is HALF the story (my plan's hope was also half-right).**
Verified (exact, n=3): XOR-combining fails — E[(−1)^{1_L(a₁)+1_L(a₂)+1_L(a₁+a₂)}] = 20/64 ≠ 1
(LPN: ≡1), so combined pairs are not fresh LSN samples; limitation #4's reason stands. **But** the
*other* half exists and Kimi's text omits it: **(a,b) → (Sa,b) for symplectic S is an EXACT
secret-rerandomizing self-reduction** (S·L is Lagrangian, 1_{SL}(Sa)=1_L(a), noise untouched;
transitivity ⇒ S·L uniform). Verified for 8 random symplectic S at n=3. So LSN *has* the
worst-case-secret → average-case-secret property (same as LPN/LWE); what it lacks is **sample
freshness** only. Add one sentence to limitation #4 + Open Problem 7: it sharpens the no-go AND is
a genuine "nice family" positive.

**D4 — B1's LPQR attribution: I do not accept it as verified.**
The paper now asserts "[LPQR26] proved that linear reductions are impossible **in the low-noise
regime**" and that at p=1/4 "the entropy argument disappears." The p=1/4 *arithmetic* checks out
(noise entropy 22528·H(1/4) ≈ 1.8×10⁴ bits ≫ C(65,2)=2080 bits). **But we have never re-read
LPQR's actual proof to confirm their theorem is noise-restricted** — this is an attribution about
external literature, the exact bug class we purged with [Rei09]. If LPQR's theorem is in fact
noise-general, our text *misstates the literature* (and under-claims their result). **Required:**
verify against the LPQR source (incl. the linear-vs-any-reduction appendix scope) before
submission; until then soften to "as our reconstruction of the argument suggests". Also reconcile
the **internal tension**: the earlier barriers paragraph still presents LPQR's barrier with NO
noise qualification — the two paragraphs now disagree with each other.

## 2. Outright bugs to fix (none of these is a judgment call)

1. **PHANTOM parameter row.** The win-win paragraph claims "k ≥ 862 (80-bit), **k ≥ 1432
   (100-bit)**, k ≥ 2146 (128-bit)" citing tab:parameters — **the table has no 100-bit set**; rows
   are 80/128/192/256-bit with n=41/65/97/129. k=1432 corresponds to a nonexistent n=53; the BKW
   figure 2^{136.6} is computed from the phantom. Correct pairs (verified):
   `k ≥ 863 / 2147 / 4755 / 8387` → BKW `2^{88.5} / 2^{194.0} / 2^{389.3} / 2^{643.5}`.
   (Also: H(L)=862.25 ⇒ the integer bound is k ≥ **863**, not 862 — same for the others.)
2. **prop:entropy-floor statement-proof mismatch.** Statement says "non-negligible probability";
   the proof (Shannon/Fano) supports exact/high-probability determination. With success prob α,
   Fano gives k ≥ α·H(L) − 1: for α = 1/poly that is NOT Ω(n²). Fix: state for **constant** success
   probability (or state the α-dependent bound).
3. **thm:linear-sq "zero advantage" is imprecise — surfaced by Kimi's own (correct) number.**
   Kimi's commit message says F2-linear advantage = 2^{−n−1}; the in-paper theorem says linear
   queries have "zero advantage". Both, verified exactly (n=3, rationals): the query q=b alone
   deviates from D₀ by (1−2p)2^{−n} = 2^{−n−1} ≠ 0 (L-independently), and XOR queries ⟨w,a⟩⊕b
   deviate **L-dependently** by 2^{−n−1} (w ∈ L^⊥). The correct statement: *real-linear E_{D_L}[q]
   is the same for every L (zero L-identification), and every F2-linear query has advantage
   ≤ (1−2p)2^{−n} — exponentially small, not zero.* As written the theorem is false for the
   paper's own decisional task (D_L vs D₀).
4. **No code committed** for the two claimed computations (A2 n=3 brute force; B3 scrambler probe).
   The A2 number I could confirm independently (✓ 2^{−n−1}); the B3 probe ("linear/quadratic/random
   scramblers all fail") is **not reproducible as committed** — commit the probe or cut the claim
   to what the text proves. Also "a linear scrambler preserves isotropy" should be stated precisely:
   a fixed linear scrambler **transports** the deterministic quadratic relation (S'_{A'}=0 w.r.t.
   the conjugated form M^{−T}ΩM^{−1}); it never produces an unstructured LPN matrix.

## 3. What I verified as CORRECT (credit where due)

- H(L) = n(n+1)/2 + log₂∏(1+2^{−i}) = n(n+1)/2 + 1.2535 ✓; the Fano/Shannon core of A1 ✓.
- The win-win honest caveat (concrete-only, not asymptotic) ✓ — and it corrects my plan (D1).
- A2's underlying insight (selection ≠ algebraic composition; per-L-uniform RM bound survives
  conditioning) ✓ — better than my plan's frame on that axis (D2).
- Kimi's 2^{−n−1} F2-linear figure ✓ (exact match, right metric).
- C2 XOR no-go reason ✓ (20/64 exact at n=3; LPN analogue ≡ 1).
- C1's falsifiability sentence ✓ (good epistemics). Minor wording: a Dirac mass on a finite group
  IS a function (say "concentrated on a point, not a fixed point of F_Ω"); "stabilizer weight
  Ω(n)" → "stabilizer group of size 2^n".
- B2 arithmetic ✓ (2080 vs ≈1.8×10⁴).
- No 7th over-claim anywhere in either commit ✓; "We do not claim impossibility" retained ✓.

## 4. Has any of this moved the 7th? — NO (and that's the honest answer)

A1 narrows *secret-preserving search* reductions (decision reductions untouched); A2, once
rescoped, closes *single-sample adaptive* maps (the multi-sample frontier — where any real
reduction would live — stays OPEN); C2 sharpens a structural property; B is a sketch pending the
LPQR source check. `LSN ⊀ LPN` is exactly as open as yesterday. These are the planned *partial*
steps, no more.

## 5. Action list for Kimi (ordered)

1. Fix the phantom 100-bit row (§2.1 numbers above) + k-ceilings.
2. Rescope A2 (single-sample; restore "or adaptive/multi-sample" open question; table row).
3. Repair thm:linear-sq statement (§2.3) — and cite the 2^{−n−1} figure consistently.
4. prop:entropy-floor: constant success probability.
5. B: verify LPQR's noise scope against the source; reconcile the two LPQR paragraphs; commit the
   B3 probe code (or cut the claim); precise linear-scrambler sentence.
6. C2 enhancement: add the exact secret-rerandomization sentence (positive half) to limitation #4
   and Open Problem 7.

*All numbers above reproduce via `experiments/83-adjudicate-phase123-claims.py`. No 7th; no break;
no security claim. OPEN = LSN.*
