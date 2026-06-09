# Lane C4 — the symplectic-completion engine of Thm 1.6 Stage 1 (LPN → sympLPN), verified

> Lane C2 illustrated the degeneracy mechanism but explicitly deferred reimplementing the
> reduction. Lane C4 closes **part** of that gap: the *algebraic engine* of Stage 1
> (LPN → sympLPN), which 2509.20697 §1.2.3 states verbatim (Eqs 1.3–1.4) and which is fully
> implementable. Verified across several `(n,ℓ,b)`: the completion turns an arbitrary matrix
> into a **symplectically-orthogonal (isotropic), full-rank** sympLPN matrix `B`, with the
> given LPN data embedded **verbatim** as the top `2n−b` rows, and `S = N1ᵀN2 + MᵀA'` exactly
> the intended symmetric matrix (Eq 1.4). **200/200 trials pass on all four checks.** This is
> the structural basis of `LPN ↪ LSN` (so `LSN ⊇ LPN`). Honest scope: the §§5–6 secret-
> preservation map is **not** reimplemented; this verifies the engine, not the whole
> reduction. Script: `lsn-experiments/20-thm16-symplectic-completion.py`.

`working code (verbatim Eq 1.3–1.4; evidence for LSN⊇LPN, not a 7th proof)`. Date: 2026-06-06.

---

## 한국어 요약

```text
Thm 1.6 Stage 1 (LPN→sympLPN)의 symplectic-completion 엔진을 verbatim Eq 1.3–1.4로 구현·검증.
구성: B=[N1;M;N2;A'] (2n×ℓ); 열 i,j의 symplectic 내적 = S_ij+S_ji, S=N1ᵀN2+MᵀA'.
  → 모든 열 symplectic-orthogonal ⟺ S 대칭. 샘플링: 랜덤 대칭 S' → T=S'−N1ᵀN2 → MᵀA'=T 풀이.
검증(200/200, (n,ℓ,b)=(3,2,3)(5,2,3)(6,4,5)(8,4,6)(10,6,7)):
  - B가 isotropic(모든 열쌍 symplectic-orthogonal) ✓
  - B full column rank ✓
  - S = 의도한 대칭 S' 정확히 일치(Eq 1.4) ✓
  - 주어진 [N1;M;N2](=LPN 데이터)가 B의 상위 2n−b행에 verbatim 임베딩 ✓
→ 임의 행렬이 행을 보존한 채 isotropic sympLPN 행렬로 완성됨 = LPN↪sympLPN(Stage 1)의 구조적 기반.
정직한 범위: §§5-6 secret-보존 맵은 미구현(엔진 검증이지 전체 reduction 아님). LSN⊇LPN 증거, 7th 증명 아님.
```

## §1 The engine (verbatim) and what is checked

Eq 1.3: `B = [N1 ; M ; N2 ; A'] ∈ F₂^{2n×ℓ}` (top `n` rows `[N1;M]` = x-half; bottom `n` rows
`[N2;A']` = z-half). Eq 1.4: the symplectic inner product of columns `i,j` of `B` equals
`S_ij + S_ji` with `S := N1ᵀN2 + MᵀA'`; hence all columns are symplectically orthogonal iff
`S` is symmetric. The reduction samples a uniform symmetric `S'`, sets `T := S' − N1ᵀN2`, and
solves `MᵀA' = T` (column by column; `M` full column rank `ℓ`, so solvable). The given LPN
matrix is the top `2n−b` rows `[N1;M;N2]`; only `A'` (`b` rows) is appended.

```text
checks (200 trials each), (n,ℓ,b):  isotropic   full-rank   S=Sym    embed-verbatim
  (3,2,3)  (5,2,3)  (6,4,5)  (8,4,6)  (10,6,7):    all 200/200 on all four checks
```

## §2 Reading

- The completion is **exact and always succeeds**: an arbitrary lower block is turned into
  one whose full column set is symplectically orthogonal (an isotropic / sympLPN matrix),
  *without disturbing the given rows*. So the LPN instance literally sits inside the sympLPN
  matrix — the structural heart of `LPN ↪ sympLPN` (Stage 1 of Thm 1.6), hence `LSN ⊇ LPN`.
- This complements **Lane C2** (degeneracy junk-register, the LSN-side reason the embedding
  works) and **Lane C** (entropy deficiency, the `LSN ⊀ LPN`-linear side): together the two
  load-bearing reduction facts behind Lane A's superset reading are now both backed by code.
- **Honest scope (unchanged):** the precise LPN-secret → sympLPN-secret map (§§5–6) is not
  reimplemented; faithfully reproducing it from the paper's later sections is deferred to
  avoid drift. This verifies the *completion engine* (Eq 1.3–1.4), the part that is stated
  explicitly — not the whole reduction.

## §3 Verdict (Sound Verifier)

**Engine verified; status unchanged.** The symplectic-completion step of Thm 1.6 Stage 1 is
confirmed exactly (isotropic + full-rank + Eq 1.4 + verbatim embedding, 200/200). This is
**evidence** for `LSN ⊇ LPN` (LPN embeds into LSN), supporting Lane A's superset reading; it
is **not** a proof that LSN is a 7th, and **not** a reimplementation of the §§5–6 secret map.
No security claim; OPEN = LSN; the one open point (non-linear `LSN ⊀ LPN`) is untouched.

---

## References
- `lsn-experiments/20-thm16-symplectic-completion.py` (this verification).
- Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan, arXiv:2509.20697, §1.2.3 (Eqs 1.3–1.4); §§5–6 (the deferred secret map).
- In-house: Lane C2 (degeneracy), Lane C (entropy deficiency), Lane A (superset reading).
