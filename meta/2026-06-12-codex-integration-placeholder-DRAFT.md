# Codex Integration Placeholder DRAFT (for paper v2)

**Status:** DRAFT — placeholder text and table slots awaiting Codex N=2048 / cryptanalysis results.  
**Scope:** How to integrate Codex empirical results into §honest-limitations L1 and §implementation.

---

## Current State (from paper v1)

**§Honest Limitations L1:**
> "The concatenated code is designed via the Bhattacharyya bound, which guarantees $P_e\leq 2^{-80}$ for the target block length $N=2048$. We have validated the SC decoder empirically for $N\in\{128,256,512\}$ (all BLER $=0$ in 200 trials), but a direct Monte-Carlo run at $N=2048$ is computationally expensive and has not been completed. The correctness claim for $N=2048$ therefore rests on the Bhattacharyya bound and the smaller-scale validation, not on a direct measurement."

**§Implementation:**
> "A production constant-time Rust implementation (including constant-time popcount, bit-sliced symplectic transforms, and a constant-time SC decoder) is planned for full $N=2048$ validation and KAT vector generation."

---

## Placeholder Text (three scenarios)

### Scenario A: Codex validates N=2048 successfully

**§Honest Limitations — L1 update:**
> ~~The concatenated code is designed via the Bhattacharyya bound, which guarantees $P_e\leq 2^{-80}$ for the target block length $N=2048$. We have validated the SC decoder empirically for $N\in\{128,256,512\}$ (all BLER $=0$ in 200 trials), but a direct Monte-Carlo run at $N=2048$ is computationally expensive and has not been completed.~~
>
> **Direct $N=2048$ validation.**  We completed [NUMBER] independent encapsulation/decapsulation trials at the design parameters $(N=2048, K=256, r=7)$ using the production Rust implementation.  Observed BLER $=0$, consistent with the Bhattacharyya bound prediction $P_e \le 2^{-80}$.  The $N=2048$ limitation is thereby resolved.

**§Implementation addition:**
> The production Rust implementation (constant-time popcount, bit-sliced symplectic transforms, constant-time SC decoder) was validated at $N=2048$ with [NUMBER] KAT vectors.  Source code and reproducibility scripts are available at [REPO].

---

### Scenario B: Codex finds a gap (BLER > 0 or parameter issue)

**§Honest Limitations — L1 update:**
> The concatenated code is designed via the Bhattacharyya bound, which guarantees $P_e\leq 2^{-80}$ for the target block length $N=2048$.  Direct Monte-Carlo validation at $N=2048$ using the production Rust implementation revealed [DESCRIPTION: e.g., "observed BLER $=X$ in $Y$ trials" or "a frozen-set construction issue at $N=2048$ requiring adjusted rate $K'/N$"].  The corrected parameters $(N=2048, K=K', r=r')$ achieve [CLAIM] with [EVIDENCE].  The limitation is updated to reflect the empirically tuned parameters.

**Table update (Table 2):**
> Adjust $K$, $r$, PK size, CT size to match validated parameters.

---

### Scenario C: Codex results are partial / ongoing

**§Honest Limitations — L1 update:**
> The concatenated code is designed via the Bhattacharyya bound, which guarantees $P_e\leq 2^{-80}$ for the target block length $N=2048$.  We have validated the SC decoder empirically for $N\in\{128,256,512,2048\}$ ([STATUS: e.g., "BLER $=0$ in 200 trials at $N=2048$ with the production Rust implementation" or "validation ongoing, preliminary results consistent with bound"]).  Full KAT vector generation and independent cryptanalysis are [STATUS].

---

## Placeholder Table Slot

**Table to insert near §Implementation or §Honest Limitations:**

| Parameter | Design (Bhattacharyya) | Empirical (Codex) | Match? |
|-----------|------------------------|-------------------|--------|
| $N$ | 2048 | 2048 | — |
| $K$ | 256 | [TBD] | [TBD] |
| $r$ | 7 | 7 | — |
| $p'$ | 0.0706 | 0.0706 | — |
| Trials | — | [TBD] | — |
| BLER observed | $\le 2^{-80}$ (bound) | [TBD] | [TBD] |
| Decoder | SC/SCL | Rust SC/SCL | — |

---

## Cryptanalysis Integration Slot

If Codex delivers cryptanalysis results (e.g., best-known attack complexity, concrete bit-security estimate):

**§Security addition:**
> **Concrete security estimate.**  Independent cryptanalysis of the LSN-KEM parameters $(n=65, N=2048, r=11)$ was performed using [METHOD].  The best attack achieves complexity $2^{[TBD]}$ [classical / quantum], yielding a concrete security level of [TBD] bits.  Details are provided in [APPENDIX / REPO].

---

## Checklist

| Item | Status |
|------|--------|
| L1 placeholder (3 scenarios) | ✅ drafted |
| Table slot | ✅ drafted |
| Cryptanalysis integration slot | ✅ drafted |
| No premature claim | ✅ all claims are conditional on Codex results |
