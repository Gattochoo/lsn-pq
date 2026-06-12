#!/usr/bin/env python3
"""196: Monte-Carlo matched-rate SD sampling for lem:m2 along m=2n.

Estimates SD((C,y), LPN_{p_eff}) for the uniform-B-per-A reduction of lem:m2.
Because the full output key space has size 2^{(n+1)m} (already 2^{40} for
n=4,m=8), exact enumeration is infeasible.  We therefore accumulate histograms
over a coarse key space:

  * rank-membership (default): dictionary keyed by
      (rank_F2(C), 1{y in col(C)}).
    This partition captures the dominant detectable correlation: under the
    reduction, y is correlated with the column space of C because v=Ax+e falls
    in span(A) with probability q(n); under LPN_{p_eff} the same event is
    governed only by the noise landing in col(C).

  * hash: hash the concatenated key (C,y) to L bits and accumulate a histogram
    over 2^L buckets.  This is the literal "coarse key space" requested in the
    work directive and provides a (looser) lower bound.

For every run we report:
  - the empirical total variation over the chosen coarse partition,
  - a bootstrap standard error,
  - the exact total variation over the (rank,membership) partition, which is a
    cheap analytic lower bound on the true SD and serves as a sanity check for
    the Monte Carlo.

The uniform average over Lagrangian subspaces A is performed by sampling a
uniform ordered isotropic basis at each trial (via symplectic basis reduction),
rather than fixing A.  This is required because the output distribution for a
fixed A is not identical to the average (see meta note).
"""
import argparse
import json
import math
import random
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Symplectic helpers and uniform Lagrangian sampling
# ---------------------------------------------------------------------------

def _make_omega_table(n: int) -> bytearray:
    """Precompute the standard symplectic form on F_2^{2n}.

    Returns a flat bytearray where entry (u,v) is omega(u,v).
    """
    size = 1 << (2 * n)
    table = bytearray(size * size)
    for u in range(size):
        row = u * size
        for v in range(size):
            res = 0
            for ii in range(n):
                ui = (u >> ii) & 1
                wi = (v >> ii) & 1
                ui2 = (u >> (ii + n)) & 1
                wi2 = (v >> (ii + n)) & 1
                res ^= (ui * wi2) ^ (ui2 * wi)
            table[row + v] = res & 1
    return table


def _omega_table(u: int, v: int, n: int, table: bytearray) -> int:
    return table[u * (1 << (2 * n)) + v]


def sample_lagrangian_basis(n: int, rng: random.Random, table: bytearray) -> list[int]:
    r"""Return a uniform ordered isotropic basis of a uniform Lagrangian subspace.

    Algorithm: build a symplectic basis of F_2^{2n} by choosing the next
    Lagrangian vector v as a uniform non-zero element of the current symplectic
    complement W, then update W to W \cap v^\perp (a symplectic subspace of
    dimension two less).  This samples a uniform ordered symplectic basis;
    the first n vectors span a uniform Lagrangian.
    """
    # Standard symplectic basis: e_i at bit i, f_i at bit n+i.
    symp_basis = []
    for i in range(n):
        symp_basis.append(1 << i)
        symp_basis.append(1 << (n + i))

    lagrangian = []
    for k in range(n):
        d = n - k  # current dimension of W is 2d
        coeff = rng.randint(1, (1 << (2 * d)) - 1)
        v = 0
        for i in range(2 * d):
            if (coeff >> i) & 1:
                v ^= symp_basis[i]

        # Decompose v in the current symplectic basis: for each pair (u_i,v_i),
        # a_i = omega(v, v_i), b_i = omega(v, u_i).
        a = []
        b = []
        for i in range(d):
            ui = symp_basis[2 * i]
            vi = symp_basis[2 * i + 1]
            a.append(_omega_table(v, vi, n, table))
            b.append(_omega_table(v, ui, n, table))

        i0 = next(i for i in range(d) if a[i] or b[i])
        u1p = v
        # Choose v1p so that omega(u1p, v1p) = 1.
        if b[i0]:
            v1p = symp_basis[2 * i0]          # u_{i0}
        else:
            v1p = symp_basis[2 * i0 + 1]      # v_{i0}

        lagrangian.append(u1p)

        # New symplectic basis for W' = W \cap span(u1p, v1p)^\perp.
        new_symp = []
        for i in range(d):
            if i == i0:
                continue
            ui = symp_basis[2 * i]
            vi = symp_basis[2 * i + 1]
            ui_p = ui ^ (_omega_table(ui, v1p, n, table) * u1p) ^ (_omega_table(ui, u1p, n, table) * v1p)
            vi_p = vi ^ (_omega_table(vi, v1p, n, table) * u1p) ^ (_omega_table(vi, u1p, n, table) * v1p)
            new_symp.append(ui_p)
            new_symp.append(vi_p)
        symp_basis = new_symp

    return lagrangian


# ---------------------------------------------------------------------------
# Linear algebra helpers
# ---------------------------------------------------------------------------

def _rank_and_member(c_rows: list[int], y: int, n: int, m: int) -> tuple[int, int]:
    """Return (rank_F2(C), 1{y in col(C)}).

    Performs Gauss-Jordan elimination on the augmented matrix [C | y].
    """
    aug = [c_rows[i] | (((y >> i) & 1) << n) for i in range(m)]
    rank = 0
    for col in range(n):
        pivot = -1
        for i in range(rank, m):
            if (aug[i] >> col) & 1:
                pivot = i
                break
        if pivot == -1:
            continue
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        for i in range(m):
            if i != rank and ((aug[i] >> col) & 1):
                aug[i] ^= aug[rank]
        rank += 1
    for i in range(rank, m):
        if (aug[i] >> n) & 1 and (aug[i] & ((1 << n) - 1)) == 0:
            return rank, 0
    return rank, 1


# ---------------------------------------------------------------------------
# Sampling distributions
# ---------------------------------------------------------------------------

def p_eff_float(n: int) -> float:
    return (1.0 - (0.75) ** (2 * n)) / 2.0


def p_eff_frac(n: int) -> Fraction:
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph_frac(n: int) -> Fraction:
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def sample_reduction_rank_member(
    n: int, m: int, rng: random.Random, table: bytearray
) -> tuple[int, int]:
    """Sample (A,x,e,B) and return the coarse bucket (rank(C), 1{y in col(C)})."""
    A_basis = sample_lagrangian_basis(n, rng, table)
    x = rng.randint(0, (1 << n) - 1)

    e = 0
    for _ in range(2 * n):
        if rng.random() < 0.25:
            e |= 1 << _

    v = 0
    for j in range(n):
        if (x >> j) & 1:
            v ^= A_basis[j]
    v ^= e

    c_rows = []
    y = 0
    for i in range(m):
        b = rng.randint(0, (1 << (2 * n)) - 1)
        c = 0
        for j in range(n):
            if _omega_table(b, A_basis[j], n, table):
                c |= 1 << j
        c_rows.append(c)
        if _omega_table(b, v, n, table):
            y |= 1 << i

    return _rank_and_member(c_rows, y, n, m)


def sample_lpn_rank_member(
    n: int, m: int, p: float, rng: random.Random
) -> tuple[int, int]:
    """Sample (C,x,e) from LPN_{p} and return the coarse bucket."""
    x = rng.randint(0, (1 << n) - 1)
    c_rows = [rng.randint(0, (1 << n) - 1) for _ in range(m)]
    y = 0
    for i in range(m):
        if (c_rows[i] & x).bit_count() & 1:
            y |= 1 << i
    for i in range(m):
        if rng.random() < p:
            y ^= 1 << i
    return _rank_and_member(c_rows, y, n, m)


def sample_reduction_hash(
    n: int, m: int, rng: random.Random, table: bytearray, hash_mult: int, hash_shift: int, mask: int
) -> int:
    """Sample reduction and return hashed bucket index."""
    A_basis = sample_lagrangian_basis(n, rng, table)
    x = rng.randint(0, (1 << n) - 1)
    e = 0
    for _ in range(2 * n):
        if rng.random() < 0.25:
            e |= 1 << _

    v = 0
    for j in range(n):
        if (x >> j) & 1:
            v ^= A_basis[j]
    v ^= e

    key = 0
    for i in range(m):
        b = rng.randint(0, (1 << (2 * n)) - 1)
        key <<= n
        c = 0
        for j in range(n):
            if _omega_table(b, A_basis[j], n, table):
                c |= 1 << j
        key |= c
        key <<= 1
        if _omega_table(b, v, n, table):
            key |= 1

    return ((key * hash_mult) >> hash_shift) & mask


def sample_lpn_hash(
    n: int, m: int, p: float, rng: random.Random, hash_mult: int, hash_shift: int, mask: int
) -> int:
    """Sample LPN and return hashed bucket index."""
    x = rng.randint(0, (1 << n) - 1)
    c_rows = [rng.randint(0, (1 << n) - 1) for _ in range(m)]
    key = 0
    for i in range(m):
        key <<= n
        key |= c_rows[i]
        key <<= 1
        bit = (c_rows[i] & x).bit_count() & 1
        if rng.random() < p:
            bit ^= 1
        key |= bit
    return ((key * hash_mult) >> hash_shift) & mask


# ---------------------------------------------------------------------------
# Exact coarse (rank, membership) total variation
# ---------------------------------------------------------------------------

def rank_distribution(m: int, n: int) -> list[Fraction]:
    """Return P(rank=r) for a uniform m x n matrix over F_2, r=0..n."""
    total = Fraction(1 << (m * n))
    probs = []
    for r in range(n + 1):
        num = Fraction(1)
        for i in range(r):
            num *= Fraction((1 << m) - (1 << i)) * Fraction((1 << n) - (1 << i))
        den = Fraction(1)
        for i in range(r):
            den *= Fraction((1 << r) - (1 << i))
        probs.append(num / den / total)
    return probs


def exact_coarse_tv(n: int, m: int) -> tuple[float, list[dict]]:
    """Exact TV over the (rank(C), 1{y in col(C)}) partition.

    For P_out: conditional on rank(C)=r, the graph component has y in col(C)
    with probability 1 and the full component with probability 2^{r-m}.  Hence
        P_out(s=1 | r) = q(n) + (1-q(n)) 2^{r-m}.

    For LPN_{p_eff}: conditional on rank(C)=r, y in col(C) iff the noise
    e lands in col(C).  Averaging over all r-dimensional subspaces gives
        f(r,m,p) = ((2^m - 2^r)(1-p)^m + (2^r - 1)) / (2^m - 1).
    """
    p = p_eff_float(n)
    q = float(q_graph_frac(n))
    probs = [float(fr) for fr in rank_distribution(m, n)]
    two_m = 1 << m
    one_minus_p_m = (1 - p) ** m
    tv = 0.0
    details = []
    for r in range(n + 1):
        p_out_s1 = q + (1 - q) * (2 ** r) / two_m
        f_r = ((two_m - 2 ** r) * one_minus_p_m + (2 ** r - 1)) / (two_m - 1)
        diff = probs[r] * abs(p_out_s1 - f_r)
        tv += diff
        details.append(
            {
                "rank": r,
                "P_rank": probs[r],
                "P_out_s1": p_out_s1,
                "P_lpn_s1": f_r,
            }
        )
    return tv, details


# ---------------------------------------------------------------------------
# Estimation and bootstrap
# ---------------------------------------------------------------------------

def empirical_tv(counts1: Counter, n1: int, counts2: Counter, n2: int) -> float:
    keys = set(counts1.keys()) | set(counts2.keys())
    return 0.5 * sum(abs(counts1.get(k, 0) / n1 - counts2.get(k, 0) / n2) for k in keys)


def bootstrap_se(
    counts1: Counter,
    n1: int,
    counts2: Counter,
    n2: int,
    n_bootstrap: int,
    seed: int,
) -> float:
    """Bootstrap standard error of the empirical TV estimate.

    Treats the coarse histograms as multinomial samples and resamples the
    bucket counts.
    """
    keys = sorted(set(counts1.keys()) | set(counts2.keys()))
    p1 = np.array([counts1.get(k, 0) / n1 for k in keys], dtype=np.float64)
    p2 = np.array([counts2.get(k, 0) / n2 for k in keys], dtype=np.float64)
    rng = np.random.default_rng(seed)
    tvs = np.empty(n_bootstrap, dtype=np.float64)
    for i in range(n_bootstrap):
        c1 = rng.multinomial(n1, p1)
        c2 = rng.multinomial(n2, p2)
        tvs[i] = 0.5 * np.sum(np.abs(c1 / n1 - c2 / n2))
    return float(np.std(tvs, ddof=1))


def estimate_rank_member(
    n: int,
    m: int,
    samples: int,
    seed: int,
    n_bootstrap: int,
) -> dict:
    table = _make_omega_table(n)
    rng = random.Random(seed)
    p = p_eff_float(n)

    out_counts = Counter()
    lpn_counts = Counter()
    for _ in range(samples):
        out_counts[sample_reduction_rank_member(n, m, rng, table)] += 1
        lpn_counts[sample_lpn_rank_member(n, m, p, rng)] += 1

    tv = empirical_tv(out_counts, samples, lpn_counts, samples)
    se = bootstrap_se(out_counts, samples, lpn_counts, samples, n_bootstrap, seed + 1)
    exact_tv, exact_details = exact_coarse_tv(n, m)

    return {
        "n": n,
        "m": m,
        "samples": samples,
        "method": "rank-member",
        "p_eff": p,
        "q_graph": float(q_graph_frac(n)),
        "estimated_sd": tv,
        "bootstrap_se": se,
        "exact_coarse_tv": exact_tv,
        "exact_coarse_details": exact_details,
        "out_histogram": {f"r{k[0]}_s{k[1]}": v for k, v in sorted(out_counts.items())},
        "lpn_histogram": {f"r{k[0]}_s{k[1]}": v for k, v in sorted(lpn_counts.items())},
    }


def estimate_hash(
    n: int,
    m: int,
    samples: int,
    seed: int,
    n_bootstrap: int,
    hash_bits: int,
) -> dict:
    table = _make_omega_table(n)
    rng = random.Random(seed)
    p = p_eff_float(n)

    # Random odd 64-bit multiplier; shift extracts the top hash_bits bits.
    hash_mult = random.Random(seed + 7).randint(1, (1 << 64) - 1) | 1
    hash_shift = 64 - hash_bits
    mask = (1 << hash_bits) - 1

    out_counts = Counter()
    lpn_counts = Counter()
    for _ in range(samples):
        out_counts[sample_reduction_hash(n, m, rng, table, hash_mult, hash_shift, mask)] += 1
        lpn_counts[sample_lpn_hash(n, m, p, rng, hash_mult, hash_shift, mask)] += 1

    tv = empirical_tv(out_counts, samples, lpn_counts, samples)
    se = bootstrap_se(out_counts, samples, lpn_counts, samples, n_bootstrap, seed + 1)

    exact_tv, exact_details = exact_coarse_tv(n, m)
    return {
        "n": n,
        "m": m,
        "samples": samples,
        "method": "hash",
        "hash_bits": hash_bits,
        "hash_buckets": 1 << hash_bits,
        "p_eff": p,
        "q_graph": float(q_graph_frac(n)),
        "estimated_sd": tv,
        "bootstrap_se": se,
        "exact_coarse_tv": exact_tv,
        "exact_coarse_details": exact_details,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, required=True, help="secret dimension")
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--samples", type=int, default=10_000_000, help="samples per distribution")
    p.add_argument("--seed", type=int, default=20260614, help="random seed")
    p.add_argument("--bootstrap", type=int, default=2000, help="bootstrap replicates")
    p.add_argument(
        "--method",
        type=str,
        default="both",
        choices=["rank-member", "hash", "both"],
        help="coarse key space method",
    )
    p.add_argument("--hash-bits", type=int, default=14, help="hash bucket bits (for hash method)")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def estimate_both(
    n: int,
    m: int,
    samples: int,
    seed: int,
    n_bootstrap: int,
    hash_bits: int,
) -> dict:
    """Run both the rank-member and hash estimators and return combined results."""
    rank_result = estimate_rank_member(n, m, samples, seed, n_bootstrap)
    hash_result = estimate_hash(n, m, samples, seed, n_bootstrap, hash_bits)
    return {
        "n": n,
        "m": m,
        "samples": samples,
        "method": "both",
        "hash_bits": hash_bits,
        "p_eff": rank_result["p_eff"],
        "q_graph": rank_result["q_graph"],
        "exact_coarse_tv": rank_result["exact_coarse_tv"],
        "rank_member": {
            "estimated_sd": rank_result["estimated_sd"],
            "bootstrap_se": rank_result["bootstrap_se"],
        },
        "hash": {
            "estimated_sd": hash_result["estimated_sd"],
            "bootstrap_se": hash_result["bootstrap_se"],
        },
    }


def main():
    args = parse_args()
    n, m = args.n, args.m

    t0 = time.time()
    if args.method == "rank-member":
        result = estimate_rank_member(n, m, args.samples, args.seed, args.bootstrap)
    elif args.method == "hash":
        result = estimate_hash(n, m, args.samples, args.seed, args.bootstrap, args.hash_bits)
    elif args.method == "both":
        result = estimate_both(n, m, args.samples, args.seed, args.bootstrap, args.hash_bits)
    else:
        raise ValueError(args.method)
    result["time_sec"] = time.time() - t0

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"196-lem-m2-matched-rate-sampling-n{n}-m{m}-{args.method}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
