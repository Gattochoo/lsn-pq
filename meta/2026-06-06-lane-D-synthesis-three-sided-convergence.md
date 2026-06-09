# Lane D — executor synthesis: the 7th question converges, from THREE sides, on one external proposition

> Autonomous-continuation synthesis (executor role; the adjudicator owns the FINAL verdict).
> This run attacked the 7th-hardness question along lanes the structural-decoder track
> (Codex + adjudicator) does not cover, and the result is a **three-sided convergence**: the
> **structural-decoder** side, the **reduction-status** side, and the **average-case-
> construction** side **all independently terminate at the same single point** — the hardness
> of `LSN ∖ LPN` (whether a *non-linear* `sympLPN → LPN` reduction exists). Every other road
> is walled; LSN is the unique live frontier; the residual is one externally-checkable
> proposition. This doc consolidates the three sides and states the precise "escape
> signature" a genuine 7th would need. **No 7th proven; no security claim.**

`executor synthesis (no over-claim; adjudicator owns FINAL)`. Date: 2026-06-06.

---

## 한국어 요약

```text
7th 질문이 세 방향에서 독립적으로 같은 한 점(LSN∖LPN의 hardness = 비선형 sympLPN→LPN
reduction 존재 여부)으로 수렴:
 (1) 구조적 디코더 측 (Codex/어댑게이터/내 Task5): 모든 구조 디코더 family가 crypto
     복잡도에서 벽. autocorrelation family는 channel-level 폐쇄(디코더 무관), symplectic-
     clique family도 poly-sample 실패(clique-drowning) → 2개 독립 family 벽. REDUCES엔
     비-autocorrelation·poly-sample·constant-rate 디코더 필요 = 외부 LSN⊀LPN.
 (2) reduction-status 측 (내 Lane A/C/C2): LSN⊀LPN은 linear만 증명(엔트로피 결핍 d→1/4
     코드검증) + LSN⊇LPN(degeneracy junk register) → LSN은 superset(≥LPN). 열린점=비선형
     LSN→LPN, win-win 장벽 부착.
 (3) avg-case 구성 측 (내 Lane B1/B2): 2026 문헌에 새 source 없음; 신선 후보 5개 전부
     known framework로 fold. G1∧¬④ = 새 framework = 수학적 발명(≈0).
→ 세 측 모두 "다른 길은 다 벽, LSN만 살아있고 그 지위는 단일 외부 명제"로 귀결.
escape signature(진짜 7th 요건): keyed avg-case ∧ G1(tight-reduction 불가) ∧ ¬④ ∧
  14-check 생존 ∧ 모든 poly-sample 구조 디코더 저항. 현존 충족 후보=LSN뿐(양자고유
  degeneracy=strictly quantum), 그조차 단일 외부명제에 의존. 7th 증명 없음, 보안 주장 없음.
```

---

## §1 The three sides (each developed independently this run / in parallel)

### Side 1 — structural decoders (Codex executable harness + adjudicator + my Task 5)
Every structural decoder family tested obeys the wall at **crypto complexity (constant rate
∧ poly samples)**:
- support-span · top-k Walsh · ISD · closure-autocorrelation(+completion) · proper
  F₂-Plücker · BP — all walled (earlier).
- **autocorrelation family** (bucket-rank-stop / isotropic-greedy / **coset-gain**, the
  strongest at 13/16 dense p=0.10): closed **channel-level** (OFA-325/327 adjudication) —
  at `m/2^n<1` the raw signal `C(d∈L)→0` for *every* decoder in the family, present or
  future. My **Task 5** closed bucket-rank-stop specifically by the sample-density sweep;
  the channel-level argument generalizes it to the whole family.
- **symplectic-clique family** (uses the public form `Ω` directly, not autocorrelation):
  also fails at poly-sample by **clique-drowning** (true clique `≈ m/2^n < 1`, false-
  positive clique `O(log n)` dominates). A **2nd independent** family walled.

⇒ a REDUCES on this side would now require a **non-autocorrelation, poly-sample,
constant-rate** structural decoder — which is exactly the external `LSN ⊀ LPN` question.

### Side 2 — reduction status of LSN vs LPN (my Lanes A / C / C2)
- **`LSN ⊀ LPN` is proven for LINEAR reductions only** (2603.19110 §2.4 + App. D), by an
  information-theoretic argument; **non-linear/adaptive is OPEN**, with a **win-win
  barrier** (a non-linear reduction would itself improve LPN self-reductions). [Lane A]
- The linear barrier's core — **entropy deficiency** of the isotropic `A` (`log₂N(n)≈
  (3/2)n²`, deficient by a constant `d→1/4`) — is **verified by exact computation**. [Lane C]
- **`LSN ⊇ LPN`** (Thm 1.6): constant-rate LPN embeds *into* LSN even at `k=1`, via
  **stabilizer degeneracy** (the n-bit junk register) — statement verified verbatim,
  mechanism illustrated combinatorially. [Lane C2]

⇒ LSN is a **superset / ≥-hard** candidate (not an in-family subset); the open point is the
single proposition **"does a non-linear `sympLPN → LPN` reduction exist?"**

### Side 3 — average-case construction space (my Lanes B1 / B2)
- **2026 literature scan**: no new hardness *source* beyond LSN; the isomorphism/group-
  action candidates are frontier (6.5th, externally re-confirmed: not NP-hard unless PH
  collapses, worst=avg); quantum-OWF papers are MicroCrypt frameworks. [Lane B1]
- **propose+attack battery**: five *fresh* candidates (PKN, rank-SD, regular-SD, tensor-PCA,
  non-Clifford-learning) **all fold** by tight reduction into known frameworks. [Lane B2]

⇒ the keyed-avg-case-OWF space is **partitioned by known frameworks**; a `G1∧¬④`
inhabitant would be a **new framework = mathematical invention** (≈0). LSN is the only
non-foldable inhabitant.

## §2 The convergence (the contribution)

```text
         Side 1 (decoders)        Side 2 (reductions)        Side 3 (constructions)
              │                          │                          │
   "no poly-sample structural   "no linear LSN→LPN;        "no new framework; every
    decoder; non-autocorr +      LSN⊇LPN; open point =      fresh candidate folds;
    non-clique route open"       non-linear LSN→LPN"        7th = new framework"
              │                          │                          │
              └──────────────► ONE EXTERNAL PROPOSITION ◄───────────┘
                    hardness of  LSN ∖ LPN  (non-linear sympLPN ⊀ LPN)
```

Three methodologies that share **no machinery** — executable structural cryptanalysis,
reduction/entropy analysis of the source papers, and avg-case construction screening —
arrive at the **same single residual**. That independent convergence is stronger evidence
for the program's conclusion than any one side alone: it is not an artifact of one tool or
one channel.

## §3 The escape signature (what a genuine 7th would require)

From the framework partition (Side 3) and the structural walls (Side 1), a real 7th source
must simultaneously be:
1. **keyed average-case hard** (a secret giving inversion asymmetry; G4 scalable);
2. **G1** — *not* tightly reducible to lattice/code(incl. rank/regular/structured/sympLPN)/
   MQ/isogeny/hash/group-action-equivalence/Goldreich/planted-SoS;
3. **¬④** — not a relabelled named assumption;
4. **survives the 14 self-checks** (no public-value inversion, no determinism collapse, no
   continuous/numerical hardness, no resemblance-only fold, …);
5. **structurally robust** — resists *all* poly-sample constant-rate decoders, including
   non-autocorrelation and non-clique routes.

The **only** known object that meets (1)–(4) in spirit is **LSN** — and it does so via a
**strictly-quantum** feature (stabilizer degeneracy, absent in classical codes) that makes
it a superset of LPN. Even LSN's (5)/G1 status rests on the one open proposition. Anything
else either folds (Side 3) or is a structural decoder target that obeys the wall (Side 1).
So the escape signature is, concretely: **"be a new quantum-native source with a strictly-
quantum structural feature, or invent a new mathematical framework."** Both are research-
discovery-scale — the arc's standing ≈0, now triangulated from three sides.

## §4 This run's deliverables (index)

```text
Task 5  ac5c080a  16-task5-sample-density-sweep.py + sign-off : OFA-322 bucket-rank-stop
                  CLOSED (signal floor m* exponential; poly-ward = 0; calibrated decoder).
Lane A  9403f316  2026-06-06-lane-A-lsn-lpn-reduction-scope.md : LSN⊀LPN = linear-only
                  (verbatim §2.4 quotes); non-linear open + win-win barrier; LSN⊇LPN superset.
Lane B1 13cb3a93  2026-06-06-lane-B1-external-survey-2026.md  : 2026 lit scan -> no new
                  source; frontier=6.5th confirmed; quantum-OWF=MicroCrypt framework.
Lane C  4520227e  17-appendixD-entropy-deficiency.py + doc    : isotropic-A entropy deficiency
                  d->1/4 verified exactly (2 independent counts).
Lane C2 20e5ff5e  18-thm16-degeneracy-junk-register.py + doc  : Thm 1.6 (LSN⊇LPN) statement
                  verbatim + degeneracy junk-register illustrated (reduction NOT reimplemented).
Lane B2 086046eb  2026-06-06-lane-B2-propose-attack-battery.md : 5 fresh candidates all fold
                  -> avg-case framework-exhaustion (concrete).
Lane D  (this)    2026-06-06-lane-D-synthesis-three-sided-convergence.md : the convergence.

Note: script number 17 appears twice (my 17-appendixD-entropy-deficiency.py and the parallel
17-autocorr-signal-vanish.py); distinct files, no overwrite. New scripts use 19+.
Parallel work integrated here: OFA-325/327 channel-level closure (adjudicator), symplectic-
clique clique-drowning (Kimi) -- credited in §1 Side 1.
```

## §5 Verdict (Sound Verifier)

**OPEN candidate = LSN; no 7th proven; no security claim.** The 7th question is reduced —
from three independent directions — to the single external proposition `LSN ∖ LPN`. Every
other road (structural decoders of two families; avg-case constructions across all known
frameworks; linear reductions) is walled. The honest status is unchanged in kind but
**triangulated**: not "one sweep shut every door," but "three methodologies with no shared
machinery converge on the same single residual, and that residual is externally checkable."
The adjudicator owns the FINAL verdict; this is the executor's consolidation feeding it.

```text
7th-EVIDENCE (executor synthesis):
  - structural: 2 decoder families walled; autocorrelation closed channel-level.
  - reductions: LSN⊇LPN (degeneracy) ∧ LSN⊀LPN-linear (entropy d->1/4); non-linear open.
  - constructions: framework-exhaustion; G1∧¬④ = new framework (≈0).
  - convergence: all three -> hardness of LSN∖LPN (non-linear sympLPN⊀LPN), external.
  no 7th; no security claim; OPEN=LSN, presumed insecure pending external review.
```

---

## References
- This run: Lanes A/B1/C/C2/B2 (above); Task 5 sign-off.
- Parallel: OFA-325/327 channel-level closure; symplectic-clique clique-drowning; FINAL
  adjudication (Task 5 verified).
- Sources: 2603.19110 (§2.4, App. D), 2509.20697 (Thm 1.6/1.9); collaboration-guide §3.
