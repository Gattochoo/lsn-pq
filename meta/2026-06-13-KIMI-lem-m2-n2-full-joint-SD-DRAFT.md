# lem:m2 $n=2$ full joint SD — 결과 DRAFT

**Date:** 2026-06-13  
**Scope:** $n=2$에서 모든 비적응 $B\in\F_2^{m\times 4}$에 대해, 환원 출력 $(C,y)$와 표준 $\mathrm{LPN}_{1/4}$의 전체 결합분포 사이 정확한 통계적 거리를 계산.

---

## 1. 실험 설정

- $n=2$, $2n=4$
- $|\mathrm{Lagr}(4,\F_2)| = 15$
- $|x| = 4$, $|e| = 16$
- $|B| = 2^{4m}$
- $e\sim\mathrm{Bernoulli}(1/4)^4$
- 비교 대상: $\mathrm{LPN}_{p'}$ with $p'=1/4$
- 산출물: `experiments/185-KIMI-lem-m2-n2-full-joint-SD.py`
- 결과 JSON: `experiments/output/185-lem-m2-n2-full-joint-SD-m{3,4}.json`

---

## 2. 핵심 수치

| $m$ | $\min_B \mathrm{SD}$ | $\max_B \mathrm{SD}$ | $\mathrm{avg}_B \mathrm{SD}$ | best $B$ | worst $B$ |
|---:|---:|---:|---:|---|---|
| 3 | $49/64 \approx 0.766$ | $4069/4096 \approx 0.993$ | $\approx 0.836$ | `[0,4,2,1]` | `[0,0,0,0]` |
| 4 | $241/256 \approx 0.941$ | $65455/65536 \approx 0.999$ | $\approx 0.961$ | `[0,8,4,2]` | `[0,0,0,0]` |

---

## 3. 해석

### 3.1 결정적 결과

- **모든 $B$에 대해 $\mathrm{SD}((C,y), \mathrm{LPN}_{1/4}) \ge 0.766$** ($m=3$), **$\ge 0.941$** ($m=4$).
- 즉, $n=2$에서 어떤 비적응 $B$도 $(C,y)$를 $\mathrm{LPN}_{1/4}$와 완벽히 또는 거의 일치시키지 못한다.

### 3.2 이전 noise-only 결과와의 대비

- noise-only 실험(184)에서는 $B=I$ 형태가 $e'=Be$를 $\mathrm{Bernoulli}(1/4)^m$와 정확히 일치시켰다 ($m=3,4$에서 min SD $=0$).
- 그러나 **전체 joint 분포로 볼 때는 그 $B$조차 LPN과 매우 멀다**.
- 이유: $C=BA$가 uniform하지 않기 때문. $B=I$일 때 $C$는 uniform Lagrangian $A$의 첫 $m$ 행으로, standard LPN의 uniform $C$와 다른 분포를 가진다.

### 3.3 lem:m2에 대한 의미

> **$n=2$ non-adaptive 설정에서 lem:m2는 성립한다.**

적어도 $m=3,4$ 범위에서는, $2n$차원 correlated noise 구조가 $(C,y)$ 전체를 위조하는 것을 막는다. 이는 `lem:m2`의 직관 — “고정 $2n$차원 잡음이 i.i.d. Bernoulli를 위조 못 한다” — 를 $n=2$에서 정량적으로 뒷받침한다.

---

## 4. 한계

- $n=2$만 다룸.
- 비적응 $B$만 열거. 적응형 $B=g(A)$, 특히 $C$를 균등하게 만드는 경우는 별도 문제.
- $p'=1/4$만 비교.

---

## 5. 다음 단계 후보

1. **적응형 $B=g(A)$**: $BA$가 균등하도록 하는 $B$를 찾아서, 그때의 full joint SD를 측정. 이게 lem:m2의 진짜 모서리.
2. **$n=3$**: 상태 공간이 커지지만, sampling 또는 Sage 기반 bulk counting으로 확장.
3. **OP7 복귀**: 현재 해석적 시도가 lem:m2 성립 쪽 강한 증거를 주었으므로, OP7 sample freshness 실험 재개.
