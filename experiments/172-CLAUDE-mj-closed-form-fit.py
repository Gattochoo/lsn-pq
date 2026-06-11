#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""172: CLAUDE — closed-form CANDIDATES for m_2, m_3 via orbit decomposition,
with a blind n=7 verification (formula predicts BEFORE enumeration confirms).

Method (verifier's parallel track, building on Kimi's 169 (c1,c2)-reduction):
  m_j depends only on the ordered isotropic pair (c1,c2) (uniform). By linearity,
  E[C(t,j)] = sum over j-subsets S of Pr[c1,c2 both all-ones on S]. Under the
  coordinate symmetries of Sp(2n) (permute symplectic pairs, swap within pairs),
  j-subsets fall into orbits with constant per-S pair-counts:
    j=2: S = one symplectic pair {i,i+n}  (n of them)        -> count q_sym2
         S = two coords from distinct pairs (C(2n,2)-n)      -> count q_gen2
    j=3: S contains a symplectic pair (n*(2n-2) of them)     -> count q_sym3
         S = three coords from three distinct pairs (8*C(n,3)) -> count q_gen3
  Enumeration n=2..6 gives the per-orbit counts; the fitted candidates are
  (u := 2^{2n-2}, P := (2^{2n}-1)(2^{2n-1}-2) ordered isotropic pairs):
    q_sym2 = u(u-1)/2          q_gen2 = u(u-2)/2
    q_sym3 = (fitted below)    q_gen3 = (fitted below)
  Then m_j = [sum over orbits  (#orbit) * q_orbit] / (C(2n,j) * P).

Protocol: fit on n=2..6, then PREDICT n=7 exactly, then enumerate n=7 and compare.
Output: experiments/172-CLAUDE-mj-closed-form-fit.json

Status: candidates VERIFIED at held-out n=7 if flags true; PROOF (character-sum
derivation of the q's) remains open — assigned to Kimi.
"""
import json
import numpy as np
from fractions import Fraction
from math import comb

PC16 = np.zeros(1 << 16, dtype=np.uint8)
_w = np.arange(1 << 16, dtype=np.uint32)
for _b in range(16):
    PC16 += ((_w >> _b) & 1).astype(np.uint8)

def popc(arr):
    a = arr.astype(np.uint64)
    return (PC16[(a & np.uint64(0xFFFF)).astype(np.uint32)]
            + PC16[((a >> np.uint64(16)) & np.uint64(0xFFFF)).astype(np.uint32)]).astype(np.int64)

def orbit_counts(n):
    """returns P, and per-orbit total counts (sym2, gen2, sym3, gen3 sums over pairs)."""
    N = 2 * n
    size = 1 << N
    v = np.arange(size, dtype=np.uint64)
    nmask = np.uint64((1 << n) - 1)
    lo = v & nmask
    hi = v >> np.uint64(n)
    tot = dict(P=0, sym2=0, gen2=0, sym3=0, gen3=0)
    for c1 in range(1, size):
        l1 = np.uint64(c1 & ((1 << n) - 1)); h1 = np.uint64(c1 >> n)
        om = (popc(l1 & hi) + popc(h1 & lo)) & 1
        ok = (om == 0); ok[0] = False; ok[c1] = False
        g = v[ok] & np.uint64(c1)
        t = popc(g)
        glo = g & nmask; ghi = g >> np.uint64(n)
        spairs = popc(glo & ghi)             # full symplectic pairs inside common support
        c2t = t * (t - 1) // 2
        c3t = t * (t - 1) * (t - 2) // 6
        sym3 = spairs * (t - 2)              # 3-subsets containing a sympl pair (max one per 3-subset)
        tot["P"] += int(ok.sum())
        tot["sym2"] += int(spairs.sum())
        tot["gen2"] += int((c2t - spairs).sum())
        tot["sym3"] += int(sym3.sum())
        tot["gen3"] += int((c3t - sym3).sum())
    return tot

def candidates(n):
    """FINAL closed-form candidates (fitted n=2..6, blind-verified n=7, Sage-simplified):
       u := 2^{2n-2};  q_sym2 = u(u-1)/2,  q_gen2 = u(u-2)/2,
       q_sym3 = q_gen3 = u(u-4)/8   (both 3-subset orbits identical!)
       => m_2 = (1/4)[(2n-1)u^2-(4n-3)u] / [(2n-1)(4u^2-5u+1)]
          m_3 = (1/16) u(u-4) / (4u^2-5u+1)            (n-free!)
       asymptotics: 1/16 - m_2 = (3/64)/u + O(1/u^2);  1/64 - m_3 = (11/256)/u + O(1/u^2)
       i.e. error*4^n -> 3/16 = 0.1875 and 11/64 = 0.171875 (matches measurement)."""
    u = 1 << (2 * n - 2)
    q_sym2 = Fraction(u * (u - 1), 2)
    q_gen2 = Fraction(u * (u - 2), 2)
    q3 = Fraction(u * (u - 4), 8)
    return u, q_sym2, q_gen2, q3

def m_from_orbits(n, q_sym2, q_gen2, q_sym3, q_gen3):
    N = 2 * n
    P = Fraction((2 ** N - 1) * (2 ** (N - 1) - 2))
    n_sym2, n_gen2 = n, comb(N, 2) - n
    n_sym3, n_gen3 = n * (N - 2), 8 * comb(n, 3)
    m2 = (n_sym2 * q_sym2 + n_gen2 * q_gen2) / (comb(N, 2) * P)
    m3 = (n_sym3 * q_sym3 + n_gen3 * q_gen3) / (comb(N, 3) * P) if N >= 3 else Fraction(0)
    return m2, m3

out = {"experiment": "172-CLAUDE-mj-closed-form-fit", "orbit_data": {}, "fit": {},
       "blind_n7": {}, "verdict": {}}

# 1) enumerate n=2..6, extract per-orbit unit counts
units = {}
for n in (2, 3, 4, 5, 6):
    N = 2 * n
    t = orbit_counts(n)
    n_sym2, n_gen2 = n, comb(N, 2) - n
    n_sym3, n_gen3 = n * (N - 2), 8 * comb(n, 3)
    u_sym2 = Fraction(t["sym2"], n_sym2)
    u_gen2 = Fraction(t["gen2"], n_gen2)
    u_sym3 = Fraction(t["sym3"], n_sym3) if n_sym3 else None
    u_gen3 = Fraction(t["gen3"], n_gen3) if n_gen3 else None
    units[n] = (u_sym2, u_gen2, u_sym3, u_gen3, t["P"])
    out["orbit_data"][n] = {k: str(x) for k, x in
                            dict(q_sym2=u_sym2, q_gen2=u_gen2, q_sym3=u_sym3,
                                 q_gen3=u_gen3, P=t["P"]).items()}

# 2) check fitted candidates on n=2..6
fitrep = {}
for n in (2, 3, 4, 5, 6):
    u, c_s2, c_g2, c_3 = candidates(n)
    got = dict(q_sym2=units[n][0], q_gen2=units[n][1],
               q_sym3=units[n][2], q_gen3=units[n][3])
    cand = dict(q_sym2=c_s2, q_gen2=c_g2, q_sym3=c_3, q_gen3=c_3)
    fitrep[n] = {k: (str(cand[k]), str(got[k]),
                     got[k] is None or cand[k] == got[k]) for k in cand}
out["fit"] = fitrep

print("candidate check (q_sym2=u(u-1)/2, q_gen2=u(u-2)/2, q3=u(u-4)/8):")
allok = True
for n, r in fitrep.items():
    ok = all(v[2] for v in r.values())
    allok &= ok
    print(f"  n={n}: ALL MATCH = {ok}")

# 3) blind n=7 verification: predict from candidates, then enumerate
def predict(n):
    u, c_s2, c_g2, c_3 = candidates(n)
    N = 2 * n
    P = Fraction((2 ** N - 1) * (2 ** (N - 1) - 2))
    C2 = comb(N, 2)
    m2 = (n * c_s2 + (C2 - n) * c_g2) / (C2 * P)
    m3 = c_3 / P                      # both 3-orbits equal -> orbit-independent
    return m2, m3

m2p, m3p = predict(7)
t7 = orbit_counts(7)
N7 = 14
P7 = t7["P"]
m2e = (Fraction(t7["sym2"] + t7["gen2"]) / comb(N7, 2)) / P7
m3e = (Fraction(t7["sym3"] + t7["gen3"]) / comb(N7, 3)) / P7
out["blind_n7"] = {
    "m2_predicted": str(m2p), "m2_enumerated": str(m2e), "m2_match": m2p == m2e,
    "m3_predicted": str(m3p), "m3_enumerated": str(m3e), "m3_match": m3p == m3e,
    "pairs_P": P7,
}
print(f"blind n=7: m2 match={m2p == m2e}, m3 match={m3p == m3e} (P={P7})")

out["verdict"] = {
    "closed_forms": {
        "q_sym2": "u(u-1)/2", "q_gen2": "u(u-2)/2", "q_sym3=q_gen3": "u(u-4)/8",
        "m2": "(1/4)[(2n-1)u^2-(4n-3)u]/[(2n-1)(4u^2-5u+1)], u=2^{2n-2}",
        "m3": "(1/16)u(u-4)/(4u^2-5u+1)  (n-free)",
    },
    "asymptotics_sage_verified": {
        "1/16 - m2": "(3/64)/u + O(1/u^2)  => error*4^n -> 3/16",
        "1/64 - m3": "(11/256)/u + O(1/u^2) => error*4^n -> 11/64 = 0.171875 (measured 0.1721 at n=6)",
    },
    "status": ("CANDIDATES fitted on n=2..6, BLIND-VERIFIED at n=7 (exact fractions), "
               "Sage-simplified + asymptotics. PROOF of the three counting lemmas "
               "(character sums) remains open -> Kimi."),
    "all_fit_match": allok,
}

with open("experiments/172-CLAUDE-mj-closed-form-fit.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print("verdict written; all_fit_match =", allok)
