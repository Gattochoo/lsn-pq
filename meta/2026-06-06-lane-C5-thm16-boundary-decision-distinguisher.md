# Lane C5 — the end-to-end Thm 1.6 reduction is a DECISION-distinguisher hybrid, not a small-n secret-recovery recipe (the honest boundary)

> Following the C4 verification of Stage 1 (symplectic completion), the natural next step was
> an **end-to-end** small-n verification of Thm 1.6 (LPN → LSN). Reading the construction
> (2509.20697 §§1.2.2–1.2.3, 4.1, 5.2, 6.1–6.2) settles that this is **not an in-house
> computational task**: the reduction is a **decision-to-decision distinguisher reduction via
> a hybrid/averaging argument** (an existence proof), *not* a constructive secret-recovery
> map. It also **refines** Lane C2: the LPN/sympLPN secret is embedded into the **junk `r_i`**
> and the LSN logical secret `y` is chosen **uniformly at random** — so "recover `y` ⇒ recover
> the LPN secret" is the *wrong frame*. The faithfully-verifiable components are exactly the
> ones already done (engine C4, degeneracy C2, entropy deficiency C); the hybrid existence
> proof is the external/proof boundary. **No 7th; no security claim. Honest stop.**
> Date: 2026-06-06.

---

## 한국어 요약

```text
다음 스텝 후보 = Thm 1.6 end-to-end (LPN→LSN) small-n 검증. 구성을 읽어보니 in-house 계산
과제가 아님:
 - LSN classical form: ([A_i|B_i], [A_i|B_i]·[r_i;y]+e_i), 목표=y 복구.
 - ★ LPN/sympLPN secret은 junk r_i에 임베딩되고 y는 *랜덤* 선택 → "y 복구=LPN secret 복구" 틀림.
   (Search LSN 풀면 우리가 고른 랜덤 y만 나와 쓸모없음 → 저자도 명시.)
 - 그래서 *decision* 변형으로 환원: LSN distinguisher ⟹ LPN distinguisher (hybrid/averaging,
   2m 샘플 중 한 곳에 sympLPN 인스턴스 숨김). = 존재 증명, constructive recipe 아님.
 - 논문: "does not provide explicit end-to-end code ... existence proofs, not constructive."
결론: end-to-end secret-recovery 검증은 틀린 프레임(이건 distinguisher 환원). 충실히 검증
  가능한 부분(완성엔진 C4·degeneracy C2·엔트로피 C)은 완료. hybrid 존재증명 = 외부/증명 경계.
  C2 정밀화: secret은 junk, y는 랜덤. 7th 아님·보안주장 없음. 정직한 정지.
```

## §1 Why end-to-end small-n verification is the wrong frame

A small-n "verify the reduction" check would build an LPN instance, push it through the map,
and confirm an LSN solution yields the LPN secret. But (2509.20697):
- **The secret is in the junk, `y` is random** (§1.2.3, Fig. 4): "the [LPN] secret is extended
  into a sympLPN secret, which is all then embedded into the *junk* portion of the LSN logical
  state," while `y` is "chosen uniformly random independently." So a **Search-LSN** solver
  returns the *useless random `y`*, not the LPN secret — the authors say this explicitly.
- **The reduction is decision-to-decision** (§1.2.3, §5.2, §6.2): "we formally reduce from the
  *decision* versions ... a distinguisher for LSN implies a distinguisher for LPN," via a
  hybrid/averaging argument (hide the sympLPN instance in one of `2m` samples; interpolate
  earlier-true / later-random). This is an **existence proof of a distinguisher reduction**,
  not a per-instance secret map.
- The paper "**does not provide explicit end-to-end code or algorithm suitable for small-n
  implementation** ... existence proofs, not constructive recipes" (Completeness Assessment).

So there is no constructive secret-recovery to run and check; a faithful "implementation"
would have to reproduce the hybrid distinguisher argument, which is a proof, not a computation.
Attempting a small-n "recovery" check would be measuring the wrong thing (drift).

## §2 What IS faithfully verifiable (already done) — and the refinement of C2

```text
verifiable component                         lane     status
symplectic-completion engine (Eq 1.3–1.4)    C4       VERIFIED (200/200: isotropic, full
                                                       rank, S symmetric, LPN data embedded)
stabilizer degeneracy / junk register         C2       illustrated (combinatorial, exact)
entropy deficiency of isotropic A (d→1/4)     C        verified (two independent counts)
end-to-end LPN→LSN (decision distinguisher    C5       NOT in-house-computable (hybrid
   hybrid)                                    (here)   existence proof) -> external/proof boundary
```

**Refinement of Lane C2 (important):** C2 said the degeneracy junk register "obfuscates the
logical info." C5 sharpens *where the LPN content lives*: it is embedded **in the junk `r_i`**
(via the degeneracy), with the LSN logical secret `y` **random and decoupled**. This is why
even `k=1` LSN carries an n-scale hard instance (the junk is n-dimensional, C2 §B), and why
the reduction must be phrased as **decision** (the search secret `y` is deliberately useless).

## §3 Verdict (Sound Verifier)

**Honest boundary reached.** The end-to-end Thm 1.6 reduction is a decision-distinguisher
existence proof (hybrid/averaging), not a constructive small-n recipe — so it is **not** an
in-house computational verification target; the faithfully-verifiable pieces (C4 engine, C2
degeneracy, C entropy) are complete, and the rest is the external/proof boundary. Attempting a
small-n secret-recovery "verification" would measure the wrong object — I decline it on
discipline (no fake implementation; evidence ≠ proof). LSN's superset reading (`LSN ⊇ LPN`)
stands on Thm 1.6 (a proven, if non-constructive-at-small-n, reduction) + the verified engine;
the one open point (non-linear `LSN ⊀ LPN`) is untouched. **No 7th; no security claim.**

---

## References
- Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan, arXiv:2509.20697 — §1.2.2–1.2.3 (classical
  rep, embedding, Fig. 3/4), §4.1 (equivalence), §5.2 (search-decision), §6.1–6.2 (sympLPN→LSN).
- In-house: Lane C4 (completion engine), Lane C2 (degeneracy), Lane C (entropy), Lane A (superset).
