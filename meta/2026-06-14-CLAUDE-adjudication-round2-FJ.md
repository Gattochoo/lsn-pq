# Claude 판정 — 병렬 라운드 2 (Tracks F–J, 5건 일괄)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 5커밋 — F(d18bcf0)·G(0eb7126)·H(0c064c2)·I(6e3d55f)·J(f904dec).
**검증:** from-scratch 5건(`experiments/256–260-CLAUDE-*`) + 모든 증명 손 재유도.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**F/H/I/J = ACCEPT(정리 3건+데이터 1건, 본문 4곳 통합). G = 분할 판정: G.1 ACCEPT,
★G.3 REFUTED(순환 실험+증명 결함) — 단 잔해에서 더 강한 정정 정리를 건져 통합**(보편 하한,
등호 iff f₁=f₂). 이로써 pairwise 수준 완전 종결(thm:joint-gf), TV rate 정리화, pencil ratio
전 (n,k) 정리화, lem:m2 frontier m≤48.

## 1. Track F — ACCEPT (m-frontier 8→48)

- 충분통계량 환원(THEOREM): **(2,3)에서 brute-force로 per-T 상수성 확인**(양쪽 밀도 모두) ✓.
- 내 독자 T-수준 구현으로 **m=2..8(기존 3중앵커)+12,16,24 정확분수 일치**, n=3 m=8,10 일치 ✓.
- 데이터의 의미(가드 준수 확인): n=2에서 SD(m=48)=0.691 — m_useful(2)=80 부근에서도 1−SD가
  완만(멱법칙 적합 ~m^{-0.32}). **고정 n에서 1로의 수렴은 느리다** = lem:m2 속도 질문의 첫
  정량 윤곽(단 n=2 한정·외삽 금지, Kimi 라벨 적정). 본문 무반영(meta 기록).

## 2. Track G — G.1 ACCEPT · ★G.3 REFUTED · 정정 정리 통합

- **G.1**(b-주변 하한): Pr[b₁≠b₂]=2q_n(1−q_n) 폐형·열거 일치(15/32·55/128) ✓. 핵심은
  μ=|L|/4^n=2^{-n}이 **L-불변**이라 b들이 무조건 iid가 되는 것 — 확인 ✓.
- **★G.3 기각**: Kimi 211 코드가 **fresh 쌍에도 f₁,f₂를 적용** → SD(Φ#P,Φ#Q)=SD(P,Q)인
  **순환 실험**(모든 f에서 123/128이 나온 이유). 증명의 "fresh를 fresh로 보낸다"도 동일 결함
  (Φ#Q는 f-뒤틀린 비밀 (f₁⁻¹L, f₂⁻¹L) 결합쌍이지 fresh가 아님).
- **진실(내 정정 정리, 256으로 정확 검증)**: same-secret 비교에서
  $\mathrm{SD}=1-4^{-n}[2p(1-p)+(1-2p)^2 A]$, $A=\Pr[\mathbf 1_L(f_1x){=}\mathbf 1_L(f_2x)]$ —
  **f-의존**. (id,Sp): 371/384·309/320, shift: 619/640, random: 743/768 등 전부 공식 일치;
  $A\le1$ ⟹ **보편 하한 $1-(p^2+(1-p)^2)/4^n$, 등호 iff $f_1=f_2$**. G.1의 3/8 하한은 이에
  흡수. n=3 spot도 일치.
- **루프 폐쇄**: strict 값 371/384·309/320 = **옛 192 버그의 스퓨리어스 값들과 정확히 동일** —
  192 버그는 사실 same-secret 비교를 계산하고 있었던 것(같은 혼동의 두 얼굴).
- 본문: OP7 항목에 정정판 보편 하한 수록(Kimi의 등식 주장은 미수록), 열린 질문을
  label-modifying/비곱구조로 재정밀화.

## 3. Track H — THEOREM ACCEPT (TV rate 승격)

증명 손 재유도 완전 건전: 3항 분해(스퓨리어스 j=0 보정 $X^2C-XC-1=4/(X-4)$ ✓),
$r_\ell=[z^\ell]((5+2z+z^2)/4)^n$ ✓, $\sum r_\ell=2^n$·전부 양수 ✓, 오차질량 $O(4^{-n})$ ✓ →
$2^n\mathrm{TV}=\tfrac12+O(2^{-n})$. **257**: 분해==역변환(n=2..10 전 ℓ), 잔차 $2^n\cdot$
$|2^n\mathrm{TV}-\tfrac12|$ 유계 확인. 본문 prop:tdist의 evidence 문장 → 증명 포함 정리로 승격.

## 4. Track I — THEOREM ACCEPT (pairwise 수준 완전 종결)

$G_n$ 폐형 손 재증명(부호행렬 → $S=T^2-4(\cdots)$ 정확, 포함-배제 $+2x_{00}^{2n}$ 정확).
**258**: 계수사전 단위로 열거와 동일(n=2,3,4), 특수화가 thm:mj-general·prop:tdist 재생(n≤6,
Kimi의 n≤4 초과), disagreement 법칙 $\binom{2n}{k}/(2^{2n}-1)$ + **한 줄 직접 증명**
($c_1+c_2$가 비영벡터 위 균등: per-v 카운트 $2^{2n-1}-2$ v-불변) 확인. 본문 thm:joint-gf +
cor:disagree 신설; Honest-Lim "pairwise 닫힘, multi-pair만 open"으로 갱신.

## 5. Track J — THEOREM ACCEPT (pencil ratio 전 (n,k))

증명 손 재유도: 몫 전단사·$\dim$ 이동 $k$·q-이항 정리로 $C_n=2^{n+1}/(2^n+1)$(Track D의
8/5·16/9와 정합) → ratio $=(2^n+1)/(2^{n-k}+1)$. **259**: thm:distance 합(n≤10)·q-이항(n≤10)·
직접 pencil(n=2,3 전 k)·**n=4 몫-리프트 독자 구현**(전 |S_W| & isotropy assert) 17/9·17/5·
17/3·17/2 전부 일치; k=3 scale-미달(n=3..8) ✓. 본문: lem:avg-corr에 $C_n$ 정확폐형,
conj:pencil 동기 단락을 정리로 격상(k=2가 4ρ_avg를 아래서 강제 — 추측 상수의 정확한 근거).

## 6. 거버넌스

블록·prefix·라벨·가드(L1–L3) 전 트랙 준수 ✓ — 단 **G의 L3-위반 아님·새 유형**: 검증 실험이
대상 분포를 검증 변환으로 오염(순환). **신규 가드 (L4): 비교분포에는 손대지 않는다** —
검증 전단사는 한쪽에만, 적용했으면 다른 쪽이 불변임을 별도 증명.

## 7. staging

S9(H rate 정리)·S10(I joint-GF)·S11(J pencil-ratio+C_n)·S12(G 정정 보편하한) 등재.
F=meta 기록. 누적 정리 10건 — 전부 posture-불변(lem:m2/L2 미동), batch 대기 유지.
**단 S-표가 이제 상당한 분량(§Moments·SQ·OP7 대폭 강화)이라 사용자 판단 시 1회 revision 묶기
자연스러움을 재명기.**

## 8. 다음 (Kimi — 선택지)

1. **F 후속**: m=64,80 도달(상태공간 ~10⁹ — C/numpy 최적화 or 대칭 축소) + n-축 비교를 위한
   n=3 m=24(=8n) — lem:m2 속도 질문의 본체.
2. **G 후속**: label-modifying family의 정밀 정의 + 장애물 탐색(이번 G2 스코프 그대로).
3. **multi-pair 수준**(I의 자연 후속): 세 secret 쌍 결합 통계 — SQ 다중상관의 다음 층.
4. 211 코드의 순환 버그 수정 커밋(track-G-fix) — 정정 공식 구현·재검증.

No closure; no break; no security claim. OPEN = LSN.
