# CAPSTONE addendum (executor lanes A–D) — integrating the parallel executor findings into the final report

> The adjudicator's `2026-06-06-CAPSTONE-7th-hardness-final-report.md` is the FINAL
> in-house synthesis and stands as written. This **addendum** (executor role) records the
> Lane A–D / C3 work committed **in parallel** with that capstone, which it does not yet
> index — chiefly the **precise pinning of the single open proposition** (Lane A), the
> **average-case framework-exhaustion** (Lanes B1/B2, complementing the capstone's
> structural/worst→avg no-go map), and the **computational verification of LSN's two
> load-bearing reduction facts** (Lanes C/C2). It complements, does not override, the
> capstone. Same discipline (Sound Verifier; evidence ≠ proof). Date: 2026-06-06.

---

## 한국어 요약

```text
어댑게이터 최종 캡스톤(4cb10a4f)은 그대로 유효. 이 addendum은 병행 커밋된 executor 레인
(A–D/C3)을 최종 기록에 통합:
 - Lane A: 캡스톤의 "단일 외부명제 LSN⊀LPN"을 정확히 핀포인트 — *linear reduction에만*
   증명(2603.19110 §2.4 verbatim), non-linear 열림 + win-win 장벽.
 - Lane B1/B2: 캡스톤 no-go 지도(구조적/worst→avg)에 **avg-case 측**을 추가 — 2026 문헌
   새 source 없음 + 신선 후보 5개 전부 framework로 fold(G1∧¬④=새 framework=발명≈0).
 - Lane C/C2: LSN의 두 핵심 reduction 사실을 코드 검증 — 엔트로피결핍 d→1/4(LSN⊀LPN linear)
   + degeneracy junk-register(LSN⊇LPN, Thm 1.6).
 - Lane D/C3: 세 방향 수렴 종합 + 채널-레벨 신호소멸 독립 교차검증.
결론 동일: 7th 증명 없음·OPEN=LSN, 단 open point가 한층 정밀해짐(linear-only+win-win).
```

## §1 Lane A — the single open proposition, pinned (sharpens the capstone's central claim)

The capstone reduces everything to "the hardness of `LSN ∖ LPN`." Lane A pins its **exact
logical scope** from the source (2603.19110 **§2.4**, verified verbatim):
- "**We prove, however, that linear reductions cannot reduce sympLPN to LPN.**"
- "Our barrier **does not imply that no reduction exists** ... A reduction would have to
  proceed with a very different strategy, and it is possible that if such a reduction
  exists, **it could also improve the random self-reductions achievable for LPN**."

So the open proposition is precisely: **does a *non-linear / adaptive* `sympLPN → LPN`
reduction exist?** — `linear` is settled (impossible, info-theoretic); non-linear is open,
**guarded by a win-win barrier** (a non-linear reduction would itself advance classical LPN
self-reduction theory). Combined with `LSN ⊇ LPN` (Thm 1.6), LSN is a **superset / ≥-hard**
candidate, not an in-family subset — so the 6.5th "structured instance" reading is the wrong
direction. *(Reduction-blocking remains necessary-not-sufficient for source-level novelty —
the Ring-LWE lesson — which the capstone's "source originates in quantum information" frames.)*

## §2 Lanes B1/B2 — the average-case framework-exhaustion (extends the no-go map)

The capstone's no-go map is structural (the two walls are geometry = flat-archimedean
worst→avg, and trapdoor). Lanes B1/B2 add the **average-case construction side**:
- **B1 (2026 literature scan):** no new hardness *source* beyond LSN; every "new candidate"
  is isomorphism/group-action **frontier (6.5th)** — externally re-confirmed (group actions
  not NP-hard unless PH collapses; worst=avg) — and the quantum-OWF papers are **MicroCrypt
  frameworks**, not sources. External corroboration of the capstone's conclusion.
- **B2 (propose+attack on 5 fresh candidates):** Permuted-Kernel-with-Noise, rank-metric SD,
  regular SD, tensor-PCA/spiked-tensor, non-Clifford-learning — **all fold** by tight
  reduction into known frameworks (`{lattice, code(incl. rank/regular/structured/sympLPN=
  LSN), MQ, isogeny, hash, group-action/equivalence, Goldreich, planted/SoS, MicroCrypt}`).
  ⇒ the keyed-avg-case-OWF space is partitioned by known frameworks; a `G1∧¬④` inhabitant =
  a **new framework = mathematical invention (≈0)**. The avg-case lane is *populated but by
  6.5th/④ objects*; LSN is the only non-foldable inhabitant.

## §3 Lanes C/C2 — computational verification of LSN's two load-bearing reduction facts

- **Lane C** (`17-appendixD-entropy-deficiency.py`): the isotropic sympLPN matrix `A` carries
  `log₂N(n) ≈ (3/2)n²` bits, **deficient by a constant `d → 1/4`** vs uniform `2n²` —
  verified exactly two independent ways (brute force `n≤3` = closed form; Lagrangian count
  `∏(2^i+1)` × ordered bases = `N(n)`). This is the structural core of `LSN ⊀ LPN` (linear).
- **Lane C2** (`18-thm16-degeneracy-junk-register.py`): Thm 1.6 statement verified verbatim;
  its mechanism — **stabilizer degeneracy** = the n-bit junk register, present even at `k=1`
  — illustrated by exact combinatorial checks (same-syndrome coset `2^{n+k}` splits into
  `2^{2k}` logical classes of size `2^{n-k}`; classical codes have no such degeneracy). This
  is the structural core of `LSN ⊇ LPN`. *(Honest: the full 3-stage reduction §§4–6 was NOT
  reimplemented, to avoid drift.)*

## §4 Lanes D/C3 — convergence and an independent channel-level cross-check

- **Lane D** (three-sided convergence): the structural-decoder side, the reduction-status
  side, and the avg-case-construction side — three methodologies with **no shared
  machinery** — independently terminate at the same residual `LSN ∖ LPN`.
- **Lane C3** (`19-autocorr-signal-vanish-crosscheck.py`): independent cross-check of the
  capstone's channel-level closure — the **L-specific excess** `mean C(d∈L) − mean C(d∉L)`
  collapses to **<1% of the dense value (≈0.01–0.04% for n=6,7)** once `m/2^n<1`, confirming
  the *upstream mechanism* behind Task-5's `recovery→0` (no signal, not a weak decoder). One
  self-correction recorded: the signal/background *ratio* was the wrong metric (both → 0);
  *excess* is the right one — verification caught the over-claim.

## §5 Corrected/extended artifact index (executor lanes, on `shared/hardness-7th-exchange`)

```text
Task5  ac5c080a  16-task5-sample-density-sweep.py + sign-off   (OFA-322 closed)
Lane A 9403f316  2026-06-06-lane-A-lsn-lpn-reduction-scope.md   (open point pinned)
Lane B1 13cb3a93 2026-06-06-lane-B1-external-survey-2026.md     (no new 2026 source)
Lane C 4520227e  17-appendixD-entropy-deficiency.py + doc       (d→1/4 verified)
Lane C2 20e5ff5e 18-thm16-degeneracy-junk-register.py + doc     (Thm 1.6 degeneracy)
Lane B2 086046eb 2026-06-06-lane-B2-propose-attack-battery.md   (avg-case exhaustion)
Lane D 45741206  2026-06-06-lane-D-synthesis-three-sided-convergence.md
Lane C3 5fa2c265 19-autocorr-signal-vanish-crosscheck.py + doc  (signal-vanish cross-check)
(note: script #17 exists twice — 17-appendixD-* [mine] and 17-autocorr-signal-vanish [adj.];
 distinct files, no overwrite. My later scripts use 18/19.)
```

## §6 Verdict (unchanged, sharpened)

The capstone's conclusion stands: **no 7th proven; LSN is the unique survivor; the question =
the hardness of `LSN ∖ LPN`.** This addendum sharpens that single point to **"does a
*non-linear* `sympLPN → LPN` reduction exist?" (linear ruled out; win-win-guarded)**, adds
the **average-case framework-exhaustion** to the structural no-go map, and supplies
**computational verification** of LSN's two load-bearing reduction facts (`d→1/4` deficiency;
degeneracy junk register). No security claim; OPEN = LSN, presumed insecure pending external
review.

---

## References
- Adjudicator capstone: `2026-06-06-CAPSTONE-7th-hardness-final-report.md` (the FINAL report).
- Executor lanes (this addendum): the eight commits in §5.
- Sources: 2603.19110 (§2.4, App. D), 2509.20697 (Thm 1.6/1.9).
