# Lane B2 — propose+attack battery on fresh candidates: every one folds (framework-exhaustion, made concrete)

> The recalibration (XLV/XLVI) re-opened the average-case lane and asked for propose+attack
> aimed at a **keyed average-case OWF that is G1 (not reducible to the 6 families + frontier)
> ∧ ¬④ (not a known assumption)**. Lane B2 runs that loop on five **fresh** candidates the
> program had not screened (verified: none appears in prior docs). Under the **Sound
> Verifier** (resemblance ≠ reduction — each fold must be a *tight* reduction or a working
> break, not a vibe), **all five fold**: each is either a *named* assumption (④) or sits in a
> known framework (code / group-action-equivalence / planted-SoS / Microcrypt), i.e. **6.5th
> at best**. None reaches G1∧¬④. This makes the avg-case framework-exhaustion **concrete**:
> the natural keyed-avg-case-OWF space is partitioned by the known frameworks, and the
> "fresh-sounding" inhabitants are just unlabelled members of them. **No OPEN survivor; no
> 7th.** (Honest: this is no-go-map extension, not a discovery; the discovery would be a
> *new framework* = mathematical invention, ≈0.)

`propose+attack (tight reductions / classification verdicts; no over-claim)`. Date: 2026-06-06.

---

## 한국어 요약

```text
목표: keyed avg-case OWF로 G1(6+frontier로 환원 불가) ∧ ¬④(알려진 가정 아님) 후보 찾기.
미스크리닝 신선 후보 5개에 Sound Verifier(tight reduction 또는 working break) 적용 → 전부 fold:
  1. Permuted-Kernel-with-Noise(PKN) → PKP(④, PERK 서명) + permutation/code-equivalence frontier.
  2. Rank-metric Syndrome Decoding(RSD) → code family(rank metric; RQC/ROLLO/Durandal) + ④.
  3. Regular Syndrome Decoding(Reg-SD) → 구조화 LPN = code family + ④(FSS/MPCitH PRG).
  4. Spiked-Tensor / Tensor-PCA OWF → planted/SoS(④, stat-comp gap) + tensor §2A frontier.
  5. "non-Clifford code learning with noise"(LSN-different 양자 시도) → stabilizer면 LSN으로
     환원, 아니면 PRS=classical OWF(QCLH 전례) → 새 source 아님.
결론: 자연스러운 keyed-avg-case-OWF 공간은 알려진 framework로 분할됨; '신선해 보이는' 후보도
  그 미표시 원소일 뿐. G1∧¬④ 도달 0개. OPEN 생존자 없음·7th 없음. (발견이 아니라 no-go
  지도 확장; 진짜 발견 = 새 framework = 수학적 발명 ≈0.)
```

---

## The bar (recalibrated) and the method

- **Target:** keyed average-case OWF (no worst→avg or trapdoor required — those were the
  dropped spurious constraints), with **G1** (not a tight reduction to lattice/code/MQ/
  isogeny/hash/group-action-frontier) and **¬④** (not a relabelled known assumption).
- **Method (Sound Verifier):** for each candidate, attempt a **working break** *or* a
  **tight reduction** to a named object. "Looks like X" is only a *hypothesis*; it earns a
  REDUCES verdict only when the reduction is actually exhibited. If both honestly fail →
  the candidate is **OPEN** (flag loudly, 10× re-verify). Run the 14 self-checks first.

---

## Candidate 1 — Permuted Kernel with Noise (PKN)

**Spec.** Secret permutation `π ∈ S_N` (key). Public random `H ∈ F_q^{m×N}`, public `v ∈
F_q^N`. Instance: `H · π(v) = 0` (PKP) or a noisy `H·π(v) = s` form. Recover `π`.

**Attack / reduction (tight).** This *is* the **Permuted Kernel Problem** — a named PQ
assumption (Shamir'89; the **PERK** signature, NIST add'l round). The reduction is the
identity: PKN with the zero syndrome is PKP verbatim. PKP is also a **permutation/code-
equivalence** problem (find the permutation relating two objects), placing it in the
group-action / equivalence **frontier** (the 6.5th: LIP/TI/code-equivalence). 14-check #8
fires ("known assumption / planted-X = ④"); the secret is a permutation ⇒ group-action.

**Verdict: REDUCES (④ = PKP) + frontier (6.5th).** Not G1, not ¬④. *(PKP is a legitimate
PQ candidate — just not a new source; it is already on the board.)*

## Candidate 2 — Rank-metric Syndrome Decoding (RSD / "rank-LPN")

**Spec.** Secret low-**rank** error `e` over `F_{q^m}` (key). Public parity-check `H`.
Observe syndrome `s = H e`, `e` of bounded rank (not Hamming weight). Recover `e`.

**Attack / reduction (tight).** This is **Rank Syndrome Decoding** — the assumption behind
**RQC, ROLLO, Durandal, Gabidulin**-based schemes. The reduction is the identity. Changing
the metric (rank instead of Hamming) keeps it **inside the code family** (a code is a code;
the source is syndrome-decoding hardness). It is also under active cryptanalysis (algebraic
"MaxMinors" / Gröbner attacks broke several parameter sets) — a *weakening*, not a new
source. 14-check #8 (④) + it is the code family.

**Verdict: REDUCES (code family, ④).** A metric variant of code decoding = 6.5th, not G1.

## Candidate 3 — Regular Syndrome Decoding (Reg-SD)

**Spec.** Syndrome decoding with a **regular** error: the `N`-bit error splits into blocks
with exactly one `1` per block (key = the block positions). Public `H`; observe `s = H e`.

**Attack / reduction (tight).** This is **Regular Syndrome Decoding** — a named structured-
LPN assumption used in MPC-in-the-head signatures and PCG/FSS PRGs (a studied object). The
regular structure is a *restriction* of syndrome decoding; the reduction is the identity and
hardness is still code-decoding. 14-check #8 (④) + code family.

**Verdict: REDUCES (structured LPN = code family, ④).** 6.5th, not G1.

## Candidate 4 — Spiked-Tensor / Tensor-PCA OWF

**Spec.** Secret low-rank 3-tensor `T = Σ_{j≤R} u_j⊗u_j⊗u_j` (key). Public probe vectors;
observe noisy contractions `c_i = T(a_i,b_i,·) + noise`. Recover `T` / its factors.

**Attack / reduction (tight).** This is **spiked-tensor estimation / Tensor-PCA**, a *named*
average-case problem with a well-studied **statistical-to-computational gap** and **SoS**
algorithms (the planted/SoS landscape the recalibration itself names). 14-check #6 fires
partially (inverting vs computing) and #8 (④, named assumption); tensor problems are the
**§2A frontier** (the memory's "tensor → frontier"; avg-case attempt #1 = tensor trapdoor
OWF was already G1-FAIL-as-7th). The reduction to Tensor-PCA is the identity.

**Verdict: REDUCES (planted/SoS = Tensor-PCA, ④) + §2A frontier.** Not G1.

## Candidate 5 — non-Clifford code learning with noise (an LSN-*different* quantum attempt)

**Spec (aiming for OPEN).** The one genuinely open direction is "a quantum noisy-learning
source *different from* LSN." Try: learn a random **non-stabilizer** code / state (e.g. a
doped-Clifford or magic-augmented code) with noise, hoping the non-Clifford structure is a
new source.

**Attack / reduction (the dichotomy).** Two cases, both fold:
- If the code stays in the **stabilizer/Clifford** formalism, the problem **reduces to LSN**
  (it *is* stabilizer decoding) ⇒ 6.5th-of-LSN, not new.
- If it leaves the stabilizer formalism (genuinely non-Clifford / random states), then
  "learning a random pseudorandom state with noise" is **PRS-learning**, which the program
  already broke as **QCLH = PRS = a classical OWF** (the landscape's own admission; the
  determinism/measurement collapse, 14-check #10) ⇒ Microcrypt framework, not a new source.

There is no middle: the thin-band census already found **Clifford = LSN is the unique
inhabitant**, with matchgate=Pfaffian/permanent and GKP=lattice closing the neighbours.

**Verdict: REDUCES (to LSN if stabilizer; to PRS/OWF if not).** No new quantum source.

---

## Synthesis — the avg-case framework partition (concrete)

```text
Every fresh candidate landed in a KNOWN cell, by a tight reduction (not resemblance):
  PKN          -> PKP / permutation-equivalence   (④ + group-action frontier)
  Rank-SD      -> rank-metric code decoding        (④ + code family)
  Regular-SD   -> structured LPN                    (④ + code family)
  Tensor-PCA   -> spiked tensor / SoS               (④ + §2A tensor frontier)
  nonClifford  -> LSN  (if stabilizer) | PRS/OWF (if not)   (6.5th-of-LSN | Microcrypt)

Known frameworks for keyed avg-case OWFs (the partition):
  { lattice/LWE · code/LPN (incl. rank, regular, structured, sympLPN=LSN) · MQ ·
    isogeny · hash · group-action/equivalence (PKP, LIP, TI, code-equiv) ·
    Goldreich/local-PRG · planted/CSP/SoS (incl. tensor-PCA) · Microcrypt/PRS }
```

Every concrete "fresh" candidate is an **unlabelled member** of one cell. The recalibration
is right that the avg-case lane is *populated* — but it is populated by **6.5th/④** objects;
a **G1∧¬④** inhabitant would be a **new framework**, i.e. a mathematical invention (the
arc's standing ≈0 conclusion, here re-confirmed from the avg-case side with fresh examples).

## Verdict (Sound Verifier)

**No OPEN survivor; no 7th.** All five fresh candidates fold by tight reduction to a named
assumption / known framework (6.5th at best). The propose+attack loop, run honestly on
genuinely-new-looking candidates, reproduces the program's conclusion **from the avg-case
direction with concrete cases**: the only inhabitant that is *not* foldable to a classical
framework is **LSN** (and its status is the single open external proposition, Lane A). No
7th proven; no security claim; the search's honest state is unchanged — LSN is the unique
live frontier, and a genuine 7th would require inventing a new framework.

---

## References
- PKP / PERK (NIST additional signatures); rank-metric: RQC, ROLLO, Durandal; Regular-SD
  (MPCitH / PCG-FSS PRGs); Tensor-PCA / spiked tensor (SoS, stat-comp gap).
- In-house: collaboration-guide §3 (14 checks), capstone (framework map), thin-band census
  (Clifford=LSN unique), QCLH break (PRS=classical OWF), Lane A/B1/C/C2 (LSN status).
