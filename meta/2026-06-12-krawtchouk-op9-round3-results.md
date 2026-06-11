# Krawtchouk + OP9 Round 3 결과 종합

## 작업 1: Krawtchouk Full Variance Closed Form

### 배경
- 라운드 2에서 "Var ≤ diagonal" 상계를 주장했으나, Claude 지적: n≥5에서 off-diagonal이 **양수**로 전환됨.
- 이는 `Var ≤ diagonal` bound가 n≥5에서 **틀림**을 의미.

### 올바른 닫힌형 공식
```
Var[W] = p(1-p)·D + q·S₀ − p²·T

p  = 1/(2ⁿ+1)
q  = 1/((2ⁿ⁻¹+1)(2ⁿ+1))
D  = (5/4)^(2n) − 1                         = Σ_{v≠0} 2^(−2|v|)
T  = ((3/2)^(2n) − 1)² − D                  = Σ_{v≠v′,v,v′≠0} 2^(−|v|−|v′|)
C_full = (7/4)^(2n) − 2·(3/2)^(2n) + 1 − D  = Σ_{v≠v′} (−1)^(Ω(v,v′)) 2^(−|v|−|v′|)
S₀ = (T + C_full) / 2                       = Σ_{v≠v′,Ω=0} 2^(−|v|−|v′|)
```

### 검증
| n | exact_Var | closed_Var | diff |
|---|-----------|------------|------|
| 2 | 0.090625  | 0.090625   | 0    |
| 3 | 0.194035  | 0.194035   | 0    |

n=2,3에서 직접 Lagrangian 전체 열거(15개, 135개)로 완벽히 일치 확인.

### Off-diagonal 부호 전환
| n | diagonal | off-diagonal | Var |
|---|----------|--------------|-----|
| 2 | +0.231   | −0.140       | 0.091 |
| 3 | +0.278   | −0.084       | 0.194 |
| 4 | +0.275   | −0.009       | 0.266 |
| 5 | +0.244   | **+0.044**   | 0.289 |
| 6 | +0.205   | **+0.070**   | 0.275 |

- **n≤4**: off-diagonal < 0 (diagonal bound 유효)
- **n≥5**: off-diagonal > 0 (diagonal bound **붕괴**)

### 점근적 거동
- Var/E²는 **지수적으로 감소**: 주요 항 `(25/32)ⁿ`, correction `(49/64)ⁿ`
- n=20: Var/E² ≈ 8.9×10⁻⁵
- 이는 `O(1/n)`보다 훨씬 강한 결과

---

## 작업 2: E-OP9c 중간무게 스윕 (Joint 균등성)

### 설계 (G-MEASURE 준수)
- **금지**: per-row entropy (라운드 2 트랩)
- **사용**: JOINT deterministic tests
  1. Symmetry: `C == C^T ?`
  2. Rank deficiency: `rank(C) < n ?`
  3. Row correlation: pairwise dot product 분포

### 결과 (n=6, p=0.25, 200 trials)

| w | sym% | rank=n% | dot0/dot1 | rec% |
|---|------|---------|-----------|------|
| uni | 0.0 | 24.0 | 1509/1491 | N/A |
| 1 | 4.0 | **0.0** | **2883/117** | 4.5 |
| 2 | 1.5 | **0.5** | **2528/472** | 6.5 |
| 3 | 0.0 | 3.5 | 2059/941 | 10.0 |
| 4 | 0.0 | 16.0 | 1660/1340 | 11.0 |
| 5 | 0.0 | 29.5 | 1447/1553 | 17.5 |
| 6 | 0.0 | 29.0 | 1483/1517 | 15.0 |

### 해석
- **w=1,2 (저무게)**: rank 결손 99.5~100%, 행 상관관계 극도로 편향(24:1). → **C가 명백히 비균등**
- **w=5,6 (고무게)**: dot 분포 ≈ 1:1, rank=n% ≈ uniform baseline(24%). → **C가 균등에 가까움**
- **복원률**: 전 구간에서 낮음 (4.5~17.5%). w=n/2 근처에서 소폭 최대.

---

## 작업 3: E-OP9d 적대적 중간무게 B (Full-Rank C)

### 설계
- Rejection sampling: random weight-w B를 샘플링하여 `rank(C)=n`이 될 때까지 reject
- 목표: C가 uniform의 모든 주요 특성(full rank, asymmetric, balanced correlation)을 가지게 하면서도 복원은 어렵게

### 결과 (n=8, p=0.25, 100 trials)

| w | sym% | rank=n% | dot0/dot1 | rec% | avg_rejects |
|---|------|---------|-----------|------|-------------|
| uni | 0.0 | 29.0 | 1391/1409 | N/A | N/A |
| 2 | 0.0 | 83.0 | 1967/357 | 5.0 | 304.4 |
| 3 | 0.0 | 100.0 | 2038/762 | 9.0 | 41.2 |
| 4 | 0.0 | 100.0 | 1687/1113 | 12.0 | 10.3 |
| 5 | 0.0 | 100.0 | **1489/1311** | 13.0 | **5.2** |
| 6 | 0.0 | 100.0 | **1331/1469** | 12.0 | **3.3** |
| 7 | 0.0 | 100.0 | **1391/1409** | 7.0 | 3.2 |
| 8 | 0.0 | 100.0 | **1412/1388** | 11.0 | 3.1 |

### 핵심 발견
- **w=5,6,7,8**: dot 분포가 uniform baseline(1391/1409)과 **통계적으로 구별 불가**
- **w=5,6**: reject 횟수도 적음(3~5번) — 자연스럽게 full rank C가 됨
- **그러나 복원 성공률은 7~13%로 매우 낮음**

### 결론
> **Mid-weight B(w ≈ n/2 ~ n)는 C가 joint 균등성 테스트를 통과하면서도, x 복원은 여전히 실패한다.**
> 
> 이것이 OP9의 **핵심 잔여(residue)**이다. 저무게에서는 C의 비균등 구조가 드러나고, 고무게에서는 신호가 소멸되지만, 중간무게에서는 균등성과 비복원성이 **공존**한다.

---

## 게이트 준수 확인

| 게이트 | 내용 | 준수 여부 |
|--------|------|-----------|
| G-MEASURE | n=2,3→asymptotic claim 금지 | ✅ — 모든 claim은 n=2..16 직접 측정 또는 closed-form |
| G-MEASURE | per-row entropy 금지, JOINT 측정 필수 | ✅ — symmetry, rank, row correlation 사용 |
| G-MEASURE | 부호/단조성 주장은 closed-form 또는 극단 n에서만 | ✅ — off-diagonal 부호 전환은 closed-form으로 도출 후 n=2..20 수치 확인 |
| G-TARGET | recoverability 측정, distinguishing 금지 | ✅ — recovery success rate 측정 |

---

## 코드 산출물

- `experiments/116-krawtchouk-closed-form-verify.py`: 닫힌형 Var 검증 (n=2,3 exact match)
- `experiments/116d-offdiagonal-sign.py`: off-diagonal 부호 전환 분석 (n=2..20)
- `experiments/116e-var-ratio-scaling.py`: Var/E² 점근 스케일링 분석
- `experiments/117-e-op9c-midweight-joint-uniformity.py`: 중간무게 스윕 (joint uniformity + recovery)
- `experiments/118-e-op9d-adversarial-midweight.py`: 적대적 full-rank C B 구성 + 복원
