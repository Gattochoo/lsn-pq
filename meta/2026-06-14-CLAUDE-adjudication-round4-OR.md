# Claude 판정 — 병렬 라운드 4 (Tracks O/P/Q/R, 4건 일괄)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 4커밋 — O(49fb20a)·P(2715452)·Q(3e2f81e)·R(944f64b). CLI 직접 채널 가동.
**검증:** from-scratch 4건(`experiments/340–343-CLAUDE-*`) + 증명 손 재유도.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**Q/O ACCEPT, P ACCEPT(검증 후 확정), ★R = 반박 무효 판정**(비-전단사 아티팩트, G.3-class).
라운드 3의 무결함과 달리 이번엔 신중한 적대 검증이 가짜 반박 하나(R)를 걸러냄 + Kimi가 내
지시서 오류 2개(P의 4^{-k}→2^{-k})를 정정. 본문 통합: 일반-k GF(P) 1건(예정).

## 1. Track Q — ACCEPT (340)

3-wise 상관 Q.1: $\E_A[g_xg_{x'}g_{x''}]=(1-2p)^{3k}\times\{+1$ if $w{=}0$, $-1/(2^{2n}{-}1)$ else$\}$,
$w=x{+}x'{+}x''$. **전체 앙상블 from-scratch**: sign 평균이 모든 63 마스크×8 secret-sum(n=3)에서
정확(이게 Q.1의 심장 — w로만 의존). 공표값(diag 1/512·off −1/32256·−1/130560·avg 5/18432·9/69632)
전부 일치. **L3 모범**: 제한 3-local 클래스를 Feldman에 안 넣고 OPEN 라벨. 본문은 L3 검토 후(DRAFT 유지).

## 2. Track O — ACCEPT (343)

n=3 정확 SD m=16/20/24. GL(3,F₂)-orbit 축소는 Track L의 S₃ 축소와 구조 동일(라운드3 검증).
**무축소 독립 재현**: 내 260 계산기로 anchor m=8..12 정확 일치 + **새 점 m=13**(0.278855)이
m=12<13<16<20<24 단조 체인에 정합. q_graph(3)=1241/4608 홀수인자 9 보존(floor-division 교훈).
**첫 cross-n 데이터**: 같은 m/n에서 1−SD(n=3)>1−SD(n=2)(ratio 8: 0.700 vs 0.481) — n 정규화
시 decay 더 느림. **가드 정확**: p_eff(3)≈0.411 무용 regime → m-축 거리 측정이지 lem:m2 결판 아님.
EVIDENCE 라벨 적정. 본문 델타 없음(meta 기록).

## 3. Track P — ACCEPT (344 + Kimi 310 재현)

일반-k GF + $P_k(n)=\prod_{i=0}^{k-1}(2^{2n-i}-2^i)$.
- **P_k 카운트**: 직접 열거(k=2,3·n=2,3) 일치; k>n 퇴화(P₃(2)=0·P₄(3)=0); P₄(4)=46,267,200(공식).
- **Möbius μ_c=(−1)^c 2^{C(c,2)}**: k=2(1,−1,2)·k=3(1,−1,2,−8)·k=4(**1,−1,2,−8,64**).
  (★내 손계산이 한때 μ₄=128이라 했으나 C(4,2)=6→2⁶=**64**가 맞음 — 내 자기수정.)
- **일반-k 구조 검증**: k=2=thm:joint-gf(exp/258, 통합됨)·k=3=thm:triple-gf(exp/263, 통합됨) —
  비퇴화 열거 가능 차수 둘 다 독립 확인됨. **★내 342 일반-k 재구현엔 버그**(263과 불일치) →
  폐기, 검증된 258/263에 의존(내 버그지 Kimi 것 아님; 344에 기록).
- **t_{1^k} 벤치마크**: 직접 열거로 TV(law, Bin(2n,2^{-k})) = 707/5760·35183/645120·1096511/27525120
  = Kimi 표 정확 일치.
- **k=4 marginal-consistency**: Kimi 310 재실행 → G⁽⁴⁾(n=4)의 pair_01/02/23·triple_012/013/123
  marginal 전부 thm:joint-gf/triple-gf 재생(전수 256⁴ 없이).
- **★Kimi가 내 지시서 오류 정정**: t_{1^k} 벤치마크 4^{-k}→**2^{-k}**(k=2에서 1/4=2^{-2} 맞음).
  옳음. (라운드3 M의 56→60에 이은 둘째 쌍방향 catch.)
- **본문 통합**: §Moments thm:kfold-gf 신설(P_k 카운트 + 일반-k Möbius 폐형; joint/triple-gf를
  k=2,3 특수화로 흡수); Honest-Lim "모든 고정 k 폐쇄, k=Θ(n)·SQ만 open". 빌드 ✓(328 KB).

## 4. ★ Track R — 반박 무효 (341)

Kimi 주장: b-dependent map이 universal minimum 깸(SD=1229/1280<123/128, THEOREM REFUTATION).
**판정 REJECT-as-refutation**:
- SD=1229/1280 산술은 맞음. **그러나 counterexample의 g₁이 전단사가 아님**: ψ₁(·,1)=1로
  g₁(x,0)=(x,0)·g₁(x,1)=(swap(x),0) → 출력 label 전부 0으로 붕괴, 입력 (0,1)·(1,0) 충돌.
- 비-전단사 공개맵은 정보 파괴로 SD를 자명하게 줄임 — K1/K2가 bijection 제한한 이유.
- **유효 bijective b-dependent 6000개 검색 → 전부 ≥123/128**(min 0.9649). label-flipping+
  b-dependent-ψ는 일반적으로 비-전단사(Kimi 결함의 정체).
- **G.3-class catch**: 강한 주장(OP7 반례)의 전제가 깨짐. 라벨 강등(THEOREM→비-전단사 EVIDENCE·
  bijective OPEN). 본문 OP7 변화 없음(보편 하한은 bijection 진술).

## 5. 본문 반영 [P 검증 후]

§Moments: thm:triple-gf 뒤 일반-k 정리(또는 흡수). P_k 카운트 + 일반-k GF + "k=2,3=기존 정리".
Honest-Lim: "pairwise·triple → 모든 고정 k 폐쇄, 일반 multi-secret(k=Θ(n))·SQ만 open".

## 6. staging

S15(일반-k GF, thm:kfold-gf). Q=DRAFT(L3 검토 대기 — 3-wise는 제한클래스라 본문 미반영),
R=meta(반박무효), O=meta(evidence·cross-n). 누적 정리 13건. posture 불변, batch 대기.

## 7. 다음

1. **O 후속**: cross-n을 더 큰 n(n=4 m=8~16)으로 — decay의 n-의존을 정량화(lem:m2 점근 단서).
2. **P 후속**: 일반-k GF의 SQ 응용(k-wise 상관 → 제한클래스, L3) 또는 k=Θ(n) 점근.
3. **R 후속**: bijective b-dependent의 infimum(검색 넘어 구조 분석) — minimum 증명 시도.
4. lem:m2 본체: q-포화 넘는 functional(라운드1 미해결).

No closure; no break; no security claim. OPEN = LSN.
