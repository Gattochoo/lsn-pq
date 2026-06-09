# Lane C — Appendix-D entropy deficiency CONFIRMED computationally (the linear `LSN ⊀ LPN` mechanism)

> Lane A pinned the one open point: `sympLPN ⊀ LPN` is proven for *linear* reductions
> only, via an information-theoretic argument (entropy deficiency + Shannon converse).
> Lane C verifies the load-bearing half of that argument — **Thm D.1's entropy
> deficiency** — by exact computation. The sympLPN matrix `A ∈ F₂^{2n×n}` (isotropic:
> pairwise symplectically-orthogonal, full-rank columns) carries `log₂N(n) ≈ (3/2)n²`
> bits, **deficient by a constant factor `d → 1/4`** versus a uniform `2n×n` matrix's
> `2n²` bits. This is the verifiable mechanism behind the linear separation (a fixed
> linear `B` cannot smooth `A` to a uniform LPN matrix). Script:
> `lsn-experiments/17-appendixD-entropy-deficiency.py`.

`working code` (supports Lane A; evidence for, not proof of, the open any-reduction
question). Date: 2026-06-06.

---

## 한국어 요약

```text
Appendix-D Thm D.1: sympLPN의 A(isotropic 2n×n)는 엔트로피 ~(3/2)n²로, uniform 2n²보다
  상수배 결핍(d→1/4). n²/2개의 symplectic-orthogonality 조건이 원인.
검증(코드, 정확):
  - full-rank isotropic frame 개수 N(n)=∏_{k=1}^n (2^{2n-k+1}-2^{k-1});
    brute-force(n=1,2,3) = 공식 일치.
  - log2 N(n)이 (3/2)n²+n/2 추종(uniform 2n² 아님); d(n)=1-log2N/(2n²)=0.21→0.24(n=32)→1/4.
  - 교차검증: Lagrangian 수 L(n)=∏(2^i+1) × ordered-bases = N(n) (독립 확인).
의미: 고정 linear B로 A를 uniform(LPN 행렬)로 smooth 불가 → Thm D.2(error가 Shannon
  converse 초과)와 합쳐 linear `sympLPN⊀LPN`의 정보이론적 핵심. 단 *linear*만 — any-reduction은
  여전히 열림(Lane A). 7th 증명 아님, 증거.
```

---

## §1 What was verified

The sympLPN matrix `A` is an ordered full-rank **isotropic frame**: `n` columns in
`F₂^{2n}`, pairwise symplectically orthogonal (`Ω(a_i,a_j)=0`) and linearly independent.
Counting them:

```text
N(n) = ∏_{k=1}^n (2^{2n-k+1} − 2^{k-1})
       (column a_k: in the (2n−k+1)-dim ⊥ of the previous k−1 columns, minus their
        own span 2^{k-1} — which lies in that ⊥ because the frame is isotropic).
```

Two independent exact confirmations (`17-appendixD-entropy-deficiency.py`):

```text
[1] brute force (enumerate all 2n×n F₂ matrices, keep isotropic + full-rank) = formula:
      n=1: 3       n=2: 90       n=3: 22680      (all match N(n))

[2] entropy:   log2 N(n)   uniform 2n^2   ~(3/2)n^2+n/2   deficiency d=1-log2N/(2n^2)
      n=2          6.49           8             7.0            0.1885
      n=4         25.46          32            26.0            0.2043
      n=8         99.46         128           100.0            0.2230
      n=16       391.46         512           392.0            0.2354
      n=32      1551.46        2048          1552.0            0.2425   -> 1/4

[3] cross-check:  L(n)=∏_{i=1}^n (2^i+1) Lagrangian subspaces × (ordered bases per L)
                  = N(n) exactly for n=1..4.
```

## §2 Reading

- `log₂N(n)` tracks **`(3/2)n²`**, not the uniform `2n²` — the `n²/2`
  symplectic-orthogonality conditions remove a **constant fraction** of the entropy, and
  the empirical deficiency `d(n)` climbs monotonically to the predicted **`1/4`**. This is
  exactly Thm D.1's "`H(BA) ≤ (1−d)mn` for a constant `d`".
- **Why it blocks linear reductions (with Thm D.2).** To turn `A` into an LPN matrix a
  linear map must make it uniform (`2n²` bits) — but `A` only has `(3/2)n²`; the missing
  `Ω(n²)` bits must be injected by `B`, and Thm D.2 shows any such `B` drives the error
  weight past the Shannon noisy-coding converse, making the image information-theoretically
  undecodable. The entropy count verified here is the first, structural half of that
  impossibility.
- **Scope, repeated honestly (Lane A):** this confirms the *linear* barrier's mechanism.
  It says nothing about non-linear/adaptive reductions (open, win-win-guarded). It is
  **evidence for** the separation, **not a proof** of the any-reduction question, and not a
  proof that LSN is a 7th.

## §3 Verdict (Sound Verifier)

**CONFIRMED (mechanism), supports OPEN (candidate).** The Appendix-D entropy deficiency —
the structural core of the linear `sympLPN ⊀ LPN` separation — is exact and verified by
two independent counts, with the constant deficiency `d → 1/4`. This strengthens the
*evidence* base under LSN's one open point without overstepping it: the separation is
real and information-theoretic for linear reductions; the any-reduction question stays
external and open. No 7th proven; no security claim.

---

## References
- `lsn-experiments/17-appendixD-entropy-deficiency.py` (this verification).
- Lu, Poremba, Quek, Ramkumar, arXiv:2603.19110v1, §2.4 + Appendix D (Thm D.1/D.2).
- Lane A (`2026-06-06-lane-A-lsn-lpn-reduction-scope.md`) — the scope this supports.
- Symplectic combinatorics: #Lagrangians of `F₂^{2n}` = `∏_{i=1}^n (2^i+1)` (standard).
