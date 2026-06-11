# Pencil-Extremality Conjecture — Analysis DRAFT (rev2)

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (rev2 after adjudication 8b3ac65 — k=1/k=3 columns fixed).  
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. 문제 정확히 세우기

### 1.1 배경

`lem:exact-corr` (Eq.~\ref{eq:exact-corr}):
$$\langle D_L, D_{L'} \rangle = \frac{(1-2p)^2}{p(1-p)} \cdot 2^{j-2n}, \qquad j = \dim(L \cap L').$$

Subset $\mathcal{D}' \subseteq \{D_L\}$의 **평균 correlation**:
$$\overline{\rho}(\mathcal{D}') = \frac{1}{|\mathcal{D}'|^2}\sum_{L,L' \in \mathcal{D}'} \langle D_L, D_{L'} \rangle \propto \frac{1}{|\mathcal{D}'|^2}\sum_{L,L' \in \mathcal{D}'} 2^{\dim(L \cap L')}.$$

**Conjecture (`conj:pencil`):** 모든 $|\mathcal{D}'| \ge |\Lagr(2n)|/2^{2n-c}$인 subset은 $\overline{\rho}(\mathcal{D}') \le 5\rho_{\mathrm{avg}}$.

### 1.2 Isotropic pencil의 정의

$W \subseteq \F_2^{2n}$를 dimension-$k$ isotropic subspace라 하자.  
**$k$-pencil** $S_W$는 $W$를 포함하는 모든 Lagrangian의 집합:
$$S_W = \{\,L \in \Lagr(2n) : W \subseteq L\,\}.$$

**크기 (exact):**
$$|S_W| = |\Lagr\bigl(2(n-k)\bigr)| = \prod_{i=1}^{n-k}(2^i+1).$$

**증명:** $W^\perp/W \cong \F_2^{2(n-k)}$이며, $W$를 포함하는 Lagrangian은 이 quotient의 Lagrangian과 일대일 대응. ∎

**평균 intersection (exact):**
$L, L' \in S_W$이면 $L = W \oplus \tilde{L}$, $L' = W \oplus \tilde{L}'$이고,
$$\dim(L \cap L') = k + \dim(\tilde{L} \cap \tilde{L}').$$
따라서
$$\frac{1}{|S_W|^2}\sum_{L,L' \in S_W} 2^{\dim(L \cap L')} = 2^k \cdot \mathbb{E}_{\tilde{L},\tilde{L}' \in \Lagr(2(n-k))}\bigl[2^{\dim(\tilde{L} \cap \tilde{L}')}\bigr].$$

---

## 2. Pencil이 threshold에 걸치는 규모

**Threshold:** $T_n = |\Lagr(2n)| / 2^{2n}$.

**$k=2$ pencil의 크기:**
$$|S_W| = \frac{|\Lagr(2n)|}{(2^{n-1}+1)(2^n+1)}.$$

**크기 비율:**
$$\frac{|S_W|}{T_n} = \frac{2^{2n}}{(2^{n-1}+1)(2^n+1)} = 2 \cdot \frac{2^{2n-1}}{(2^{n-1}+1)(2^n+1)} \xrightarrow[n\to\infty]{} 2.$$

| $n$ | $|S_W|$ | $T_n$ | $|S_W|/T_n$ |
|-----|--------|-------|-------------|
| 3 | 3 | 2.11 | 1.42 |
| 4 | 15 | 8.96 | 1.67 |
| 5 | 135 | 73.96 | 1.83 |
| 6 | 2295 | 1201.85 | 1.91 |
| 8 | 4922775 | 2490307.00 | 1.98 |

**→ $k=2$ pencil은 asymptotically $2 \times$ threshold.** $k \ge 3$은 모든 $n \ge 3$에서 threshold 아래. 이건 `experiments/80` 수치와 일치.

---

## 3. Pencil의 평균 correlation 비율

**Global 평균:** $E_n = \mathbb{E}_{L,L' \in \Lagr(2n)}[2^{\dim(L \cap L')}]$ (distinct pairs).

**$k$-pencil 평균:** $E_{n,k}^{\mathrm{pen}} = 2^k \cdot E_{n-k}$.

**비율:** $R_{n,k} = E_{n,k}^{\mathrm{pen}} / E_n = 2^k \cdot E_{n-k} / E_n$.

| $n$ | $E_n$ | $R_{n,1}$ | $R_{n,2}$ | $R_{n,3}$ |
|-----|-------|-----------|-----------|-----------|
| 3 | 1.7313 | 1.6502 | **2.3103** | — |
| 4 | 1.8762 | 1.8456 | **3.0457** | 4.2639 |
| 5 | 1.9390 | 1.9352 | **3.5716** | 5.8941 |
| 6 | 1.9692 | 1.9693 | **3.8111** | 7.0336 |
| 8 | 1.9922 | 1.9922 | **3.9538** | 7.7863 |
| 10 | 1.9980 | 1.9980 | **3.9883** | 7.9457 |

**관찰:**
- $R_{n,1} \to 2$ from below (exact limit: $2^1 \cdot 2 / 2 = 2$).
- $R_{n,2} \to 4$ from below (exact limit: $2^2 \cdot 2 / 2 = 4$).
- $R_{n,3} \to 8$ from below (exact limit: $2^3 \cdot 2 / 2 = 8$), and $k=3$ pencils are below threshold for all $n \ge 3$ (size ratio $0.47 \cdot T_3$ at $n=3$).
- **Conjecture의 $5\rho_{\mathrm{avg}}$ threshold는 $k=2$ pencil의 $\approx 4\rho_{\mathrm{avg}}$보다 여유 있음.**

---

## 4. n=3 완전 열거 검증 (G-MEASURE)

`experiments/80-sda-pencil-and-spread.py` part1 결과:
- $n=3$, $|\Lagr| = 135$, $T_3 = 135/64 = 2.11$.
- 모든 dim-2 isotropic subspace $W$에 대해 pencil $S_W$의 평균 $2^{\dim\cap} = 4.0$.
- Global 평균 $E_3 = 1.7313$.
- **Ratio = $4.0 / 1.7313 = 2.3103$** — 이 값은 **$R_{3,2}$**이다 (주의: $n=3$에서 $n-k=1$, $E_1=1$, $2^2 \cdot 1 / 1.7313 = 2.3103$). $R_{3,1} = 2 \cdot E_2 / E_3 = 1.6502$.

**완전 열수 추가 검증:** size $\ge T_3 = 2.11$ (즉 $\ge 3$)인 모든 subset 중에서 pencil이 extremal인지 brute-force 확인.
- size=3 subset: $\binom{135}{3} = 397,110$개. 계산 가능.
- size=4 subset: $\binom{135}{4} \approx 9.2 \times 10^6$개. 계산 가능하지만 시간 소모.

⚠ **n=3은 특수:** $n-k=1$이라 $E_{n-k}=1$ (Lagr(2)는 3개 line, pairwise intersection dim=0). 따라서 $n=3$에서의 ratio는 $n \ge 4$의 asymptotic과 다르다. **n=3 단정 금지** (지시서 G-MEASURE 가드 준수).

---

## 5. Proof strategy (시도)

### 5.1 Character sum 접근

모든 Lagrangian에 대한 평균은 Krawtchouk appendix에서처럼 character sum으로 쓸 수 있다. 하지만 **subset에 대한 worst-case**는 Fourier coefficient의 최댓값 문제가 되어, random subset이 아닌 structured subset에서의 extremal behavior를 다루어야 한다.

**핵심 어려움:** Krawtchouk appendix는 **평균**($\mathbb{E}_A$)을 다룸. Pencil-extremality는 **worst-case** subset을 다룸. 둘의 난이도 차이가 크다.

### 5.2 구조적 분류 접근

논문 motivation: "A proof would require classifying near-extremal subsets."

가능한 접근:
1. **Alon–de la Vega–Kannan–Krivelevic–Samotij style** sparse graph regularity: Lagrangian graph를 dense graph로 보고, extremal subset이 "almost pencil" 구조를 가져야 함을 보임.
2. **Fourier analysis on $\mathrm{Sp}(2n)$:** subset $\mathcal{D}'$의 indicator function을 $\mathrm{Sp}(2n)$ representation theory로 전개. 큰 Fourier coefficient를 가지면 subgroup structure(pencil)이 나타난다는 결과 활용 (Gowers norm / higher-order Fourier analysis).
3. **Combinatorial design theory:** symplectic spread와 pencil은 특수한 block design. Extremal subset이 이런 design의 union이나 perturbation임을 보임.

### 5.3 현실적 평가

| 접근 | 가능성 | 코멘트 |
|------|--------|--------|
| Character sum (Krawtchouk식) | 낮음 | Worst-case가 아닌 평균만 다룸. |
| Fourier on Sp(2n) | 중간 | Representation theory 복잡. symplectic group의 덧셈 캐릭터가 non-abelian. |
| Graph regularity + structure | 중간 | Alon-style argument가 적용될 수 있으나, Lagrangian graph의 특수 구조가 필요. |
| 직접 조합 분류 | 높음 (장기) | Near-extremal subset이 "almost pencil"임을 직접 증명. $n=2,3,4$ brute-force로 pattern 확인 후 일반화. |

---

## 6. 다음 단계 제안

1. **n=4 brute-force:** $|\Lagr(8)| = 2295$. Size $\ge T_4 = 2295/256 \approx 8.96$ (즉 $\ge 9$)인 모든 subset을 brute-force로 검증하는 것은 $\binom{2295}{9} \approx 10^{24}$로 불가. 하지만 **pencil과 그 perturbation**만 검증 가능:
   - $k=2$ pencil ($|S_W|=15$) 주변의 perturbation: pencil에 1~2개 random Lagrangian을 섞었을 때 correlation이 급격히 떨어지는지 확인.
   - 이건 `experiments/`로 코드+JSON 산출 가능.

2. **Perturbation 검증 (코드+JSON):**
   - Fix a $k=2$ pencil $S_W$ (size 15).
   - Add $t$ random Lagrangians (not in $S_W$) to form $S_W^{(t)}$.
   - Measure $\overline{\rho}(S_W^{(t)})$ for $t = 1, 2, \dots, 20$.
   - Hypothesis: correlation drops quadratically (as motivation says "mixtures dilute quadratically").

3. **Meta-question:** 이 conjecture가 논문 v2에 **conditional로 유지**되는 것이 현실적으로 최선인지, 아니면 **unconditional로 격상**할 단서가 있는지 판단.
   - 현재 단서: perturbation dilution은 강하지만, **닫힌형 proof는 없음**.
   - **권고: v2에는 conditional로 유지. Track B는 long-term로 두고, OP8 다리가 더 immediate 가치.**

---

## 7. Gate check

- **No closure claim:** "proof strategy"는 시도, 증명 아님.
- **No break:** conjecture 실패 ≠ scheme broken.
- **No security claim:** LSN hardness를 주장하지 않음.
- **수치 = 코드+JSON:** `experiments/80` 및 위 perturbation 제안.
- **n=3 단정 금지:** "n=3은 special" 명시. asymptotic 극한만 참조.

No closure; no break; no security claim. OPEN = LSN.
