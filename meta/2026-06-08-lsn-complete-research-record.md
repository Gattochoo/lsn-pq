# LSN Complete Research Record (2026-06-05 — 2026-06-08)

**Purpose**: Comprehensive timeline of all LSN research activities, findings, and artifacts during the 4-day intensive session.

---

## Day 1: 2026-06-05 (Friday)

### Morning
- **Claude**: Lane-A LSN↔LPN reduction scope analysis
  - File: `2026-06-06-lane-A-lsn-lpn-reduction-scope.md`
  - Finding: `sympLPN ⊀ LPN` proven for **linear reductions only**; any-reduction open
  - Win-win heuristic: non-linear reduction would improve LPN self-reductions

### Afternoon
- **Claude**: SEED symplectic-Fourier self-duality verification
  - File: `2026-06-06-SEED-symplectic-fourier-selfduality.md`
  - Verified: `F_Ω[1_L] = 2^n · 1_L` for n=2,3,4
  - Self-dual noise rigidity: `g(0) = 2^{-n}` (unusable error rate)
  - Instance randomization is FREE (Witt theorem)

### Evening
- **Claude → Kimi handoff**: Worst→avg localization
  - File: `2026-06-07-claude-to-codex-kimi-handoff-worstavg-localization.md`
  - Barrier localized ENTIRELY to noise, not instance
  - Three concrete tasks assigned to Codex/Kimi/Claude

---

## Day 2: 2026-06-06 (Saturday)

### Early Morning
- **Kimi**: SBS signing-oracle attack adjudication
  - File: `2026-06-06-sbs-signing-oracle-adjudication.md`
  - **SBS = BROKEN** — 2-8 signatures → 100% key recovery

### Morning
- **Kimi**: Decoder battery — Experiment 18 (symplectic clique)
  - File: `lsn-experiments/18-kimi-symplectic-clique-decoder.py`
  - Finding: Clique-drowning — planted clique < random clique number

- **Kimi**: Experiment 19 (symplectic Fourier, SFT-P)
  - File: `lsn-experiments/19-kimi-symplectic-fourier-decoder.py`
  - Finding: Fourier Drowning — SNR = O(√m / 2^n) → 0

- **Kimi**: Experiment 20 (discrete derivative, DDD)
  - File: `lsn-experiments/20-kimi-discrete-derivative-decoder.py`
  - Finding: Noise amplification — even full observation fails

### Afternoon
- **Claude**: Lane E — Quantum Fourier sampling attack
  - File: `2026-06-07-lane-E-quantum-fourier-sampling-attack.md`
  - **Death mode ⑤ (BQP-easy): CLOSED**
  - Natural quantum attack (Weil sampling) fails at poly samples
  - Collapses to uniform when m/2^n < 1

- **Claude**: SBS BROKEN verified + imported
  - File: `2026-06-07-sbs-BROKEN-signing-oracle-verified-import.md`
  - 100% exact key recovery in O(few) chosen messages, n≤16

### Evening
- **Claude**: K4 quantum assessment
  - All known quantum vectors blocked (QFS, HSP, Grover, quantum walk)
  - Quantum info-theoretic lower bound matches SQ bound
  - **K4 = CLOSED**

---

## Day 3: 2026-06-07 (Sunday)

### Morning
- **Kimi**: Experiment 21 (ML classifier)
  - Finding: PARTIAL — 65-70% distinguishability, NO exact subspace recovery
  - Separation: decision (easy) vs search (hard)

- **Kimi**: Experiment 22 (decoupling rigidity)
  - Witt theorem verified — instance randomization FREE

- **Kimi**: Experiment 23 (Weil noise preservation)
  - Corrected per OFA-360: nonlocal Sp maps do NOT preserve per-qubit law
  - Decoupling: OPEN (not "fully viable")

### Afternoon
- **Codex**: OFA-342 (worst→avg locality crux)
  - n=2: local orbits [6,9], full-Sp orbit 15
  - Entangling support-weight changes: 8
  - Local support-weight changes: 0

- **Codex**: OFA-343 (local orbit n=4 scaling)
  - n=4: local orbits [81,108,162,324,648,972]
  - Support-preserving transvections: 3n = 12
  - Nonlocal support-preserving: 0

- **Codex**: OFA-344 (support-preserving group closure)
  - Local generated group order = 6^n · n!

### Evening
- **Kimi**: Experiment 24 v2 (quantum Fourier sampling)
  - Calibration: clean/dense ratio = 2^n exact, recovery 100%
  - Poly-sample collapse confirmed

- **Kimi**: Experiment 25 (low-degree polynomial / AKKLR)
  - Finding: DEAD — n-th order derivative requires 2^n points per evaluation
  - Sample complexity: Ω(N^{1-1/2^k})

- **Claude**: Codex→Kimi handoff (K3 cross-check)
  - OFA-386 (Product Chi2) + OFA-387 (distance distribution) received
  - Codex independently confirmed q-binomial formula n=2..8

---

## Day 4: 2026-06-08 (Monday) — TODAY

### 00:00–06:00
- **Kimi**: K3 formal SQ proof assembly
  - File: `2026-06-08-k3-formal-sq-proof.md`
  - 7 Lemmas + Theorem 5.1
  - Commit: `22ecd44a`

- **Kimi**: Experiment 27b (distance distribution)
  - Mean dim(L ∩ L') ~ 0.5–0.7, does NOT grow with n

### 06:00–09:00
- **Kimi**: K3 Lemma 3.1 exact correlation
  - File: `2026-06-08-k3-lemma-3-1-exact-correlation.md`
  - Exact formula by intersection dimension j

- **Kimi**: K3 Lemma 6.1 query class + adaptive
  - File: `2026-06-08-k3-lemma-6-1-query-class-adaptive.md`
  - Full query class Q = {q: V×F₂ → [-1,1]}

- **Kimi**: P4 external impossibility
  - File: `2026-06-08-p4-lsn-not-reducible-to-lpn.md`
  - 5 barriers documented

### 09:00–12:00
- **Kimi**: Noise wall theory
  - File: `2026-06-08-kimi-noise-wall-theory.md`
  - SNR analysis, threshold m = Θ(2^{2n})

- **Kimi**: Decoder landscape
  - File: `2026-06-08-kimi-decoder-landscape.md`
  - Unified taxonomy of 15+ families

- **Kimi**: Security parameterization
  - File: `2026-06-08-kimi-security-parameterization.md`
  - 80/128/192/256-bit concrete params

### 12:00–14:00
- **Kimi**: BKW analysis + n=8 transition
  - File: `2026-06-08-kimi-bkw-analysis.md`
  - BKW NOT A THREAT
  - n=8 transition: m ≈ 10,000 threshold

- **Claude**: K3 full SQ proof (current session)
  - S_A = 0 gap analysis
  - Revised argument: structural knowledge does not increase bound
  - Empirical validation (Exp 28)

### 14:00–NOW
- **Kimi**: Phase 1–3 completion
  - K3 full SQ proof integrated (commit `fbaa9c7f`)
  - Codex OFA cross-checks integrated (commit `5e62e88b`)
  - Worst→avg local subgroup results integrated (commit `fbb52fb5`)
  - Uniform-error decoder battery (commit `cae6c91c`)
  - Paper skeleton v2 (commit pending)

---

## Artifact Index

### Specs (docs/superpowers/specs/)
| File | Content | Status |
|------|---------|--------|
| `2026-06-08-lsn-7th-family-status-report.md` | Academic literature review | ✅ Complete |
| `2026-06-08-lsn-research-consolidation-codex-handoff.md` | Internal consolidation | ✅ Complete |
| `2026-06-08-k3-full-sq-proof-integrated.md` | **Full SQ proof (standard model)** | ✅ Complete |
| `2026-06-08-k3-sa-zero-symmetric-conditioning.md` | S_A = 0 argument (revised v2) | ✅ Complete |
| `2026-06-08-lsn-paper-skeleton-v2.md` | **Draft paper (polished)** | ✅ Complete |
| `2026-06-08-experiment-29-uniform-error-decoder-battery.md` | P4 uniform-error results | ✅ Complete |
| `2026-06-07-claude-to-codex-kimi-handoff-worstavg-localization.md` | Worst→avg handoff + OFA-342/343 | ✅ Complete |

### Experiments (lsn-experiments/)
| File | Content | Status |
|------|---------|--------|
| `28-sa-zero-sq-preservation.py` | S_A = 0 empirical validation | ✅ Complete |
| `29-uniform-error-lsn-battery.py` | Uniform-error decoder battery | ✅ Complete |

### Git Commits (shared/hardness-7th-exchange)
| Commit | Content |
|--------|---------|
| `fbaa9c7f` | K3 Full SQ proof with S_A=0 |
| `5e62e88b` | Codex OFA cross-checks (389-396) |
| `fbb52fb5` | Worst→avg local subgroup (342/343/362) |
| `cae6c91c` | Uniform-error decoder battery |

---

## Open Problems Tracker

| P# | Problem | Status | Blocker | Next Action |
|----|---------|--------|---------|-------------|
| P1 | Worst→avg reduction | 🔴 OPEN | Noise decoupling | Codex 06-11 collaborative attack |
| P2 | LPN→sympLPN | 🔴 OPEN | Vacuous at crypto p | Theoretical construction |
| P3 | sympLPN→LPN (non-linear) | 🔴 OPEN | Win-win guarded | New algebraic approach |
| P4 | Uniform-error (Sp-invariant) | 🟡 PARTIAL | n≥6 infeasible | Asymptotic proof |
| P5 | Practical primitive | 🔴 OPEN | Needs protocol design | Signature/KEM design |
| P6 | LWE→LSN | 🔴 OPEN | External | Track only |

---

*Record compiled 2026-06-08 KST*
*Session duration: ~72 hours (Claude/Codex/Kimi collaborative)*
