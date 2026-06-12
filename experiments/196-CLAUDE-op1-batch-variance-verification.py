#!/usr/bin/env python3
"""
196-CLAUDE-op1-batch-variance-verification.py

Independent adjudication of Kimi's maximal-block variance multiplier
(meta/2026-06-14-KIMI-op1-batch-variance-theta-n.md, experiments/195).

CLAIM (Kimi boxed): with X = 4^n, sigma^2 = 4/3 (p = 1/4),

    V_{2n} = sum_{j=0}^{2n} C(2n,j) sigma^{2j} m_j
           = [X^4 - 2X*25^n + X*13^n - 4X*9^n + 4*9^n] / [9^n (X-1)(X-4)],

with V_iid = (16/9)^n and relative deviation -2(25/64)^n + O(4^{-n}).

Independent checks here (all exact rational arithmetic):

  (1) DEFINITION-LEVEL: for n = 2,3,4 compute m_j by exhaustive enumeration
      of ordered isotropic pairs (NO closed forms anywhere), form
      V = sum C(2n,j)(4/3)^j m_j, and compare to the boxed formula exactly.
  (2) CLOSED-FORM SUM: for n = 2..14 compare the boxed formula against the
      direct sum using the (already independently verified, exp/194) m_j
      closed form. Exact equality required.
  (3) DERIVATION CROSS-CHECK: my own binomial-sum decomposition
        V_{2n} = 1 + [ (X^2/2)((16/9)^n - 1) - X((25/9)^n - 1)
                       + (X/2)((13/9)^n - 1) ] / P,    P = (X-1)(X-4)/2,
      obtained by splitting the moment numerator into its two orbit parts
      and summing C(2n,j)(s/4)^j, C(2n,j)(s/2)^j, C(n,i)(s^2/4)^i.
      Must equal the boxed formula exactly for n = 2..14.
  (4) ASYMPTOTICS: rel_dev / (-2(25/64)^n) -> 1; five-term leading
      approximation error at n = 12 ~ 7.4e-9 (Kimi's figure); absolute
      deviation peaks near n = 4.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from math import comb


# ---------- definition-level machinery (same approach as exp/194) ----------

def symplectic_pairs(n):
    N = 2 * n
    full = 1 << N

    def omega(a, b):
        s = 0
        for i in range(n):
            s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
                 (((a >> (i + n)) & 1) & ((b >> i) & 1))
        return s

    return [(c1, c2)
            for c1 in range(1, full)
            for c2 in range(1, full)
            if c1 != c2 and omega(c1, c2) == 0]


def m_all_from_definition(n):
    N = 2 * n
    pairs = symplectic_pairs(n)
    P = len(pairs)
    hist = [0] * (N + 1)
    for c1, c2 in pairs:
        hist[bin(c1 & c2).count("1")] += 1
    m = {0: Fraction(1)}
    for j in range(1, N + 1):
        num = sum(hist[t] * comb(t, j) for t in range(j, N + 1))
        m[j] = Fraction(num, P * comb(N, j))
    return m


# ---------- verified m_j closed form (exp/194) ----------

def m_j_closed(n, j):
    if j == 0:
        return Fraction(1)
    N = 2 * n
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    Dj = 2 ** (N - j)
    C = comb(N, j)
    num = C * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return num / (C * P)


# ---------- the three formulas under test ----------

S2 = Fraction(4, 3)  # sigma^2 at p = 1/4


def V_sum(n, m):
    """Direct sum  V_{2n} = sum_j C(2n,j) s^j m_j  from a moment table."""
    return sum(comb(2 * n, j) * S2 ** j * m[j] for j in range(0, 2 * n + 1))


def V_boxed(n):
    """Kimi's boxed closed form."""
    X = 4 ** n
    num = (X ** 4 - 2 * X * 25 ** n + X * 13 ** n
           - 4 * X * 9 ** n + 4 * 9 ** n)
    den = 9 ** n * (X - 1) * (X - 4)
    return Fraction(num, den)


def V_derivation(n):
    """My independent binomial-sum decomposition (check (3))."""
    X = 4 ** n
    P = Fraction((X - 1) * (X - 4), 2)
    t16 = Fraction(16 ** n, 9 ** n)   # (1+s/4)^{2n}
    t25 = Fraction(25 ** n, 9 ** n)   # (1+s/2)^{2n}
    t13 = Fraction(13 ** n, 9 ** n)   # (1+s^2/4)^n
    A = Fraction(X * X, 2) * (t16 - 1) - X * (t25 - 1)
    B = Fraction(X, 2) * (t13 - 1)
    return 1 + (A + B) / P


def main():
    ok = True
    print("=" * 76)
    print("196-CLAUDE  maximal-block variance multiplier V_{2n} — independent check")
    print("=" * 76)

    # (1) definition-level, no closed forms anywhere
    print("\n(1) definition-enumeration vs boxed formula (exact):")
    for n in (2, 3, 4):
        m_def = m_all_from_definition(n)
        v_def, v_box = V_sum(n, m_def), V_boxed(n)
        match = v_def == v_box
        ok &= match
        print(f"   n={n}:  V_def = {v_def}  "
              f"{'== boxed OK' if match else '*** MISMATCH vs ' + str(v_box)}")

    # (2)+(3) closed-form sum and my derivation, n = 2..14
    print("\n(2)(3) boxed vs direct closed-form sum vs my derivation, n=2..14:")
    for n in range(2, 15):
        m_cf = {j: m_j_closed(n, j) for j in range(0, 2 * n + 1)}
        v_sum, v_box, v_der = V_sum(n, m_cf), V_boxed(n), V_derivation(n)
        match = (v_sum == v_box == v_der)
        ok &= match
        print(f"   n={n:>2}:  {'sum == boxed == derivation OK' if match else '*** MISMATCH ***'}"
              f"   V = {float(v_box):.12f}")

    # (4) asymptotics
    print("\n(4) asymptotics:")
    print("   rel_dev / (-2*(25/64)^n)  (should -> 1):")
    for n in (4, 8, 12, 14):
        v, vi = V_boxed(n), Fraction(16 ** n, 9 ** n)
        rel = (v - vi) / vi
        lead = -2 * Fraction(25 ** n, 64 ** n)
        print(f"     n={n:>2}: ratio = {float(rel / lead):.6f}")
    # five-term approximation error at n=12
    n = 12
    approx = ((Fraction(16, 9)) ** n - 2 * (Fraction(25, 36)) ** n
              + 5 * (Fraction(4, 9)) ** n + (Fraction(13, 36)) ** n
              - 4 * (Fraction(1, 4)) ** n)
    err = abs(float(V_boxed(n) - approx))
    print(f"   five-term approx error at n=12: {err:.3e}  (Kimi: 7.4e-9)")
    ok &= 5e-9 < err < 1e-8
    # absolute-deviation peak near n=4
    absdev = {n: abs(float(V_boxed(n) - Fraction(16 ** n, 9 ** n)))
              for n in range(2, 9)}
    peak = max(absdev, key=absdev.get)
    print(f"   |V - V_iid| peak at n = {peak}  (claim: near 4): "
          f"{ {k: round(v,4) for k, v in absdev.items()} }")
    ok &= peak == 4

    # interpretation guard: individual moments near j = 2n are NOT close in
    # relative terms (m_j = 0 for j >= 2n-1 while (1/4)^j > 0) — V_{2n} is one
    # functional, not a closure of the whole j = Theta(n) distributional regime.
    print("\n(guard) m_j relative deviation at j near 2n (n=6):")
    n = 6
    for j in (2 * n - 3, 2 * n - 2, 2 * n - 1):
        mj = m_j_closed(n, j)
        rel = float(mj * 4 ** j - 1)
        print(f"     j={j:>2}: m_j*4^j - 1 = {rel:+.4f}"
              f"{'  (vanishes entirely)' if mj == 0 else ''}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — boxed V_{2n} formula ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
