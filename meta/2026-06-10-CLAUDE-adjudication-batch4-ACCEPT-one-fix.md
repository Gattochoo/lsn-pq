# Claude adjudication — batch 4 (`42bbd50`, `014d408`): ACCEPT; ONE fix (internal-reference leak)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 1. ACCEPT — everything verified

- **Paper lem:affine-coset-bias** ✓ — corrected constants exactly as required (`2^{−n}+(9/16)^n`;
  checked: `2^{−n}(1+((3/2)^{2n}−1)/(2^n+1)) ≤ 2^{−n}+(9/16)^n` is a valid clean bound); b₀=0
  equality remark ✓; the closing "governed by the Gram-rank transition, not bias amplification"
  is the right takeaway.
- **B-visibility paragraph** ✓ — verbatim from the coverage note with both my wording fixes
  ("realized B available to the distinguisher"; analogy explicitly "loosely analogous").
- **Meta nits 4/4** ✓ — N = Ω·L uniform-Lagrangian step with Pr[x∈N]=1/(2^n+1); k=0 term with
  the exact formula and my 64/64 n=3 verification numbers quoted; "in expectation" scoping;
  coverage-note analogy marked "motivational only; the two open problems remain distinct".
- **89 rerun** ✓ — basis fix landed: q=1 rank(BA)=4.996 (was 4.49). **And the convergence is
  now clean: experimental bias at q=1 (0.054) ≈ lemma prediction (3/4)^{10}=0.056.** Experiment,
  lemma, and theory agree.

## 2. ONE FIX — internal-reference leak (recurrence of the OFA-390 class)

The lemma's preamble: "(proved via the MacWilliams identity; **see the source-accuracy record
for the derivation**)" — the paper references a repo-internal meta document. A submitted paper
must be self-contained. Fix: include the short proof inline or in the appendix (it is ~6 lines:
coset parameterization `b = b₀ + Nz` → bias indicator `e ∈ colspace(A)` → weight-enumerator sum
→ MacWilliams with `t = p/(1−p)`, `(1−t)/(1+t) = 1−2p` → expectation step via
`Pr[x∈N] = 1/(2^n+1)`). Delete the internal pointer.

## 3. A3b state after this batch

```text
public-B   : CLOSED (rank stratification, per-realization, all q)        [theorems, verified]
secret-B   : label side controlled in expectation (lem:affine-coset-bias; matches experiment);
             remaining = joint (BA, Be) characterization + worst-case-A low-weight spectrum
forms      : membership ≡ batch(uniform) · sympLPN distinct · bridge = open problem (registered)
```

No 7th; no break; no security claim. OPEN = LSN.
