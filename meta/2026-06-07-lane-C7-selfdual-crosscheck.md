# Lane C7 — independent cross-check of the self-duality SEED + an angle (the worst→avg barrier is localized ENTIRELY to the noise)

> A parallel agent's SEED (`2026-06-06-SEED-symplectic-fourier-selfduality.md`) relocated the
> LSN worst→avg "quantum barrier" from geometry to the **noise distribution**, with two
> verified claims. Lane C7 **independently reproduces both** with my own implementation, adds
> the structural reason, and contributes one **new angle** that sharpens the seed's live tip:
> the *other* half of a Regev-style worst→avg — **instance-randomization — is FREE**, so the
> obstruction is **entirely** the noise rigidity. Script:
> `lsn-experiments/22-selfdual-crosscheck.py`. Date: 2026-06-07.

---

## 한국어 요약

```text
SEED 두 주장 독립 확증 + 새 각도:
 (a) F_Ω[1_L]=2ⁿ·1_L (Lagrangian이 symplectic-Fourier self-dual): 30/30 (n=2,3,4) ✓
 (c) [내 추가] F_Ω²=2^{2n}I (오차~1e-14) → 고유값 ±2ⁿ = (b) rigidity의 구조적 이유 ✓
 (b) self-dual 분포는 g(0)=2^{-n} (0.5/0.25/0.125 정확); depolarizing은 q=1/6서만 self-dual
     (P(I)=0.5=2^-1) ✓ → self-dual noise는 error rate 1-2^{-n}→1로 rigid (사용불가) ✓
 (d) [내 추가] instance-randomization은 FREE: rand_lagrangian이 전체 Lagrangian uniform 커버
     (15/15, 135/135); Witt 정리(Sp가 Lagrangian에 transitive)로 worst-case L*→uniform L'를
     efficient symplectic map으로 보냄.
종합: Regev식 worst→avg = (i)instance 무작위화[free,(d)] + (ii)self-dual noise smoothing[rigid
  차단,(b)]. (i)는 공짜, (ii)만 막힘 → ★worst→avg 장벽이 전적으로 NOISE에 국한(seed live tip 정밀화).
  단 이것은 LSN을 위한 hardness reduction 방향(외부 LSN⊀LPN과 다름); 양쪽 다 여전히 OPEN. 7th 아님.
```

## §1 Independent reproduction of the SEED's two claims

```text
(a) F_Ω[1_L] = 2^n·1_L     : 30/30 self-dual for n=2,3,4   (my FWHT∘J implementation)
(b) self-dual g ⇒ g(0)=2^{-n}: exact (n=1,2,3 → 0.5, 0.25, 0.125)
    depolarizing self-dual only at q=1/6 (P(I)=0.5=2^{-1})  : confirmed
```

Both reproduce exactly. (Implementation note: `F_Ω[f] = WHT[f∘J]` where `J` swaps the two
symplectic halves, since `Ω(w,v) = ⟨w, Jv⟩` — so the symplectic Fourier transform is the
ordinary Walsh–Hadamard transform precomposed with the half-swap.)

## §2 The structural reason for the rigidity (added)

```text
(c) F_Ω∘F_Ω = 2^{2n}·I    : max error ~1e-14 (machine precision), n=2,3
```

`F_Ω² = 2^{2n} I` ⇒ the eigenvalues of `F_Ω` are exactly `±2^n`. Self-dual = the `+2^n`
eigenspace; for any vector there with `Σg=1`, evaluating `F_Ω[g](0)=Σ_v g(v)=1=2^n g(0)` forces
`g(0)=2^{-n}`. (The `−2^n` eigenspace would force `g(0)=−2^{-n}<0`, impossible for a
distribution.) So the rigidity is a direct consequence of the involution structure — not a
coincidence.

## §3 ★ The new angle — instance-randomization is FREE, so the barrier is ENTIRELY the noise

A Regev-style worst→avg has **two** ingredients: (i) randomize the *instance* (worst-case →
average-case), and (ii) smooth with a *self-dual noise*. The seed showed (ii) is rigidly
blocked for LSN (`g(0)=2^{-n}`). Lane C7 checks (i):

```text
(d) random Lagrangians sampled ~uniformly:  n=2 → 15/15 distinct (= all),  n=3 → 135/135 (= all)
```

Instance-randomization is **free**: uniform Lagrangians are efficiently sampleable, and by
**Witt's theorem** `Sp(2n,F₂)` acts **transitively** on Lagrangians — so a worst-case `L*` maps
to a uniform `L'` by an efficient symplectic change of basis (and back). Therefore:

> **The worst→avg obstruction for LSN is NOT in the instance (that half is free) — it is
> ENTIRELY in the noise (the `g(0)=2^{-n}` self-dual-noise rigidity).** This localizes the
> seed's barrier precisely: unlike LWE (where the Gaussian is self-dual at *every* width, a
> family Regev tunes), the symplectic self-dual noise is a *single rigid point* at error rate
> `1−2^{-n}`, unusable. The code's self-duality (Lagrangian) is present and the instance side
> is free; the one missing ingredient a LSN worst→avg must supply is a way to use the code's
> self-duality **without** a self-dual noise (decoupling code from noise — exactly what LWE
> gets for free and LSN does not).

## §4 Verdict (Sound Verifier)

**SEED reproduced independently; barrier localized to the noise.** Claims (a),(b) reproduce
exactly; (c) gives their structural cause (`F_Ω²=2^{2n}I`); (d) shows instance-randomization is
free, so the worst→avg barrier is **entirely** the noise rigidity. This is **evidence /
structural clarification**, not a worst→avg reduction and not a 7th proof. Note this is the
*hardness-FOR-LSN* direction (a worst→avg reduction), **distinct** from the external
`LSN ⊀ LPN` reducibility question — both remain OPEN. No 7th; no security claim.

---

## References
- `lsn-experiments/22-selfdual-crosscheck.py` (this cross-check).
- SEED: `2026-06-06-SEED-symplectic-fourier-selfduality.md` (parallel agent) and its
  `18-symplectic-fourier-selfduality.py`, `19-selfdual-noise.py`.
- Witt's theorem (Sp transitive on Lagrangians); Regev LWE worst→avg (Gaussian self-duality).
