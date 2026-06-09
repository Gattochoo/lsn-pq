# Claude Review Brief: Post-Audit Fixes & Open Questions

**Date:** 2026-06-08  
**Repo:** `Gattochoo/lsn-pq` (main branch)  
**Commit:** `8d578ca`  
**Context:** Deep audit completed; critical fixes applied. Requesting adjudicator review of fixes and remaining surface.

---

## 1. Executive Summary

A full line-by-line audit of `paper/lsn-paper.tex` (1,148 lines) was performed. **One fatal citation error, one internal note leak, one numerically impossible parameter, and one cryptographically broken FO-transform description** were found and fixed. All fixes are in commit `8d578ca`.

The paper is now believed to be mathematically sound and submission-ready pending adjudicator sign-off on the FO-transform rewrite and the remaining minor items listed in §4.

---

## 2. Critical Fixes Applied (with line refs)

### 2.1 Fatal citation `[Rei09]` — Ben Recht’s matrix-completion paper mis-cited as Regev’s quantum SQ result
- **Location:** §2 (Related Work), §6.3 (Quantum SQ), Bibliography.
- **Error:** The paper cited as "Regev [Rei09] showed that quantum learning algorithms respect statistical-query dimension…" was actually **Recht–Fazel–Parrilo, *Guaranteed minimum-rank solutions…*, SIAM Review 2010** — completely unrelated to quantum learning.
- **Fix:** Removed `[Rei09]` entry entirely. Replaced both in-text sentences with accurate, citation-free statements about Grover speed-ups and classical SQ lower bounds.
- **Lines affected:** ~194, ~417, ~1101.

### 2.2 Internal project note leaked into proof
- **Location:** Lemma 5.3 (SDA concentration), line 356.
- **Error:** `…contributes at most 1.12% of all pairs (OFA-390)…`
- **Fix:** Removed `(OFA-390)`.

### 2.3 KEM public-key size understated below info-theoretic minimum
- **Location:** Table 1 (line 240), Table `tab:kem-sizes` (line 607).
- **Error:** LSN-128 PK listed as **2.72 KB**. With $N=2048, r=11$, the $y$-vector alone is $22{,}528$ bits = **2.75 KB**; with a 256-bit seed the minimum is **2.78 KB**.
- **Fix:** Updated both tables to **2.78 KB**.

### 2.4 Fujisaki–Okamoto (FO) transform description was cryptographically broken
- **Location:** §7.2.5 (CCA Security), lines 615–623.
- **Error:** The CCA construction said $c=(c_0,r)$ and `Decaps` computed $r' \gets \mathsf{Decaps}(\mathsf{sk},c_0)$ then re-encapsulated with $G(r')$. But base decaps outputs $K_{\text{base}}=\mathsf{Hash}(s,u')$, not $r$. Re-encapsulating with $G(K_{\text{base}})$ produces a **different** ciphertext with overwhelming probability, so even honest ciphertexts would be rejected.
- **Fix:** Rewrote the CCA layer to be mathematically sound:
  - Base `Encaps` is now deterministic given the random pair $\rho=(s,u)$.
  - CCA-Encaps: chooses $s,u$ directly, runs base encaps with $(s,u)$, outputs $c=c_0$ and $K=H(s,u,c_0)$.
  - CCA-Decaps: parses $c=(s,\mathsf{syn})$, recovers $u'$ via polar decode (or $\perp$), re-encapsulates with $(s,u')$, checks $c_0'=c$, and outputs $H(s,u',c)$ or $H(d,c)$ on failure.
  - Removed the unused hash function $G$.
- **Impact:** Ciphertext size remains $\lambda+N$ (288 B), consistent with Table `tab:kem-sizes`. Theorem 7.1 (IND-CCA) statement and proof sketch remain valid because the general FO$^{\not\perp}$ theorem still applies.

### 2.5 Multi-user bound exponent inconsistency
- **Location:** §7.2.6, line 647.
- **Error:** Computed $q \gtrsim 2^{115.5}$ using $2n=130$, but Table 1 gives $\log_2(q_{\min})=128.6$ for $n=65$. The exact figure is $128.6-14.5 \approx 2^{114.1}$.
- **Fix:** Changed to $q \gtrsim 2^{114}$.

### 2.6 Misleading phrasing in base KEM decaps
- **Location:** §7.2.2, line 554.
- **Error:** `"always correct because the encapsulator and decapsulator use the same x's"` — readers could interpret this as $v'=v$.
- **Fix:** Clarified that $v'$ is deterministic (same $x$'s) but need not equal the noisy $v_j$, and that $v_j \oplus v'_j$ is the effective noise seen by the polar decoder.

### 2.7 Enumerate count mismatch
- **Location:** §9.1 (Honest Limitations), line 735.
- **Error:** `"We flag seven practical gaps…"` but only 5 items listed.
- **Fix:** Changed to `"five"`.

---

## 3. Additional Polish Applied

| # | Item | Location |
|---|------|----------|
| 3.1 | Acronym unified: Title/Abstract/§1.2 now all use **"Lagrangian Subspace Noise"** as primary, with *Learning Stabilizers with Noise* and *symplectic LPN* as aliases. | §1.2 |
| 3.2 | `[TV22]` ("Personal communication") removed from §1.1, §2, and Bibliography. Replaced with `"no published exponential quantum speed-up is known"`. | §1.1, §2, Bib |
| 3.3 | Table 1: 192/256-bit PK sizes changed to `"---"` with footnote explaining they depend on unstated $r$ and are standard extrapolations. | Table 1 |
| 3.4 | Theorem 3.1: added `"Numerical evaluation shows that"` before $\E[j] \to 0.76$. | §3.1 |
| 3.5 | Lemma 5.3: added `"A direct computation shows that"` before the 1.12% tail claim. | §5.3 |
| 3.6 | Terminology: `"re-encryption check"` → `"re-encapsulation check"` (2 occurrences). | §7.2.5 |
| 3.7 | SNARK public-key wording: `"additionally stores"` → `"is augmented with"`. | §6 |

---

## 4. Known Open Items (no action required for submission, but flag for reviewer)

1. **$N=2048$ empirical gap:** No direct Monte Carlo at $N=2048$; correctness rests on Bhattacharyya bound + $N \in \{128,256,512\}$ validation. Rust implementation pending (June 11).
2. **Full-protocol SNARK:** Only membership sub-circuit ($n^2$) is done. Polar encode + majority vote + permutation proof is future work.
3. **Rust reference implementation:** Pending Codex (June 11).
4. **Worst-case SDA bound:** Still open (Open Problem 6); existence-based bound only.
5. **Table 1 PK sizes for 192/256-bit:** Explicit $r$ not fixed; marked as extrapolation.

---

## 5. Files Modified

- `paper/lsn-paper.tex` — all fixes and polish.
- `meta/acknowledgment.md` — AI assistance acknowledgment (new file).

---

## 6. Request for Adjudicator Review

Please verify:

1. **FO-transform rewrite (§7.2.5):** Is the new CCA-Encaps / CCA-Decaps description sound? In particular, does re-encapsulating with $(s,u')$ correctly reproduce the original ciphertext $c_0=(s, v \oplus \mathsf{PolarEncode}(u))$ when $u'=u$?
2. **PK size arithmetic:** Is 2.78 KB the correct minimum for LSN-128 ($N=2048, r=11, \lambda=256$)?
3. **Citation integrity:** Confirm `[Rei09]` is fully purged and no other mis-citations remain.
4. **Cross-reference sanity:** Confirm Theorem 7.1 and its proof sketch are consistent with the rewritten CCA construction.
5. **Submission readiness:** Are there any remaining internal notes, numerical inconsistencies, or misleading phrasings that would trigger a reviewer red flag?

---

*Prepared by Kimi for Claude adjudicator review.*
