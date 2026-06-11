# v2 Paper Audit Report — Full Survey of Errors, Exaggerations, and Falsehoods

**Date:** 2026-06-12. **Actor:** Kimi. **Scope:** `paper/lsn-paper.tex` (EN) + `paper/lsn-paper-ko.tex` (KO).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## Executive Summary

| Severity | Count | Category |
|---|---|---|
| **Critical** | 3 | Quantitative overstatement in main text |
| **Critical** | 6 | KO-EN synchronization failures |
| **Minor** | 9 | KO missing content / tables |
| **Note** | 3 | Unverified theoretical estimates (not errors, but flagged) |

**Good news:** No "app:superseded" or "Lemma D.1–D.6" references survive in the paper body (meta-only issues, already fixed in rev2). OP8 text is correctly pinned. I(x;y|C) text is correct in EN. The vast majority of numerical claims (~45) are exactly correct and code-backed.

---

## 1. Critical Errors in EN Body

### 1.1 Fannes bound overstated (line 919)

**Claim:** "At $n=41$, $m=82$ this distance is at least $0.2497$."

**Exact calculation:** LPQR26 Theorem D.1 gives $H(BA) \le (1-d)mn$ with $d = 1 - H(A)/(mn)$ for the finite parameters. Using the exact frame entropy $H(A) = (3/2)n^2 + n/2 + O(1)$ and $m=82$, $n=41$:
\[
d = 1 - \frac{(3/2)(41)^2 + 41/2 + O(1)}{41 \cdot 82} = 1 - \frac{2560.5}{3362} \approx 0.2382.
\]
The Fannes–Csiszár continuity bound gives $\operatorname{SD} \ge d - 1/(mn) \approx 0.2382 - 0.0003 = 0.2379$. Even using the asymptotic $d \to 1/4$ (which is an upper bound on $d$ at finite $n$), we get $0.25 - 0.0062 = 0.2438$.

**Verdict:** **FAIL.** The paper uses the asymptotic $d=1/4$ directly without subtracting $1/(mn)$, obtaining $0.2497$. The exact finite-$n$ value is $0.2438$ (off by $2.4\%$). The qualitative claim (constant non-negligible distance) remains valid, but the specific number is an optimistic rounding.

**Fix:** Replace with the exact finite-$n$ calculation or state "$\ge 0.24$".

---

### 1.2 $q_{\min}$ table systematically inflated (lines 345–348)

**Claim:**
| Security | $n$ | $\log_2(q_{\min})$ |
|---|---|---|
| 80-bit | 41 | 80.6 |
| 128-bit | 65 | 128.6 |
| 192-bit | 97 | 192.6 |
| 256-bit | 129 | 256.6 |

**Theorem 5.3 (thm:main-sq-cond) proof:** Applying Feldman (\Cref{thm:feldman}) with $\alpha=2/3$, $\gamma=5\rho_{\mathrm{avg}}$, SDA $\ge 2^{2n}$:
\[
q \ge (2\alpha - 1) \cdot \mathrm{SDA} = (4/3 - 1) \cdot 2^{2n} = \frac{1}{3} \cdot 2^{2n} = 2^{2n - \log_2 3}.
\]
Thus $\log_2(q) = 2n - \log_2 3 = 2n - 1.58496\dots$.

**Exact values:**
| $n$ | $2n$ | $\log_2(q)$ exact | Table | Error |
|---|---|---|---|---|
| 41 | 82 | **80.415** | 80.6 | +0.185 |
| 65 | 130 | **128.415** | 128.6 | +0.185 |
| 97 | 194 | **192.415** | 192.6 | +0.185 |
| 129 | 258 | **256.415** | 256.6 | +0.185 |

The table consistently adds $\approx 0.185$ to the exact Feldman bound. This corresponds to using $\log_2(3) \approx 1.4$ instead of $1.585$, or equivalently treating $(2\alpha-1)=1/3$ as $2^{-0.6} \approx 0.66$ rather than $0.333$.

**Verdict:** **FAIL.** The caption states "$q_{\min}$ figures use the exact pairwise-correlation formula ... so the 80-bit line is met exactly at $n=41$ with no asymptotic slack." The claim "exactly" and "no asymptotic slack" is **false**: the table values are approximations with a systematic $+0.185$ slack. The constant factor in the exponent is misstated.

**Fix:** Either (a) correct the table to 80.4, 128.4, 192.4, 256.4, or (b) explicitly state that the values are rounded-up design targets, not exact theorem outputs.

---

### 1.3 "Constant factor in the exponent is $\approx 0.67$" — origin unknown (line 355)

**Claim:** "The constant factor in the exponent is $\approx 0.67$ (below $1$), so parameters with $2n < \lambda$ are not advised without a rigorous upper bound."

**Analysis:** No calculation in the paper or repo yields $0.67$.
- If referring to the Feldman constant $(2\alpha-1)=1/3$, then $\log_2(1/3) = -1.585$, so the constant factor in the exponent is $1.585$, not $0.67$.
- If referring to $\rho_{\mathrm{avg}} = (3/4)2^{-n}$, then $\log_2(3/4) = -0.415$, not $0.67$.
- If referring to $1/\log_2(3) \approx 0.631$, this is close to $0.67$ but has no standard interpretation as a "constant factor in the exponent."

**Verdict:** **FAIL.** This number appears to be either a miscalculated or misattributed constant. It is not derivable from any theorem or formula in the paper.

**Fix:** Delete or replace with the correct constant ($\log_2 3 \approx 1.585$ for the Feldman bound, or $-\log_2(3/4) \approx 0.415$ for the correlation coefficient).

---

## 2. Critical KO–EN Synchronization Failures

### 2.1 OP4 replaced by wrong content (KO line 593 vs EN line 1171)

- **EN:** "Quantum lower bound. Prove \Cref{conj:quantum}: any quantum algorithm solving LSN requires $\Omega(2^n)$ queries."
- **KO:** "\textbf{worst-case 하드니스.} LSN의 worst-case 토대."

The numbered open-problem list in KO is corrupted at item 4. The Quantum lower bound must be restored.

---

### 2.2 OP9 missing the $I(x;y|C)$ insight (KO lines 598–599 vs EN lines 1181–1183)

- **EN:** Full discussion of conditional mutual information $I(x;y|C)$, the inequality $I(x;y) \le I(x;y|C)$, and why Fisher/TV approaches targeted the wrong quantity.
- **KO:** Entirely absent. KO's OP9 is only the mechanical noise-structure question.

This is the sharpened content of v2 OP9; its absence in KO nullifies the v2 upgrade for Korean readers.

---

### 2.3 Quantum LSN Conjecture missing in KO (EN §7 vs KO §7)

- **EN:** Numbered \begin{conjecture}[Quantum LSN] environment.
- **KO:** No numbered conjecture; only a brief paragraph.

---

### 2.4 Honest Limitations content mismatch (EN lines 1186–1201 vs KO lines 601–604)

EN has 5 items: (1) Empirical gap at $N=2048$, (2) No constant-time implementation, (3) Full-protocol SNARK is future work, (4) Loose multi-user reduction, (5) Practical optimizations deferred.

KO has different items: (1) Standard-model gap, (2) SQ is evidence not proof, (3) Polar verification, (4) Loose multi-user, (5) Practical optimizations.

Items 1–2 of EN are missing in KO; items 1–2 of KO are valuable but should not replace EN items.

---

### 2.5 Lemma M2 missing $m$ lower-bound condition (KO lines 566–568 vs EN lines 1143–1149)

- **EN:** "provided $m\ge \frac{4n}{(1-2p')^{2}}\cdot\operatorname{polylog}(n)$"
- **KO:** Omits this proviso entirely.

---

### 2.6 Theorem marginal-adaptive missing $p'$ condition (KO line 572 vs EN line 1154)

- **EN:** "for every $p'$ with $1-2p'\ge 1/\operatorname{poly}(n)$"
- **KO:** "어떤 사용가능한 LPN 분포로도 사상이 불가능하다" — no explicit condition.

---

## 3. Minor KO–EN Discrepancies

| # | Item | EN | KO | Fix |
|---|---|---|---|---|
| 7 | R1CS comparison table (tab:r1cs) | Present (lines 621–637) | Absent | Insert table |
| 8 | Implementation Security comparison table | Present (lines 803–817) | Absent | Insert table |
| 9 | Empirical sample-complexity table | Present (lines 388–397) | Absent | Insert table |
| 10 | KEM Security Remark paragraph | Present (lines 698–699) | Absent | Insert paragraph |
| 11 | sympLPN $k=n$ special-case note | Present (lines 229–231) | Absent | Add sentence |
| 12 | Threshold Cryptography paragraph | Present (lines 1203–1205) | Absent | Add paragraph |
| 13 | Quantum ECC interoperability paragraph | Present (lines 1205) | Absent | Add paragraph |
| 14 | Detailed FO-transform Decaps | Present (lines 766–772) | Condensed | Expand to match |
| 15 | Quantum Analysis subsections | 5 subsections (7.1–7.5) | No subsections | Add subsections |
| 16 | Related Work citations | 12 citations | 6 citations | Add missing cites |

---

## 4. Previously Flagged Issues — Status in Paper Body

| Issue | Source | Status in body |
|---|---|---|
| `app:superseded` referenced | Changelog rev2 | **Absent** — was removed in 4d2bf97. No error in body. |
| "Lemma D.1–D.6" fabricated | Changelog rev2 | **Absent** — `app:krawtchouk` is unnumbered. No error in body. |
| OP8 "public isotropic matrix [A\|B]" | KLP+25 pins | **Fixed** — now reads "public stabilizer matrix $[A \mid B]$ with a Lagrangian $A$-block ... concatenated matrix is not itself isotropic." |
| I(x;y) vs I(x;y\|C) | OP9 status check | **Correct** — line 1181 has the exact inequality and Fisher/TV note. |

---

## 5. Unverified Theoretical Estimates (Not Errors, But Flagged)

| Claim | Location | Status |
|---|---|---|
| SNARK full-circuit 4,500–4,700 constraints | line 648 | Theoretical estimate; no experiment verifies Poseidon + Siegel-chart count. |
| SHA-256 $\approx$25,000 / AES-128 $\approx$16,000 / ZK-Kyber millions | line 650 | Standard literature values; no experiments in repo. |
| BLER = 0.115 at $N=256$ (historical bug) | line 707 | No saved intermediate experiment with the buggy value. |

These are not errors, but they are not backed by repo experiments. The paper correctly labels the SNARK count as a prediction and the BLER 0.115 as a resolved historical anomaly.

---

## 6. What Is *Not* an Error

The following items were examined and found to be **correct**:

- **Exact pairwise correlation formula** (\Cref{lem:exact-corr}): algebra verified.
- **"No asymptotic error term"**: true — the formula is closed-form.
- **Decoder recovery rates** (n=3,4,5): exact match to experiments 71 & 73.
- **Rust cross-check** (0.25/0.90/1.00): exact match to experiment 129.
- **KEM polar bounds** ($p'=0.0706$, $2^{-81}$, etc.): match experiments 41 & 148.
- **KEM trials** (2000 trials, 0 errors, 95% bound $1.5\times10^{-3}$): match experiment 127.
- **Cryptanalysis** (ISD, BKW, span-of-positives): match experiments 132, 133, 130.
- **PK/CT sizes** (1.78 KB, 288 B): correctly inferred from parameters.
- **Dilution constant** ($3 \cdot 2^{-n}$ asymptotically, $3/10$ at $n=3$): exact Bayes calculation.
- **Distance distribution** ($\E[j] \to 0.76$, $\operatorname{Var}(j) \to 0.60$): exact computation.
- **Correlation coefficient** ($4/3$ at $p=1/4$): exact algebra.
- **Enrichment bound** ($\delta \le 2^{-50}$ at $n=65$): experiment 92b gives $\approx 2^{-57}$.
- **LPQR26 Theorem D.1 citation**: structure matches the pinned source.
- **KLP+25 Thm 6.6 citation**: correctly pinned to single-sample Search LSN.
- **"Three of four cells closed unconditionally"**: true — public-B, fixed-B (LPQR26), conditional-uniform adaptive are unconditional; marginal-adaptive is OPEN.
- **"Information-theoretically secure with poly(n) samples"**: true — Prop.~\ref{prop:per-sample-mi} and \ref{prop:chi2-sample} support this.
- **"80-bit security" naming**: the paper explicitly states in Table~\ref{tab:parameters} caption that $q_{\min}$ uses the **conditional** bound. This is a naming convention, not a false claim.
- **SNARK "1,000× smaller than ZK-Kyber"**: reasonable given published ZK-Kyber circuits (millions of constraints) vs LSN membership (~4,225).

---

## 7. Recommended Fix Priority

### P0 (before ePrint revision note)
1. Correct $q_{\min}$ table values or add explicit rounding disclaimer.
2. Fix Fannes bound 0.2497 → 0.2438 (or "$\ge 0.24$").
3. Delete or correct "constant factor $\approx 0.67$".

### P1 (KO sync — before Korean ePrint)
4. Restore Quantum lower bound as OP4 in KO.
5. Add $I(x;y|C)$ discussion to KO OP9.
6. Add Quantum LSN Conjecture to KO §7.
7. Synchronize Honest Limitations list.
8. Add missing $m$ condition and $p'$ condition to KO lemmas/theorems.

### P2 (tables and minor content)
9. Insert missing tables (R1CS, Implementation Security, empirical sample-complexity) into KO.
10. Add missing paragraphs (KEM Security Remark, Threshold Crypto, Quantum ECC).

---

## Gate Check

- **No closure claim broken:** Audit findings are quantitative slippages and sync gaps, not scheme-breaking errors.
- **No security claim falsely upgraded:** The "80-bit" naming is explicitly conditional.
- **All numbers either verified or flagged:** Every numerical claim has been checked against code+JSON or explicitly marked as unverified.

No closure; no break; no security claim. OPEN = LSN.
