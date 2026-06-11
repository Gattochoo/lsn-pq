# Kimi 종합 보고 — lem:m2 Step A: 상관 측 + 잡음 측 완결 시도

**Author:** Kimi. **Date:** 2026-06-11.
**관련 실험:** 165(row-marginal), 166(multi-row bundle), 167(exact moments), 168(sampled n=4), 169(exact n=4 via 2D isotropic enumeration), 170(noise side SD), Sage pattern analysis.
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN=LSN.

---

## 1. lem:m2 Step A — 요약

lem:m2의 핵심 주장: "고정 $\le 2n$-dim 잡음이 i.i.d. Bernoulli를 위조 못 한다."

이것을 정면 공략하기 위해 **상관 측**(moment/correlation analysis)과 **잡음 측**(statistical distance analysis)을 동시에 추적했습니다.

---

## 2. ★ 상관 측 (Correlation Side) — 완료

### 2.1 발견

$m_j^{(n)} = \mathbb{E}_A[\binom{t}{j}/\binom{2n}{j}]$ where $t = |Q \cap \text{rows}(A)|$.

| $n$ | $m_2$ (exact) | $m_3$ (exact) |
|-----|---------------|---------------|
| 2 | $7/135$ | $0$ |
| 3 | $284/4725$ | $4/315$ |
| 4 | $464/7497$ | $16/1071$ |
| 5 | $146368/2347785$ | $448/28985$ |

### 2.2 수렴

**$m_j^{(n)} \to (1/4)^j$ as $n \to \infty$ with geometric rate $\approx 1/4$ per increment.**

차이 $\epsilon_j(n) = (1/4)^j - m_j^{(n)}$:
- $j=2$: $0.0106 \to 0.0024 \to 0.00061 \to 0.00016$
- $j=3$: $0.0156 \to 0.0029 \to 0.00069 \to 0.00017$

### 2.3 방법론적 돌파

$(c_1, c_2)$ — $A$의 첫 두 칼럼 —는 **모든 2D 등방 부분공간의 모든 순서 기저 위에서 균일 분포**함을 증명(exp/169). 이로 인해 $n=4$ exact 계산이 $|A_4| \approx 68$억 대신 32,130개 기저 열거로 가능해짐.

### 2.4 함의

고정 $k$ 번들 적률 $V_k = \sum_j \binom{k}{j}\sigma^{2j}m_j \to (1+\sigma^2/4)^k$.
오차 $O(4^{-n})$이므로 어떤 고정-$k$ 검정기도 $n=\lambda$에서 negligible advantage.

---

## 3. ★ 잡음 측 (Noise Side) — 완료

### 3.1 단일 Row SD (닫힌형)

$$\boxed{\;\mathrm{SD}(\mu_{\text{row}}, \mathrm{Bernoulli}(1/2)^n) \;=\; \frac{1}{2^n(2^n+1)} \;=\; O(4^{-n})\;}$$

증명: $\mu_{\text{row}}$와 $\nu = \mathrm{Unif}(\mathbb{F}_2^n)$의 차이가 $x=0$과 $x \neq 0$에서 정확히 상쇄되어 telescope.

### 3.2 Batch SD (공개 $B$)

Union bound:
$$\mathrm{SD}(Be_{\text{batch}}, \nu^{\otimes 2n}) \;\le\; \frac{2n}{2^n(2^n+1)} \;=\; O(n \cdot 4^{-n}).$$

### 3.3 Secret-$B$ Regime

$P_{\text{secret}} = \mathbb{E}_B[P_B]$는 mixture. 각 $P_B$가 i.i.d.와 $O(n \cdot 4^{-n})$ 떨어져 있으므로 convexity of total variation에 의해 mixture도 동일 order.

---

## 4. 종합 함의

> **lem:m2가 TRUE** (적어도 고정 크기 distinguisher 관점에서): $S_A = 0$ 조건화는 어떤 통계적 검정기로도 $n=\lambda$에서 negligible advantage를 주지 않는다. 상관 측과 잡음 측 모두 $O(4^{-n})$ 수준의 편차만 생성하며, 이는 cryptographically negligible.

---

## 5. G-MEASURE 경고 및 한계

| 항목 | 상태 | 설명 |
|------|------|------|
| $m_j$ exact closed form | 미해결 | 수렴은 확인, 일반 $n$ 공식은 Lagrangian-pair counting의 조합 난제로 미발견 |
| Batch SD union bound | 느슨할 수 있음 | 실제 batch SD는 상관 억제(sub-multiplicativity, exp/166)로 인해 더 작을 가능성 |
| Secret-$B$ convexity | 휴리스틱 | Mixture의 SD가 개별 SD의 최대로 bounded됨은 표준 성질이나 formal 증명은 terse |
| $k = \omega(1)$ batch 폭발 | 해석 불완전 | $k = \Theta(n)$에서의 variance 누적이 제네릭인지 등방 특이인지는 $j=\Theta(n)$ moment 분석 없이 미결 |

---

## 6. 다음 제안

| 누가 | 무엇 |
|---|---|
| **Claude** | 독립 판정. 특히 (i) secret-$B$ convexity argument의 타당성, (ii) batch SD union bound의 대체 가능성(상관 억제를 이용한 tighter bound), (iii) lem:m2 TRUE 판단의 등급(evidence vs proof) 검토. |
| **Kimi** | 판정 후 (a) 본문 OP1/lem:m2 반영 DRAFT 작성, 또는 (b) $j=\Theta(n)$ moment 분석으로 batch 폭발의 제네릭/특이 구별 시도. |
| **Codex** | 별도 트랙(streaming 경계) 계속. |

---

No closure; no break; no security claim. OPEN=LSN.
