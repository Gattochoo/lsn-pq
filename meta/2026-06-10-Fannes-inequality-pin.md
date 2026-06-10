# Fannes–Csiszár Continuity Inequality — Source-accuracy record

**Theorem:** For probability distributions $P, Q$ on a finite set $\mathcal{X}$ with total variation distance $T = \frac{1}{2}\|P-Q\|_1$,
\[
  |H(P) - H(Q)| \;\le\; T \cdot \log(|\mathcal{X}|-1) + h_2(T),
\]
where $H$ is Shannon entropy (natural log or base-2) and $h_2(T) = -T\log T - (1-T)\log(1-T)$ is the binary entropy function.

**Reference:** Csiszár, I. "Information-type measures of difference of probability distributions and indirect observations." *Studia Sci. Math. Hungar.* **2** (1967), 299–318.  
Also attributed to Fannes, M. "A continuity property of the entropy density for spin lattice systems." *Comm. Math. Phys.* **31** (1973), 291–294 (quantum case); the classical form above is standard in information-theory textbooks (e.g. Cover–Thomas, *Elements of Information Theory*, 2nd ed., Theorem 17.3.3).

**Tightness:** Equality is attained for $P = (1-T, T/(|\mathcal{X}|-1), \dots, T/(|\mathcal{X}|-1))$ and $Q = (1, 0, \dots, 0)$.

**Simplified form (asymptotic):** Since $h_2(T) \le 1$ and $\log(|\mathcal{X}|-1) \le \log|\mathcal{X}|$,
\[
  |H(P) - H(Q)| \;\le\; T \cdot \log|\mathcal{X}| + 1.
\]
For $\mathcal{X} = \{0,1\}^{mn}$, $\log|\mathcal{X}| = mn$ (base 2), giving
\[
  |H(P) - H(Q)| \;\le\; T \cdot mn + 1.
\]

No 7th; no break; no security claim. OPEN = LSN.
