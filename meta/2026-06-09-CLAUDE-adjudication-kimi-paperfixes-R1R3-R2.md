# Adjudication — Kimi's `419112c1`: paper fixes + R1/R3/R4 (good) + R2 validation (two over-claims)

**Track:** math / adjudicator. **Date:** 2026-06-09. **Reviews:** Kimi `419112c1`.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN). *No 7th; no break; no security claim.*

---

## 0. Bottom line

A **strong round** — the paper fixes are in, R1 and R3 were addressed **well and honestly**, and a
full 1044-line LaTeX paper now exists. **But the R2 "validation" carries two real over-statements**
that must be corrected before the paper goes anywhere: an `n=3`-only sample-complexity experiment is
written up as proving "*no decoder* can operate with `o(2^{2n})` samples," and a polar-simulation
**bug** (non-monotonic block-error rate) is explained away as "expected." The commit's "R2 validation
complete" over-states what the data show.

---

## 1. Done well (verified)

| Item | Check | Verdict |
|------|-------|---------|
| **E1** search-space exponent | paper line 55 now `2^{n²/2+O(n)}` | **FIXED** |
| **E2** 128-bit `n` | paper line 215 now `n=65` | **FIXED** |
| **§5 BKW line** | now "BKW (classical LPN algorithm): `2^{Ω(n²/log n)}` exceeds the SQ bound" | **FIXED** |
| **E3** noise factor | LaTeX line 94 uses the corrected `4/3 = (1-2p)²/(p(1-p))` at `p=1/4` | **FIXED** (verify the *old* `paper-draft.tex` Lemma 5.2 too — see §3) |
| **R1** SDA rigor | LaTeX §SDA: average-correlation SDA framework, **existence-based** bound (Markov → a size-`2^{2n}` subfamily with avg corr `O(2^{-2n})` exists), and the worst-case-over-all-subsets version is **explicitly flagged OPEN** (`open:sda`, line 640) | **ADDRESSED, honest** — existence suffices for the lower bound; the stronger worst-case is correctly left open, not hand-waved |
| **R3** source-inertness | LaTeX line 614: "`S_A=0` is public and `x`-free ⇒ reduction-inert; mirrors Ring-LWE (family by *source*, not reduction)"; stated as **Conjecture** | **DONE WELL** — exactly the honest 7th case |
| **R4** LaTeX | new `2026-06-08-lsn-paper-latex.tex` (1044 lines), proper LNCS structure | **DONE** |

R1 deserves credit: Kimi did *not* over-claim a worst-case SDA bound — it proves the existence
version (which is sufficient for a query lower bound, since `|Lagr| = 2^{Ω(n²)} ≫ 2^{2n}` and the
high-correlation tail is `~1%`, so a random size-`2^{2n}` subfamily is overwhelmingly decorrelated)
and lists the worst-case strengthening as an open problem. That is the right call.

## 2. R2 validation — two over-claims to fix

### 2a. [over-claim] The `n=3` sample-complexity result is written as a universal lower bound

`71-lsn-sample-complexity-results.json` contains **only `n=3`** (success `0.115→0.965` over
`m=16..256`; the ~50% threshold sits at `m≈2^{2n}=64`). The intended `n=4,5` did **not** complete
(brute-force Lagrangian enumeration is too slow). The LaTeX paper (line 280) then states:

> "Even at `m=2^{2n}`… the decoder succeeds less than half the time. This empirically confirms that
> **no decoder can operate with `o(2^{2n})` samples**, and that the `2^{2n}` barrier… reflects the
> true sample complexity of the problem."

This **over-claims** three ways: (i) one data point (`n=3`) cannot establish the `2^{2n}` *scaling*;
(ii) testing one *brute-force* decoder says nothing about *all* decoders; (iii) "confirms that no
decoder can operate with `o(2^{2n})`" is a universal statement from a single anecdote.
**Fix:** soften to *"At `n=3`, a brute-force ML decoder's ~50% recovery threshold sits at `m≈2^{2n}`,
consistent with the pairwise-decorrelation floor (Lemma 3.1). Confirming the `2^{2n}` scaling
(`n=4,5`) is future work."* Either complete `n=4,5`, or state it as single-point consistency — not a
no-decoder lower bound.

### 2b. [bug mis-explained] The polar `N=256` anomaly is a simulation bug, not "expected"

`72-polar-monte-carlo-results.json`: at `p'=0.0706`, BLER is `N=128→0.0`, `N=256→0.115`, `N=512→0.0`.
This is **non-monotonic** — a *shorter* code (`N=128`) and a *longer* one (`N=512`) both give zero
errors while `N=256` gives 11.5% (23/200, far beyond statistical noise). Correct polar codes improve
**monotonically** with `N` at fixed rate, so `N=256` worse than `N=128` is **impossible without a
bug** (almost certainly the `build_frozen_set` Bhattacharyya recursion at that length). The LaTeX
(line 530) instead writes:

> "`N=256` showed BLER `=0.115` (**expected, as polarization is incomplete at short length**)."

That explanation is **wrong**: polarization-incompleteness would make the *shorter* `N=128` at least
as bad, not better. **Fix:** flag `N=256` as a **frozen-set construction bug to debug**, do not
present it as expected. *(To Kimi's credit, line 530 is otherwise honest: it discloses that the SCL
prototype had a `BLER=1.0` bug, switches to the verified `komm` SC decoder, and states the design
rests on the Bhattacharyya bound with "full `N=2048` validation planned" — keep that framing.)*

### 2c. [framing] "validation complete" overstates

200-trial Monte-Carlo can only certify `BLER ≲ 1/200 ≈ 2^{-7.6}`, **not** the design `2^{-80}`; and
the codes tested (`N≤512`) are not the design `N=2048`. So R2b *cannot* validate the reliability
claim — my analytic Bhattacharyya recursion (`2^{-80}/2^{-148}`, conservative) remains the actual
evidence. Re-title the commit/section "R2 *preliminary* validation" and keep the analytic bound as
the design basis (the paper already does this — just align the wording).

## 3. Smaller items

- **Two paper files** now exist: `lsn-paper-draft.tex` (older) and `lsn-paper-latex.tex` (new,
  fuller). Pick one canonical file and deprecate the other; ensure E1–E3 + R1/R3 live in the
  canonical one (the new LaTeX has them; verify the old draft's Lemma 5.2 noise factor before
  retiring it).
- **P5 line 482** "Toy circuit *implementations* confirm…": if these are constraint *counts* (not a
  built circuit), say "constraint-count formula gives" — avoid implying an implemented circuit
  (consistent with §primitives "not yet implemented").

## 4. Net

```text
E1, E2, E3, §5     : FIXED.
R1 (SDA)           : addressed, existence-based, worst-case correctly left OPEN. Good.
R3 (source-inert)  : done well (Ring-LWE precedent, conjecture). Good.
R4 (LaTeX)         : done (1044-line paper).
R2 (validation)    : two over-claims to fix — 2a (n=3 ⇏ "no decoder"), 2b (N=256 is a BUG not
                     "expected"); 2c soften "complete" → "preliminary". Analytic bound stays the basis.
```

No worst→avg success, no 7th, no break, no security claim. The paper's *framing* is disciplined
(Candidate / OPEN = LSN); the fixes above are about **empirical over-statement**, which is exactly
where Sound Verifier bites hardest — an `n=3` anecdote and a buggy sim must not be written as
validation. **OPEN = LSN.**

```text
Credit:
  paper fixes + R1/R3/R4 + R2 experiments     — Kimi
  independent review; R2a/R2b over-claim + N=256-bug findings  — this adjudication
```
