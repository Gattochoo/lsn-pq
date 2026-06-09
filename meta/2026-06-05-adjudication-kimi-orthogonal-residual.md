# Adjudication — Kimi's orthogonal-residual experiment → workstream B CLOSES (theorem)

> Kimi ran the JW-factoring test from the handoff (`kimi_experiment_orthogonal_residual.py`,
> `kimi_experiment_results.md`), found **CLOSES** for all tested O(2m,F₂) stabilizer
> structures, and — crucially — **did not over-claim a NEW CANDIDATE**, flagging the
> search as non-exhaustive and asking Claude for the theoretical argument. This note
> is the sign-off + that argument, which **elevates Kimi's empirical CLOSES to a
> theorem for the stabilizer class** and closes workstream B.

## Kimi's work: disciplined and genuine (sign-off)

- **Code is real**, not a fabricated pass: brute-forces `|O⁺(4,2)|=72`, `|O⁻(4,2)|=120`
  over all 2¹⁶ matrices (same method as our anchor), reuses our exact `jw_gamma` map,
  builds stabilizers and checks JW images form valid qubit codes. Verified.
- **Results match our anchor** and extend it: O⁻(4,2) elliptic = order 120, 6 singular
  vectors, **0** maximal totally-singular 2-spaces (Witt index 1 ⇒ max isotropic is
  dim 1 — correct).
- **CLOSES for all m=2..5, both ± forms**: every standard O(2m,F₂) stabilizer factors
  through JW to a valid qubit stabilizer code.
- **No over-claim.** Kimi explicitly refused "NEW CANDIDATE," listed honest limits, and
  handed back the completeness question. This is the Sound-Verifier discipline working —
  the opposite of the old "8/8 passed" pattern.

## The theoretical argument Kimi asked for (the completion)

**Theorem (standard).** Jordan–Wigner is a complete *-algebra isomorphism
`Cl(2m, ℂ) ≅ M_{2^m}(ℂ)` (the unique irreducible Clifford representation). Under it,
**every even-Majorana monomial ↦ a Pauli operator**, and **commutation is preserved**.

Consequences, each closing a leg Kimi left open:

1. **CLOSES is a theorem, not an m≤5 sample.** A fermionic *stabilizer* code = an abelian
   group of commuting even-Majorana monomials = an isotropic subspace under the Majorana
   form. The isomorphism sends it to commuting Paulis = a qubit stabilizer code. So **every
   fermionic stabilizer code factors through JW**, all m, both ± forms. Decoding it ≡ qubit
   stabilizer decoding = **LSN**. Empirical CLOSES (Kimi) ⇒ structural CLOSES.

2. **Part D necessarily found nothing — it searched for a contradiction.** Kimi looked for
   operators that *commute in O(2m,F₂) but anticommute as qubits*. The isomorphism makes
   that **impossible by construction** (it preserves commutators). So the null result is
   **guaranteed**, not a sampling limitation — *stronger* than Kimi's "limited search"
   caveat.

3. **Non-locality (Part E) is irrelevant to hardness.** JW images grow non-local
   (weight ~m/2), but the iso preserves the *algebraic* decoding problem (syndromes, error
   cosets). Non-locality changes the geometric/physical layout, **not** the abstract
   LSN-style decoding hardness. "Non-local but still factors" is correct and harmless.

4. **The "non-stabilizer residual" is not a new door — it is the already-walled census.**
   Kimi's remaining caveats (odd-length operators; interacting/non-Gaussian) resolve:
   - **odd-Majorana monomials** anticommute with fermion parity ⇒ **not physical
     stabilizers** (they cannot stabilize a code). Not a residual.
   - **non-stabilizer / interacting / non-Gaussian** = workstream-B census **routes 1**
     (free-fermion Gaussian → continuous learning → F-1 easy) and **4** (non-Gaussian →
     permanent #P computing + BQP-universal ⑤) — **already walled** in
     `…workstream-b-matchgate-screen.md`.

## Verdict: the orthogonal residual CLOSES → workstream B is definitively closed

```text
symplectic↔orthogonal F2 gap:
  stabilizer part      -> JW algebra-isomorphism theorem -> = LSN (CLOSES, all m)
  non-stabilizer part  -> census routes 1 (F-1) & 4 (#P/⑤) -> already walled
  => NO second band inhabitant.
```

Workstream B upgrades from "screen + named residual" (Result #3) to **closed**: the one
pre-screened door does not open. **LSN's uniqueness as the band's sole inhabitant is now
backed by a theorem for the stabilizer class plus the census for the rest** — not just a
screen. Joint credit: Kimi ran the disciplined experiment and asked the right question;
the JW-isomorphism completion answers it.

## Honest scope

The CLOSES is a theorem **for the fermionic-stabilizer class** (the only class that could
host a *discrete-decodable simulable* second inhabitant — VII §2). It is not a claim that
*no* exotic non-stabilizer quantum-native source exists anywhere; those fall to the census
walls (F-1 / #P / ⑤), which are screens, not theorems. Net: workstream B has done its job —
LSN remains the unique live frontier, and the companion search is closed.
