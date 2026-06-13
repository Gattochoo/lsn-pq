#!/usr/bin/env python3
"""
344-CLAUDE-trackP-general-k-light.py

Light, independent adjudication of Kimi Track P (2715452).

NOTE: my own general-k closed-form reimplementation in 342 had a bug (it
disagreed with my already-verified k=3 code in 263). Rather than ship my buggy
code, this adjudication rests on:
  - the general-k CONSTRUCTION verified independently at the only enumerable
    non-degenerate orders: k=2 (exp/258, integrated as thm:joint-gf) and
    k=3 (exp/263, integrated as thm:triple-gf);
  - the count law P_k and Mobius pattern verified here;
  - the t_1k benchmark computed by DIRECT ENUMERATION (not the buggy GF);
  - Kimi's k=4 marginal-consistency reproduced by re-running her 310/311.

Checks:
  (1) P_k(n) = prod_{i=0}^{k-1}(2^{2n-i}-2^i): enum vs formula (k=2,3; n=2,3),
      degeneracy k>n, P_4(4)=46,267,200.
  (2) Mobius mu_c = (-1)^c 2^{C(c,2)}: (1,-1),(1,-1,2,-8),(1,-1,2,-8,64).
      [my earlier hand-value 128 was wrong: C(4,2)=6, 2^6=64.]
  (3) t_1k law by direct enumeration; exact TV to Bin(2n, 2^{-k}) (the CORRECT
      benchmark — the directive's 4^{-k} was wrong, as Kimi flagged) ==
      Kimi's published TVs at (2,2),(3,2),(3,3).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from math import comb

src = open("experiments/342-CLAUDE-trackP-general-k-verification.py").read()
ns = {}
exec(src.split("def main()")[0], ns)
Pk, enum_count, enum_law = ns["Pk"], ns["enum_count"], ns["enum_law"]


def main():
    ok = True
    print("=" * 72)
    print("344-CLAUDE  Track P (light) — P_k, Mobius, t_1k benchmark")
    print("=" * 72)

    print("\n(1) P_k(n) formula vs enumeration:")
    for n, k in ((2, 2), (2, 3), (3, 2), (3, 3)):
        f, e = Pk(n, k), enum_count(n, k)
        ok &= f == e
        print(f"   n={n} k={k}: {f} == {e} {'OK' if f == e else 'FAIL'}", flush=True)
    ok &= Pk(2, 3) == 0 and Pk(3, 4) == 0 and Pk(4, 4) == 46267200
    print(f"   P_4(4)={Pk(4,4)} (=46,267,200); degeneracy k>n: P_3(2)={Pk(2,3)}, "
          f"P_4(3)={Pk(3,4)} {'OK' if Pk(2,3)==0 and Pk(3,4)==0 else 'FAIL'}")

    print("\n(2) Mobius mu_c = (-1)^c 2^{C(c,2)} (corrected: mu_4 = 64, not 128):")
    for k in (2, 3, 4):
        print(f"   k={k}: {[(-1)**c * 2**comb(c,2) for c in range(k+1)]}")
    ok &= [(-1)**c * 2**comb(c, 2) for c in range(5)] == [1, -1, 2, -8, 64]

    print("\n(3) t_1k law (direct enum) -> TV to Bin(2n, 2^{-k}):")
    kimi_tv = {(2, 2): "707/5760", (3, 2): "35183/645120",
               (3, 3): "1096511/27525120"}
    for n, k in ((2, 2), (3, 2), (3, 3)):
        law_dict = enum_law(n, k)        # {composition: prob}, pure enumeration
        N = 2 * n
        allone = (1 << k) - 1
        law = [Fraction(0)] * (N + 1)
        for comp, v in law_dict.items():
            law[comp[allone]] += v
        assert sum(law) == 1
        pq = Fraction(1, 2 ** k)
        ref = [comb(N, l) * pq ** l * (1 - pq) ** (N - l) for l in range(N + 1)]
        tv = sum(abs(a - b) for a, b in zip(law, ref)) / 2
        m = tv == Fraction(kimi_tv[(n, k)])
        ok &= m
        print(f"   n={n} k={k}: TV={tv}={float(tv):.6f} "
              f"{'OK (= Kimi)' if m else 'FAIL vs ' + kimi_tv[(n,k)]}", flush=True)

    print("\n   (k=2 GF = thm:joint-gf verified in exp/258; "
          "k=3 GF = thm:triple-gf in exp/263;")
    print("    k=4 marginal-consistency = Kimi 310 reproduction, separate run.)")

    print("\n" + "=" * 72)
    print("RESULT:", "PASS — P_k + Mobius + benchmark ACCEPT; general-k construction"
          "\n         verified at k=2,3 (258/263); k=4 via Kimi 310" if ok
          else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
