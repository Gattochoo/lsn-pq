# P5c: F_q Barrier Generalization Sketch

**Date:** 2026-06-11 (overnight). **Status:** DRAFT — algebraic skeleton; no complete proof.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Setup

Replace $\mathbb{F}_2$ with $\mathbb{F}_q$ ($q = p^r$, $p$ odd or $p=2$).

- Symplectic vector space $V = \mathbb{F}_q^{2n}$ with form $\Omega(u,v) = u^T J v$.
- Isotropic subspace: $L \subseteq V$ with $\Omega|_L = 0$, $\dim L = n$.
- Lagrangian: maximal isotropic, $\dim = n$.
- Secret space: Lagrangian Grassmannian $\operatorname{Lagr}(2n, \mathbb{F}_q)$.
- Cardinality: $|\operatorname{Lagr}| = q^{n(n+1)/2} \prod_{i=1}^n (1 + q^{-i})$ (same $q^{n^2/2 + O(n)}$ scaling).

---

## 1. Transport theorems (full / near-full rank)

**F_2 version (paper):** For public-$B$ linear reduction, the rank of $BA$ stratifies into full-rank vs near-full-rank vs low-rank. The determinant of a certain Gram matrix detects the stratification.

**F_q adaptation:**
- The symplectic group $\operatorname{Sp}(2n, \mathbb{F}_q)$ acts transitively on Lagrangians.
- The isotropic-point count: number of isotropic 1-dimensional subspaces in $\mathbb{F}_q^{2n}$ is $(q^{2n} - 1) / (q - 1)$ for the total points, but the number of isotropic points depends on the form.
- For the standard symplectic form over $\mathbb{F}_q$: a 1D subspace $\langle v \rangle$ is isotropic iff $\Omega(v,v) = 0$. Since $\Omega$ is alternating, $\Omega(v,v) = 0$ for ALL $v$. So every 1D subspace is isotropic.
- The number of isotropic points is therefore $(q^{2n} - 1) / (q - 1)$.
- The number of Lagrangians containing a fixed isotropic line: by transitivity, this is $|\operatorname{Lagr}| / $ (number of isotropic lines) $= \dots$

Actually, for general $q$, the counting is more subtle because the symplectic form over $\mathbb{F}_q$ behaves differently. But for alternating forms, all vectors are isotropic regardless of $q$.

**Key invariant:** The determinant / Pfaffian argument for rank stratification relies on the symplectic form being non-degenerate and the isotropy condition $A^T \Omega A = 0$. Over $\mathbb{F}_q$, the same algebraic identity holds: $S_A = A^T \Omega A = 0$ implies the columns are isotropic.

The transport theorems (Lemmas 6.1, 6.2 in the paper) should transfer verbatim because they only use:
1. $S_A = 0$ (isotropy)
2. Rank of matrices over a field
3. The symplectic group action

All of these are valid over any field.

---

## 2. Reachability theorem (any-B uniformity)

**F_2 version:** The counting bound uses $R_w = \{b \in \mathbb{F}_2^{2n} : |b| \le w\}$ with $|R_w| = \sum_{j=0}^w \binom{2n}{j}$.

**F_q adaptation:**
- Weight is replaced by Hamming support: $b \in \mathbb{F}_q^{2n}$ has support $\operatorname{supp}(b) = \{i : b_i \neq 0\}$.
- $R_w = \{b : |\operatorname{supp}(b)| \le w\}$.
- $|R_w| = \sum_{j=0}^w \binom{2n}{j} (q-1)^j$.
- For $w = \alpha \cdot 2n$ with $\alpha < 1/2$, this is still $2^{2n \cdot H_2(\alpha) + o(n)} \cdot (q-1)^{\alpha \cdot 2n}$... wait, the $(q-1)^j$ factor changes the growth rate.

Actually, for fixed $q$ and $n \to \infty$:
$|R_w| = \sum_{j=0}^w \binom{2n}{j} (q-1)^j \le \sum_{j=0}^w \binom{2n}{j} (q-1)^w = (q-1)^w \sum_{j=0}^w \binom{2n}{j}$.

For $w = 0.19n$:
$|R_w| \le (q-1)^{0.19n} \cdot 2^{2n \cdot H_2(0.19)} = (q-1)^{0.19n} \cdot 2^{1.38n}$.

The reachability condition requires $|R_w| \ll q^n$ (since the secret space is over $\mathbb{F}_q$ now, dimension is $n$ over $\mathbb{F}_q$, so $q^n$ vectors).

For $q=2$: $|R_w| \le 2^{1.38n} \ll 2^n$? Wait, $2^{1.38n} > 2^n$. The actual bound in the paper uses a more refined counting.

For the F_2 reachability theorem, the key step is:
$|R_w| = 2^{n \cdot c}$ for some constant $c < 2$ (actually $c \approx 1.38$ for $w=0.19n$), and the number of possible rows is $2^{2n}$. The fraction of low-weight rows is $2^{(c-2)n} = 2^{-0.62n}$. With $m = \operatorname{poly}(n)$, the probability that any row has weight $\le w$ is negligible.

For F_q:
- Total number of rows: $q^{2n}$.
- $|R_w| \approx (q-1)^w \cdot 2^{2n H_2(w/2n)}$... wait, the binomial coefficient $\binom{2n}{j}$ counts subsets, not vectors.

Actually, $\binom{2n}{j} (q-1)^j$ is the number of vectors in $\mathbb{F}_q^{2n}$ with exactly $j$ non-zero coordinates. This is correct.

For $w = \alpha \cdot 2n$, using entropy approximation:
$|R_w| \approx \exp_{q}\left(2n \cdot \frac{H_2(\alpha) + \alpha \log_2(q-1)}{\log_2 q}\right)$.

The reachability argument requires $|R_w| \ll q^n$, i.e.,
$2n \cdot \frac{H_2(\alpha) + \alpha \log_2(q-1)}{\log_2 q} < n$,
$2 \cdot \frac{H_2(\alpha) + \alpha \log_2(q-1)}{\log_2 q} < 1$.

For $q=2$: $2 \cdot H_2(\alpha) < 1$, i.e., $H_2(\alpha) < 0.5$, which gives $\alpha < 0.11$. But in the paper, $\alpha = 0.19$ works because the counting is more refined (it uses the exact structure of $R_w(A)$, not just $R_w$).

For larger $q$, the denominator $\log_2 q$ increases, making the bound easier to satisfy. So F_q should actually make the reachability theorem STRONGER, not weaker.

---

## 3. Conjecture

> **Conjecture.** The transport theorems (public-$B$ rank stratification) and the reachability theorem (conditional-uniformity any-$B$ counting bound) hold over any finite field $\mathbb{F}_q$ with the same qualitative conclusions. The constants in the reachability bound improve as $q$ increases.

**Evidence:** Algebraic structure (isotropy, symplectic group, rank) is field-independent. Counting bounds improve with larger $q$.

**Missing:** Detailed verification of each lemma's field dependence; explicit F_q constants for the reachability threshold.

---

*By Kimi, 2026-06-11 ~04:15 KST. DRAFT — await Claude adjudication.*
