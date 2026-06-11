# v1 → v2 Changelog DRAFT (ePrint revision note) (rev2)

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (rev2 after adjudication 8b3ac65 — app:superseded/Lemma-D removed, I(x;y|C) tightened).  
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## Summary

Version 2 strengthens the security evidence and sharpens the open-problem landscape in four areas: (1)~Krawtchouk lemma upgraded from expectation to w.h.p.; (2)~empirical validation at the design length $N=2048$; (3)~new cryptanalysis evidence (ISD, BKW, span-of-positives, Rust ML cross-check); (4)~OP9 honest sharpened to the conditional mutual information $I(x;y|C)$, with an explicit note that prior Fisher-information and total-variation approaches targeted $I(x;y)$ and therefore could not upper-bound the working quantity. No security claim is upgraded; all additions are evidence-based or structural.

---

## Detailed Changes

### 1. Krawtchouk lemma: expectation → w.h.p. (§Barriers, Appendix)

- **v1:** `lem:affine-coset-bias` gave an *expectation* bound
  $$\mathbb{E}_A\bigl|\mathbb{E}_{b,e}[(-1)^{b^\top e}]\bigr| \le 2^{-n} + (9/16)^n.$$
- **v2:** Promoted to **high-probability** (`lem:affine-coset-bias-whp`):
  $$\bigl|\mathbb{E}_{b,e}[(-1)^{b^\top e}]\bigr| \le \bigl(2^{-n} + (9/16)^n\bigr)(1+o(1)) \quad \text{w.p. } 1-2^{-\Omega(n)}.$$
- **New Appendix `app:krawtchouk`:** Full closed-form proof of the variance bound in four paragraphs: (i)~exact first two moments of $W_N(1/2)$; (ii)~block factorisation of the character sum with $\sigma = 49/16 = (7/4)^2$ per symplectic coordinate block; (iii)~explicit cancellation of $(81/64)^n$ terms via $q/2-p^2$; (iv)~Chebyshev concentration with $\varepsilon_n = (50/81)^{n/4}$ giving $2^{-\Omega(n)}$ tail.
- **Impact:** The secret-$B$ regime is now controlled w.h.p., not just in expectation. This removes a conditional expectation step in the linear-reduction barrier chain.

### 2. L1 $N=2048$ empirical validation (§KEM-Correctness)

- **v1:** Implementation note cited $N \in \{128,256,512\}$ validation (200 trials each, BLER $=0$). $N=2048$ was deferred to "production Rust implementation."
- **v2:** Added Codex P1b Rust validation results:
  - $N=2048$, $K=256$, SCL decoder ($L=8$, min-sum path metric).
  - $2000$ independent trials at both design noise points ($p'=0.0706$ for $r=7$, $p'=0.0343$ for $r=11$).
  - Zero block errors observed; one-sided 95\% BLER upper bound $\approx 1.5 \times 10^{-3}$.
  - High-noise negative controls ($p' \in \{0.3,0.4,0.5\}$): BLER $0.965$–$1.000$, confirming harness integrity.
- **Honest limitation retained:** The design claims $P_e \le 2^{-80}$ ($r=7$) and $P_e \le 2^{-128}$ ($r=11$) still rest on the conservative Arıkan–Bhattacharyya bound; direct Monte-Carlo validation of $2^{-80}$ is infeasible.

### 3. Cryptanalysis evidence (§Decoders)

- **v2 new:** Codex P2 systematic cryptanalysis screen, all consistent with $2^{2n}$ brute-force scale:
  - **ISD positive-basis search:** $n=5$, $50\,000$ attempts → $3/10$ success. Attempt budget $\gg 2^{2n}=1024$, no speedup over brute-force regime.
  - **BKW bucket-pair screen:** One-round bucket pairing shows no scalable signal at $n=6$–$8$; noise-growth model $p \mapsto 2p(1-p)$ kills multi-round structure exploitation.
  - **Span-of-positives:** Perfect recovery at $p=0$ (sanity check), zero recovery at $p=1/4$ ($n=3,4,5$); false positives span ambient space.
  - **Rust ML cross-check:** $n=5$ compact count-aggregated scorer confirms Python brute-force trend ($0.25$ at $m=512$, $0.90$ at $m=1024$, $1.00$ at $m=2048$).
- **Impact:** Strengthens the empirical claim that no known attack family beats the $2^{2n}$ sample/query scale. No attack success = no CLOSURE-GRADE claim.

### 4. OP9 sharpened (§Open Problems)

- **v1:** Open Problem 9 (marginal-adaptive linear reductions) posed the correlated-noise obstacle without pinning the exact information-theoretic quantity.
- **v2:** Sharpened to:
  - Correct quantity identified: **conditional mutual information** $I(x;y|C)$. Because $x \perp C$, we have $I(x;y) \le I(x;y|C)$; therefore earlier approaches that bounded $I(x;y)$ (Fisher information, total variation) did not upper-bound the working quantity.
  - Honest phrasing: "Strong empirical evidence shows single-sample recovery vanishes; rigorous proof that $I(x;y|C)=o(n)$ remains open."
- **Impact:** Prevents future readers from retracing the same dead end; pins the exact open question.

### 5. Minor fixes

- Fixed multi-label `\Cref{label1,label2}` syntax to individual `\Cref` calls (cleveref compatibility).
- KO sync: `lsn-paper-ko.tex` line 542 carries the w.h.p. promotion inline; no separate appendix needed.

---

## ePrint Revision Note (suggested text)

> **Revision v2 (2026-06-12):** Strengthened security evidence in four areas: (i) the affine-coset bias bound is upgraded from expectation to w.h.p. with a full closed-form proof in a new appendix; (ii) the $N=2048$ polar decoder is empirically validated (2000 trials, zero errors); (iii) systematic cryptanalysis screens (ISD, BKW, structural) confirm no attack beats the $2^{2n}$ scale; (iv) Open Problem 9 is sharpened to the conditional mutual information $I(x;y|C)$, with an explicit note that earlier Fisher/TV approaches bounded $I(x;y)$ and therefore could not upper-bound the working quantity. No security claim is changed; all additions are evidence-based.

---

## Gate check

- **No closure claim:** "Strengthened evidence" ≠ proof.
- **No break:** No scheme weakness disclosed.
- **No security claim upgrade:** $2^{-80}$ claim still rests on Bhattacharyya bound.
- **All numbers code-backed:** Codex P1b/P2 experiments referenced.

No closure; no break; no security claim. OPEN = LSN.
