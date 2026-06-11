#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""165: CLAUDE adjudication of Kimi's OP1 single-sample DRAFT (2026-06-12).

Tests the load-bearing §5 conjecture: is the row-marginal mu_row of the uniform
full-rank isotropic ensemble A_n uniform over nonzero F_2^n? If yes, the single-
sample model is IDENTICAL to standard LPN (c_mu(x,x')=1/4), so conditioning on
S_A=0 does NOT reduce statistical dimension via this model -> OP1 answered for
the single-row model (but "too weak" per §4).

Also verifies §3 single-sample correlation formula <D_x,D_x'> = sigma^2 * c_mu,
unconstrained c_mu = 1/4, and the diagonal P(<a,x>=1).

Method: full enumeration of A_n = {full-rank 2n x n isotropic matrices} =
bases of Lagrangians, for n=2,3. Tabulate exact mu_row(v) for every v in F_2^n,
and c_mu(x,x') for all distinct nonzero pairs grouped by Hamming distance.

Output: experiments/165-CLAUDE-op1-rowmarginal-check.json
"""
import json
from collections import defaultdict

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
    for i in range(1, n + 1): c *= (2 ** i + 1)
    return c

def gl_count(n):
    c = 1
    for i in range(n): c *= (2 ** n - 2 ** i)
    return c

def isotropic_lagrangians(n):
    omega = make_omega(n); N = 2 * n
    levels = [{frozenset([0])}]
    for _ in range(n):
        nxt = set()
        for S in levels[-1]:
            for v in range(1, 1 << N):
                if v in S: continue
                if all(omega(v, s) == 0 for s in S):
                    nxt.add(frozenset(list(S) + [s ^ v for s in S]))
        levels.append(nxt)
    return list(levels[n])

def rank(cols, N):
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

def all_bases(n):
    """all full-rank isotropic matrices as [col_1..col_n], col in F_2^{2n}."""
    N = 2 * n
    mats = []
    for L in isotropic_lagrangians(n):
        elems = [e for e in L if e != 0]
        def rec(ch):
            if len(ch) == n: mats.append(ch[:]); return
            for e in elems:
                if rank(ch + [e], N) == len(ch) + 1: rec(ch + [e])
        rec([])
    return mats

def rows_of(cols, n):
    """row i (i in 0..2n-1) as vector in F_2^n: bit j = bit i of col_j."""
    N = 2 * n
    return [sum(((cols[j] >> i) & 1) << j for j in range(n)) for i in range(N)]

out = {"experiment": "165-CLAUDE-op1-rowmarginal-check", "results": {}, "verdict": {}}

for n in (2, 3):
    N = 2 * n
    mats = all_bases(n)
    assert len(mats) == lagr_count(n)*gl_count(n), (n, len(mats))
    # mu_row(v)
    rowcount = defaultdict(int); total = 0
    for cols in mats:
        for v in rows_of(cols, n):
            rowcount[v] += 1; total += 1
    mu = {v: rowcount.get(v, 0)/total for v in range(1 << n)}
    nonzero_vals = [mu[v] for v in range(1, 1 << n)]
    uniform_nonzero = 1.0/((1 << n) - 1)
    is_uniform_nonzero = all(abs(mu[v] - uniform_nonzero) < 1e-12 for v in range(1, 1 << n))
    # c_mu(x,x') = E_a[(a.x)(a.x')] over a~mu_row
    def dot(a, x): return popcount(a & x) & 1
    by_hd = defaultdict(list)
    for x in range(1, 1 << n):
        for x2 in range(x+1, 1 << n):
            cval = sum(mu[a]*dot(a, x)*dot(a, x2) for a in range(1 << n))
            by_hd[popcount(x ^ x2)].append(cval)
    # diagonal P(<a,x>=1)
    diag = {x: sum(mu[a]*dot(a, x) for a in range(1 << n)) for x in range(1, 1 << n)}
    out["results"][n] = {
        "num_isotropic_fullrank": len(mats),
        "mu_row_prob_of_zero": mu[0],
        "mu_row_nonzero_probs": {bin(v): round(mu[v], 8) for v in range(1, 1 << n)},
        "uniform_nonzero_prob": uniform_nonzero,
        "mu_is_uniform_over_nonzero": is_uniform_nonzero,
        "c_mu_by_hamming": {str(hd): {"min": min(v), "max": max(v), "avg": sum(v)/len(v)}
                            for hd, v in by_hd.items()},
        "unconstrained_c_mu_baseline": 0.25,
        "diag_P(<a,x>=1)_range": [min(diag.values()), max(diag.values())],
    }

c2 = out["results"][2]; c3 = out["results"][3]
allc = []
for n in (2,3):
    for hd in out["results"][n]["c_mu_by_hamming"].values():
        allc += [hd["min"], hd["max"]]
out["verdict"] = {
    "mu_row_zero_mass_n2": c2["mu_row_prob_of_zero"],
    "mu_row_zero_mass_n3": c3["mu_row_prob_of_zero"],
    "mu_uniform_over_nonzero_n2": c2["mu_is_uniform_over_nonzero"],
    "mu_uniform_over_nonzero_n3": c3["mu_is_uniform_over_nonzero"],
    "all_c_mu_values_observed": sorted(set(round(x,8) for x in allc)),
    "kimi_conjecture_mu_uniform_nonzero": (c2["mu_is_uniform_over_nonzero"]
                                           and c3["mu_is_uniform_over_nonzero"]),
    "note": ("If mu uniform over nonzero AND c_mu == 1/4 across all pairs: single-row "
             "model = standard LPN exactly -> OP1 answered for single-row (S_A=0 does "
             "not reduce SDA via this model), but per Kimi §4 this is 'too weak' and "
             "the real bite needs the multi-row bundle (Step 4)."),
}

with open("experiments/165-CLAUDE-op1-rowmarginal-check.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps(out["results"], indent=1))
print("--- VERDICT ---")
print(json.dumps(out["verdict"], indent=1))
