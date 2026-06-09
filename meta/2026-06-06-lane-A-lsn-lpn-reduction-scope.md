# Lane A — the one open point, pinned: `LSN ⊀ LPN` is a LINEAR-reduction separation only

> The in-house program concluded with the entire 7th question reduced to a single
> external proposition: the hardness of `LSN ∖ LPN`, i.e. whether quantum stabilizer
> decoding (sympLPN) reduces to classical LPN. Our notes flagged the **proofs of
> Appendix D** (the separation argument) as the one **unread** gap. This closes that
> gap by reading the source (arXiv:2603.19110v1, *Post-Quantum Cryptography from
> Quantum Stabilizer Decoding*, Lu–Poremba–Quek–Ramkumar). Finding: the authors
> **explicitly restrict the separation to linear reductions** — "We prove, however,
> that linear reductions *cannot* reduce sympLPN to LPN" — and state that it "does not
> imply that no reduction exists." **`LSN ⊀ LPN` is therefore a linear-reduction
> separation; the any-reduction question is open, with a heuristic "win-win" barrier
> against the non-linear case.** This is the precise logical status of LSN's 7th-claim.

Lane A of the autonomous continuation. `analysis of an external proposition` (Sound
Verifier: in-house ≈0 to *prove*; what is achievable is to *pin the status* with the
source text). Date: 2026-06-06.

---

## 한국어 요약

```text
마지막 열린점 = LSN ⊀ LPN 이 any-reduction 증명인가, linear-reduction만인가?
저자 명시(2603.19110 Appendix D):
  "We prove, however, that linear reductions cannot reduce sympLPN to LPN."
  "Our barrier does not imply that no reduction exists ... A reduction would have to
   proceed with a very different strategy, and it is possible that if such a reduction
   exists, it could also improve the random self-reductions achievable for LPN."
→ 분리는 LINEAR reduction에 한정. non-linear/adaptive는 완전히 열림.
새 논거(win-win 장벽): 비선형 sympLPN→LPN reduction이 존재하면 LPN의 self-reduction을
  개선하는 셈 → 쉬운 비선형 reduction은 없을 것이라는 *증거(증명 아님)*.
종합: 2509.20697 Thm 1.6은 LPN ↪ LSN(LSN ⊇ LPN). 합치면 LSN은 LPN의 *상위집합·
  최소 LPN만큼 어려움*이고 linear로는 되돌릴 수 없음. 단 source-level "새 family"는
  reduction이 결정 못 함(Ring-LWE 교훈: reduction 부재 ≠ 새 source). any-reduction
  열림이 7th의 *필요조건이지 충분조건 아님*.
판정(Sound Verifier): LSN = 강한 under-verification 7th 후보. 열린점은 정확히
  "non-linear/adaptive sympLPN→LPN reduction"(외부, in-house ≈0), win-win 장벽 부착.
  증명도 반증도 아님 — OPEN.
```

---

## §1 The question

The whole in-house search collapsed to: **is quantum stabilizer decoding (its classical
core, sympLPN) a genuinely new hardness source (7th), or does it reduce to the code
family / LPN (a 6.5th quantum lift)?** Reductions cannot fully settle *source-level*
novelty (the Ring-LWE lesson, §5), but a `sympLPN → LPN` reduction *would* demote it.
So the sharp, decidable sub-question is: **for what class of reductions is
`sympLPN ⊀ LPN` actually proven?** Our prior read (§3.6) inferred "natural linear class
only" from line numbers but left the proof text unread. This pins it from the source.

---

## §2 What Appendix D actually argues (from the source)

Appendix D is an **informal argument** (not formally-numbered theorems), in two moves.
The "most natural approach to a reduction" (the paper) is to turn a sympLPN sample
`(A ∈ Z₂^{2n×n}, Ax+e)` into an LPN sample, either by removing ~`n/2` rows of `A` or by
left-multiplying by some `B ∈ Z₂^{m×2n}` to get `(BA, B(Ax+e))`. Both are blocked:

**(1) Entropy deficiency.** (arXiv:2603.19110v1, Appendix D)
> "for any *fixed* `B ∈ Z₂^{m×2n}`, the random matrix `BA ∈ Z₂^{m×n}` is severely
> deficient in entropy. That is, while `BA` must have entropy about `mn` to be uniformly
> random (and thus a LPN matrix), it actually only has entropy at most `(1−d)mn` for some
> constant `d`."

The isotropic (symplectically-orthogonal) constraint costs `Θ(n²)` bits, so the columns
of `A` cannot be smoothed to uniform by a fixed linear map.

**(2) Error-weight exceeds the Shannon converse.** (same)
> "in the codeword `(BA)x + Be` part of the input, the error `Be` has error weight larger
> than `(1−r−δ)m/2` for any `δ>0` with overwhelming probability, where `r=n/m`. Shannon's
> noisy coding converse theorem turns out to imply that this error weight is undecodable
> even information-theoretically."

So any linear `B` that *did* randomize `BA` toward uniform would inflate the error past
the information-theoretic decoding threshold — the transformed instance carries no
recoverable signal. **This is an information-theoretic barrier (Shannon converse), not a
"no algorithm found yet" gap** — which is why the separation is *stronger* than the mere
*absence* of a Ring-LWE→LWE reduction.

---

## §3 ★ The scope, pinned: LINEAR reductions only (verbatim)

The authors state the scope and its limits explicitly, in **§2.4 (Comparative Hardness of
LPN and sympLPN)** — their own summary of the Appendix-D barrier (all three sentences
below verified verbatim against the arXiv HTML, §2.4):

> "We prove, however, that **linear reductions** *cannot* reduce sympLPN to LPN."

> "Our barrier **does not imply that no reduction exists**, but it shows that the most
> clearly motivated approach fails."

> "A reduction would have to proceed with a **very different strategy**, and it is
> possible that if such a reduction exists, it could also improve the random
> self-reductions achievable for LPN."

**Non-linear / adaptive / randomized reductions are not analyzed at all** — left entirely
open. The reverse direction is also open at the crypto-relevant noise:

> "it is not known if LPN reduces to sympLPN in this low-noise regime, or if in fact
> sympLPN reduces to LPN."

(At high noise `p = ω(n^{-1/2})` there *is* a known `LPN → sympLPN` reduction, but the
PKE construction runs at `p = O(1/√n)`, making that prior reduction vacuous for crypto.)

**Net (the pinned status):** `sympLPN ⊀ LPN` is proven **for the linear `B`-multiply
(and row-removal) class**, by an information-theoretic argument; **for arbitrary
(non-linear / adaptive) reductions it is open.** This confirms the §3.6 reading, now from
the source text rather than inferred from line numbers.

---

## §4 ★ New observation — the "win-win" heuristic barrier against non-linear reductions

The authors' own remark upgrades "open" to "open, but with evidence against":

> "…if such a reduction exists, it could also **improve the random self-reductions
> achievable for LPN**."

This is a **win-win barrier** of the same shape that protects many canonical assumptions:
a non-linear `sympLPN → LPN` reduction would have to do something no known LPN technique
can — and in doing so would itself be a breakthrough in classical LPN self-reduction
theory. So the *absence* of such a reduction is not just "nobody tried"; it is tied to a
well-studied classical open problem (LPN self-reducibility). Two honest qualifications:
(i) this is **evidence, not proof** — the authors say "it is possible that if such a
reduction exists"; (ii) win-win barriers can fail (a reduction could be found that *does*
advance LPN theory). But it means the linear-only restriction is **not obviously a
technical artifact**: the natural next class (non-linear) is gated by an independent hard
problem, not merely unexamined.

---

## §5 Synthesis — the logical status of LSN's 7th-claim

Combine the two papers' load-bearing facts:

```text
 (i)  LSN ⊇ LPN          (2509.20697, Thm 1.6: LPN(⌊np/6⌋,2n,p/6) ↪ LSN(k,n,p),
                          via the degeneracy "junk" register; even k=1 is ≥ const-rate LPN)
 (ii) sympLPN ⊀ LPN       (2603.19110, App. D: LINEAR reductions only; info-theoretic)
 (iii) any-reduction      OPEN, with a win-win heuristic barrier (§4)
 (iv) worst→avg           a strong QUANTUM barrier (2509.20697, Thm 1.9): no lattice-style
                          random self-reduction; like LPN, no worst→avg confidence.
```

Reading:
- **(i)+(ii) ⇒ LSN is a *superset / at-least-as-hard* candidate, not an in-family
  *subset*.** Ring-LWE *narrows* the lattice family (a special structured case); LSN
  *extends past* LPN (LPN is the special case of LSN). The 6.5th "structured instance of
  the code family" reading is therefore the *wrong direction* — LSN contains LPN, not vice
  versa.
- **(ii)+(iii): reducibility is bounded to linear-only; the any-reduction question is the
  single remaining external proposition.** It is *necessary but not sufficient* for 7th:
  - a non-linear `sympLPN → LPN` reduction would **demote LSN to 6.5th** (and, per §4,
    would itself advance LPN theory — unlikely-but-not-impossible);
  - even a future **proof** that no reduction exists would *not by itself* certify "new
    source" — the **Ring-LWE lesson**: Ring-LWE has no known `→LWE` reduction yet is
    lattice-family by *geometry/source*. Source-level novelty is about the *origin of
    hardness* (degeneracy + symplectic coupling + quantum-nativeness), which reductions
    never touch.

So the 7th-vs-6.5th verdict rests on **two** layers, only one of which is the reduction
question: (a) the any-reduction separation (open, win-win-guarded), and (b) source-level
novelty (behavioral: #P-flavoured ML lineage, stabilizer degeneracy splitting
classically-identical problems [2509.20697 Thm 1.5/1.8], non-CSS symplectic coupling —
all *absent* in classical code decoding).

---

## §6 Verdict (Sound Verifier)

**OPEN — strong under-verification 7th candidate; the one open point is now precisely
located and partially guarded.**

```text
- BROKEN?  No. No reduction sympLPN→LPN exists in any class that has been exhibited;
           the linear class is info-theoretically blocked.
- REDUCES? Not established. The only proven reduction is the WRONG way (LPN ↪ LSN); the
           sympLPN→LPN direction is proven IMPOSSIBLE for linear reductions and merely
           OPEN (not exhibited) for non-linear, with a win-win barrier against it.
- OPEN:    YES. LSN survives as the unique live frontier. The entire 7th question = one
           external proposition: does a NON-LINEAR/adaptive sympLPN→LPN reduction exist?
           in-house ≈0 to settle; the honest, source-grounded status is OPEN.
```

**What external review would test (falsifiability):** (a) construct a non-linear
`sympLPN → LPN` reduction at `p=O(1/√n)` — if found, LSN is 6.5th *and* LPN
self-reduction improves (the win-win); (b) failing that, prove an any-reduction
separation (would make the reducibility leg of 7th solid, leaving only source-level
novelty); (c) settle whether random-Clifford randomization can give a search-level
worst→avg despite the Thm 1.9 entropy/Pauli-mixing barrier.

**No 7th proven; no security claim.** LSN is *not* certified new and is *not* refuted; it
is the one assumption for which every in-house road is walled and the residual is a
single, well-posed, externally-checkable proposition — exactly the life-cycle state of a
pre-acceptance canonical assumption. The contribution of Lane A: the open point is no
longer "Appendix D unread" but the sharply-stated **"non-linear sympLPN→LPN reduction,
win-win-guarded,"** with the source quotes that fix its scope.

---

## References
- Lu, Poremba, Quek, Ramkumar, *Post-Quantum Cryptography from Quantum Stabilizer
  Decoding*, arXiv:2603.19110v1 (2026); = ePrint 2026/548. Scope statements (§3 here)
  verified verbatim in **§2.4** (Comparative Hardness of LPN and sympLPN); the technical
  entropy/Shannon-converse argument (§2 here) is in **Appendix D**.
- Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan, *Average-Case Complexity of Quantum
  Stabilizer Decoding*, arXiv:2509.20697 (2025) — Thm 1.5/1.6/1.8/1.9 (§5).
- Poremba, Quek, Shor, *The Learning Stabilizers with Noise Problem*, arXiv:2410.18953.
- In-house: `2026-06-02-hardness-7th-LSN-reassessment.md` §3.5–3.9 (this pins its one
  "unread" gap); the FINAL adjudication (in-house program concluded → this single point).
