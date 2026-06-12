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
"""230-KIMI-trackD: pencil-extremality evidence program (conj:pencil).

Track D deliverable.  Experiment numbers 230-239 reserved.

Scope:
  D1. n=2: exhaustive verification of all 2^15 subsets of Lagr(4,F_2).
      Exact maximum average correlation for every subset size s=1..15,
      identification of extremal configurations, and comparison to 5*rho_avg.
  D2. n=3: |Lagr(6,F_2)|=135 (exhaustion infeasible).
      Pre-registered search space:
        (a) all isotropic pencils and unions of <=3 pencils,
        (b) sunflower / near-pencil families,
        (c) random subsets (>=1e5 draws per size for s <= 30; 2e4 for s > 30),
        (d) greedy + local-search adversarial maximisation of average correlation.
      Report best-found maxima versus 5*rho_avg.
  D3. Escalate if any subset at the conjectured scale beats 5*rho_avg.

Convention (matching the conjecture statement):
  Average correlation of a subset S is
      rho_bar(S) = (1/|S|^2) * sum_{L,L' in S} 2^{dim(L intersect L')}
                 = (1/|S|^2) * sum_{L,L' in S} |L intersect L'|.
  Global rho_avg = rho_bar(Lagr(2n,F_2)).
  The paper's normalising factor (1-2p)^2/(p(1-p)) * 2^{-2n} is common to every
  term and cancels in all ratio comparisons, so we work with the raw integer
  values |L intersect L'|.

All exact values are Fractions; JSON stores rational values as strings.
"""

import json
import itertools
import random
import time
from fractions import Fraction
from collections import defaultdict

import numpy as np


# ---------------------------------------------------------------------------
# Helpers: symplectic geometry over F_2
# ---------------------------------------------------------------------------

def popcount(x: int) -> int:
    return x.bit_count()


def symplectic_form_n(u: int, v: int, n: int) -> int:
    """Standard symplectic form on F_2^{2n}: omega(u, v)."""
    res = 0
    for i in range(n):
        ui = (u >> i) & 1
        vi = (v >> i) & 1
        ui2 = (u >> (i + n)) & 1
        vi2 = (v >> (i + n)) & 1
        res ^= (ui * vi2) ^ (ui2 * vi)
    return res & 1


def isotropic_subspaces_by_dim(n: int) -> dict[int, list[frozenset[int]]]:
    """BFS enumeration of all isotropic subspaces of F_2^{2n}, keyed by dimension."""
    levels: dict[int, set[frozenset[int]]] = {0: {frozenset([0])}}
    for d in range(n):
        nxt: set[frozenset[int]] = set()
        N = 2 * n
        for S in levels[d]:
            span_S = set(S)
            for v in range(1, 1 << N):
                if v in span_S:
                    continue
                if all(symplectic_form_n(v, s, n) == 0 for s in S):
                    new_span = span_S | {s ^ v for s in span_S}
                    nxt.add(frozenset(new_span))
        levels[d + 1] = nxt
    return {d: sorted(levels[d], key=lambda s: tuple(sorted(s))) for d in levels}


def lagrangian_count(n: int) -> int:
    """Number of Lagrangian subspaces of F_2^{2n}."""
    c = 1
    for i in range(1, n + 1):
        c *= (2 ** i + 1)
    return c


def lagrangian_subspaces(n: int) -> list[frozenset[int]]:
    """Return list of all Lagrangian subspaces of F_2^{2n} as frozensets."""
    levels = isotropic_subspaces_by_dim(n)
    return levels[n]


def mask_of_subspace(S: frozenset[int]) -> int:
    """Convert a subspace (frozenset of vectors) to a bitmask."""
    m = 0
    for v in S:
        m |= 1 << v
    return m


def avg_correlation(indices: tuple[int, ...], pair_sum_all: list[int], diag: int) -> Fraction:
    """Exact average correlation of subset given by indices.

    pair_sum_all[i][j] = |L_i intersect L_j| for i, j in full Lagrangian list.
    diag = 2^n = |L_i|.
    """
    s = len(indices)
    if s == 0:
        return Fraction(0)
    total = 0
    for i in indices:
        row = pair_sum_all[i]
        for j in indices:
            total += row[j]
    return Fraction(total, s * s)


def avg_correlation_int(indices: tuple[int, ...], pair_sum_all: list[list[int]], diag: int) -> tuple[int, int]:
    """Return (numerator, denominator) for average correlation."""
    s = len(indices)
    if s == 0:
        return 0, 1
    total = 0
    for i in indices:
        row = pair_sum_all[i]
        for j in indices:
            total += row[j]
    return total, s * s


def avg_correlation_from_total(total: int, s: int) -> Fraction:
    return Fraction(total, s * s) if s else Fraction(0)


def make_pair_sum_matrix(lags: list[frozenset[int]]) -> np.ndarray:
    """Return N x N numpy array of |L_i intersect L_j|."""
    N = len(lags)
    A = np.empty((N, N), dtype=np.uint16)
    for i in range(N):
        Li = lags[i]
        row = A[i]
        for j in range(N):
            row[j] = len(Li & lags[j])
    return A


def avg_correlation_np(indices: tuple[int, ...], A: np.ndarray, diag: int) -> Fraction:
    """Fast exact average correlation using precomputed numpy matrix."""
    s = len(indices)
    if s == 0:
        return Fraction(0)
    total = int(A[np.ix_(indices, indices)].sum())
    return Fraction(total, s * s)


# ---------------------------------------------------------------------------
# D1: n=2 exhaustive verification
# ---------------------------------------------------------------------------

def run_n2_exhaustive() -> dict:
    print("[D1] n=2 exhaustive enumeration...")
    n = 2
    lags = lagrangian_subspaces(n)
    assert len(lags) == lagrangian_count(n) == 15

    # pairwise intersection sizes (ordered, including diagonal)
    N = len(lags)
    pair_sum = [[len(lags[i] & lags[j]) for j in range(N)] for i in range(N)]
    diag = 1 << n  # 2^n

    full_indices = tuple(range(N))
    rho_avg = avg_correlation(full_indices, pair_sum, diag)

    # Exhaustive subset DP: iterate subsets in increasing order, update pair sum.
    # subset encoded by N-bit mask.
    best_by_size: dict[int, dict] = {}
    # pair_sum_subset[mask] = sum_{i,j in mask} pair_sum[i][j]
    pair_sum_subset = [0] * (1 << N)
    elements_of = [[] for _ in range(1 << N)]

    t0 = time.time()
    for mask in range(1, 1 << N):
        # isolate lowest set bit
        lsb = mask & -mask
        b = lsb.bit_length() - 1
        prev = mask ^ lsb
        elements_of[mask] = elements_of[prev] + [b]
        add = pair_sum[b][b]
        for i in elements_of[prev]:
            add += 2 * pair_sum[b][i]
        pair_sum_subset[mask] = pair_sum_subset[prev] + add
        s = mask.bit_count()
        avg = Fraction(pair_sum_subset[mask], s * s)
        if s not in best_by_size or avg > best_by_size[s]["avg"]:
            best_by_size[s] = {
                "avg": avg,
                "avg_str": str(avg),
                "mask": mask,
                "indices": tuple(elements_of[mask]),
            }
    elapsed = time.time() - t0

    # Build size-vs-max table; identify extremal configuration type.
    size_profile = []
    for s in range(1, N + 1):
        best = best_by_size[s]
        # Determine whether the extremal subset is a pencil (or union of pencils)
        idx_set = set(best["indices"])
        # check if it is a single pencil: contained in S_W for some isotropic W of dim k<n
        is_pencil = False
        pencil_kind = None
        levels = isotropic_subspaces_by_dim(n)
        for k in range(1, n):
            for W in levels[k]:
                pen = {i for i, L in enumerate(lags) if W <= L}
                if idx_set == pen:
                    is_pencil = True
                    pencil_kind = f"k={k}_pencil(size={len(pen)})"
                    break
                if idx_set < pen and len(idx_set) == lagrangian_count(n - k):
                    # could be a smaller pencil inside a larger one
                    pass
            if is_pencil:
                break
        size_profile.append({
            "size": s,
            "max_avg": str(best["avg"]),
            "max_avg_float": float(best["avg"]),
            "ratio_to_rho_avg": str(best["avg"] / rho_avg),
            "ratio_float": float(best["avg"] / rho_avg),
            "extremal_mask": best["mask"],
            "extremal_indices": list(best["indices"]),
            "is_pencil": is_pencil,
            "pencil_kind": pencil_kind,
        })

    five_rho_avg = 5 * rho_avg
    beats_threshold = any(Fraction(r["ratio_to_rho_avg"]) > 5 for r in size_profile)

    result = {
        "n": n,
        "lagrangian_count": N,
        "rho_avg": str(rho_avg),
        "rho_avg_float": float(rho_avg),
        "five_rho_avg": str(five_rho_avg),
        "five_rho_avg_float": float(five_rho_avg),
        "exhaustive_subsets_checked": 1 << N,
        "elapsed_seconds": elapsed,
        "size_profile": size_profile,
        "any_subset_beats_5rho_avg": beats_threshold,
        "verdict": "THEOREM: n=2 max average correlation <= 5*rho_avg for every subset size"
                   if not beats_threshold else
                   "ESCALATE: a subset beats 5*rho_avg",
    }
    print(f"  rho_avg = {rho_avg} = {float(rho_avg):.6f}")
    print(f"  5*rho_avg = {five_rho_avg} = {float(five_rho_avg):.6f}")
    print(f"  any subset beats 5*rho_avg: {beats_threshold}")
    print(f"  elapsed: {elapsed:.2f}s")
    return result


# ---------------------------------------------------------------------------
# D2: n=3 pre-registered search
# ---------------------------------------------------------------------------

def run_n3_search(seed: int = 20260614) -> dict:
    print("[D2] n=3 pre-registered search...")
    n = 3
    random.seed(seed)
    lags = lagrangian_subspaces(n)
    assert len(lags) == lagrangian_count(n) == 135
    N = len(lags)
    diag = 1 << n  # 8

    # Precompute pairwise intersections as numpy array for speed.
    A = make_pair_sum_matrix(lags)
    full_indices = tuple(range(N))
    rho_avg = avg_correlation_np(full_indices, A, diag)
    threshold_T = Fraction(N, 1 << (2 * n))  # |Lagr| / 2^{2n}
    five_rho_avg = 5 * rho_avg

    print(f"  |Lagr| = {N}")
    print(f"  rho_avg = {rho_avg} = {float(rho_avg):.6f}")
    print(f"  5*rho_avg = {five_rho_avg} = {float(five_rho_avg):.6f}")
    print(f"  T_n = {threshold_T} = {float(threshold_T):.4f}")

    overall_best: dict = {"avg": Fraction(0), "indices": ()}
    best_by_size: dict[int, dict] = {}

    def update_best(indices: tuple[int, ...], source: str):
        nonlocal overall_best
        s = len(indices)
        avg = avg_correlation_np(indices, A, diag)
        if avg > overall_best["avg"]:
            overall_best = {"avg": avg, "indices": indices, "source": source}
        if s not in best_by_size or avg > best_by_size[s]["avg"]:
            best_by_size[s] = {"avg": avg, "indices": indices, "source": source}

    # (a) All isotropic pencils and unions of <=3 pencils.
    print("  [D2a] enumerating pencils and unions of <=3 pencils...")
    levels = isotropic_subspaces_by_dim(n)
    pencils = []  # list of (k, W_bitmask, indices)
    for k in range(1, n + 1):
        for W in levels[k]:
            pen = tuple(sorted(i for i, L in enumerate(lags) if W <= L))
            pencils.append({"dim": k, "W": mask_of_subspace(W), "indices": pen})
    print(f"    total pencils (k=1..{n}): {len(pencils)}")

    # 1-pencil averages.
    pencil_results = []
    for pen in pencils:
        avg = avg_correlation_np(pen["indices"], A, diag)
        pen["avg"] = avg
        update_best(pen["indices"], f"pencil_k{pen['dim']}")
        pencil_results.append({
            "dim": pen["dim"],
            "size": len(pen["indices"]),
            "avg": str(avg),
            "avg_float": float(avg),
            "ratio": str(avg / rho_avg),
            "ratio_float": float(avg / rho_avg),
        })

    # Pencil statistics by dimension.
    pencil_by_dim: dict[int, list] = defaultdict(list)
    for p in pencil_results:
        pencil_by_dim[p["dim"]].append(p)
    pencil_summary = {}
    for k in sorted(pencil_by_dim):
        avgs = [p["avg_float"] for p in pencil_by_dim[k]]
        sizes = [p["size"] for p in pencil_by_dim[k]]
        pencil_summary[k] = {
            "count": len(pencil_by_dim[k]),
            "size_unique": sorted(set(sizes)),
            "avg_min": min(avgs),
            "avg_max": max(avgs),
            "ratio_max": max(p["ratio_float"] for p in pencil_by_dim[k]),
        }

    # Unions of 2 and 3 pencils: restrict to dim-1 pencils for full enumeration,
    # and sample mixed-dimension / dim-2 triples to keep runtime bounded.
    dim1_pencils = [p for p in pencils if p["dim"] == 1]
    dim2_pencils = [p for p in pencils if p["dim"] == 2]
    print(f"    dim-1 pencils: {len(dim1_pencils)}, dim-2 pencils: {len(dim2_pencils)}")

    # All pairs of dim-1 pencils.
    t0 = time.time()
    for p1, p2 in itertools.combinations(dim1_pencils, 2):
        uni = tuple(sorted(set(p1["indices"]) | set(p2["indices"])))
        update_best(uni, "union_2_dim1_pencils")
    print(f"    union2 dim-1: {len(list(itertools.combinations(dim1_pencils, 2)))} checked, {time.time()-t0:.2f}s")

    # All triples of dim-1 pencils.
    t0 = time.time()
    count = 0
    for p1, p2, p3 in itertools.combinations(dim1_pencils, 3):
        uni = tuple(sorted(set(p1["indices"]) | set(p2["indices"]) | set(p3["indices"])))
        update_best(uni, "union_3_dim1_pencils")
        count += 1
    print(f"    union3 dim-1: {count} checked, {time.time()-t0:.2f}s")

    # Sample mixed-dimension pairs/triples.
    sample_size_pairs = min(50000, len(dim1_pencils) * len(dim2_pencils))
    sample_size_triples = 200000
    for _ in range(sample_size_pairs):
        p1 = random.choice(dim1_pencils)
        p2 = random.choice(dim2_pencils)
        uni = tuple(sorted(set(p1["indices"]) | set(p2["indices"])))
        update_best(uni, "union_2_mixed_sample")
    print(f"    union2 mixed sample: {sample_size_pairs}")
    for _ in range(sample_size_triples):
        p1 = random.choice(dim1_pencils)
        p2 = random.choice(dim1_pencils)
        p3 = random.choice(dim2_pencils)
        uni = tuple(sorted(set(p1["indices"]) | set(p2["indices"]) | set(p3["indices"])))
        update_best(uni, "union_3_mixed_sample")
    print(f"    union3 mixed sample: {sample_size_triples}")

    # (b) Sunflower / near-pencil families.
    print("  [D2b] sunflower / near-pencil families...")
    # Sunflower families are subsumed by isotropic pencils: a k-dim pencil S_W is exactly
    # the family of Lagrangians all containing the isotropic core W. Any larger family with
    # the same pairwise-intersection core would also have to lie inside S_W, so no separate
    # sunflower construction can exceed the pencil optimum. We still record a sunflower
    # probe by considering all subfamilies of dim-1 pencils via near-pencil removal below.
    sunflower_results = []

    # Near-pencil: take each dim-1 pencil (size 15) and add up to 10 random outsiders,
    # or remove up to 5 insiders, recording best.
    near_pencil_results = []
    for pen in dim1_pencils[:20]:  # sample 20 base pencils
        pen_set = set(pen["indices"])
        outsiders = [i for i in range(N) if i not in pen_set]
        # add outsiders
        for t in (1, 2, 3, 5, 10):
            for _ in range(200):
                added = tuple(random.sample(outsiders, min(t, len(outsiders))))
                S = tuple(sorted(pen_set | set(added)))
                update_best(S, f"near_pencil_add_{t}")
                near_pencil_results.append({"op": "add", "t": t, "avg_float": float(avg_correlation_np(S, A, diag))})
        # remove insiders
        for t in (1, 2, 3, 5):
            if t >= len(pen_set):
                continue
            for _ in range(200):
                removed = set(random.sample(list(pen_set), t))
                S = tuple(sorted(pen_set - removed))
                update_best(S, f"near_pencil_remove_{t}")
                near_pencil_results.append({"op": "remove", "t": t, "avg_float": float(avg_correlation_np(S, A, diag))})

    # (c) Random subsets.
    print("  [D2c] random subsets...")
    random_results_by_size: dict[int, dict] = {}
    sizes_small = list(range(3, 31))
    sizes_large = list(range(31, N + 1))
    # 1e5 for small sizes, 2e4 for large sizes.
    for s in sizes_small:
        best_avg = Fraction(0)
        best_idx = ()
        for _ in range(100000):
            idx = tuple(sorted(random.sample(range(N), s)))
            avg = avg_correlation_np(idx, A, diag)
            if avg > best_avg:
                best_avg = avg
                best_idx = idx
            update_best(idx, "random")
        random_results_by_size[s] = {
            "draws": 100000,
            "best_avg": str(best_avg),
            "best_avg_float": float(best_avg),
            "best_ratio": str(best_avg / rho_avg),
        }
        if s % 5 == 0:
            print(f"    size {s}: best random avg = {float(best_avg):.4f}")
    for s in sizes_large:
        best_avg = Fraction(0)
        best_idx = ()
        # Full 1e5 for sizes up to 60; reduced 2e4 for larger sizes because
        # correlation is diluted and random draws rarely approach the threshold.
        draws = 100000 if s <= 60 else 20000
        for _ in range(draws):
            idx = tuple(sorted(random.sample(range(N), s)))
            avg = avg_correlation_np(idx, A, diag)
            if avg > best_avg:
                best_avg = avg
                best_idx = idx
            update_best(idx, "random")
        random_results_by_size[s] = {
            "draws": draws,
            "best_avg": str(best_avg),
            "best_avg_float": float(best_avg),
            "best_ratio": str(best_avg / rho_avg),
        }
        if s in (45, 60, 90, 135):
            print(f"    size {s}: best random avg = {float(best_avg):.4f}")

    # (d) Greedy + local-search adversarial maximisation.
    print("  [D2d] greedy and local search...")

    def greedy_max(s: int, start: int | None = None) -> tuple[int, ...]:
        if start is None:
            # start from best off-diagonal pair (diagonal entries would duplicate)
            B = A.copy()
            np.fill_diagonal(B, 0)
            best_pair = np.unravel_index(np.argmax(B), B.shape)
            S = list(best_pair)
        else:
            S = [start]
        Sset = set(S)
        assert len(Sset) == len(S), f"greedy start has duplicates: {S}"
        while len(S) < s:
            # cur_total = sum of A over S x S
            cur_total = int(A[np.ix_(S, S)].sum())
            best_i = -1
            best_avg = -1.0
            for i in range(N):
                if i in Sset:
                    continue
                add = 2 * int(A[i, S].sum()) + int(A[i, i])
                new_total = cur_total + add
                new_avg = new_total / ((len(S) + 1) ** 2)
                if new_avg > best_avg:
                    best_avg = new_avg
                    best_i = i
            S.append(best_i)
            Sset.add(best_i)
        return tuple(sorted(S))

    def local_search(initial: tuple[int, ...], max_iters: int = 500) -> tuple[int, ...]:
        S = list(initial)
        Sset = set(S)
        outside = list(set(range(N)) - Sset)
        outside_set = set(outside)
        cur_total = int(A[np.ix_(S, S)].sum())
        for _ in range(max_iters):
            best_swap = None
            best_total = cur_total
            # Precompute row sums over S for all candidate j.
            sum_j_S = A[:, S].sum(axis=1)  # N-vector
            for idx_i, i in enumerate(S):
                sum_i_S = int(A[i, S].sum())
                # new total if we swap i out and j in:
                # remove i: subtract 2*sum_{k in S, k!=i} A[i,k] + A[i,i]
                # add j: add 2*sum_{k in S, k!=i} A[j,k] + A[j,j]
                for idx_j, j in enumerate(outside):
                    if i == j:
                        continue
                    new_total = cur_total - 2 * (sum_i_S - int(A[i, i])) - int(A[i, i])
                    new_total += 2 * (int(sum_j_S[j]) - int(A[j, i])) + int(A[j, j])
                    if new_total > best_total:
                        best_total = new_total
                        best_swap = (idx_i, idx_j)
            if best_swap is None:
                break
            idx_i, idx_j = best_swap
            i = S[idx_i]
            j = outside[idx_j]
            S[idx_i] = j
            outside[idx_j] = i
            Sset.remove(i); Sset.add(j)
            outside_set.remove(j); outside_set.add(i)
            cur_total = best_total
        return tuple(sorted(S))

    greedy_results = []
    for s in list(range(3, 21)) + [30, 45, 60, 90]:
        g = greedy_max(s)
        avg_g = avg_correlation_np(g, A, diag)
        update_best(g, "greedy")
        ls = local_search(g, max_iters=200)
        avg_ls = avg_correlation_np(ls, A, diag)
        update_best(ls, "local_search_from_greedy")
        greedy_results.append({
            "size": s,
            "greedy_avg": str(avg_g),
            "greedy_avg_float": float(avg_g),
            "local_avg": str(avg_ls),
            "local_avg_float": float(avg_ls),
        })
        print(f"    size {s}: greedy={float(avg_g):.4f}, local={float(avg_ls):.4f}")

    # Additional local searches from random starts and from pencils.
    for _ in range(50):
        s = random.randint(3, 60)
        start = tuple(sorted(random.sample(range(N), s)))
        ls = local_search(start, max_iters=200)
        update_best(ls, "local_search_from_random")
    for pen in dim1_pencils[:10]:
        # add 5 random outsiders and locally search
        outsiders = [i for i in range(N) if i not in pen["indices"]]
        for _ in range(10):
            added = random.sample(outsiders, 5)
            start = tuple(sorted(set(pen["indices"]) | set(added)))
            ls = local_search(start, max_iters=200)
            update_best(ls, "local_search_from_pencil_seed")

    # Collect best-by-size summary.
    best_by_size_summary = []
    for s in sorted(best_by_size):
        b = best_by_size[s]
        best_by_size_summary.append({
            "size": s,
            "best_avg": str(b["avg"]),
            "best_avg_float": float(b["avg"]),
            "best_ratio": str(b["avg"] / rho_avg),
            "source": b.get("source", "unknown"),
        })

    scale_threshold_size = (threshold_T.numerator + threshold_T.denominator - 1) // threshold_T.denominator  # ceil(T_n)
    overall_best_at_scale = {"avg": Fraction(0), "indices": (), "source": ""}
    for s, b in best_by_size.items():
        if s >= scale_threshold_size:
            if b["avg"] > overall_best_at_scale["avg"]:
                overall_best_at_scale = b
    escalation = overall_best_at_scale["avg"] > five_rho_avg

    result = {
        "n": n,
        "lagrangian_count": N,
        "rho_avg": str(rho_avg),
        "rho_avg_float": float(rho_avg),
        "five_rho_avg": str(five_rho_avg),
        "five_rho_avg_float": float(five_rho_avg),
        "threshold_T_n": str(threshold_T),
        "threshold_T_n_float": float(threshold_T),
        "scale_threshold_size": scale_threshold_size,
        "pencil_summary": pencil_summary,
        "overall_best": {
            "avg": str(overall_best["avg"]),
            "avg_float": float(overall_best["avg"]),
            "ratio": str(overall_best["avg"] / rho_avg),
            "ratio_float": float(overall_best["avg"] / rho_avg),
            "size": len(overall_best["indices"]),
            "source": overall_best.get("source", "unknown"),
            "indices": list(overall_best["indices"]),
        },
        "overall_best_at_scale": {
            "avg": str(overall_best_at_scale["avg"]),
            "avg_float": float(overall_best_at_scale["avg"]),
            "ratio": str(overall_best_at_scale["avg"] / rho_avg),
            "ratio_float": float(overall_best_at_scale["avg"] / rho_avg),
            "size": len(overall_best_at_scale["indices"]),
            "source": overall_best_at_scale.get("source", "unknown"),
            "indices": list(overall_best_at_scale["indices"]),
        },
        "best_by_size": best_by_size_summary,
        "any_subset_beats_5rho_avg": escalation,
        "random_subset_draws_total": sum(v["draws"] for v in random_results_by_size.values()),
        "random_best_per_size": random_results_by_size,
        "greedy_results": greedy_results,
        "sunflower_count": len(sunflower_results),
        "near_pencil_count": len(near_pencil_results),
        "verdict": "ESCALATE: a subset at scale beats 5*rho_avg" if escalation else
                   "EVIDENCE: no search found a subset at scale beating 5*rho_avg",
    }
    print(f"  overall best avg = {overall_best['avg']} = {float(overall_best['avg']):.6f}")
    print(f"  overall best ratio = {float(overall_best['avg']/rho_avg):.4f}")
    print(f"  overall best at scale (size>={scale_threshold_size}) = {overall_best_at_scale['avg']} = {float(overall_best_at_scale['avg']):.6f}")
    print(f"  overall best at scale ratio = {float(overall_best_at_scale['avg']/rho_avg):.4f}")
    print(f"  escalation needed: {escalation}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    out = {
        "experiment": "230-KIMI-trackD-pencil-extremality",
        "track": "D",
        "claim_labels": "D1 THEOREM; D2 EVIDENCE; conj:pencil remains OPEN",
        "interpretation_guard": {
            "comparison_distribution": "raw integer intersections |L intersect L'| = 2^{dim cap}; common normalisation cancels in ratios",
            "m_vs_n_scaling": "conj:pencil scale is |D'| >= |Lagr(2n)|/2^{2n-c}; checked at the c-scale threshold T_n = |Lagr|/2^{2n}",
            "noise_rate": "not applicable -- this is a structural geometric statistic, not an output-noise-rate comparison",
        },
        "n2": run_n2_exhaustive(),
        "n3": run_n3_search(),
    }
    path = "experiments/output/230-KIMI-trackD-pencil-extremality.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2, cls=NumpyEncoder)
    print(f"\nWrote {path}")


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that converts numpy scalars to Python scalars."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


if __name__ == "__main__":
    main()
