# Lane C8 — the transitivity-vs-locality conflict SCALES (n=2,3,4): quantitative flesh on the SvN closure

> The worst→avg-for-LSN sub-investigation (my Lane C7 localization → parallel SEED step 2 →
> adjudicator's Sp-irreducibility/SvN proof) converged on: full `Sp` is transitive on
> Lagrangians (free code-randomisation) but its noise-preserving subgroup (LOCAL-Clifford) is
> NOT transitive — so a noise-preserving worst→avg is blocked. The parallel agent verified the
> *existence* of the conflict at `n=2`; the adjudicator proved it in general (irreducibility).
> Lane C8 adds the **quantitative scaling** (own independent enumeration): the number of
> LOCAL-Clifford orbits on Lagrangians is **K(n) = 2, 3, 6 for n = 2, 3, 4** and grows — so a
> noise-preserving code-randomisation gets **increasingly far from transitive** with `n`.
> Confirmatory, not a new barrier. Script: `lsn-experiments/23-locality-conflict-scaling.py`.
> Date: 2026-06-07.

---

## 한국어 요약

```text
worst→avg-for-LSN 장벽 = transitivity-vs-locality conflict(SEED step2, n=2) = Sp-irreducibility
(adjudicator, 일반증명). Lane C8 = 그 정량 스케일링(독립 enumeration):
  n   #Lagrangians   full-Sp orbits   LOCAL-Clifford(noise-preserving) orbits K(n)
  2        15              1                K=2  [9,6]
  3       135              1                K=3  [54,54,27]
  4      2295              1                K=6  [972,648,324,162,108,81]
full Sp는 항상 transitive(1 orbit=free code-randomisation)이나 noise를 깨는 entangling 필요;
noise-preserving local 부분군은 K(n)개 orbit으로 쪼개고 K(n)↑(2→3→6) → noise-preserving
무작위화는 n 커질수록 transitive에서 멀어짐. #Lag(15/135/2295)=∏(2^i+1) 일치(검증), n=2 K=2는
병행 에이전트와 일치. 확정적 정량화지 새 장벽 아님. open route(fresh-noise encoding)는 여전히 ≈0.
```

## §1 What was computed (independent enumeration)

All Lagrangians of `F₂^{2n}` were enumerated as the single orbit of the standard one under the
full transvection group (which is `Sp`), giving `#Lagrangians = 15, 135, 2295` for `n=2,3,4`
(`= ∏_{i=1}^n (2^i+1)`, a correctness check), with **full-`Sp` = 1 orbit** (transitive ⇒ free
code-randomisation). Then the **LOCAL-Clifford subgroup** `Sp(2,F₂)^n ⋊ S_n` (per-qubit
transvections `X_i,Z_i,Y_i` + qubit permutations — exactly the symplectic elements that
**preserve the per-qubit depolarizing noise**) was used to count its orbits on the Lagrangians:

```text
  n   #Lagrangians   full-Sp orbits   LOCAL-Clifford orbits K(n)   orbit sizes
  2        15              1                   2                    9, 6
  3       135              1                   3                    54, 54, 27
  4      2295              1                   6                    972,648,324,162,108,81
```

## §2 Reading

- **Full `Sp` is transitive** (1 orbit) — code-randomisation is free, *but only with entangling
  elements that change qubit-support and destroy the per-qubit noise* (SEED step-2 check 3a).
- **The noise-preserving subgroup is NOT transitive**, and the conflict **scales**: `K(n) = 2,
  3, 6` grows with `n`. So as `n` increases, a noise-preserving code-randomisation is split
  across ever more orbits — ever farther from the single-orbit transitivity a free worst→avg
  would need. (`n=2` reproduces the parallel agent's result; `n=3,4` are the new data.)
- This is the **quantitative flesh** on the adjudicator's qualitative "no `Sp`-equivariant
  code⊕noise split" (`Sp`-irreducibility = finite Stone–von Neumann): the obstruction is not
  just present but *grows*, so the noise-preserving route does not recover even approximately
  at scale.

## §3 Verdict (Sound Verifier)

**Confirmatory quantitative result; not a new barrier, not a reduction.** The
transitivity-vs-locality conflict — full `Sp` transitive (free, noise-destroying) vs.
LOCAL-Clifford non-transitive (noise-preserving, `K(n)=2,3,6` growing) — is the concrete,
scaling form of the worst→avg obstruction the collaboration named and proved. It **does not**
close the one open route (a *fresh-noise* encoding of worst-case stabilizer decoding into
average-case sympLPN, ≈0 in-house, distinct from the external `LSN ⊀ LPN` question). Credit:
the conflict — parallel agent (SEED step 2); the general proof — adjudicator (Sp-irreducibility);
the scaling data — this lane. **No 7th; no security claim; OPEN.**

---

## References
- `lsn-experiments/23-locality-conflict-scaling.py` (this scaling computation).
- SEED step 2 (`2026-06-06-SEED-symplectic-fourier-selfduality.md`, `21-worstavg-locality-crux.py`) — n=2 conflict.
- Adjudicator (`2026-06-07-lane-adjudicator-svn-decoupling-assessment.md`, `22-svn-irreducibility.py`) — the general SvN/irreducibility proof.
- Lane C7 (`2026-06-07-lane-C7-selfdual-crosscheck.md`) — the localization this scales.
