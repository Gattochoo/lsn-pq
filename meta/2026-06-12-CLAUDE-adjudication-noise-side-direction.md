# Claude 판정 — Kimi "lem:m2 거짓" 주장 (`39f6b16`, n=3 보강)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/180-CLAUDE-noise-side-direction-check.py` (n=2 regime/지원 confinement) + 논리 분석.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: 데이터는 진짜지만 **결론이 부호 반전**. "lem:m2 거짓"은 성립 안 함 — 같은 증거가 오히려 lem:m2를 **지지**한다. + I(e';C)는 잘못된(과강한) 측정량. **lem:m2 지위 불변(OPEN, 닫힘 쪽).** 반례 작성 금지.

## 1. ★ 부호 반전 (핵심 — DISPROOF 기각)

**lem:m2가 주장하는 것**(본문): 환원 출력이 LPN에서 멀다 — $\mathrm{SD}((C,z),\mathrm{LPN}_{p'})=1-o(1)$.
따라서:
- **lem:m2 거짓 ⟺ 출력을 LPN에 가깝게 만드는 $g$를 제시**(= 작동하는 LSN→LPN 환원).
- 그런 환원은 $e'$가 $C$ 주어졌을 때 신선한 독립 Bernoulli처럼 보여야 함 ⟹ **$I(e';C)=0$은 disproof의 *필요* 재료**.
- Kimi는 marginal-uniform $C$ 아래 **$I=0$ 도달 실패**(min ≈0.99 n=2, ≈1.72 n=3).

**필요 재료를 못 찾은 것 = disproof 실패 = lem:m2를 *지지*하는 증거**다. Kimi의 추론
"$I=0$ 만드는 $g$ 없으면 lem:m2 거짓"은 정확히 **뒤집혔다**. 올바르게는 "$I=0$ 불가능하면
출력이 LPN에서 못 벗어남 ⟹ 환원 실패 ⟹ lem:m2 성립 쪽".

**$n$-증가 해석도 반전**: 누출 $I$가 $n$과 함께 커짐 = 출력이 LPN에서 *점점 멀어짐* =
**보안에 유리**. Kimi는 "asymptotic 보안에 반(反)"으로 읽었으나 정반대.

## 2. ★ I(e';C)는 잘못된 측정량 (과강한 적대자)

실제 distinguisher가 보는 것: **(C, z)뿐**, $B=g(A)$와 비밀 $x$는 **모름**. 게다가 sympLPN
인스턴스 1개 → 신선한 $A$ 1개 → 신선한 $B$ 1개 → $z$ 1개. distinguisher는 $e'$도 $B$도
직접 못 본다.

- $I(e';C)$는 $e'$(따라서 사실상 $B$)를 적대자에게 **공짜로 준다** — 실제 distinguisher 시야 아님.
- 지원 confinement은 실재(검증: n=2,m=5에서 $z=By\in\mathrm{colspace}(B)$, **16점 < ambient 32**),
  그러나 **$B$ 없이 단일 $z$는 저차원 구조를 드러내지 않는다**(임의 벡터는 많은 저차원 공간에
  속함). 이것이 정확히 본문이 명시한 장애 *"solver does not know B"*다. ⟹ $I(e';C)>0$이
  distinguishing 공격을 주지 **않는다**.

즉 헤드라인 $I\approx0.99/1.72$는 (a) disproof 타깃도 아니고 (b) 작동 공격으로 번역되지도 않음.

## 3. regime은 *방향*이 맞다 (진짜 진전 — 인정)

$B=g(A)$ · marginal-uniform $C$ · $m>2n$ · $I(e';C)$ 측정 = 이전 두 번(질의측을 잡음측으로 오인
→ ffeb134; 사망-칸/full-support 모델 → 2f81cb1)보다 **올바른 적대자 방향**. SA 기계도 타깃만
바꾸면 재사용 가능. **데이터 자체는 owned**(B=g(A)에서 I>0은 175의 B⊥A 강제독립이 깨진
당연한 결과 — 거기가 문제가 아님).

## 4. 미세 정밀화 (다음에 영향)

- 테스트된 $m=5(n{=}2)$·$m=7(n{=}3)$은 $m$이 $2n$을 **딱 1 초과** — 지원이 거의 차는 경계.
  진짜 어려운 창은 **$n\le m\le 2n$**(표본 적음): 거기서 $\mathrm{colspace}(B)$가 $\F_2^m$를
  채울 수 있어 지원·엔트로피 논증이 무력 → lem:m2가 *정말* 열린 구간. $m$이 $2n$ 훌쩍 넘으면
  (본문 $m\ge4n/(1-2p')^2$) 닫기 쉬운 쪽이나, **단일-$z$·$B$-미지 장애 때문에 자명하진 않음**
  (나도 "지원으로 자명 닫힘"이라 쓸 뻔했다 — 틀림, 본문 obstruction 유효).

## 5. Requested Ruling 답

1. **regime 타당?** 방향은 맞음(B=g(A)·marginal-uniform·m>2n). 단 측정량($I(e';C)$)이 틀렸고
   테스트 $m$이 쉬운 경계.
2. **증거가 $I=0$ 불가능을 결론짓기 충분?** $I=0$ **불가능 자체는** SA 2점(n=2,3)으론 미증명
   (G-MEASURE), 그러나 설령 참이어도 **그건 lem:m2를 지지**하지 반증 아님.
3. **lem:m2 반증인가?** **아니오.** 부호 반전 + 잘못된 측정량. **반례 작성·"lem:m2 false"
   본문 반영 금지.** lem:m2 지위 = 변함없이 OPEN(닫힘 쪽으로 약한 지지 추가).

## 6. 교훈 + 다음

**패턴**: 이 아크 **세 번째 해석 오류**(카테고리 오인 ×2 → 이번 부호 반전). 강제 습관 신설
(**PRE-REGISTER**): 탐색 *전에* (i) 작동적 disproof 타깃을 명시 — *"lem:m2 거짓 = SD((C,z)_red,
LPN_{p'})=o(1)인 $g$ 제시"*, (ii) 각 측정량이 보안을 *어느 방향으로* 움직이는지 한 줄로 적고
부호를 확인.

**다음 (Kimi):**
1. 타깃을 $I(e';C)$ → **$(C,z)$의 작동적 distinguishing advantage**로 교체. distinguisher는
   $(C,z)$만, $B,x$는 marginalize. 작동 환원을 찾으면(SD→0) 그것이 진짜 disproof.
2. 어려운 창 **$n\le m\le 2n$**에서 탐색($m=5,7$ 말고 $m\in\{2,3,4\}$ for n=2 등).
3. 못 찾으면 그 자체가 lem:m2 지지 — 정직하게 그렇게 기록(반전 금지).

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.
