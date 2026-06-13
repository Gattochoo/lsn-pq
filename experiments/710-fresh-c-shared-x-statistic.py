#!/usr/bin/env python3
"""Track FF round 8: fresh-C, shared-x multi-block distinguisher at n=2.

Model (verbatim from the standing directive):
  k blocks  (C^(i), y^(i) = C^(i) x + B^(i) e^(i))
  with the SAME secret x ∈ F_2^n, and independent
  (A^(i), B^(i), e^(i)).

Here n = 2, A^(i) is a uniform isotropic basis of F_2^{2n},
B^(i) ~ Unif(F_2^{m × 2n}) is drawn independently per block, and
e^(i) ~ Bernoulli(1/4)^{2n}.

The matched LPN comparison distribution uses the same shared-x,
m-row-per-block structure with C^(i) ~ Unif(F_2^{m × n}) and
independent Bernoulli(p_eff)^m noise, where p_eff is the marginal
bit-error rate induced by a uniform B row.

All probabilities are exact rationals (Fraction).  Informational
quantities are evaluated in high-precision floating point from the
exact counts.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
)


# ---------------------------------------------------------------------------
# Exact per-secret conditional counts
# ---------------------------------------------------------------------------

def per_x_uniform_B_counts(m: int) -> tuple[list[list[int]], int]:
    """Return (counts_x, denom) for n=2 uniform-B-per-A reduction.

    counts_x[x][key] / denom  ==  P((C, y) = key  |  secret x),
    where key = ((c0 << m) | c1) << m | y.
    """
    bases = enumerate_lagrangian_bases()
    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    size = 1 << (3 * m)
    counts_x = [[0] * size for _ in range(4)]

    c0_list = [(C_key >> m) & mask for C_key in range(num_C)]
    c1_list = [C_key & mask for C_key in range(num_C)]
    two_to_2m = 1 << (2 * m)
    two_to_m = 1 << m

    # case3 weight is accumulated independently of x, then added uniformly.
    case3_weight_sum = [0] * 4

    for a0, a1 in bases:
        span_map = {0: (0, 0), a0: (1, 0), a1: (0, 1), a0 ^ a1: (1, 1)}
        for x in range(4):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w = e.bit_count()
                weight = 3 ** (4 - w)
                v = a ^ e

                if v == 0:
                    add = weight * two_to_2m
                    arr = counts_x[x]
                    for C_key in range(num_C):
                        arr[(C_key << m)] += add
                elif v in span_map:
                    alpha, beta = span_map[v]
                    add = weight * two_to_2m
                    arr = counts_x[x]
                    for C_key in range(num_C):
                        y = 0
                        if alpha:
                            y ^= c0_list[C_key]
                        if beta:
                            y ^= c1_list[C_key]
                        arr[(C_key << m) | y] += add
                else:
                    case3_weight_sum[x] += weight

    # case3 is uniform over the full (C, y) space for each x separately.
    for x in range(4):
        case3_add = case3_weight_sum[x] * two_to_m
        for key in range(size):
            counts_x[x][key] += case3_add

    denom = len(bases) * 256 * (1 << (4 * m))
    return counts_x, denom


def per_x_lpn_counts(m: int, p: Fraction) -> tuple[list[list[int]], int]:
    """Per-secret counts for standard LPN with shared x.

    For a fixed output (C, y) the likelihood depends on x through the
    implied noise vector e = y + C x.  This dependence is what makes
    shared-x LPN informative across blocks.
    """
    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    size = 1 << (3 * m)
    counts_x = [[0] * size for _ in range(4)]
    D = p.denominator ** m
    pnum = p.numerator
    qnum = p.denominator - p.numerator

    for C_key in range(num_C):
        base = C_key << m
        c0 = (C_key >> m) & mask
        c1 = C_key & mask
        for y in range(1 << m):
            key = base | y
            for x in range(4):
                e = y
                if x & 1:
                    e ^= c0
                if x & 2:
                    e ^= c1
                w = e.bit_count()
                counts_x[x][key] += (pnum ** w) * (qnum ** (m - w))

    denom = num_C * D
    return counts_x, denom


# ---------------------------------------------------------------------------
# Statistics on the k-block product distribution
# ---------------------------------------------------------------------------

def _decode_key(key: int, m: int) -> tuple[int, int, int]:
    mask = (1 << m) - 1
    y = key & mask
    c1 = (key >> m) & mask
    c0 = (key >> (2 * m)) & mask
    return c0, c1, y


def _y_in_colspace(c0: int, c1: int, y: int, m: int) -> bool:
    """Check whether y lies in span{c0, c1} in F_2^m."""
    # Gaussian elimination on the two column vectors, test membership of y.
    rows = [c0, c1, y]
    pivots: dict[int, int] = {}
    for r in rows:
        x = r & ((1 << m) - 1)
        if x == 0:
            continue
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    # y is in span iff adding it did not increase rank beyond the span of c0,c1.
    rank_cols = 0
    tmp = c0
    while tmp:
        rank_cols += 1
        tmp &= tmp - 1
    tmp = c1
    while tmp:
        rank_cols += 1
        tmp &= tmp - 1
    # Remove redundant column.
    span = [0]
    for v in (c0, c1):
        span += [s ^ v for s in span]
    return y in span


def graph_weight(counts: list[int], m: int) -> Fraction:
    """Fraction of mass with y in col(C)."""
    mask = (1 << m) - 1
    total = sum(counts)
    in_graph = 0
    for key, cnt in enumerate(counts):
        if cnt == 0:
            continue
        y = key & mask
        c1 = (key >> m) & mask
        c0 = (key >> (2 * m)) & mask
        if _y_in_colspace(c0, c1, y, m):
            in_graph += cnt
    return Fraction(in_graph, total)


def per_block_sd(counts_x_f: list[list[int]], denom_f: int,
                 counts_x_l: list[list[int]], denom_l: int) -> Fraction:
    """SD between the mixtures over x for one block."""
    total_f = [0] * len(counts_x_f[0])
    for x in range(4):
        for k, c in enumerate(counts_x_f[x]):
            total_f[k] += c
    total_l = [0] * len(counts_x_l[0])
    for x in range(4):
        for k, c in enumerate(counts_x_l[x]):
            total_l[k] += c
    return exact_sd_counts(total_f, 4 * denom_f, total_l, 4 * denom_l)


def k_block_statistics(counts_x: list[list[int]], denom: int, k: int):
    """Compute MI, expected true-posterior, and MAP-recovery probability.

    Returns dict with Fraction values (plus float MI).
    """
    S = len(counts_x[0])
    D = denom
    Dk = D ** k
    inv = Fraction(1, 4 * Dk)

    mi = 0.0
    exp_true_post = Fraction(0)
    recovery_prob = Fraction(0)

    # Enumerate all k-tuples of outputs.
    for tup in product(range(S), repeat=k):
        # N_x = product_i counts_x[x][t_i]
        N = [1] * 4
        for idx in tup:
            for x in range(4):
                N[x] *= counts_x[x][idx]
        M = sum(N)
        if M == 0:
            continue

        mix_prob = Fraction(M, 4 * Dk)

        # Mutual information contribution:  sum_x (N_x/M) log2(N_x/M)
        ent = 0.0
        for x in range(4):
            if N[x] == 0:
                continue
            prob = N[x] / M
            ent += prob * math.log2(prob)
        mi += float(mix_prob) * ent

        # Expected posterior weight of true x.
        sum_sq = sum(nx * nx for nx in N)
        exp_true_post += Fraction(sum_sq, 4 * Dk * M)

        # MAP recovery probability with lexicographic tie-break.
        max_val = max(N)
        map_x = next(i for i in range(4) if N[i] == max_val)
        recovery_prob += Fraction(N[map_x], 4 * Dk)

    # mi = - H(x | observations), so I(x; observations) = H(x) + mi = 2 + mi.
    mutual_information = 2.0 + mi
    return {
        "mi": mutual_information,
        "mi_bits": mutual_information,
        "expected_true_posterior": exp_true_post,
        "map_recovery_probability": recovery_prob,
    }


def k_block_sd(counts_x_f: list[list[int]], denom_f: int,
               counts_x_l: list[list[int]], denom_l: int, k: int) -> Fraction:
    """Exact SD between k-block fresh-C and matched-LPN mixtures."""
    S = len(counts_x_f[0])
    Df = denom_f
    Dl = denom_l
    Dfk = Df ** k
    Dlk = Dl ** k

    num = 0
    for tup in product(range(S), repeat=k):
        Nf = [1] * 4
        Nl = [1] * 4
        for idx in tup:
            for x in range(4):
                Nf[x] *= counts_x_f[x][idx]
                Nl[x] *= counts_x_l[x][idx]
        Mf = sum(Nf)
        Ml = sum(Nl)
        if Mf == 0 and Ml == 0:
            continue
        num += abs(Mf * Dlk - Ml * Dfk)

    return Fraction(num, 4 * Dfk * Dlk * 2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    n = 2
    p = Fraction(1, 4)
    # Marginal output-noise bias for a uniform row of B over F_2^{2n}.
    bias = Fraction(3, 4) ** (2 * n)  # = ((1-2p)/2 + 1/2)^{2n}
    p_eff = Fraction(1, 2) - bias / 2

    results = {
        "n": n,
        "input_noise_p": str(p),
        "marginal_output_bias": str(bias),
        "matched_lpn_p_eff": str(p_eff),
        "claim_labels": {
            "model": "EVIDENCE / definition",
            "per_block_sd": "EVIDENCE (exact enumeration, n=2)",
            "kblock_sd": "EVIDENCE (exact enumeration, n=2)",
            "asymptotic_conclusion": "NO-GO / OPEN: advantage not bounded away from 0 for m=poly(n)",
        },
        "governance": {
            "L1_exact_arithmetic": True,
            "L2_J_twist_duality": "standard symplectic form on F_2^4 used; column/row duality preserved",
            "L3_query_class_hygiene": "comparison is standard shared-x LPN; no non-LPN queries used",
            "L4_no_transform_comparison": "matched LPN distribution is sampled natively, not transformed",
        },
        "per_block": {},
        "k_block": [],
    }

    # Precompute per-secret tables for m = 2,3,4.
    tables: dict[int, dict] = {}
    for m in (2, 3, 4):
        counts_x_f, denom_f = per_x_uniform_B_counts(m)
        counts_x_l, denom_l = per_x_lpn_counts(m, p_eff)
        tables[m] = {
            "fresh": (counts_x_f, denom_f),
            "lpn": (counts_x_l, denom_l),
        }

        # Sanity-check the q_graph spike for fresh-C.
        total_f = [sum(counts_x_f[x][k] for x in range(4)) for k in range(len(counts_x_f[0]))]
        q_graph = graph_weight(total_f, m)

        sd1 = per_block_sd(counts_x_f, denom_f, counts_x_l, denom_l)
        results["per_block"][m] = {
            "output_space_size": len(counts_x_f[0]),
            "q_graph_y_in_col_C": str(q_graph),
            "sd_fresh_vs_lpn": str(sd1),
        }

    # k-block exact statistics for feasible (m, k) pairs.
    # (Larger tuples are omitted because the exact O(2^{3mk}) enumeration
    # becomes impractical in pure Python; the included pairs already test the
    # cross-block leakage question.)
    pairs = [(2, 2), (2, 3), (3, 2)]
    for m, k in pairs:
        counts_x_f, denom_f = tables[m]["fresh"]
        counts_x_l, denom_l = tables[m]["lpn"]

        stats_f = k_block_statistics(counts_x_f, denom_f, k)
        stats_l = k_block_statistics(counts_x_l, denom_l, k)
        sdk = k_block_sd(counts_x_f, denom_f, counts_x_l, denom_l, k)

        results["k_block"].append({
            "m": m,
            "k": k,
            "sd_fresh_vs_lpn": str(sdk),
            "mi_fresh_bits": stats_f["mi_bits"],
            "mi_lpn_bits": stats_l["mi_bits"],
            "expected_true_posterior_fresh": str(stats_f["expected_true_posterior"]),
            "expected_true_posterior_lpn": str(stats_l["expected_true_posterior"]),
            "map_recovery_fresh": str(stats_f["map_recovery_probability"]),
            "map_recovery_lpn": str(stats_l["map_recovery_probability"]),
        })

    # Per-block SD for a slightly larger m to show the fixed-n trend.
    for m in (5, 6):
        counts_x_f, denom_f = per_x_uniform_B_counts(m)
        counts_x_l, denom_l = per_x_lpn_counts(m, p_eff)
        sd1 = per_block_sd(counts_x_f, denom_f, counts_x_l, denom_l)
        results["per_block"][m] = {
            "output_space_size": len(counts_x_f[0]),
            "sd_fresh_vs_lpn": str(sd1),
        }

    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "710-fresh-c-shared-x-statistic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
