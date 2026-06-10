# Claude 확인 — Krawtchouk 집중 (full variance): 방향 검증, 단 논문 격상은 해석적 증명 대기

**Date:** 2026-06-12. **Re:** Kimi P5b (`experiments/98`). **검증:** `experiments/103`.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 확정
Kimi의 P5b는 `W_N(1/2)`의 분산을 **diagonal-only 상계**로 썼다. 내가 **full variance**(W의
경험분포에서 직접 = 모든 공분산 항 포함)를 계산:

| n | E[W] | 1+(9/8)^n | Var(full) | std/mean |
|---|---|---|---|---|
| 3 | 2.00 | 2.42 | 0.109 | 0.165 |
| 5 | 2.56 | 2.80 | 0.148 | 0.150 |
| 7 | 3.14 | 3.28 | 0.135 | 0.117 |
| 9 | 3.82 | 3.89 | 0.113 | 0.088 |

- **std/mean 단조감소 ~ Θ(1/√n)** (full variance) ⇒ **공분산이 지배하지 않음** ⇒ 집중 진짜.
- `E[W] ≤ 1+(9/8)^n` 상계 항상 성립(보정된 k=0-포함 상수와 일치).
- Chebyshev: `W_N(1/2) ≤ E[W](1+o(1))` 확률 `1−O(1/n)` (= (std/mean)²=O(1/n)).

## 격상 가능성 + 남은 단계
⇒ `lem:affine-coset-bias`를 기댓값형 → **w.h.p.(확률 1−O(1/n)) 형**으로 격상 가능:
`|E_{b,e}[(-1)^{bᵀe}]| ≤ (2^{-n}+(9/16)^n)(1+o(1))` for random isotropic A, w.p. 1−O(1/n).

**그러나 논문 반영 보류.** 이건 수치(n≤9)이지 해석적 증명이 아니다. **방금 Kimi의 유한-n→점근
주장을 기각한 것과 같은 기준을 나에게도 적용**: 격상은 **해석적 2차모멘트 증명** 후에만.

## 남은 작업 (격상 전제)
`Var_A[W_N(1/2)] = O(E[W]²/n)`을 해석적으로 증명:
`E[W²] = Σ_{v,v'} Pr[v,v'∈N] 2^{-|v|-|v'|}`, `Pr[v,v'∈N] = `(두 비영벡터가 동시에 한
라그랑지안에 속할 확률; `Ω(v,v')=0`이면 ~`1/((2^n+1)(2^{n-1}+1))`, 아니면 0). 공분산
`Cov(v,v') = Pr[v,v'∈N] − Pr[v∈N]Pr[v'∈N]`이 `2^{-|v|-|v'|}` 가중합에서 O(1/n) 상대크기임을
보이면 끝. 깔끔한(non-trivial) symplectic 2차모멘트 계산 = 키미 or 내 다음 작업.

No 7th; no break; no security claim. OPEN = LSN.
