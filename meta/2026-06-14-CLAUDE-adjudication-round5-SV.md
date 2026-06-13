# Claude 판정 — 병렬 라운드 5 (Tracks S/T/U/V, 4건 일괄)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 4커밋 — S(4ea5eed)·T(cfa7001)·U(636188c)·V(0089ad2). CLI 직접 채널. 정직 의무 라운드.
**검증:** from-scratch 4건(`experiments/440–442-CLAUDE-*` + 443 anchor) + 증명 손 재유도.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**U/V ACCEPT(정리)·S 부분 ACCEPT(결론 옳음·proof 결함 정정)·T NO-GO(정직 모범).** lem:m2 본체는
못 닫았으나 **의미 있는 진전**: syndrome-weight가 q-cap을 넘어 full SD를 99.9% 포착(라운드1 우려
해소), 극한=1은 고정 n에서 옳음(메커니즘 정정). 정직 의무 잘 지켜진 라운드(T가 자기 버그 발견·NO-GO).

## 1. Track U — ACCEPT (440)

label-preserving b-dependent bijection: SD = 1−(p²+(1−p)²)/4ⁿ + (1−2p)²/(2·4ⁿ)(2−A₀−A₁).
**from-scratch 검증**: 명명 케이스(literal dup 123/128·transp 1231/1280·sym·random) + 1500
bijection 검색(전부 ≥min, min 0.9651) + n=3 spot 전부 공식==열거. A_β≤1 ⟹ ≥min, 등호 iff g₀=g₁.
**라운드4 R의 비-전단사 함정을 정리로 닫음**(R이 mishandle한 bijective sub-family).

## 2. Track V — ACCEPT (441) + 선형 converse 강화증명

**V1: valid-output 공개 bijection ⟺ g(x,b)=(S(x),b), S∈Sp(2n,F₂)**(secret rerandomization).
Kimi 증명은 "symplectic polar space automorphism=Sp" finite-geometry fact에 의존(정직히 OPEN 라벨).
**★내가 선형 converse를 GL(4,2) 전수로 증명**: 20,160개 중 Lagrangian-보존 = 정확히 Sp(4,2)
720개(M^T J M=J), 비-symplectic Lagrangian-보존 0개. forward(Sp→valid-output) + negative
controls(affine t≠0 전부·random 200/200 실패) 재현. V2: duplicate 123/128·non-dup ≥min(0.9646).
**OP7 의미**: valid-output=secret rerandomization(선형 증명) → correctness-constrained family에선
fresh 불가. 열린 영역이 비선형/비-valid-output으로 좁혀짐. 비선형 converse OPEN(Kimi 라벨 유지).

## 3. Track S — 부분 ACCEPT (442): 결론 옳음, entropy proof 정정

### S1 ACCEPT (EVIDENCE) — explicit functional 발견
full SD를 잡는 test가 **syndrome-weight** T_sw=min_w wt(y+Cw): m=8에서 full의 99.4%, m=80에서
99.9% 포착. rank-member는 q(2)=29/64=0.453에 포화(라운드1 우려). **라운드1 "q-포화"를 넘는
explicit functional 확인** — 좋은 진전. (검증: Kimi 표 sanity + 메커니즘 독립 확인.)

### S2 — ★결론 ACCEPT·proof REJECT-as-entropy-theorem
주장: lim_{m→∞} SD(P_out, P_lpn)=1 (uniform-B-per-A, 고정 n). **결론은 옳다. 그러나 entropy
"THEOREM"은 결함**:
- Kimi의 per-row entropy H(Q_x)=n+H(2p_eff)+2p_eff는 **틀림** — matched LPN의 정확한 per-row
  entropy는 **n+H(p_eff)**(c uniform n bits + noise H(p_eff)). n=2: Kimi 3.584 vs 정확 2.925.
- **정확한 메커니즘(내 442)**: P_out=q·P_graph+(1−q)·P_full(uniform). ① graph(질량 q): y∈col(C)
  강제 → LPN에선 rare(rank-member가 잡는 q-cap). ② full(질량 1−q, uniform): per-row
  SD(uniform, LPN_{p_eff})=(1/2ⁿ)(1/2−p_eff)>0 strict(p_eff<1/2) → product가 m→∞에서 →1
  (syndrome-weight noise-rate gap). **두 component 다 분리 → SD→1.** 단조증가 확인(m=1..32).
- **cross-n 정합**: per-row SD가 (1/2ⁿ)(1/2−p_eff)이고 p_eff(n)→1/2 → 큰 n에서 수렴 느림 =
  Track O의 "1−SD가 n으로 커짐" 데이터 설명.
- **권고**: S2 라벨 THEOREM(entropy)→EVIDENCE+corrected-mechanism. 본문 미반영(uniform-B-per-A
  한정·sketch). lem:m2 OPEN(일반 randomized B 아님, S3 정직).

## 4. Track T — NO-GO (정직 모범) (443 anchor)

n=4 cross-n 셋째 점 시도. **GL(4,F₂) orbit 축소가 버그**(m=2: orbit 0.068 vs anchor 0.0076,
9× 불일치) → Kimi가 자기 anchor와 대조해 **스스로 발견·NO-GO 선언, m=8/12 미신뢰**. anchor(무축소
충분통계량, m≤6)는 THEOREM-grade. **내 443: 내 260 계산기로 n=4 m≤4 anchor 독립 재현**[결과 확인].
정직 의무 모범 — 가짜 데이터 대신 벽 보고. cross-n 셋째 점은 OPEN(anchor m≤6은 slower-decay와
informally 정합하나 formal 비교 불가).

## 5. 본문 반영

V의 valid-output=Sp(선형 증명)를 OP7 항목에 한 문장 추가(가장 OP7-유의미). S/T/U는 meta 기록
(S=uniform-B 한정·sketch, T=NO-GO, U=R 후속 정리).

## 6. staging

S16(OP7 valid-output 선형 특성화). 누적 정리 13건+. posture 불변(lem:m2 본체 미해결, syndrome-
weight+극한은 uniform-B 한정). batch 대기.

## 7. 다음

1. **S2 정확화**: 정정 메커니즘(two-component)으로 극한=1을 엄밀 정리화 — 본문 후보(uniform-B 한정
   명시). full-component product-SD→1은 표준, graph 분리도 명확 → 닫을 수 있음.
2. **T 재시도**: GL(4) orbit 버그 수정 or 무축소로 m=8(C(23,15) 무거우나 가능).
3. lem:m2 본체: uniform-B는 닫혀가나 **일반 randomized marginal-adaptive B**가 핵심 OPEN.
4. V 비선형 converse(automorphism fact 직접 증명).

No closure; no break; no security claim. OPEN = LSN.
