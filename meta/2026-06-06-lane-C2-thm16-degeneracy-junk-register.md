# Lane C2 — Thm 1.6 (LSN ⊇ LPN): degeneracy "junk register" illustrated (the other half of Lane A)

> Lane A's "superset" reading rests on two facts: `LSN ⊀ LPN` (linear; Lane C verified its
> entropy-deficiency core) and **`LSN ⊇ LPN`** (Thm 1.6: constant-rate LPN reduces *into*
> LSN, even at k=1). Lane C2 addresses the second. The theorem **statement is verified
> verbatim**, and its mechanism — **stabilizer degeneracy**, the per-sample n-bit "junk
> register" — is **illustrated by exact combinatorial checks** in the symplectic
> (Pauli ↔ F₂^{2n}) representation. The full 3-stage reduction (paper §§4–6) is **not**
> reimplemented (avoided to prevent drift). Script:
> `lsn-experiments/18-thm16-degeneracy-junk-register.py`.

`working code (mechanism illustration, not a reduction reimplementation)`. Date: 2026-06-06.

---

## 한국어 요약

```text
Thm 1.6 (2509.20697 §1.2.1, verbatim): "reduction from LPN(⌊np/6⌋,2n,p/6) to LSN(k,n,p),
  any k≥1." Cor 1.7: sub-exp LSN(any rate) ⇒ classical-crypto breakthrough. ⇒ k=1 LSN조차
  constant-rate LPN만큼 어렵다. 메커니즘 = degeneracy.
LSN classical form: b_i = A_i r_i + B_i y + e_i  (A_i=stabilizer+logical-Z[isotropic],
  r_i=n비트 junk, B_i=logical-X, y=logical secret). degeneracy로 r_i가 생긴다.
검증(코드, 정확):
  - 같은 syndrome 코셋 E+S^⊥(크기 2^{n+k})이 2^{2k} logical class로 쪼개지고 각 class 크기
    |S|=2^{n-k} → 이 2^{n-k}개가 코드 위에서 구별불가(=degeneracy; ML은 합산=#P).
  - junk register 차원 = n (k와 무관, k=1도) → 단일 logical-qubit LSN도 n-스케일 hard
    인스턴스를 숨김 → LPN 임베딩 가능.
  - 고전 코드엔 이런 degeneracy 없음(message↦codeword 단사, 유일 coset leader).
정직한 범위: 정리 진술은 verbatim 검증, degeneracy 메커니즘은 조합론적으로 illustration;
  전체 3단계 reduction은 미구현(drift 방지). Lane A superset 독법의 *증거*지 7th 증명 아님.
```

---

## §1 The theorem (verbatim) and the mechanism

> **Thm 1.6** (arXiv:2509.20697, §1.2.1): "Fix any `k≥1` and `p∈(0,1)` ... There exists a
> reduction from `LPN(⌊np/6⌋, 2n, p/6)` to `LSN(k,n,p)`."
> **Cor 1.7**: "any sub-exponential time algorithm which solves LSN at any rate `k/n`
> implies a breakthrough in classical cryptography."

Classical representation of an LSN sample (paper §1.2.2, Fig. 3):
`b_i = A_i r_i + B_i y + e_i`, with `A_i ∈ F₂^{2n×n}` (stabilizers + logical-Z, isotropic),
`r_i ∈ F₂^n` a per-sample **junk vector**, `B_i ∈ F₂^{2n×k}` (logical-X), secret `y ∈ F₂^k`,
`e_i` depolarizing at `p`. The junk `r_i` exists because stabilizers act trivially on
codewords — **degeneracy**.

## §2 What the code verifies (exact combinatorial checks)

Working in the symplectic representation (Pauli ↔ `F₂^{2n}`, commutation ↔ `Ω`), with a
random stabilizer code `S` (isotropic, `dim = n−k`):

```text
[A] structure + degeneracy, all checks OK for (n,k) ∈ {(2,1),(3,1),(3,2),(4,1),(4,2)}:
      |S| = 2^{n-k}          (stabilizer group / degeneracy multiplicity)
      |S^perp| = 2^{n+k}     (same-syndrome coset; S ⊆ S^perp since isotropic)
      |S^perp / S| = 2^{2k}  (number of logical classes)
    A random error E: every E+s (s∈S) has the SAME syndrome and is logically equivalent
      (degeneracy); a logical L ∈ S^perp\S preserves the syndrome but changes the class.
    => the same-syndrome coset (2^{n+k}) splits into 2^{2k} classes each of size 2^{n-k};
       those 2^{n-k} representatives are indistinguishable on the code. ML decoding sums
       over each class (the #P / IP15 feature). That within-class freedom = the junk register.

[B] junk-register dimension = n for EVERY k (incl. k=1): A_i = (n-k) stabilizers + k
    logical-Z spans an isotropic n-space; r_i ∈ F₂^n. So a single-logical-qubit (k=1) LSN
    still hides an n-dimensional (LPN-scale) instance -- the room Thm 1.6 plants LPN into.

[C] classical contrast: a linear code's message↦codeword map is injective and syndrome
    decoding seeks the UNIQUE coset leader -- no 2^{n-k}-size subgroup acts trivially on the
    message. Degeneracy is strictly quantum.
```

## §3 Reading (with Lane A and Lane C)

- The degeneracy is the **mechanism** of `LSN ⊇ LPN`: the n-bit junk register, present even
  at `k=1`, is where constant-rate LPN is embedded (Thm 1.6), so `LSN` is **at least as hard
  as** constant-rate LPN regardless of rate (Cor 1.7).
- Combined with **Lane C** (`LSN ⊀ LPN` linear, entropy deficiency `d→1/4`) this gives the
  full **superset picture**: `LPN ↪ LSN` (Thm 1.6) and no linear `LSN → LPN` (App. D) ⇒ LSN
  is a **superset / ≥-hard** candidate, not an in-family *subset*. The 6.5th "structured
  instance of the code family" reading is the wrong direction (Lane A §5).
- Degeneracy being **strictly quantum** (absent in classical codes) is also the behavioral
  core of the *source-level* novelty argument (the only 6.5th leg, "still coding theory", is
  the taxonomic one) — though source-level novelty remains, as always, the deeper open
  question reductions cannot settle.

## §4 Verdict (Sound Verifier)

**Statement verified verbatim; mechanism illustrated; reduction NOT reimplemented (honest).**
Thm 1.6 / Cor 1.7 are quoted exactly; the degeneracy junk-register mechanism is confirmed by
exact structural identities in the symplectic representation. This is **evidence** for Lane
A's superset reading (`LSN ⊇ LPN` ∧ `LSN ⊀ LPN`-linear), **not** a proof that LSN is a 7th,
and **not** a reimplementation of the paper's §§4–6 reduction. No security claim.

```text
LSN status after Lanes A + C + C2:
  LSN ⊇ LPN          : Thm 1.6 (verbatim); degeneracy junk register illustrated (here).
  LSN ⊀ LPN (linear) : App. D; entropy deficiency d→1/4 verified (Lane C).
  LSN ⊀ LPN (any)    : OPEN, win-win-guarded (Lane A) -- the one external proposition.
  source-level new?  : behavioral yes (degeneracy strictly quantum); taxonomic 6.5th; open.
=> OPEN, strong under-verification 7th candidate. No 7th proven; no security claim.
```

---

## References
- `lsn-experiments/18-thm16-degeneracy-junk-register.py` (this illustration).
- Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan, arXiv:2509.20697, §1.2.1–1.2.3, §§4–6 (Thm 1.6 / Cor 1.7).
- Lane A (`2026-06-06-lane-A-lsn-lpn-reduction-scope.md`), Lane C (`...-lane-C-appendixD-entropy-deficiency-verified.md`).
- Stabilizer formalism: Pauli ↔ `F₂^{2n}`; degeneracy / ML-decoding #P-completeness (Iyer–Poulin, IP15).
