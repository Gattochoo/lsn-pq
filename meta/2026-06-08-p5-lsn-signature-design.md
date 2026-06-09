# P5: LSN-Based Signature — ZK Proof-of-Knowledge Design

**Status:** Design proposal  
**Date:** 2026-06-08  
**Context:** SBS signature broken by signing-oracle key recovery (2–8 signatures → 100% recovery). New design uses ZK to prevent coordinate leakage.

---

## 1. SBS Failure Analysis

**Root cause:** SBS signature revealed **exact coordinates** of critical points for native verification.  
**Attack:** 2–8 signatures → trilateration → full key recovery.  
**Lesson:** Any signature that reveals the secret structure directly is broken under EUF-CMA.

**New design principle:** The signature must be a **zero-knowledge proof of knowledge** of the secret Lagrangian `L`. The verifier checks the proof without learning `L`.

---

## 2. Core Idea: LSN as a Hard Relation

**Hard relation:** `R = {(pk, sk) = (samples, L)}` where `pk = {(x_i, y_i)}` are `m` samples from `D_L`.

`R` is hard because recovering `L` from `pk` is the LSN problem (SQ lower bound proven, K3).

**Signature:** A proof of knowledge of `L` such that `(pk, L) ∈ R`.

---

## 3. Polynomial Representation for ZK

The indicator `1_L(x)` has an exact polynomial representation:

```
1_L(x) = ∏_{j=1}^n (1 + ⟨w_j, x⟩)
```

where `{w_j}` is a basis of `L^⊥`.

**Key property:** For fixed `x`, this is a degree-n polynomial in the secret variables `{w_j}`.  
It can be evaluated in `n` multiplicative steps:

```
a_1 = 1 + ⟨w_1, x⟩
a_2 = a_1 · (1 + ⟨w_2, x⟩)
...
a_n = a_{n-1} · (1 + ⟨w_n, x⟩)
1_L(x) = a_n
```

Each step is a **degree-2 constraint** (quadratic in the variables).

---

## 4. Signature Scheme: LSN-SNARK

### 4.1 Parameters

| Symbol | Meaning | Typical Value |
|--------|---------|---------------|
| n | Security parameter (Lagrangian dimension) | 64 (128-bit) |
| p | Noise rate | 1/4 |
| m | Number of samples in pk | 1000–2000 |

### 4.2 KeyGen

```
L ← random Lagrangian in F_2^{2n}
{w_1, ..., w_n} ← basis of L^⊥
pk_hash ← Hash(w_1, ..., w_n)
pk_samples ← {(x_i, y_i)}_{i=1}^m where x_i ← Uniform(V), y_i = 1_L(x_i) ⊕ e_i
sk ← (w_1, ..., w_n)
pk ← (pk_hash, pk_samples)
```

**Public key size:** `|pk_hash| + m·(2n+1)` bits ≈ 256 + 2000·31 = **62,000 bits ≈ 8 KB**.

### 4.3 Sign

The signer constructs a ZK circuit proving:

```
I know w_1, ..., w_n such that:
  1. Hash(w_1, ..., w_n) = pk_hash
  2. For all i = 1..m:  y_i = ∏_{j=1}^n (1 + ⟨w_j, x_i⟩) ⊕ e_i
  3. HammingWeight(e_1, ..., e_m) ≤ m·p
```

The circuit uses `n` multiplicative steps per sample, giving `m·n` degree-2 constraints.

For `n=64, m=1000`: **64,000 constraints** — feasible for modern SNARKs.

**Signature:** `σ = SNARK.Prove(circuit, witness=(w_1,...,w_n, e_1,...,e_m))`

### 4.4 Verify

```
Verify(pk, M, σ):
  c ← Hash(pk, M)  // Fiat-Shamir challenge (binds message)
  Check SNARK.Verify(pk, c, σ)
```

**Verification:** Single SNARK verification (e.g., Groth16: 3 pairings ≈ 1.5ms).

---

## 5. Security Analysis

### 5.1 EUF-CMA Security

**Theorem 5.1** (Informal). The LSN-SNARK signature is EUF-CMA secure in the random oracle model, assuming:

1. **Knowledge soundness of SNARK:** A valid proof implies knowledge of witness.
2. **LSN hardness:** Recovering `L` from `pk_samples` requires `2^{Ω(n)}` queries.
3. **Collision resistance of Hash.**

*Proof sketch:* By SNARK knowledge soundness, a forgery implies knowledge of `w_1,...,w_n` satisfying the circuit. By circuit condition (1), these `w_j` hash to `pk_hash`. By circuit conditions (2)–(3), the samples are consistent with `L = (span{w_j})^⊥`. Thus the forger knows `L`. But by LSN hardness, finding `L` from `pk` is hard. Contradiction. ∎

### 5.2 Comparison with SBS

| Property | SBS (Broken) | LSN-SNARK (Proposed) |
|----------|--------------|----------------------|
| Secret leak | **Coordinates revealed** | **Zero-knowledge** |
| Key recovery | 2–8 signatures | Requires solving LSN |
| Signature size | Small (~KB) | SNARK-dependent (~200 bytes for Groth16) |
| Verification | Native (fast) | SNARK verifier (fast) |
| Hardness basis | IBP (irrelevant under CMA) | **LSN (SQ lower bound)** |

### 5.3 Advantages over SBS

1. **No coordinate leakage:** ZK proof reveals nothing about `L`.
2. **SQ lower bound foundation:** Based on K3 SQ lower bound, not heuristic IBP.
3. **Standard paradigm:** Uses well-understood SNARK + Fiat-Shamir structure.
4. **Flexible:** Any SNARK system can be plugged in (post-quantum SNARKs for quantum security).

---

## 6. Open Design Questions

1. **SNARK choice:** Groth16 (small proofs, trusted setup) vs STARKs (no trusted setup, larger proofs) vs post-quantum SNARKs.
2. **Noise rate:** Lower p → smaller circuits (fewer `e_i` variables) but harder LSN instance.
3. **Sample count m:** Larger m → stronger soundness but larger pk and circuit.
4. **Quantum security:** Current SNARKs are not post-quantum. Need lattice-based or hash-based SNARKs for full quantum resistance.

---

## 7. Next Steps

1. **Implement ZK circuit** for `1_L(x)` evaluation (Python prototype)
2. **Benchmark** with Groth16 or similar SNARK system
3. **Compare** signature size and verify time with existing PQC signatures (Dilithium, SPHINCS+)
4. **Analyze** post-quantum SNARK compatibility

---

*Design by Kimi, 2026-06-08.*
