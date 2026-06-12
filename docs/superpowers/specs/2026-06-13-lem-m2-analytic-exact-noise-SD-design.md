# lem:m2 해석적 시도 설계 — $n=2$ exact conditional noise SD

**Date:** 2026-06-13  
**Author:** Kimi  
**Scope:** `lem:m2`의 noise-side 장애물을 SageMath로 정면 조사. OP7은 본 시도가 마무리된 뒤 진행.

---

## 1. 목표

`lem:m2`의 핵심 장애물:

> 고정 $2n$차원 symplectic-LPN 잡음 $e$에 대해, 적응 행렬 $B$가 만들어내는 $e'=Be$가 공개 질의 행렬 $C=BA$만 보고서도 i.i.d. $\mathrm{Bernoulli}(p')^m$와 통계적으로 구별되는가?

이를 $n=2$에서 **완전 열거**로 정량적으로 검증한다. 결과는 `lem:m2`가 성립하는 쪽의 증거가 될 수도, 반례 후보를 줄 수도 있다.

---

## 2. 계산할 정확한 대상

- $n=2$이므로 $2n=4$.
- $A \in \mathrm{Lagr}(4,\F_2)$: 2차원 Lagrangian 부분공간 전체. 개수
  $$|\mathrm{Lagr}(4,\F_2)| = (2^1+1)(2^2+1) = 15.$$
- $B \in \F_2^{m\times 4}$: 모든 $m\times 4$ 이진 행렬. 개수 $2^{4m}$.
- $e \in \F_2^4$: 각 좌표 독립 $\mathrm{Bernoulli}(1/4)$, 즉
  $$P(e) = (1/4)^{|e|}(3/4)^{4-|e|}.$$
- 출력:
  $$C = BA \in \F_2^{m\times 2}, \qquad e' = Be \in \F_2^m.$$

### 2.1 조걶부 잡음 분포

주어진 $C=C_0$에 대해

$$P(e'=v \mid C=C_0)
= \frac{\sum_{A,B,e:\, BA=C_0,\, Be=v} P(A)P(e)}
       {\sum_{A,B,e:\, BA=C_0} P(A)P(e)}.$$

$P(A)$는 Lagrangian 부분공간 위의 균등분포.

### 2.2 비교 대상

$$Q_{p'} = \mathrm{Bernoulli}(p')^m, \qquad p' \in [0,1/2].$$

`lem:m2`는 $1-2p' \ge 1/\operatorname{poly}(n)$인 모든 $p'$를 다루므로, $p'=1/4$ 외에도 여러 값을 시험한다. 추가로 각 $(B,C)$ 쌍에서 $p'$를 최적화한

$$\mathrm{SD}_{\min}(B,C) = \min_{p'\in[0,1/2]} \mathrm{SD}\bigl(P(e'\mid C),\, Q_{p'}\bigr)$$

도 기록한다.

### 2.3 통계적 거리

$$\mathrm{SD}(P,Q) = \frac12 \sum_{v\in\F_2^m} \bigl|P(v)-Q(v)\bigr|.$$

Sage의 `QQ`를 사용해 정확한 유리수로 계산한다.

---

## 3. 파라미터와 상태 공간

| $m$ | $|B|=2^{4m}$ | $|A|$ | 총 $(A,B)$ 쌍 | 예상 시간 |
|---:|---:|---:|---:|---|
| 3 | 4,096 | 15 | 61,440 | 즉시 |
| 4 | 65,536 | 15 | 983,040 | 수 초 |
| 5 | 1,048,576 | 15 | 15,728,640 | 수 분 |
| 6 | 16,777,216 | 15 | 251,658,240 | 수십 분~1시간 |

$m=3,4,5$는 완전 열거. $m=6$은 필요 시 제한적 샘플링 또는 추가 최적화.

---

## 4. Sage 워크플로우

1. **Lagrangian 열거**: Sage `VectorSpace(GF(2), 4)`에서 2차원 isotropic subspace 중 maximal인 것만 추려 15개 생성.
2. **$B$ 생성**: 비트마스크를 이용해 $\F_2^{m\times 4}$ 전체 생성.
3. **결합 분포 누적**: 모든 $(A,B,e)$에 대해
   - $C = BA$ 계산,
   - $e' = Be$ 계산,
   - $P(C)$ 및 $P(C,e')$에 가중치 $P(A)P(e)$ 누적.
4. **조걶부 분포**: 각 $C$별로 $P(e'\mid C)$를 정확 유리수로 구성.
5. **SD 계산**: $Q_{p'}$와의 SD를 계산하고, $p'$ 그리드 및 최적 $p'$에 대한 값 저장.
6. **결과 JSON 저장**:
   - $m$별 $\min/\max/\mathrm{avg}_{B,C}\, \mathrm{SD}$,
   - $\mathrm{SD}$가 최소가 되는 $B$와 $C$의 예시,
   - 조걶부 vs 비조걶부 SD 비교.

---

## 5. 성공/실패 기준

| 결과 | 해석 |
|------|------|
| $\min_{B,C} \mathrm{SD}$가 $0.3$ 이상 | 어떤 $B$도 $C$ 조건 하에서 i.i.d. 잡음을 완벽히 위조하지 못함. `lem:m2` 성립 쪽 정량적 근거. |
| 어떤 $B$에서 $\mathrm{SD} < 0.1$ | correlated noise $Be$가 i.i.d.처럼 보일 수 있는 후보. `lem:m2` 반례 후보로 분석 필요. |
| 조걶부 SD $\approx$ 비조걶부 SD | $e' \perp C$가 성립하는 징후. noise-side 독립성에 대한 강한 증거. |

---

## 6. 한계 및 다음 단계

- **$n=2$ 한계**: 결과가 일반 $n$에 자동으로 적용되지 않는다. 패턴/점근 분석이 필요.
- **비적응 $B$**: 본 실험은 $B$가 $A$와 독립일 때의 전수 조사다. 적응형 $B=g(A)$는 상태 공간이 훨씬 크므로, 이 실험 이후 제한된 적응 패밀리를 추가 조사한다.
- **전체 joint SD**: $\mathrm{SD}((C,y), \mathrm{LPN}_{p'})$는 상태 공간이 커서 별도 단계로 분리.
- **$m=6$ 이상**: 완전 열거가 무거우므로, 먼저 $m=3,4,5$ 결과를 보고 필요 시 확장.

---

## 7. 산출물

- `experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py`
- `experiments/output/184-lem-m2-n2-exact-conditional-noise-SD.json`
- 후속 메모: `meta/2026-06-13-KIMI-lem-m2-n2-exact-conditional-noise-SD-DRAFT.md`

---

**결정 사항:** 본 설계 A대로 진행한다. OP7은 본 실험이 종료된 뒤 재개.
