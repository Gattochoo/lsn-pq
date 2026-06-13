# Claude 판정 — 라운드 7 (AA/BB/CC/DD) + Gemini stacked-rank

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 4트랙(AA 1453bf9·BB 854e748·CC 7b17b4e·DD f488ad6) + Gemini-3.1-Pro stacked-rank
답(사용자 터미널 채널). **3-에이전트 협업 본격 가동.**
**검증:** from-scratch(`experiments/640–642-CLAUDE-*`).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**★라운드 7이 점근 lem:m2를 `shared-B vs fresh-B`로 정밀화 — shared-B는 닫힘(Gemini
stacked-rank, non-vanishing; CC 계산 확증), fresh-B가 진짜 residual(모든 distinguisher rate→0).**
q_graph→0 벽을 넘는 첫 구조적 진전. 3-에이전트 수렴(Gemini 구조·Kimi 계산·Claude 판정).

## 1. ★ Gemini stacked-rank (642) — ACCEPT, n=2 catch

statistic = Rank(HY), Y=[y⁽¹⁾..y⁽ᵏ⁾] (shared C), H=parity-check(C).
- **Reduction bound**(provable, B-무관): HY=HBE, B∈F₂^{m×2n} → Rank(HY)≤2n deterministic.
  **200 random shared-B 전부 ≤4 확인.** ✓ **rank는 차원이라 q_graph→0 벽을 넘음**(n에 비례, 분모 아님).
- **LPN 점근**: p_eff→1/2(lem:m1)이면 HZ uniform화 → Rank→min(m-n,k)>2n (k>2n) → non-vanishing
  detection. uniform 5×5 full-rank=9765/32768=0.298(Gemini 값 정확).
- **★내 catch**: Gemini n=2 evidence 0.298은 **p=1/2 가정**. 실제 matched LPN n=2는 p_eff=0.342≠1/2
  → 정확 advantage=**0.190**(p_eff<1/2라 Z sparse·HZ rank 낮음). 점근 메커니즘 맞으나 유한-n 수치 정정.
- **결론**: shared-B(고정 B·공유 C로 k>2n 샘플)면 stacked-rank로 **점근 배제**. fresh-B면 회피
  (각 샘플 다른 C⁽ⁱ⁾, noise 공통 공간 안 함).

## 2. Track CC (640) — NO-GO ACCEPT + q_graph 공식 오류 catch

- **fresh-B k-sample rank NO-GO**: SD(P^⊗k,Q^⊗k)≤k·SD(P,Q), single rank advantage≤q_graph→0 →
  fixed-k rate→0. ACCEPT. shared-B OPEN(이걸 Gemini가 답).
- **★q_graph 공식 오류**: CC가 "Sp(2n,2)가 Lagrangian transitive·Bernoulli weight coordinate-wise라
  Pr[e∈L] 모든 L 동일 → (3/4)^n"이라 했으나 **틀림** — **Sp는 Bernoulli weight 불변 아님**(symplectic은
  좌표 선형혼합; Hamming-weight 확률은 permutation에만 불변). **640**: Pr[e∈L]이 L마다 다름
  (n=2: {3/8,25/64,15/32,9/16}); reduction A는 uniform Lagrangian → q_graph=평균=**29/64**(라운드1),
  not (3/4)^n=9/16. NO-GO 결론은 둘 다 →0이라 불변, rate formula만 정정.

## 3. Track AA (W-law) — ACCEPT, 점근 OPEN 정직

W=min_w wt(y+Cw) 전체 분포 정확(n=2, m≤7), 여러 B family. q_graph=29/64 맞음(CC와 달리).
새 family complementary-pair marginal-uniform **확인**(모든 좌표 각 row uniform). 모든 B에서
TV(W-law)≥baseline(위협 아님). **점근 하한 정직하게 OPEN**(n=2만). W만으론 점근 못 넘음 — Gemini
stacked-rank(multi-sample)가 W를 넘는 도구.

## 4. Track DD (threat) — 음성 ACCEPT

structured marginal-uniform B 3 family(UCS-r·Block·Parity) 전부 SD≥baseline(위협 없음). q_graph=29/64
맞음. 어떤 single-sample structured B도 출력을 LPN쪽으로 못 옮김.

## 5. Track BB — 진행 중 (641)

I(x;y|C) 정확(n=2). column-pair λ=1/4가 I를 baseline 아래로(m≥5). **단 I↓≠SD↓**: I 낮음=output이
x 덜 누설=reduction 약화=lem:m2 지지(위협 반대). 641이 column-pair SD 직접 계산 중(무거움) →
SD≥baseline 예상(I-drop은 위협 아님 확증). 완료 후 incremental 판정. Kimi 정직(escalate 안 함·OPEN 라벨).

## 6. 본문 반영 + staging

**open:marginal-adaptive에 stacked-rank 통합**(S19): shared-sample(고정 B)이면 Rank(HY)≤2n vs
LPN rank min(m-n,k) = non-vanishing → 점근 배제; fresh-B가 residual(모든 distinguisher rate→0,
n=2 m≤80). 빌드 ✓(335 KB). CC q_graph 정정은 meta(본문 q_graph=29/64 이미 맞음). BB는 641 후.

## 7. 메타 — 3-에이전트 협업 성과

Gemini(구조: stacked-rank invariant) → Claude(n=2 값 catch + shared/fresh 명확화) → Kimi CC(계산:
fresh NO-GO·shared OPEN 확증). **셋이 같은 결론 수렴**: q_graph→0 벽을 넘는 invariant는 shared-B에만
존재. Gemini가 over-claim(n=2 p=1/2) 했으나 판정이 catch. agy 운영: 짧은 질문=Claude 자동(인자순서
-p 마지막·리다이렉트 없이); 긴 질문=사용자 터미널 직접(리다이렉트 막힘).

## 8. 다음

**lem:m2 residual = fresh-B 모델의 점근 distinguishability.** shared-B 닫힘. fresh-B에선 W·rank·MI·
threat 다 rate→0. 남은 질문: fresh-B에서 점근 distinguisher가 (a)없다(reduction 가능, lem:m2 거짓?)
or (b)있으나 우리가 못 찾음. reduction model(LSN sample이 shared C 강제하나 fresh 허용하나)이 결정적 —
이게 lem:m2의 최종 형태.

No closure; no break; no security claim. OPEN = LSN.
