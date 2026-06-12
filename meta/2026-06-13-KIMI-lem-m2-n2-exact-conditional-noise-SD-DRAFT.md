# lem:m2 $n=2$ exact conditional noise SD — 결과 DRAFT

**Date:** 2026-06-13  
**Scope:** $n=2$에서 모든 $B\in\F_2^{m\times 4}$, 모든 Lagrangian $A$, 모든 noise $e$를 완전 열거하여 $P(e'=Be\mid C=BA)$와 $\mathrm{Bernoulli}(p')^m$의 정확한 SD를 계산.

---

## 1. 실험 설정

- $n=2$, $2n=4$
- $|\mathrm{Lagr}(4,\F_2)| = 15$
- $|B| = 2^{4m}$
- $e\sim\mathrm{Bernoulli}(1/4)^4$
- 비교 대상: $\mathrm{Bernoulli}(p')^m$, $p'\in\{0,0.05,0.1,\dots,0.5\}$
- 산출물: `experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py`
- 결과 JSON: `experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m{3,4,5}.json`

---

## 2. 핵심 수치 ($p'=1/4$)

| $m$ | best $B$ (열 표현) | best avg SD | worst avg SD | global conditional SD | global unconditional SD |
|---:|---|---:|---:|---:|---:|
| 3 | `[4,2,1,0]` | $0$ | $37/64\approx0.578$ | $31891/163840\approx0.195$ | $95/512\approx0.186$ |
| 4 | `[8,4,2,1]` | $0$ | $175/256\approx0.684$ | $33651/131072\approx0.257$ | $257/1024\approx0.251$ |
| 5 | `[8,4,2,1]$ | $1/4$ | $781/1024\approx0.763$ | $784095/2097152\approx0.374$ | $2775/8192\approx0.339$ |

---

## 3. 해석

### 3.1 worst / global — 랜덤 $B$는 i.i.d.를 못 흉낸다

- **worst avg SD**는 $m$이 커질수록 $1$에 가까워진다.
- **global conditional SD** 역시 $m=5$에서 $0.37$로 증가.
- 무작위 $B$에 대해서는 $Be$가 $C$ 조건 하에서도 i.i.d. Bernoulli와 명확히 구별된다.

### 3.2 best — 최악의 $B$는 완벽하게 흉낼 수 있다

- $m=3,4$에서 $B=I$ 형태의 행렬이 avg SD $=0$을 달성.
  - 이유: $e\in\F_2^4$의 처음 $m$ 비트를 그대로 출력하면 $\mathrm{Bernoulli}(1/4)^m$와 동일한 분포가 된다.
- $m=5$에서도 같은 $B$를 쓰면 5번째 출력 비트가 항상 $0$이 되어 SD $=1/4$.
  - $2n=4$차원 잡음으로는 5개 독립 좌표를 만들 수 없으므로 필연적.

### 3.3 lem:m2에 대한 의미

이 결과는 **noise-only 관점에서 lem:m2의 직관적 장애물이 $n=2$에서는 성립하지 않음**을 보인다:

- $m\le 2n$ 범위에서, 적절한(비적응) $B$가 있으면 $e'=Be$를 $p'=1/4$ i.i.d.와 완벽히 일치시킬 수 있다.
- 따라서 "$Be$가 $2n$차원 부분공간에 산다"는 사실만으로는 $C$ 조건 하에서의 i.i.d. 위조를 막지 못한다.

**하지만 이것이 lem:m2를 반증하는 것은 아니다.** `lem:m2`의 실제 명제는 전체 출력 $(C,y)$가 $\mathrm{LPN}_{p'}$와 가까운지를 묻는다. 여기서:

- $B=I$일 때 $C=BA$는 uniform $A$의 첫 $m$ 행이므로, **$C$ 자체가 uniform 한지는 별개 문제**다.
- $C$가 uniform하지 않다면 $(C,y)$는 이미 $\mathrm{LPN}_{p'}$가 아니다.
- 본 실험은 **noise 분포만** 격리해서 쟀을 뿐, $C$의 분포나 전체 joint SD는 측정하지 않았다.

따라서 결론은:

> **$n=2$에서 noise-only 장벽은 낮다.** lem:m2를 닫거나 열기 위해서는 $(C,y)$의 **전체 joint 분포**를 공격해야 한다.

---

## 4. 한계

- $n=2$만 다룸.
- $B$는 $A$와 독립인 비적응 행렬만 열거. 적응형 $B=g(A)$는 상태 공간이 훨씬 큼.
- $C=BA$의 균등성과 전체 $\mathrm{SD}((C,y),\mathrm{LPN}_{p'})$는 측정하지 않음.

---

## 5. 다음 단계 후보

1. **전체 joint SD**: $n=2$, $m=3$ 정도에서 $(C,y)$ 전체를 $\mathrm{LPN}_{p'}$와 비교.
2. **적응형 $B=g(A)$**: $C$를 균등하게 만드는 적응 행렬에서 $e'$ 분포 재조사.
3. **OP7로 복귀**: 해석적 시도가 noise-only로는 결론을 내리지 못했으므로, OP7 sample freshness 실험 재개.
