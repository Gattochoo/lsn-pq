# Lane G — "try everything": (#1) SQ positive-evidence for sympLPN + (#2) the fresh-noise worst→avg obstruction

> Per the "we try everything, not choose" mandate, both deferred directions were run.
> **#1 (SQ / statistical dimension):** the sympLPN a-distribution is **balanced** (no Fourier
> coefficient `μ̂(Δ)` stands out above the uniform-LPN / sampling floor), so its secret-pairwise
> correlation `(1−2p)²μ̂(Δ)` stays exponentially small like LPN — **sympLPN inherits LPN's SQ
> lower bound** at the per-sample marginal level. This is the program's first *positive* hardness
> ingredient (a broad attack class — statistical-query — provably needs ~exp queries),
> complementary to the decoder no-go results. **#2 (fresh-noise worst→avg encoding):** the
> *natural* i.i.d. fresh-noise encoding is **obstructed** — discrete smoothing is all-or-nothing
> (`leak(q,w)→0` only as `q→1/2`, unusable; at usable `q≤0.25` the worst-case instance leaks),
> the discrete shadow of the C7 self-dual-noise rigidity. Both with honest scope; no 7th; no
> security claim. Scripts: `lsn-experiments/25-sq-statistical-dimension.py`, `26-freshnoise-
> encoding-obstruction.py`. Date: 2026-06-07.

---

## 한국어 요약

```text
"선택 말고 모두" → #1·#2 둘 다 실행.
#1 SQ: 노이즈-선형 학습의 SQ-hardness = secret 쌍 상관 (1-2p)²·μ̂(Δ), μ̂=a-분포 Fourier bias.
  sympLPN(열이 symplectic-orthogonal인 A의 행들) max|μ̂(Δ)| = 0.007–0.020 ≈ uniform LPN·sampling
  floor → 두드러지는 Δ 없음 → marginal이 balanced → LPN처럼 SQ-hard(SQ 알고리즘 ~지수 쿼리 필요).
  ★프로그램 최초의 *긍정* hardness 증거(broad SQ class), 디코더 no-go와 상보적. 범위: marginal.
#2 fresh-noise worst→avg: leak(q,w)=TV(Bern(q)^w,Bern(1-q)^w)는 q→1/2에서만 0(w=1도 q≈0.496);
  usable q≤0.25서 leak 0.4–1.0 → 자연 i.i.d. fresh-noise는 smooth와 usable 동시 불가(이산
  all-or-nothing) = C7 self-dual rigidity의 이산 그림자(self-dual=q→1/2). LWE 가우시안(연속
  tunable, usable width서 smooth)과 대조. exotic(non-i.i.d.) encoding은 안 막힘(열린 ≈0).
판정: #1 긍정증거(상속된 SQ-hardness, marginal) · #2 자연경로 obstruction(exotic 열림). 7th 아님.
```

## §1 (#1) SQ / statistical-dimension positive-evidence

For "learn `x` from `(a, ⟨a,x⟩⊕e)`", SQ-hardness is governed by the secret-pairwise correlation
`Cor(x,x') = (1−2p)²·μ̂(x⊕x')`, where `μ̂(Δ)=E_{a~μ}[(−1)^{⟨a,Δ⟩}]` is the Fourier bias of the
a-distribution. Uniform `a` (LPN): `μ̂(Δ)=0` for `Δ≠0` (maximal SQ-hardness). For sympLPN, `a` =
rows of a matrix with symplectically-orthogonal columns:

```text
  n  k   #rows    sympLPN max|μ̂(Δ)|   uniform-LPN max|μ̂|   sampling 1/√#rows
  4  2   32000        0.0116               0.0041              0.0056
  4  4   32000        0.0199               0.0111              0.0056
  5  3   40000        0.0106               0.0081              0.0050
  6  4   48000        0.0120               0.0095              0.0046
```

The sympLPN bias is the **same order** as uniform-LPN and the sampling floor — **no `Δ` stands
out**. So the symplectic structure does **not** bias the a-distribution's marginal; the
secret-pairwise correlation stays exponentially small like LPN, and **sympLPN inherits LPN's SQ
lower bound** (statistical-query algorithms — a broad class covering most known average-case
attacks — need ~exp queries). This is a **positive** hardness ingredient, the first the program
has produced (everything prior is no-go). **Honest scope:** the per-sample *marginal* ingredient;
a full SQ proof would also bound within-matrix row correlations. No `Δ` with an `Ω(1)` bias was
found (any such would be a concrete SQ attack — none exists in the structure's marginal).

## §2 (#2) The fresh-noise worst→avg encoding — the precise obstruction

The one open worst→avg route (the symmetry route closed by Sp-irreducibility, C7/C8/adjudicator):
a Regev-style **fresh-noise** encoding. For it to map worst-case instances to the average
(instance-independent) distribution, two worst-case errors differing by `Δ` (weight `w`) must
become indistinguishable: `leak(q,w)=TV(Bern(q)^w, Bern(1−q)^w) → ε`.

```text
  leak(q,w):    q=0.05  0.10  0.20  0.30  0.40  0.45  0.49
       w=1       0.900  0.800 0.600 0.400 0.200 0.100 0.020
       w=8       1.000  0.995 0.933 0.748 0.420 0.217 0.044
  smallest q with leak<0.01:  w=1→0.496, w=4→0.497, w=16→0.499   (all UNUSABLE: q→1/2)
```

`leak→0` **only as `q→1/2`** (even a weight-1 difference needs `q≈0.496`). So a worst-case
instance is smoothed into the average distribution only at **near-total noise** (`q→1/2`,
undecodable); at any **usable** rate (`q≤0.25`) the worst-case leaks (`leak` ≥ 0.4). **The natural
i.i.d. fresh-noise encoding cannot simultaneously smooth and stay usable** — discrete smoothing is
all-or-nothing. This is the **discrete shadow of the C7 self-dual-noise rigidity** (the self-dual
point is exactly `q→1/2`): LWE's Gaussian is a *continuous, tunable* family that smooths at a
*usable* width, whereas F₂ depolarizing has no usable smoothing width. **Honest scope:** this
obstructs the *natural* encoding; a *clever non-i.i.d./correlated ("exotic")* encoding is **not**
ruled out — that remains the open ≈0 route (the papers' "exotic requirements").

## §3 Verdict (Sound Verifier)

**Both run; both genuine; neither yields a 7th or a break.**
- **#1: positive SQ evidence (new).** sympLPN's marginal a-distribution is balanced ⇒ it inherits
  LPN's SQ lower bound (broad-class hardness), complementing the decoder no-go. *Marginal scope.*
- **#2: the natural fresh-noise worst→avg encoding is obstructed (concretized).** Discrete
  smoothing is all-or-nothing (the C7 rigidity's discrete shadow); only an exotic encoding is left
  open (≈0).

Together they sharpen LSN's status from two new sides: a *positive* lower-bound ingredient (SQ),
and a *precise obstruction* on the last open worst→avg route (natural fresh-noise). **No 7th; no
security claim; OPEN = LSN; the residual open questions (external `LSN ⊀ LPN`; exotic fresh-noise
worst→avg; beyond-Fourier quantum) remain ≈0 / external.**

---

## References
- `lsn-experiments/25-sq-statistical-dimension.py` (#1), `26-freshnoise-encoding-obstruction.py` (#2).
- SQ framework: secret-pairwise correlation = `(1−2p)²·μ̂(Δ)`; LPN SQ lower bound (classical).
- Lane C7 (self-dual-noise rigidity `g(0)=2^{-n}`, the q→1/2 point), adjudicator SvN (symmetry route closed).
- Regev LWE worst→avg (Gaussian = tunable smoothing) — the contrast #2 makes precise.
