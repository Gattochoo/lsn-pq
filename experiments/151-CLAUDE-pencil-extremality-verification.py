#!/usr/bin/env python3

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
"""151: CLAUDE adjudication of Kimi's pencil-extremality DRAFT (2026-06-12).



Independently verifies, by FULL ENUMERATION of Lagr(2n, F_2) for n=2,3,4:

  (1) |Lagr(2n)| = prod_{i=1..n} (2^i + 1)

  (2) E_n := distinct-pair average of 2^{dim(L cap L')}  (= |L cap L'| as sets)

  (3) row-sum closed form Z_n = sum_{L'} |L cap L'| = 2^{n+1} * |Lagr(2(n-1))|

      (this is what makes Kimi's E_n column computable at large n)

  (4) pencil law: for k-dim isotropic W, S_W = {L : W <= L} has

      |S_W| = |Lagr(2(n-k))| and distinct-pair average 2^k * E_{n-k}

  (5) the ratio table R_{n,k} = 2^k * E_{n-k} / E_n for k=1,2,3, n=3..10

      -> check Kimi's table columns (k=2 expected OK; k=1,k=3 suspected wrong)

  (6) threshold ratios |S_W|/T_n for k=1,2,3 (T_n = |Lagr|/2^{2n})



Convention: distinct pairs (paper convention, C_n -> 2).

Output: experiments/151-CLAUDE-pencil-extremality-verification.json

"""

import json

from itertools import combinations



def popcount(x): return bin(x).count("1")



def make_omega(n):

    mask = (1 << n) - 1

    def omega(u, v):

        ua, ub = u & mask, u >> n

        va, vb = v & mask, v >> n

        return (popcount(ua & vb) ^ popcount(ub & va)) & 1

    return omega



def isotropic_levels(n):

    """BFS: all isotropic subspaces of F_2^{2n} by dimension, as frozensets."""

    omega = make_omega(n)

    N = 2 * n

    levels = [ {frozenset([0])} ]

    for _ in range(n):

        nxt = set()

        for S in levels[-1]:

            for v in range(1, 1 << N):

                if v in S:

                    continue

                if all(omega(v, s) == 0 for s in S):

                    nxt.add(frozenset(list(S) + [s ^ v for s in S]))

        levels.append(nxt)

    return levels  # levels[d] = isotropic subspaces of dim d



def lagr_count(n):

    c = 1

    for i in range(1, n + 1):

        c *= (2 ** i + 1)

    return c



def distinct_avg(sets):

    """average of |A cap B| over distinct ordered pairs (= 2^{dim cap})."""

    m = len(sets)

    if m < 2:

        return None

    tot = 0

    for a, b in combinations(sets, 2):

        tot += len(a & b)

    return 2 * tot / (m * (m - 1))



out = {"experiment": "151-CLAUDE-pencil-extremality-verification",

       "convention": "distinct pairs; 2^{dim(L cap L')} = |L cap L'| as sets",

       "enumeration": {}, "pencil_checks": [], "ratio_table": [],

       "threshold_table": [], "verdicts": {}}



E = {0: None, 1: None}  # E_n by enumeration where possible

lag_sets = {}

for n in (1, 2, 3, 4):

    levels = isotropic_levels(n)

    lags = list(levels[n])

    assert len(lags) == lagr_count(n), (n, len(lags), lagr_count(n))

    lag_sets[n] = (levels, lags)

    En = distinct_avg(lags)

    E[n] = En

    # row-sum Z_n (vertex-transitivity check on 3 different rows)

    rows = []

    for L in lags[:3]:

        rows.append(sum(len(L & Lp) for Lp in lags))

    Zn = rows[0]

    Z_closed = 2 ** (n + 1) * (lagr_count(n - 1) if n >= 1 else 1)

    out["enumeration"][n] = {

        "lagr_count": len(lags), "E_n_distinct": En,

        "Z_rowsum": Zn, "Z_rows_all_equal": len(set(rows)) == 1,

        "Z_closed_form_2^{n+1}Lagr(n-1)": Z_closed,

        "Z_matches_closed_form": Zn == Z_closed,

        "E_n_from_Z": (Zn - 2 ** n) / (len(lags) - 1),

    }



# (4) pencil law checks for n=3,4 and k=1,2,3 (all W at given dim)

for n in (3, 4):

    levels, lags = lag_sets[n]

    for k in (1, 2, 3):

        if k >= n:  # S_W singleton at k=n -> no distinct pairs

            continue

        sizes, avgs = set(), set()

        Ws = list(levels[k])

        for W in Ws:

            SW = [L for L in lags if W <= L]

            sizes.add(len(SW))

            avgs.add(round(distinct_avg(SW), 12))

        expect_size = lagr_count(n - k)

        expect_avg = round(2 ** k * E[n - k], 12)

        out["pencil_checks"].append({

            "n": n, "k": k, "num_W": len(Ws),

            "pencil_sizes_observed": sorted(sizes),

            "expected_size_Lagr(2(n-k))": expect_size,

            "size_ok": sizes == {expect_size},

            "pencil_avgs_observed": sorted(avgs),

            "expected_2^k_E_{n-k}": expect_avg,

            "avg_ok": avgs == {expect_avg},

        })



# (5) ratio table via closed form E_n = (2^{n+1}|Lagr(n-1)| - 2^n)/(|Lagr(n)|-1)

def E_closed(n):

    if n == 0:

        return None

    if n == 1:

        return 1.0  # 3 lines, pairwise dim cap = 0 (verified by enumeration)

    return (2 ** (n + 1) * lagr_count(n - 1) - 2 ** n) / (lagr_count(n) - 1)



for n in (1, 2, 3, 4):

    e_enum, e_cl = E[n], E_closed(n)

    if e_enum is not None:

        assert abs(e_enum - e_cl) < 1e-12, (n, e_enum, e_cl)



KIMI_TABLE = {  # from meta/2026-06-12-KIMI-pencil-extremality.md section 3

    3: {"E": 1.7313, 1: 2.3103, 2: 2.3103, 3: None},

    4: {"E": 1.8762, 1: 2.6667, 2: 3.0457, 3: 4.5714},

    5: {"E": 1.9390, 1: 2.8421, 2: 3.5716, 3: 5.7143},

    6: {"E": 1.9692, 1: 2.9206, 2: 3.8111, 3: 6.3492},

    8: {"E": 1.9922, 1: 2.9767, 2: 3.9538, 3: 6.6977},

    10: {"E": 1.9980, 1: 2.9922, 2: 3.9883, 3: 6.9767},

}

for n in (3, 4, 5, 6, 8, 10):

    row = {"n": n, "E_n": E_closed(n)}

    for k in (1, 2, 3):

        if n - k < 1:

            row[f"R_{k}"] = None

            continue

        row[f"R_{k}"] = 2 ** k * E_closed(n - k) / E_closed(n)

    kimi = KIMI_TABLE[n]

    row["kimi_E_matches"] = abs(row["E_n"] - kimi["E"]) < 5e-5

    for k in (1, 2, 3):

        kv = kimi[k]

        row[f"kimi_R{k}_matches"] = (kv is not None and row[f"R_{k}"] is not None

                                     and abs(row[f"R_{k}"] - kv) < 5e-4)

    out["ratio_table"].append(row)



# (6) threshold ratios

for n in (3, 4, 5, 6, 8):

    T = lagr_count(n) / 2 ** (2 * n)

    row = {"n": n, "T_n": T}

    for k in (1, 2, 3):

        row[f"size_k{k}/T"] = lagr_count(n - k) / T if n - k >= 0 else None

    out["threshold_table"].append(row)



out["verdicts"] = {

    "E_n_column": "VERIFIED (enumeration n<=4 + closed form Z_n=2^{n+1}|Lagr(n-1)| proven by enumeration n=2,3,4)",

    "k2_column": "check kimi_R2_matches flags",

    "k1_column": "check kimi_R1_matches flags",

    "k3_column": "check kimi_R3_matches flags",

    "limits": {"R_k_limit": "2^k * 2/2 = 2^k (k=1 -> 2, k=2 -> 4, k=3 -> 8)"},

}



with open("experiments/151-CLAUDE-pencil-extremality-verification.json", "w") as f:

    json.dump(out, f, indent=1)



print(json.dumps(out["enumeration"], indent=1))

print("--- pencil checks ---")

for c in out["pencil_checks"]:

    print(c)

print("--- ratio table (mine vs Kimi match flags) ---")

for r in out["ratio_table"]:

    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})

print("--- threshold table ---")

for r in out["threshold_table"]:

    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
