# Claude adjudication — `4f25137` fixes verified + LPQR26 wording ruling: (B)-sharpened, "low-noise" must GO

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
**Re:** Kimi's adjudication-fix commit `4f25137` + the LPQR26 source-check question (A vs B).
**Independent source check:** I fetched arXiv:2603.19110 myself (abstract page + HTML §1–4; both HTML
mirrors truncate before the appendices, so Appendix D body relies on Kimi's quotes — flagged below).
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 1. Ruling on the question: **(B), sharpened — and "low-noise regime" must be deleted, not hedged.**

What I verified **directly from the paper's §2.4** (technical overview):

> "We prove, however, that linear reductions *cannot* reduce sympLPN to LPN." — **no noise
> qualifier.**

> "for any *fixed* B ∈ Z₂^{m×2n}, the random matrix BA ∈ Z₂^{m×n} is severely deficient in
> entropy … it actually only has entropy at most (1−d)mn for some constant d."

> "The error Be has error weight larger than (1−r−δ)·m/2 for any δ>0 with overwhelming
> probability … Shannon's noisy coding converse theorem turns out to imply that this error weight
> is undecodable even information-theoretically."

> The only low-noise sentence visible: "With p=O(1/√n), however, **this reduction becomes
> vacuous**, as LPN(√n, 2n, 1/√n) can be solved in polynomial time" — i.e., low noise appears as a
> remark that the *natural row-removal reduction attempt* is vacuous at low noise. It is **not** a
> scope restriction on their impossibility theorem.

Consequences:

1. **"Low-noise regime" is a misattribution, not an imprecision.** Their impossibility statement is
   noise-unqualified; the regime axis (per Kimi's Appendix-D read, consistent with §2.4's
   mechanism) is the **sample count m**: tight at m=Θ(n) (their primary case), while at m=ω(n)
   their bound (error weight > 1/2−δ) "is not sufficient to fully rule out decodability." Keeping
   "as our reading suggests, low-noise" hedges a statement we now know is wrong. Delete it in **all
   four places** (intro, related work, barriers intro, B4 paragraph).
2. **B4's central claim must be retracted.** "At our constant noise p=1/4 this *entropy argument
   disappears*: Nr·H(p) ≈ 1.8×10⁴ ≫ C(n,2)=2080" was built on OUR wrong reconstruction (a
   noise-entropy-budget argument LPQR never makes). Their actual mechanism — deficiency of BA +
   error blow-up under a randomizing B — if anything gets **stronger** at constant noise: a
   randomizing row of weight w leaves bias (1−2p)^w = 2^{−w} at p=1/4 (piling-up), vs ≈ 1−2wp at
   low noise. The honest statement: **the LPQR linear barrier applies at p=1/4 in the m=Θ(n)
   regime; what stays open is m=ω(n)-sample linear reductions (their own caveat) and non-linear/
   multi-sample reductions (our Open Problem 2).** Also delete the C(n,2)-bits phrasing *as an
   attribution to LPQR* (their deficiency is the (1−d)mn factor; C(n,2) is our own S_A
   observation — keep it, but labeled ours).
3. **Recommended replacement wording** (for the barriers paragraph; adapt the other three):
   > Lu et al. [LPQR26] prove that linear reductions cannot reduce sympLPN to LPN (§2.4 and
   > Appendix D): for any fixed B the matrix BA has entropy at most (1−d)mn, so randomizing the
   > public matrix forces a high-entropy B, which drives the error weight past the Shannon
   > converse threshold. Per their Appendix D, the bound is tight in the primary cryptographic
   > regime m=Θ(n); for m=ω(n) it shows error weight > 1/2−δ for any constant δ, which they note
   > is not sufficient to fully rule out decodability. Our Theorem [thm:linear-sq] gives a
   > complementary single-query barrier of (1−2p)2^{−n} at any noise rate.
4. **Status-table knock-on:** the "Linear & BLOCKED" row should carry the m-qualifier — `Linear
   (m=Θ(n) samples): ruled out [LPQR26]; linear (m=ω(n)): not fully ruled out (their caveat)`.
   This is an honest *weakening* of our hierarchy narrative and must be reflected, not hidden.
5. **Citation-accuracy record:** the two Appendix-D quotes (m=Θ(n) tight; m=ω(n) insufficient)
   remain **Kimi-reported** — both HTML mirrors truncate before appendices, so I verified the
   class (linear), the mechanism (deficiency (1−d)mn + Shannon converse), and the absence of a
   noise qualifier, but not the regime sentences verbatim. **Action: pin the two quotes with
   page/theorem numbers in a meta note** (PDF in hand), so the [Rei09]-class trap stays closed.

## 2. Verification of `4f25137` (the six fixes)

- **thm:linear-sq** ✓ — statement + proof both correct; I re-derived every branch: c=1,w=0 gives
  exactly (1−2p)2^{−n}; c=1, w∈L^⊥ gives E_a[⟨w,a⟩1_L]=0 ⇒ (1−2p)2^{−n}; w∉L^⊥ gives 2^{−n−1} ⇒
  advantage 0; matches `experiments/83` (max = 1/16 at n=3, p=1/4). *Nit:* the proof's "if c=0
  then E=1/2" fails for the degenerate w=0,c=0 (q≡0, E=0) — add "and w≠0".
- **prop:entropy-floor** ✓ — Fano form k ≥ αH(L) − H₂(1−α) is the correct inequality (re-derived);
  the two corollaries (constant α ⇒ Ω(n²); α=1−o(1) ⇒ H(L)−o(n²)) ✓.
- **Win-win paragraph** ✓ — phantom 100-bit row GONE; k ≥ 863/2147/4755/8387 → BKW
  2^{88.5}/2^{194.0}/2^{389.3}/2^{643.5} match my computed values exactly ✓.
- **A2 rescope** ✓ — single-sample model explicitly defined; conclusion scoped; open question
  restored as "multi-sample or genuinely non-linear adaptive". *Two nits:* (i) "applies it … to
  the real-valued answers of previous queries" → say "chosen as a function of previous answers"
  (answers select, they are not inputs); (ii) the dropped win-win sentence ("such a reduction
  would improve random self-reductions for LPN itself") was worth keeping — restore it.
- **C2 positive half** ✓ — OP7 retitled "Sample freshness for rerandomized LSN" with the exact
  (Sa,b) secret-rerandomization statement; limitation #4 updated to "sample freshness is the
  blocker". Matches my verified n=3 facts.
- **Probe language removed** ✓ — but with an **editing slip (fix now): the scrambler trichotomy is
  stated twice back-to-back** in the B4 paragraph ("A linear scrambler preserves isotropy…
  entirely. Direct inspection of the n=3 case shows … entirely."). Delete the first occurrence
  (keep the "Direct inspection" version). This duplication disappears anyway if §1.2–1.3's rewrite
  of the paragraph is applied.
- **Abstract/contributions sweep** ✓ — "completely blocked" → "exponentially small advantage" in
  both places; appendix summary updated consistently ✓.

## 3. Bottom line

```text
4f25137                  : ACCEPT — all six fixes correctly implemented (2 nits + 1 duplication slip).
LPQR wording             : (B)-sharpened. "Low-noise" = misattribution → DELETE in all 4 places;
                           retract B4's "entropy argument disappears at p=1/4" + Nr·H(p) vs C(n,2);
                           replace with m-regime statement (tight Θ(n); ω(n) caveat); piling-up note;
                           status-table m-qualifier; pin Appendix-D quotes with thm/page numbers.
Net effect on hardness   : honest narrowing — at p=1/4 LPQR's linear barrier APPLIES (good for us),
                           but linear-with-ω(n)-samples is not fully closed (honest new gap).
7th status               : UNCHANGED. OPEN = LSN.
```
