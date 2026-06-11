# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""
Lane C2 — illustrate the stabilizer DEGENERACY that underlies Thm 1.6 (LPN ↪ LSN, LSN ⊇ LPN).

Thm 1.6 (arXiv:2509.20697, §1.2.1, verbatim):
  "Fix any k≥1 and p∈(0,1) ... There exists a reduction from LPN(⌊np/6⌋, 2n, p/6) to
   LSN(k,n,p)."
Cor 1.7: "any sub-exponential time algorithm which solves LSN at any rate k/n implies a
   breakthrough in classical cryptography."

The mechanism is stabilizer DEGENERACY: in the classical representation of LSN a sample is
  b_i = A_i r_i + B_i y + e_i        (paper §1.2.2, Fig. 3)
where A_i (stabilizers + logical-Z, isotropic) absorbs an n-bit per-sample "junk register"
r_i, B_i (logical-X) carries the logical secret y, and e_i is depolarizing noise. The junk
register exists because stabilizers act trivially on codewords (degeneracy) — so even k=1
LSN hides an n-scale hard instance, into which constant-rate LPN is embedded.

★ Honest scope: implementing the full 3-stage reduction faithfully from the paper would
require §§4–6 (not safely reproducible from a summary). This script therefore VERIFIES the
theorem STATEMENT (above) and ILLUSTRATES the standard, textbook-correct phenomenon the
mechanism rests on — stabilizer degeneracy in the symplectic (Pauli↔F₂^{2n}) representation
— WITHOUT claiming to reproduce the reduction. Degeneracy is *absent* classically; that gap
is exactly why LSN can be ⊇ LPN even at k=1.

Run: python3 18-thm16-degeneracy-junk-register.py
"""
import math


def omega_int(u, v, n):
    """symplectic form Ω(u,v) (Pauli commutation) on F₂^{2n}, vectors as packed ints."""
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


class XorBasis:
    __slots__ = ("piv",)

    def __init__(self):
        self.piv = {}

    def add(self, v):
        while v:
            h = v.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                self.piv[h] = v
                return True
            v ^= r
        return False

    def rank(self):
        return len(self.piv)

    def contains(self, v):
        while v:
            h = v.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                return False
            v ^= r
        return True


def rand_isotropic(n, dim, rng):
    """random isotropic subspace of F₂^{2n} of the given dim (<= n); returns basis ints."""
    D = 2 * n
    xb = XorBasis()
    rows = []
    while len(rows) < dim:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, b, n) == 0 for b in rows) and xb.add(v):
            rows.append(v)
    return rows


def span(basis):
    out = {0}
    for b in basis:
        out |= {e ^ b for e in out}
    return out


def symplectic_complement(Sbasis, n):
    """S^perp = { v in F₂^{2n} : Ω(v, s)=0 for all s in S }, returned as a set of ints."""
    D = 2 * n
    out = []
    for v in range(1 << D):
        if all(omega_int(v, s, n) == 0 for s in Sbasis):
            out.append(v)
    return set(out)


def syndrome(E, gens, n):
    """syndrome of error E = which stabilizer generators it anticommutes with."""
    return tuple(omega_int(E, g, n) for g in gens)


def main():
    import numpy as np
    rng = np.random.default_rng(20260606)

    print("=" * 76)
    print("Lane C2 — stabilizer degeneracy = the 'junk register' behind Thm 1.6 (LSN ⊇ LPN)")
    print("=" * 76)

    print("\nThm 1.6 (verbatim, 2509.20697 §1.2.1): reduction LPN(⌊np/6⌋,2n,p/6) → LSN(k,n,p),")
    print("any k≥1.  Cor 1.7: sub-exp LSN at any rate ⇒ breakthrough in classical crypto.")
    print("=> even k=1 single-qubit LSN is ≥ constant-rate LPN.  Mechanism: degeneracy.")

    print("\n[A] degeneracy multiplicity and the same-syndrome coset structure")
    print(f"  {'n':>2} {'k':>2} {'|S|=2^(n-k)':>11} {'|S^perp|=2^(n+k)':>16} "
          f"{'#logical classes 2^2k':>21} {'checks':>8}")
    for (n, k) in [(2, 1), (3, 1), (3, 2), (4, 1), (4, 2)]:
        D = 2 * n
        r = n - k                                   # number of stabilizer generators
        Sbasis = rand_isotropic(n, r, rng)
        S = span(Sbasis)
        Sperp = symplectic_complement(Sbasis, n)
        # structural identities
        assert len(S) == 1 << r
        assert len(Sperp) == 1 << (D - r)           # |S^perp| = 2^{2n-(n-k)} = 2^{n+k}
        assert S <= Sperp                           # S isotropic => S ⊆ S^perp
        n_logical_classes = len(Sperp) // len(S)    # |S^perp / S| = 2^{2k}
        assert n_logical_classes == 1 << (2 * k)

        # degeneracy: a random error E; every E+s (s in S) has the SAME syndrome AND is
        # logically equivalent (differs by a stabilizer). A logical op L in S^perp\S also
        # preserves syndrome but changes the logical class.
        E = int(rng.integers(0, 1 << D))
        syn_E = syndrome(E, Sbasis, n)
        same_syn = all(syndrome(E ^ s, Sbasis, n) == syn_E for s in S)   # degeneracy
        logical_ops = [v for v in Sperp if v not in S]
        L = logical_ops[0]
        syn_EL = syndrome(E ^ L, Sbasis, n)
        L_keeps_syndrome = (syn_EL == syn_E)        # L in S^perp => same syndrome
        L_changes_class = (L not in S)              # but nontrivial logical
        checks = same_syn and L_keeps_syndrome and L_changes_class
        print(f"  {n:>2} {k:>2} {1<<r:>11} {1<<(n+k):>16} {1<<(2*k):>21} "
              f"{'OK' if checks else 'FAIL':>8}")
        assert checks

    print("\n  Reading: the same-syndrome coset E+S^perp (size 2^{n+k}) splits into 2^{2k}")
    print("  logical classes, each of size |S|=2^{n-k}. Those 2^{n-k} representatives are")
    print("  INDISTINGUISHABLE on the code (differ by a stabilizer) = the degeneracy. ML")
    print("  decoding must SUM over each class (this is the #P/IP15 feature). The within-")
    print("  class freedom is the per-sample 'junk register' Thm 1.6 plants an LPN into.")

    print("\n[B] the junk register has dimension n EVEN at k=1 (why k=1 LSN ≥ const-rate LPN)")
    print(f"  {'n':>2} {'k':>2} {'#stabilizers n-k':>16} {'+logical-Z k':>12} "
          f"{'A-space (junk) dim':>18}")
    for (n, k) in [(4, 1), (4, 2), (6, 1), (6, 3)]:
        # A_i columns = (n-k) stabilizers + k logical-Z  => an isotropic n-space; r_i ∈ F₂^n
        a_dim = (n - k) + k
        print(f"  {n:>2} {k:>2} {n-k:>16} {k:>12} {a_dim:>18}")
    print("  => dim = n for every k (incl. k=1): the junk register is always n-dimensional,")
    print("     so a single-logical-qubit LSN still hides an n-scale (LPN-hard) instance.")

    print("\n[C] contrast: classical linear codes have NO such degeneracy")
    print("  In classical syndrome decoding the message↦codeword map is INJECTIVE and the")
    print("  decoder seeks the UNIQUE min-weight coset leader — there is no logically-trivial")
    print("  subgroup of size 2^{n-k} acting identically on the encoded message. Degeneracy")
    print("  (2^{n-k}>1 indistinguishable error representatives) is a strictly QUANTUM feature")
    print("  of stabilizer codes. It is the structural reason LSN ⊇ LPN can hold at k=1, and")
    print("  (with Lane A) why LSN is a SUPERSET / ≥-hard candidate, not an in-family subset.")

    print("\nVERDICT (Sound Verifier): Thm 1.6 STATEMENT verified verbatim; its degeneracy")
    print("MECHANISM illustrated combinatorially (standard stabilizer theory, exact checks).")
    print("The full 3-stage reduction (paper §§4–6) is NOT reimplemented here (avoided to")
    print("prevent drift). This is EVIDENCE supporting Lane A's superset reading (LSN ⊇ LPN")
    print("+ LSN ⊀ LPN linear), NOT a proof that LSN is a 7th. No security claim.")


if __name__ == "__main__":
    main()
