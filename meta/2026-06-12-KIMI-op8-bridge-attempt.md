# OP8 Bridge Attempt — Direction 2: THEIR LSN ≤ OUR membership-LSN

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review.  
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 정직한 출발점 — 정의 격차 (definition gap)

논문 `subsec:two-forms` line 238은 그들 LSN을 요약적으로만 기술:
> "Their (classical) LSN has a public isotropic matrix $[A \mid B]$, a junk register $x$, and a secret logical string $y$."

**정확한 라벨 생성 메커니즘**이 명시되지 않았다. 아래 분석은 *구조적 유추*를 바탕으로 하며, KLP+25 원문 확인이 필요한 지점은 **⚠ gap**으로 표기.

---

## 1. 구조적 유추 — 그들 인스턴스의 합리적 모델링

### 1.1 그들 LSN의 자연스러운 해석

KLP+25의 stabilizer-decoding LSN은 stabilizer code의 *고전적* 샘플링 문제로 해석될 수 있다.

- **Physical space:** $\F_2^{2n}$ (Pauli operator space, symplectic).
- **Public $S = [A \mid B] \in \mathrm{Sp}(2n)$:** symplectic basis.  
  - 첫 $n$ columns $A$가 하나의 Lagrangian $L_0 = \operatorname{colspan}(A)$를 생성.
  - 나머지 $n$ columns $B$는 dual basis.
- **Secret $y \in \F_2^k$ ($k=1$ for KLP+25 single-logical):** logical string.
- **Junk $x \in \F_2^{n-k}$:** stabilizer group 내의 자유도 (ancilla / syndrome space).

**라벨의 자연스러운 형태 (가설):**  
⚠ gap — KLP+25 원문 확인 필요. 가장 합리적인 추정은:
$$b = \mathbf{1}_{C_{x,y}}(q) \oplus e$$
where $C_{x,y} = \{\,S \cdot (x', y')^T \;:\; x' \in \F_2^{n-k},\; y' = y\,\}$ is the **code coset** for logical string $y$ (with junk $x$ marginalized or fixed).

즉, 그들의 라벨은 **고정 logical string $y$에 해당하는 stabilizer code coset**에 대한 membership이다.

**우리 membership-LSN과의 차이:**
| | 우리 | 그들 (가설) |
|---|---|---|
| 비밀 | Lagrangian $L$ | logical string $y$ (공개 $S$가 주어짐) |
| 쿼리 분포 | uniform $a \sim \F_2^{2n}$ | uniform $q \sim \F_2^{2n}$ (또는 $S$의 row) |
| 라벨 | $1_L(a) \oplus e$ | $1_{C_{x,y}}(q) \oplus e$ |

---

## 2. Direction 2 환원 맵 (THEIR ≤ OUR)

**목표:** 그들 인스턴스 $(S, y, \{(q_i, b_i)\})$를 우리 인스턴스 $(L, \{(a_i, b_i)\})$로 변환하여, 우리 solver가 $L$을 찾으면 $y$를 복원.

### 2.1 제안된 환원 (가설적)

**Step 1 — 공구조 숨기기 (hiding public structure).**  
그들 인스턴스의 공개 $S$는 symplectic matrix. $S$를 "숨기기" 위해 쿼리를 $S^{-1}$로 변환:
$$a_i := S^{-1} q_i$$
$q_i$가 uniform이고 $S \in \mathrm{Sp}(2n)$이면 $a_i$도 uniform.

**Step 2 — 라벨의 재표현.**  
$b_i = 1_{C_{x,y}}(q_i) \oplus e_i = 1_{C_{x,y}}(S a_i) \oplus e_i = 1_{S^{-1} C_{x,y}}(a_i) \oplus e_i$.

$S^{-1} C_{x,y}$는 무엇인가?  
$C_{x,y} = S \cdot \{(x', y) : x' \in \F_2^{n-k}\}$  
$S^{-1} C_{x,y} = \{(x', y) : x' \in \F_2^{n-k}\} = \F_2^{n-k} \times \{y\}$.

이건 **affine subspace**이지만 **Lagrangian이 아니다** (dimension $n-k < n$ for $k \ge 1$).

**결론:** 이 직접적인 환원은 우리의 membership-LSN (Lagrangian secret)로 직접 매핑되지 않는다. 그들의 coset은 dimension $n-k$인 반면, 우리 secret은 dimension $n$.

---

## 3. 막힘 분석 — 핵심 obstacle

### Obstacle 1: Dimension mismatch
그들의 secret은 $k$-bit logical string ($k=1$ 또는 작음). 우리 secret은 $n^2/2$-bit Lagrangian.  
그들 인스턴스의 "하드니스"는 $k$-bit secret에서 온다. 우리 solver가 $2^{n^2/2}$ 크기의 공간을 검색한다면 $k$-bit secret은 지나치게 쉬울 수 있다.

### Obstacle 2: Public structure cannot be fully hidden
$S$가 public이면, adversary는 $S^{-1}$를 써서 문제를 표준 형태로 변환할 수 있다. 우리 membership-LSN은 *어떤 공개 구조도 없다*. 그들의 공개 $S$를 "숨기는" 환원은 adversary의 능력을 제한하지 않는다 (reduction algorithm은 $S$를 볼 수 있으므로).

### Obstacle 3: Different secret spaces
- 그들: secret $y \in \F_2^k$ (적은 엔트로피).
- 우리: secret $L \in \Lagr(2n)$ (많은 엔트로피).
- 환원 THEIR ≤ OUR은 "OUR solver를 써서 THEIR를 푼다"는 의미. OUR solver가 $L$을 복원하면, 거기서 $y$를 추출해야 한다. 하지만 $L$이 $y$보다 훨씬 더 큰 secret space를 가지므로, 이 추출이 non-trivial.

---

## 4. 대안 가설 — 그들 LSN이 batch-LSN의 특수한 경우?

**가설 B:** 그들 LSN이 실은 **우리 batch-LSN**과 동일하거나 더 구조화된 형태일 수 있다.

- 만약 KLP+25의 classical LSN이 "public $S$, secret = Lagrangian $L = S \cdot L_0$"라면:
  - 이건 우리 batch-LSN의 특수한 경우 (public matrix가 symplectic constraint를 만족).
  - 그 경우 THEIR ≤ OUR은 **자명** (더 구조화된 문제 → 덜 구조화된 문제).
  - 하지만 논문 line 238은 secret을 "logical string $y$"라고 하지 "Lagrangian"이라고 하지 않는다.

- 만약 secret이 $y$이고 $L$이 $y$의 함수 $L(y)$라면:
  - 환원: $(S, y) \mapsto L(y)$, 쿼리는 $S^{-1}$ 변환.
  - 그들 solver가 $y$를 찾으면 $L(y)$도 알 수 있음 (public $S$로부터).
  - 반대 방향(OUR ≤ THEIR)이 더 자연스러울 수 있다.

---

## 5. 정직한 평가

| 결과 시나리오 | 가능성 | 코멘트 |
|---|---|---|
| **REDUCES** | 낮음 (현재 정보로) | Dimension mismatch + public structure hiding 문제. $k$-bit secret을 $n^2/2$-bit secret으로 embed하는 것이 non-trivial. |
| **BROKEN (named obstruction)** | 높음 | 위 Obstacle 1–3이 정확한 named obstruction으로 작용 가능. "Public symplectic basis $S$는 membership oracle의 query-independent secret structure와 호환되지 않음" 같은 정밀한 서술 가능. |
| **OPEN (gap narrowing)** | 가능 | 그들 LSN의 정확한 라벨 정의가 확인되면 gap이 더 좁혀질 수 있음. |

**현재 상태:** 정의 격차 ⚠ gap 때문에 formal proof는 불가. 하지만 **structural mismatch**가 명확하며, 이를 precise obstruction으로 정형화할 수 있다.

---

## 6. 다음 단계 제안

1. **KLP+25 원문 확인** — classical LSN의 정확한 정의(라벨 생성, 쿼리 분포, secret space) 확인. ⚠ gap 해소.
2. **Named obstruction DRAFT** — 현재 obstacle 1–3을 "public symplectic basis ↔ secret Lagrangian" incompatibility로 정형화. 이것 자체가 논문급 진보.
3. **작은 $n$ sanity check** — KLP+25 정의 확인 후, $n=2,3$에서 환원 시도 (코드+JSON).

---

## 7. Gate check

- **No closure claim:** "낮음/높음"은 휴리스틱 평가, proof 아님.
- **No break:** REDUCES 실패 ≠ scheme broken.
- **No security claim:** LSN 자체의 hardness를 주장하지 않음.
- **정의 격차 명시:** ⚠ gap 표기로 정직함 유지.

No closure; no break; no security claim. OPEN = LSN.
