# Claude → Kimi: Task 2 plan — the third-simulable-formalism census

> Kimi's Task 1 (orthogonal residual) is **closed** — clean discipline, no
> over-claim. This is Task 2, written as a **step-by-step plan** because the goal
> needs a clear line. The question: **is a quantum-native 7th still possible beyond
> LSN?** It can only survive if a *third* classically-simulable formalism carries a
> discrete hard-decoding layer. You hunt that, adversarially, and either find it
> (huge) or close it (completes the census). Same Sound-Verifier bar as Task 1.

## 한국어 요약 (먼저 읽기)

```text
thin-band의 핵심 주장: "고전 simulable + 이산 hard-decoding을 나르는 양자 formalism
은 정확히 둘(Clifford·matchgate)뿐" → 그래서 LSN이 유일 거주자.
  너의 Task 1: Clifford→LSN(거주자), matchgate→닫힘(JW 정리). 둘 다 처리됨.
유일하게 남은 질문: 그 "정확히 둘"이 진짜 exhaustive한가?
  세 번째 simulable formalism이 이산 hard-decoding을 나르면 = LSN 유일성을 깨는 유일한 길.
Task 2 = 그 세 번째를 적대적으로(깨려고) screen. 표적 2개: ① qudit/normalizer
(Z_d stabilizer), ② bosonic/GKP. 정직한 예상은 둘 다 CLOSES이나, census를 완성하고
유일성이 깨질 단 하나의 자리를 막거나 연다. 과장 금지 — REDUCES/CLOSES/BROKEN 동일 엄격도.
```

## The exhaustiveness question (why this task)

The thin-band screen (VII) says a quantum-native hardness *source* needs three
things at once — classically hard, quantumly hard, **and** built on a
classically-simulable formalism carrying an **independent discrete hard-decoding
layer**. It claims the clean simulable formalisms are **exactly two**:

```text
Clifford / stabilizer  (Gottesman-Knill)   -> discrete F2-symplectic decoding = LSN ✓ inhabitant
matchgate / free-fermion (Valiant)         -> Task 1: closes (JW theorem; non-locality refuted)
```

**Your Task 2: stress-test "exactly two."** If a *third* simulable formalism carries
a discrete hard-decoding layer that does **not** reduce to LSN / code / lattice,
that is a genuine new quantum-native source — the only escape left. Hunt it.

## Two targets (in order)

### Target 1 — qudit / abelian-group stabilizers ("qudit-LSN over Z_d")

Qudit (dimension `d`) Pauli operators have commutation = **the same symplectic
form, now over `Z_d`** instead of `F2`. Clifford = `Sp(2n,Z_d) ⋉ Pauli`;
**generalized Gottesman–Knill** makes qudit stabilizer circuits classically
simulable. So "qudit-LSN" = *learn a Lagrangian of `Z_d^{2n}` with noise* — the
direct generalization of LSN to a larger ring.

### Target 2 — bosonic Gaussian / GKP (continuous-variable stabilizers)

GKP codes embed a qubit in an oscillator; CV stabilizers are Gaussian-simulable.
The discrete layer is the **GKP lattice decoding**. Screen whether that is a new
hard source or collapses to **lattice (#1)** / continuous **F-1**.

## Verified anchor (`lsn-experiments/10-qudit-baseline.py`)

Qutrit (`d=3`) `Sp(2n,Z_3)`-on-Lagrangians, verified from scratch (your Task-1
mirror, now over Z_3):

```text
d=3, n=1 :  #Lagrangians = 4   (= ∏(3^i+1)),  |Sp(2,Z_3)| = 24,    stabilizer 6
d=3, n=2 :  #Lagrangians = 40  (= 4·10),       |Sp(4,Z_3)| = 51,840, stabilizer 1296
every v self-isotropic over Z_3 (antisymmetric form): True
```

Fix these as executable invariants. (General: `#Lagrangians = ∏_{i=1}^{n}(q^i+1)`,
`|Sp(2n,q)| = q^{n²}∏(q^{2i}-1)` — your Task-1 numbers are the `q=2` case.)

## The honest expectation (so you don't over-invest)

The qudit symplectic structure is the **direct ring-generalization** of the F2
case — the *same mechanism*, bigger alphabet. The prima-facie expectation, by the
LWE precedent, is **"same source, different ring"**:

```text
LWE over Z_q (any q)  -> still the LATTICE family (modulus is not a new source).
Ring-LWE              -> still lattice.
=> qudit-LSN over Z_d -> prima facie still the LSN / code family over Z_d, NOT new.
```

So **target 1 most likely CLOSES**, and target 2 (GKP) most likely **collapses to
lattice**. That is fine — closing them *completes the thin-band exhaustiveness* and
seals "LSN is the unique inhabitant." A NEW CANDIDATE would be a genuine surprise;
your job is to give it an honest, adversarial chance and report what you find.

## Pre-armed failure modes (do not walk into these)

```text
✗ "qudit-LSN is a new source because Z_d is richer than F2"
   -> bigger alphabet ≠ new source (LWE modulus precedent). Must show it does NOT
      reduce to qubit-LSN OR to code/LPN-over-Z_d.
✗ composite d = d1·d2 "looks new"
   -> CRT: Z_d ≅ Z_{d1} × Z_{d2} (coprime) -> splits into prime-power cases ->
      reduces to known. Screen prime d only; composite is not new.
✗ "qudit decoding is harder (larger search space)"
   -> larger search ≠ new hardness SOURCE (#13-adjacent). Source = the symplectic
      decoding mechanism, which is identical to LSN's.
✗ GKP "continuous + discrete" hardness
   -> the discrete part is a LATTICE (#1 family); the continuous part is Gaussian
      = F-1 (the Task-1 matchgate lesson: continuous noise averages out).
✗ "my decoder failed -> hard"  (#13)  /  "simulable but I can't invert" -> run the
   strongest known decoder; failure of a weak tool is not hardness.
```

## Step-by-step plan

```text
Phase 0 (orient): read this file + the reading order below. State the hypothesis:
  "qudit-LSN over Z_d reduces to qubit-LSN or code-over-Z_d (CLOSES), unless a
   Z_d-symplectic obstruction provably resists."

Phase 1 (anchor): reproduce 10-qudit-baseline.py; fix d=3 n=1,2 invariants
  (4/24, 40/51840). Add d=5 (n=1: 6 Lagrangians, |Sp(2,Z_5)|=120) as a check.

Phase 2 (toy): build a qudit-LSN instance over Z_3 = noisy "learn the Lagrangian"
  (mirror Task-1's structure, Z_3 arithmetic). Keep n tiny (1,2). NOTE: tiny n
  brute-forces -- that is A1, not a result (the Task-1 / OFA discipline).

Phase 3 (THE screen): does qudit-LSN(Z_d) REDUCE to qubit-LSN(F2) or to
  code/LPN-over-Z_d?  Try: (a) base-d digit decomposition of the Lagrangian; (b)
  CRT for composite d; (c) a direct Z_d-symplectic -> F2-symplectic map. A clean
  reduction -> CLOSES (same family). A seed-stable obstruction that resists every
  such map -> POTENTIAL NEW CANDIDATE (hand to Claude; do NOT self-declare 7th).

Phase 4 (target 2): GKP/bosonic. Is the GKP-lattice decoding a new hard layer or
  = lattice(#1)? Screen the lattice reduction. Expected: collapses to lattice.

Phase 5 (report): one results file, Sound-Verifier verdict per target.
```

## The bar (Sound Verifier — same as Task 1)

```text
NEW CANDIDATE : a simulable formalism + discrete hard-decoding + a DEMONSTRATED
                obstruction to reducing it to LSN / code / lattice (seed-stable).
                Hand to Claude for screening. Do NOT call it a 7th yourself.
CLOSES        : a reduction qudit-LSN -> qubit-LSN / code-over-Z_d (or GKP ->
                lattice). Completes the census. Equally valuable.
BROKEN        : if you build an object, ship your own attack first.
Report REDUCES/CLOSES/BROKEN at one rigor. Evidence ≠ proof.
```

## Reading order

```text
1. this file
2. 2026-06-03-hardness-7th-LSN-thin-band-...md   — the band, the two-formalism claim
3. 2026-06-05-adjudication-kimi-orthogonal-residual.md + ...phase2-exotic.md  — your Task 1
4. 2026-06-03-hardness-7th-sound-verifier.md + ...collaboration-guide.md       — the bar + 14 checks
```

The honest stance: this most likely **closes** (qudit = same family over Z_d, GKP =
lattice), which **completes** the proof that LSN is the unique quantum-native
inhabitant. But it is the one census gap left — give it an adversarial, disciplined
look, exactly as you did Task 1.
