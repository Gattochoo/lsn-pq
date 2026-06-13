#!/usr/bin/env python3
"""
850-CLAUDE-symplectic-selfreduction-noise-probe.py

Opens the WORST-TO-AVERAGE self-reduction arc for LSN. The engine: Sp(2n,F_2)
acts transitively on Lagrangians, so g~Unif(Sp) maps the secret Lagrangian to a
uniform one (structure randomizes perfectly). The OBSTACLE: g distorts the
Bernoulli noise, ge !~ Bernoulli(p). This probe measures the distortion at n=2
and tests the structural facts that frame the whole approach.

Measured (n=2, Sp(4,F_2), |Sp|=720):
  (1) Sp transitive on F_2^{2n}\{0}? If yes, the ONLY Sp-invariant noise laws are
      weight-BLIND (alpha*delta_0 + (1-alpha)*uniform_{!=0}) -- Bernoulli(p) is
      weight-GRADED, so it is NOT Sp-invariant. Confirms the obstacle is structural.
  (2) SD(law(ge), Bernoulli(p)) over sampled g: histogram. Fraction with SD=0 =
      the weight-preserving (monomial) subgroup.
  (3) The full Sp-TWIRL E_g[law(ge)] -> the invariant law = (3/4)^{2n} delta_0 +
      (1-(3/4)^{2n}) uniform_{!=0}, which is ~uniform (signal destroyed). So you
      CANNOT twirl over all of Sp; a usable self-reduction needs an INTERMEDIATE
      subgroup H (monomial < H <= Sp) transitive-enough on Lagrangians yet noise-
      correctable. This probe quantifies the gap H must bridge.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from fractions import Fraction as Fr

n = 2
NN = 2 * n
P = Fr(1, 4)


def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def matvec(M, v):
    # M: list of NN column-ints (each col is an NN-bit vector); v: NN-bit
    out = 0
    for j in range(NN):
        if (v >> j) & 1:
            out ^= M[j]
    return out


def is_invertible(M):
    cols = list(M)
    basis = []
    for c in cols:
        x = c
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return len(basis) == NN


def is_symplectic(M):
    # columns m_0..m_{NN-1}; need omega(M e_i, M e_j) = omega(e_i,e_j)
    # i.e. omega(col_i, col_j) = omega(e_i,e_j) for all i<j
    for i in range(NN):
        for j in range(NN):
            if omega(M[i], M[j]) != omega(1 << i, 1 << j):
                return False
    return True


def sample_symplectic(rng, count):
    out = []
    tries = 0
    seen = set()
    while len(out) < count and tries < count * 400:
        tries += 1
        M = tuple(rng.randrange(1 << NN) for _ in range(NN))
        if M in seen:
            continue
        if is_invertible(M) and is_symplectic(M):
            seen.add(M)
            out.append(M)
    return out


def bernoulli_law():
    law = {}
    for e in range(1 << NN):
        w = P ** bin(e).count("1") * (1 - P) ** (NN - bin(e).count("1"))
        law[e] = w
    return law


def push(M, base):
    law = {}
    for e, w in base.items():
        ge = matvec(M, e)
        law[ge] = law.get(ge, Fr(0)) + w
    return law


def SD(p, q):
    keys = set(p) | set(q)
    return sum(abs(p.get(k, Fr(0)) - q.get(k, Fr(0))) for k in keys) / 2


def main():
    rng = random.Random(23)
    print("=" * 74)
    print("850-CLAUDE  symplectic self-reduction noise probe (n=2)")
    print("=" * 74)
    BERN = bernoulli_law()

    # (1) Sp transitivity on nonzero vectors
    G = sample_symplectic(rng, 700)
    print(f"  sampled {len(G)} distinct symplectic matrices (|Sp(4,2)|=720)")
    orbit = set()
    v0 = 1  # e_0
    for M in G:
        orbit.add(matvec(M, v0))
    nonzero = (1 << NN) - 1
    print(f"  orbit of e_0 under sampled Sp: {len(orbit)} of {nonzero} nonzero vectors"
          f"  => {'TRANSITIVE on nonzero (only weight-blind noise is Sp-invariant)' if len(orbit)==nonzero else 'not transitive (sample more)'}")

    # (2) SD(law(ge), Bernoulli) histogram
    sds = []
    preserve = 0
    for M in G:
        d = SD(push(M, BERN), BERN)
        sds.append(d)
        if d == 0:
            preserve += 1
    sds.sort()
    import statistics
    print(f"\n  SD(law(g.e), Bernoulli(1/4)) over {len(G)} g:")
    print(f"    min={float(sds[0]):.4f}  median={float(sds[len(sds)//2]):.4f}  "
          f"max={float(sds[-1]):.4f}")
    print(f"    #weight-preserving (SD=0, monomial subgroup): {preserve} / {len(G)}"
          f"  ({100*preserve/len(G):.1f}%)")

    # (3) full Sp-twirl -> invariant law
    twirl = {}
    for M in G:
        d = push(M, BERN)
        for k, w in d.items():
            twirl[k] = twirl.get(k, Fr(0)) + w
    s = sum(twirl.values())
    twirl = {k: w / s for k, w in twirl.items()}
    # invariant law prediction: (3/4)^{2n} delta_0 + rest uniform on nonzero
    a = (Fr(3, 4)) ** NN
    inv = {0: a}
    for v in range(1, 1 << NN):
        inv[v] = (1 - a) / nonzero
    unif = {v: Fr(1, 1 << NN) for v in range(1 << NN)}
    print(f"\n  Sp-twirl E_g[law(g.e)]:")
    print(f"    SD(twirl, predicted invariant [(3/4)^4 d_0 + unif_!=0]) = {float(SD(twirl, inv)):.4f}")
    print(f"    SD(twirl, Bernoulli) = {float(SD(twirl, BERN)):.4f}  "
          f"(signal vs Bernoulli)")
    print(f"    SD(twirl, full-uniform) = {float(SD(twirl, unif)):.4f}  "
          f"=> twirl is ~weight-blind (P[0]={float(a):.3f}); full twirl destroys signal")

    print("\n  STRUCTURAL READ:")
    print("  - Sp transitive on nonzero => no weight-graded Sp-invariant noise =>")
    print("    Bernoulli is not Sp-invariant; full Sp-twirl -> weight-blind ~uniform")
    print("    (useless). So NO full-Sp self-reduction preserving usable noise.")
    print("  - Monomial (weight-preserving) subgroup is small and NOT transitive on")
    print("    Lagrangians. The self-reduction needs an INTERMEDIATE H, OR a noise-")
    print("    CORRECTION (convert D_g back to Bernoulli(p')), OR LSN robustness to")
    print("    the orbit {D_g}. That trilemma is the worst-to-avg crux (-> Gemini).")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
