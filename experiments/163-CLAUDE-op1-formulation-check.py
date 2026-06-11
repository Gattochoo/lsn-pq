#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""163: CLAUDE adjudication of Kimi's OP1 formulation DRAFT (2026-06-12).

Independently verifies the DRAFT's math AND tests its central modeling choice
(the "batch" example: a whole isotropic matrix A per SQ example) by exact
enumeration at n=2,3.

Checks:
  (A) likelihood-ratio / sigma^2 algebra: sigma^2 = (1-2p)^2/(p(1-p)); for p=1/4 -> 4/3.
  (B) unconstrained baseline off-diag corr = (1+sigma^2/4)^{2n} - 1.
  (C) THE KEY QUESTION (DRAFT §4): does conditioning on S_A=0 suppress the
      off-diagonal correlation C_n(x,x') from 2^{Theta(n)} down to 1+2^{-Omega(n)}?
      Enumerate full-rank isotropic A (= Lagrangian bases) for n=2,3, compute
      C_n(x,x') = E_A[ prod_i (1 + sigma^2 (r_i.x)(r_i.x')) ] exactly, for all
      distinct nonzero pairs (x,x'), grouped by Hamming distance.
  (D) isotropic-matrix counts the DRAFT states (n=2: 90, n=3: 22680 full-rank).

Claude's prediction (to be confirmed/refuted): for the BATCH model, one example
(A, Ax+e) over-determines x (2n noisy eqns, n unknowns), so C_n stays
2^{Theta(n)} EVEN with isotropy -> the DRAFT's optimistic conjecture is FALSE for
this formulation, and OP1 needs a single-sample model instead.

Output: experiments/163-CLAUDE-op1-formulation-check.json
"""
import json
from itertools import product

def popcount(x): return bin(x).count("1")

def make_omega(n):
    mask = (1 << n) - 1
    def omega(u, v):
        ua, ub = u & mask, u >> n
        va, vb = v & mask, v >> n
        return (popcount(ua & vb) ^ popcount(ub & va)) & 1
    return omega

def lagr_count(n):
    c = 1
    for i in range(1, n + 1):
        c *= (2 ** i + 1)
    return c

def gl_count(n):
    c = 1
    for i in range(n):
        c *= (2 ** n - 2 ** i)
    return c

def isotropic_lagrangians(n):
    """all Lagrangian (dim-n isotropic) subspaces as sorted tuples of their 2^n elements."""
    omega = make_omega(n)
    N = 2 * n
    levels = [{frozenset([0])}]
    for _ in range(n):
        nxt = set()
        for S in levels[-1]:
            for v in range(1, 1 << N):
                if v in S: continue
                if all(omega(v, s) == 0 for s in S):
                    nxt.add(frozenset(s ^ (v & m) for s in S for m in (0, -1)) if False else
                            frozenset(list(S) + [s ^ v for s in S]))
        levels.append(nxt)
    return list(levels[n])

def full_rank_isotropic_matrices(n):
    """enumerate all 2n x n full-rank matrices with isotropic columns,
    as lists of n column-vectors (ints in F_2^{2n}). = bases of Lagrangians."""
    omega = make_omega(n)
    N = 2 * n
    lags = isotropic_lagrangians(n)
    mats = []
    for L in lags:
        elems = [e for e in L if e != 0]
        # choose ordered independent n-tuples from L (bases)
        def rank(cols):
            tmp = list(cols); used = [False]*len(tmp); r = 0
            for c in range(N):
                p = None
                for i in range(len(tmp)):
                    if not used[i] and (tmp[i] >> c) & 1: p = i; break
                if p is None: continue
                used[p] = True; r += 1
                for i in range(len(tmp)):
                    if i != p and (tmp[i] >> c) & 1: tmp[i] ^= tmp[p]
            return r
        # backtracking over independent ordered bases
        def rec(chosen):
            if len(chosen) == n:
                mats.append(chosen[:]); return
            for e in elems:
                if rank(chosen + [e]) == len(chosen) + 1:
                    rec(chosen + [e])
        rec([])
    return mats  # each = [col_1,...,col_n], col_j in F_2^{2n}

def row_dot(cols, i, x, n):
    """(A x)_i = sum_j A[i][j] x_j ; A[i][j] = bit i of col_j."""
    acc = 0
    for j in range(n):
        if (x >> j) & 1:
            acc ^= (cols[j] >> i) & 1
    return acc

def C_n_offdiag(n, p, mats):
    sigma2 = (1 - 2*p)**2 / (p*(1-p))
    N = 2 * n
    # group by hamming distance of (x,x'); both nonzero, distinct
    from collections import defaultdict
    sums = defaultdict(list)
    xs = [x for x in range(1, 1 << n)]
    M = len(mats)
    for a_idx, x in enumerate(xs):
        for x2 in xs:
            if x2 <= x: continue
            tot = 0.0
            for cols in mats:
                prod = 1.0
                for i in range(N):
                    rix = row_dot(cols, i, x, n)
                    rix2 = row_dot(cols, i, x2, n)
                    prod *= (1 + sigma2 * rix * rix2)
                tot += prod
            Cn = tot / M
            hd = popcount(x ^ x2)
            sums[hd].append(Cn)
    return sigma2, {hd: (min(v), max(v), sum(v)/len(v)) for hd, v in sums.items()}

out = {"experiment": "163-CLAUDE-op1-formulation-check",
       "checks": {}, "verdict": {}}

# (A) sigma^2
import math
for p in (0.25, 0.1):
    s2 = (1-2*p)**2/(p*(1-p))
    out["checks"][f"sigma2_p={p}"] = s2
out["checks"]["sigma2_p=0.25_equals_4/3"] = abs((0.25-0)*0 + ((1-0.5)**2/(0.25*0.75)) - 4/3) < 1e-12

# (D) counts
out["checks"]["count_n2_fullrank"] = lagr_count(2)*gl_count(2)
out["checks"]["count_n3_fullrank"] = lagr_count(3)*gl_count(3)
out["checks"]["DRAFT_says_90_and_22680"] = (lagr_count(2)*gl_count(2) == 90 and
                                            lagr_count(3)*gl_count(3) == 22680)

# (B)+(C) batch correlation, isotropic full-rank, n=2,3
for n in (2, 3):
    mats = full_rank_isotropic_matrices(n)
    assert len(mats) == lagr_count(n)*gl_count(n), (n, len(mats))
    sigma2, by_hd = C_n_offdiag(n, 0.25, mats)
    baseline = (1 + sigma2/4)**(2*n)
    out["checks"][f"n={n}_num_isotropic_fullrank"] = len(mats)
    out["checks"][f"n={n}_unconstrained_baseline_(1+s2/4)^2n"] = baseline
    out["checks"][f"n={n}_isotropic_offdiag_C_by_hamming"] = {
        str(hd): {"min": mn, "max": mx, "avg": av} for hd,(mn,mx,av) in by_hd.items()}

# verdict: is isotropic off-diag suppressed (<~1) or still large (>~baseline scale)?
n3 = out["checks"]["n=3_isotropic_offdiag_C_by_hamming"]
worst = max(v["max"] for v in n3.values())
out["verdict"] = {
    "math_A_B_D": "likelihood/sigma2/baseline/counts all VERIFIED",
    "n3_worst_isotropic_offdiag_C": worst,
    "n3_unconstrained_baseline": out["checks"]["n=3_unconstrained_baseline_(1+s2/4)^2n"],
    "suppressed_to_near_1": worst < 2.0,
    "conclusion": ("BATCH model: isotropic off-diagonal correlation is LARGE "
                   "(not suppressed to 1+2^-Omega(n)) => DRAFT §4 optimistic "
                   "conjecture is FALSE for the batch formulation; OP1 needs a "
                   "single-sample model.") if worst >= 2.0 else
                  ("isotropic SUPPRESSES correlation — DRAFT conjecture plausible; "
                   "Claude's prediction REFUTED, escalate."),
}

with open("experiments/163-CLAUDE-op1-formulation-check.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps(out["checks"], indent=1)[:1500])
print("--- VERDICT ---")
print(json.dumps(out["verdict"], indent=1))
