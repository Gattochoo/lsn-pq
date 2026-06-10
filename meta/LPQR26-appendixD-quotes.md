# LPQR26 Appendix D — Source-accuracy record

**Paper:** Lu, Poremba, Quek, Ramkumar. *Post-quantum cryptography from quantum stabilizer decoding.* arXiv:2603.19110.
**Version fetched:** v1 (Thu, 19 Mar 2026 16:35:31 UTC).
**Record created:** 2026-06-10.
**Fetched by:** Kimi (PDF via arXiv direct link).

---

## Theorem D.1 (entropy deficiency of fixed linear reductions)

> **Theorem D.1.** Let $m \geq cn$ for $c > 1$. Then there exists a constant $d > 0$, such that for sufficiently large $n$ and any fixed choice of $B \in \mathbb{Z}_2^{m \times 2n}$, $H(BA) \leq (1-d)mn$.

**Location:** Appendix D, page 42 of the PDF (page number in the rendered document).

---

## §2.4 error-weight bound (Shannon-converse regime)

> "...the error $Be$ has error weight larger than $(1-r-\delta)\frac{m}{2}$ for any $\delta > 0$ with overwhelming probability, where $r$ is the rate $r = \frac{n}{m}$."

Clarification: the PDF rendering splits the fraction across two lines as $(1-r-\delta)$ followed by a denominator $2$ and numerator $m$ on the next line. The intended bound is error weight $> \frac{(1-r-\delta)m}{2}$.

**Location:** §2.4 (Technical overview), page 11 of the PDF.

---

## $m = \omega(n)$ caveat (bound insufficient to rule out decodability)

> "When $m = \omega(n)$, the result shows that the output error has weight larger than $\frac{1}{2} - \delta$ for any constant $\delta$, since $r = o(1)$. This bound is not sufficient to fully rule out decodability."

**Location:** Appendix D, page 42 of the PDF.

---

## $m = \Theta(n)$ — primary / tight case

> "...the primary case of interest for the result was to rule out a reduction where $m = (1+\epsilon)n$, i.e. when the number of rows decreased rather than increasing."

(Preceding sentence: "We believe that it should be possible to do so for any $m = \operatorname{poly}(n)$—however, the primary case of interest...")

**Location:** Appendix D, page 42 of the PDF.

---

## Verification notes

- The HTML abstract page (arXiv abstract) does **not** contain the appendices; direct PDF download was required to verify these quotes.
- The "low-noise regime" phrasing used in earlier drafts of our paper ($m = \Theta(n)$ vs. $m = \omega(n)$ distinction) was a misattribution: LPQR26's linear-reduction impossibility is **not** restricted to low noise. The true scope axis is the sample regime $m$. At constant noise $p=1/4$ the piling-up lemma makes the error-amplification step even stronger (per-bit bias $(1-2p)^w = 2^{-w}$).
- The $C(n,2)$ isotropy-entropy cost phrase used in earlier drafts is **ours** (derived from the $S_A=0$ public quadratic constraint), not LPQR26's. Their argument uses the $(1-d)mn$ entropy-deficiency factor.

---

## Theorem D.2 (error-weight lower bound for randomized linear reductions)

> **Theorem D.2.** Let $m = \operatorname{poly}(n)$ with $m > cn$ for some $c > 1$, and let $p = \omega(1/n)$. Suppose that $B \in \mathbb{Z}_2^{m \times 2n}$ is a random variable such that $BA \in \mathbb{Z}_2^{m \times n}$ is statistically indistinguishable from uniformly random. Fix any $\delta > 0$ and let $r := n/m$ be the rate of the transformed code $\operatorname{im}(BA)$. Then $|Be|$, the weight of the distorted error, satisfies
> $$
> \Pr_{B, e \sim D_p^{\otimes n}}\!\left[ |Be| \ge \frac{(1-r-\delta)\,m}{2} \right] \ge 1 - \operatorname{negl}(n).
> $$

Clarification: Equation (63) in the PDF renders the fraction $(1-r-\delta)$ on one line and $m/2$ on the next; the intended bound is $|Be| \ge \frac{(1-r-\delta)m}{2}$.

**Location:** Appendix D, page 42 of the PDF (page number in the rendered document).
