# 7th-hardness — reassessment: is LSN (quantum stabilizer decoding) a genuine 7th?

**Status**: mathematics research note — `no code / no claim`. A self-correction:
re-opening a candidate the arc dismissed too quickly.
**Date**: 2026-06-02.
**Trigger**: the challenge that real 7th candidates exist and are under verification —
the answer is not "none", it is "not yet found / not yet settled".

---

## §0 The self-correction

The external screen filed LSN/HPS as "quantum-origin but code-adjacent ⇒ 6.5th". That
was a *judgment*, not an established reduction. Re-reading the LSN paper
(Lu–Poremba–Quek–Ramkumar, arXiv:2603.19110), the honest status is **open**: LSN is a
*genuine 7th candidate under active verification*, not a settled 6.5th.

---

## §1 What the paper actually claims (and proves)

- LSN = decoding random **quantum stabilizer codes**; "a quantum analog of LPN",
  native to quantum computation, with an equivalent **classical** formulation
  (Khesin et al., STOC '26).
- **Proves**: average-case hardness ⇒ PKE, OT, OWF (full Cryptomania); PKE as
  efficient as LPN-based, OT round-optimal.
- **Evidence (not proof)**: stabilizer decoding does *not* reduce to LPN
  (Appendix D: for fixed `B`, `BA` is entropy-deficient ⇒ the error blows up
  irrecoverably; linear reductions are ruled out). Reverse `LPN → sympLPN` open in
  low noise `p=O(1/√n)`.
- The classical core is **sympLPN** — LPN with columns **symplectically orthogonal**:
  "closely resembling LPN, but equipped with additional symplectic algebraic
  structure … essential to the quantum nature … raises significant barriers to
  security reductions."

---

## §2 The honest two-sided verdict

**Toward 6.5th (code-family quantum lift):**
- sympLPN = LPN + a symplectic constraint; the symplectic form is exactly the
  structure of **stabilizer/CSS quantum codes** (built from classical codes). So the
  *classical shadow* sits in the code-decoding paradigm, and **ISD** (a code attack)
  is the dominant cryptanalysis. By analogy to Ring/Module-LPN (variants that do not
  linearly reduce to LPN yet remain *in* the lattice/code family), sympLPN may be a
  structured **instance of the code family**, not a new family.

**Toward a genuine 7th:**
- The reduction `sympLPN → LPN` is **proven impossible for linear reductions**
  (Appendix D) — stronger separation evidence than most frontier candidates have.
- LSN is **fully quantum-native** (the HPS-style "weaker than OWF / Microcrypt"
  flavour); its hardness *originates* in quantum information, not in a classical code.
- The authors explicitly argue **"genuinely new"**, with a win-win framing (breaking
  it advances quantum information science).

**The decisive open question**: *does quantum stabilizer-code decoding reduce
(by any reduction, not just linear) to the classical code family — making it a 6.5th
quantum lift — or is the symplectic/quantum structure a genuinely independent
hardness source — a 7th?* The paper leaves this as **evidence, not proof**. It is
under verification. **Neither "6.5th" nor "7th" is established.**

---

## §3 Where our framework can actually contribute

This is a concrete, tractable question our rubric is built for:

1. **Non-linear reductions**: Appendix D rules out *linear* sympLPN→LPN. Probe whether
   a *non-linear* / algebraic reduction (exploiting the symplectic form) exists — if
   yes, 6.5th; if a barrier, 7th-evidence strengthens.
2. **Family vs instance**: is "code + symplectic form" inside the code family the way
   Ring-LPN is inside it, or does the symplectic/quantum layer change the *source* of
   hardness? The Ring-LPN analogy is the key test.
3. **The quantum-origin line**: HPS (worst→avg!) + LSN together suggest quantum-origin
   is a *real, citable frontier* — whether it is "6.5th" (code/quantum lift) or "7th"
   (independent) is the live research question, not a closed one.

---

## §3.5 First result — the Ring-LPN / Ring-LWE test

Applying clause-§3.2 (family vs instance), with the exact definition from the paper
(§ around l.354): **`sympLPN(k,n,p) = LPN(k, 2n, p)`** with two twists — `A` is uniform
*subject to symplectically-orthogonal columns* (and jointly full rank), and the error is
the depolarizing distribution's symplectic representation. **Form**: this is a
*structured-`A` LPN*, the same shape as Ring-LPN (circulant `A`) / Module-LPN (module
`A`).

**But behavior diverges sharply from Ring/Module-LPN.** The trivial tool that helps
place Ring/Module-LPN *inside* the family — LPN's self-reduction
`LPN(k,n) → LPN(k−1,n)` — **"fails completely" on sympLPN** (paper §5, l.429–442),
because symplectic-orthogonal `A` is "jointly nearly maximally far from uniform" (the
Appendix-D entropy deficiency). The authors had to invent a *new* technique (scrambling
symplectic subspaces) to get `sympLPN(n,n) → sympLPN(n−1,n)` at all. So:

> **Form in-family (structured-`A` LPN), behavior out-of-family (standard LPN tooling
> fails).** That tension is *precisely* why LSN resists a clean 6.5th label.

**Sharper framing via Ring-LWE.** Ring-LWE does **not** reduce to LWE, yet it *is*
lattice-family — because an ideal lattice is still a lattice (same geometry / same
worst-case source). The decisive question becomes:

> Is sympLPN's symplectic structure a **source-preserving** extension (like
> Ring-LWE → still the family ⇒ 6.5th, a *quantum lift* of code decoding), or a
> **source-changing** one (quantum stabilizer decoding = a new hardness origin ⇒ 7th)?

The evidence splits cleanly:
- **For source-preserving (6.5th)**: stabilizer/CSS codes are *built from* classical
  codes; the object is "still a code."
- **For source-changing (7th)**: the entropy deficiency (`A` maximally-far-from-uniform)
  is **absent in classical LPN/code decoding** — it breaks the standard tooling, which
  is qualitatively new behavior, not a Ring-LWE-style benign restriction. Plus LSN is
  fully quantum-native.

**Next probe**: Appendix D — decide whether the entropy deficiency is a *removable
technical artifact* (⇒ tooling will catch up ⇒ 6.5th) or an *essential barrier* (⇒
source-changing ⇒ 7th-evidence). This is the single most decisive sub-question, and it
is concretely analyzable.

---

## §3.6 Appendix D verdict — essential (not removable), but bounds the *natural* reduction only

**What it proves.** For the natural reduction class — map sympLPN `(A,r)` to `(BA,Br)`
with random `B` (l.2880):
- **Thm D.1**: an isotropic `A∈Z₂^{2n×n}` has only `~(3/2)n²` bits of entropy (the `n²`
  symplectic-orthogonality conditions); for *any fixed* `B`, `H(BA) ≤ (1−d)mn` —
  deficient by a constant factor. Making `BA` uniform (needed for LPN) forces `B` to
  inject `Ω(n²)` bits.
- **Thm D.2**: any `B` that randomizes `BA` to uniform forces error weight `|Be| ≥
  ((1−r−δ)/2)m`, **exceeding the Shannon noisy-coding converse** ⇒ the transformed code
  is *information-theoretically undecodable*. So **no reduction of this form exists**.

This is an **information-theoretic** barrier (Shannon converse), not a "none found yet"
gap ⇒ the entropy deficiency is **structurally real and essential, NOT a removable
artifact**. **Naive 6.5th is rejected**: the separation is *actively enforced* —
**stronger than Ring-LWE**, where `Ring-LWE→LWE` is merely *unknown*, not blocked.

**What it does NOT prove** (authors explicit): only the **natural linear `B`-multiply
class** is covered (l.2880); the `m=ω(n)` sub-case is "believe… not proven" (l.2962);
**non-linear/adaptive** reductions are untouched, converse **open** (l.736–739).

**Verdict on the decisive sub-question.** The deficiency is *essential against the
natural reduction* (not 6.5th-by-collapse) but does **not** settle 7th, because:
1. **all-reduction is open** (non-linear, `m=ω(n)`); and
2. **reduction-blocking ≠ source-level family membership** — the Ring-LWE lesson:
   Ring-LWE is lattice-family despite no `→LWE` reduction. The remaining 7th question is
   *source-level*: is symplectic/stabilizer decoding a **quantum lift of code decoding
   (6.5th)** or a **new origin (7th)**? Appendix D, being about reductions, never touches
   it.

**Net**: LSN is confirmed a **strong under-verification 7th candidate** — naive 6.5th
*rejected* by an information-theoretic separation (stronger than Ring-LWE), while genuine
7th status hinges on two still-open layers (all-reduction; source-level novelty). The
opposite end of the spectrum from AIIP (broken): LSN is *alive and sharp*.

---

## §3.7 Source-level verdict — behavior says 7th, taxonomy says 6.5th

The paper's structure settles what Appendix D (about reductions) could not — the
*source*:
- **#P-complete** (l.122): optimal quantum stabilizer decoding is #P-complete [IP15],
  strictly above classical syndrome decoding's NP-completeness. Not a mere lift — a
  *harder* problem.
- **Stabilizer degeneracy** (l.365): a "uniquely quantum phenomenon" — distinct Pauli
  errors act identically on the code, so ML decoding sums over cosets. Absent in
  classical code decoding.
- **General Clifford-encoded, not CSS** (l.170, 815): a *random Clifford* stabilizer
  code, not two classical codes glued (CSS) ⇒ it does **not** separate into two classical
  decoding problems; the X/Z parts are symplectically coupled.
- **Depolarizing correlation** (l.685): X and Z errors are correlated (the Y component),
  unlike classical Bernoulli single-type noise.

So the source splits on a **taxonomy vs behavior** axis:
- **Taxonomy (lineage)**: stabilizer codes are objects of *quantum coding theory* —
  "still coding theory" ⇒ 6.5th.
- **Behavior (hardness)**: #P (vs NP) + degeneracy + non-CSS symplectic coupling +
  Appendix-D info-theoretic LPN-separation ⇒ qualitatively distinct from classical
  syndrome decoding ⇒ 7th.

**Which is cryptographically meaningful?** A hardness *family* is defined by its hardness
*source* (lattice = SVP-hardness; code = NP syndrome decoding) — **by behavior, not
lineage**. On our rubric's G1 (irreducibility), **every behavioral axis points to 7th**;
only the taxonomic "it's quantum coding theory" gives 6.5th.

**Residual to a final verdict** (the genuine "under verification"):
1. **Average-case complexity** — #P-completeness is *worst-case optimal* decoding; LSN is
   *average-case random*. Does random stabilizer decoding inherit #P / degeneracy, or
   collapse to something NP-like? (Open — the standard worst→avg gap.)
2. **The community's "family" definition** (lineage vs hardness-source).

**Net (three rounds)**: LSN is a **strong under-verification 7th candidate**. Every
*behavioral* test — form/behavior split (§3.5), Appendix-D info-theoretic separation
(§3.6, stronger than Ring-LWE), source-level #P + degeneracy + non-CSS (§3.7) — points to
7th; the only 6.5th case is *taxonomic lineage*. The honest gap to a *proof* is
average-case complexity + a community definition — exactly what "under verification"
means. The polar opposite of AIIP (broken).

---

## §3.8 Attacking the residual — the #P evidence is worst-case-ML only (self-correction)

We pushed §3.7's residual ("does average-case inherit worst-case #P?"). The paper's own
structure answers it, and forces a **self-correction**.

**The #P result is about a *different problem* than LSN.** Iyer–Poulin (l.122, l.253):
*optimal / **maximum-likelihood** stabilizer decoding* is #P-complete — this is **counting**
(compare the total probability of each error coset; #P precisely because of degeneracy).
LSN, by contrast, is **average-case search/decision** (l.130, l.147): find/decide the
planted error on a random instance — an **NP-flavoured** task (a solution is checkable).

So along **three axes** the #P evidence and the crypto problem differ:
- **ML (counting) vs search**: #P is ML; LSN is search. ML ≥ search; #P does not transfer down.
- **worst vs average**: #P is worst-case; LSN is average-case.
- A worst-case #P-hardness for ML does **not** imply average-case hardness for search.

**Self-correction of §3.7.** Listing "#P-complete" as a *behavioral 7th-evidence for LSN*
was too strong: #P is a fact about *worst-case ML decoding*, not about the average-case
search problem LSN actually uses. We retract #P as direct LSN evidence.

**What the average-case 7th-evidence actually is.** With #P removed, LSN's separation from
the code family rests on: (i) **Appendix-D information-theoretic separation** (sympLPN⊀LPN,
stronger than Ring-LWE, §3.6) and (ii) **quantum-nativeness**. These stand. The worst→avg
picture also sharpens: LPN *has* a code-smoothing worst→avg (BLVW18/YZ20, l.605), and a
random-Clifford (2-design) code+error randomization plausibly gives stabilizer decoding a
**search-level** worst→avg — but **search-level, not #P-level**. #P stays stranded at the
worst-case-ML corner.

**Net (the contribution of this attack).** The 7th-vs-6.5th question for LSN does **not**
hinge on #P (a worst-case-ML side-fact). It hinges, in the crypto-relevant average-case
search regime, on whether sympLPN's Appendix-D separation makes it a new source or an
in-family variant (§3.5–3.6) — exactly the Ring-LWE question. This *narrows* the open
problem (one fewer false lead) and is our own theorem-grade clarification — a real, citable
result of the attack, even though it does not *settle* average-case hardness (still ≈0
single-shot).

---

## §3.9 External follow-up — the average-case residual, answered (2509.20697)

We treated §3.8 as saturated. It was not. A follow-up directly attacks §3.7's residual #1
(does average-case inherit, or collapse?): *Average-Case Complexity of Quantum Stabilizer
Decoding*, Khesin–Lu–Poremba–Ramkumar–**Vaikuntanathan**, arXiv:2509.20697 (2025-09).
Vaikuntanathan is a principal lattice-crypto authority — **external verification is live**
(the user's "another group is checking", confirmed). From the paper's stated theorems
(informal; parameters per the paper, see caveat):

1. **Average-case does NOT collapse — it embeds LPN.** *Thm 1.6*: `LPN(⌊np/6⌋,2n,p/6) →
   LSN(k,n,p)` — constant-rate classical LPN reduces *into* single-qubit LSN. *Cor 1.7*: a
   sub-exp LSN algorithm ⇒ sub-exp constant-rate LPN ⇒ a classical-crypto breakthrough. The
   §3.8 worry ("average-case search collapses to NP-easy") is settled negatively: the
   average-case lower bound is **LPN-hardness** (not the retracted #P). The *mechanism* is
   degeneracy (point 3): a **k-independent n-bit "junk" register** makes even k=1 as hard
   as constant-rate LPN — so points 1 and 3 are *one* phenomenon, not two.
2. **The Ring-LWE question resolves by reduction *direction* (our sharpening).** A
   "structured instance" à la Ring-LPN is a *special case* (family ⊇ variant). But Thm 1.6
   makes classical LPN a special case of LSN (**LSN ⊇ LPN**, the opposite direction);
   combined with the `LSN ⊀ LPN` evidence, LSN is a *superset / strictly-harder* candidate,
   not an in-family *subset*. This weakens the 6.5th "in-family variant" reading — Ring-LWE
   *narrows* the family; LSN *extends past* it.
3. **Degeneracy splits classically-identical definitions — an external theorem for our
   §3.7 "behavior = 7th".** *Thm 1.5 / 1.8*: three classically-equivalent search variants
   (find logical state / synthesize recovery ops / output low-weight error) are *not*
   quantumly equivalent — degeneracy creates an n-bit "junk" register obfuscating the
   logical info. Classical coding theory has no such separation, so the *taxonomic* "still
   coding theory" (the sole 6.5th leg) is itself undercut by a complexity theorem.
4. **Worst→avg is a quantum barrier — correcting our §3.8 conjecture.** §3.8 conjectured a
   search-level worst→avg via random-Clifford randomization. *Thm 1.9* + §1.2.6 say the
   opposite: search↔decision self-reductions hold, but *random* self-reduction (worst→avg)
   faces entropy / Pauli-mixing barriers ("must satisfy very exotic properties"). So LSN has
   **no lattice-style worst→avg confidence** (like LPN itself) — that one axis stays
   code-like; but this is a trait of average-case assumptions, not a break.

**Net update to the verdict.** Relative to §3.8, LSN's 7th standing is **strengthened**:
the average-case residual is answered (LPN-embedding lower bound), the Ring-LWE/in-family
reading is weakened by reduction *direction* (LSN ⊇ LPN), and degeneracy-separation is now
an external complexity theorem against the taxonomic 6.5th leg. The honest last open point
is unchanged *in kind*: **`LSN ⊀ LPN` is strong evidence, not a proof** (no proof that *no*
poly-time reduction exists). worst→avg is now a *strong quantum barrier* — entropy Ω(n²)
vs sparse-Clifford o(n²), Pauli-mixing forces error randomization, any reduction would need
"exotic properties" (barriers *shown*, no constructive reduction; not absolutely ruled
out) — not the open avenue §3.8 imagined. LSN remains the one live under-verification 7th
candidate — now with external corroboration.

> **Verification (full-text pass, 2026-06-02)**: the theorem *statements*, directions, and
> parameters above were checked against the full arXiv:2509.20697 HTML and confirmed —
> Thm 1.6 `LPN(⌊np/6⌋,2n,p/6)→LSN(k,n,p)` (6× noise blowup; any k incl. k=1, via the
> degeneracy junk register); Cor 1.7; Thm 1.5 (Decision LSN≡stateLSN, converse search needs
> success ≫ ½+1/2^{k+1} or k=O(log n)); Thm 1.8 (worst-case QNCP/QSDP/recQNCP/errQNCP;
> errQNCP→recQNCP *is* an SVP, equivalences routed through syndrome decoding QSDP); Thm 1.9
> (search↔decision at p≫log n/n). **Unread**: the proofs themselves, and 2603.19110's
> Appendix-D linear-vs-any-reduction scope (unchanged from §3.6 — the one remaining gap).

---

## §4 Honest stance

- **No false claim**: LSN is *not* proven to be a 7th, and we do not claim it is.
- **No false despair (the correction)**: it is *not* settled as a 6.5th either. It is a
  **real, strong, under-verification 7th candidate** — exactly what "the answer
  exists, it just hasn't been found/settled" means.
- Our contribution: pinning the **one decisive question** (any reduction sympLPN↔code
  family? symplectic = new source or structured instance?) and locating it precisely
  in the no-go map — turning a dismissal back into an open, tractable target.
- **External corroboration (§3.9, arXiv:2509.20697)**: the average-case residual is
  answered (LPN-embedding lower bound), degeneracy-separation is now a complexity theorem,
  and worst→avg is a quantum barrier — our internal §3.7–3.8 verdict is confirmed and
  sharpened from outside; Vaikuntanathan's involvement shows the verification is live. The
  one open point narrows to: is `LSN ⊀ LPN` provable for *any* reduction, not just evidence?

---

## §5 References

- Lu, Poremba, Quek, Ramkumar, *Post-Quantum Cryptography from Quantum Stabilizer
  Decoding*, arXiv:2603.19110 (2026) = eprint 2026/548; Khesin et al. (STOC '26, classical
  formulation).
- Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan, *Average-Case Complexity of Quantum
  Stabilizer Decoding*, arXiv:2509.20697 (2025-09) — §3.9 (Thm 1.5 / 1.6 / 1.8 / 1.9).
- Poremba, Quek, Shor, *The Learning Stabilizers with Noise Problem*, arXiv:2410.18953
  (ITCS 2026) — the original LSN.
- HPS (arXiv:2410.08073). Ring/Module-LPN (the in-family-variant analogy).
- Our: external-candidates screen, capstone §5b, discovery spec.
