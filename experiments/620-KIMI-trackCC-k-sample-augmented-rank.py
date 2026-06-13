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

"""620 (Track CC): k-sample augmented-matrix rank statistic for lem:m2.

Track CC asks for a structural statistic *beyond* the min-syndrome-weight W
that uses k reduction samples.  We study the rank of the augmented matrix

    R_k = [ C_1 | y_1 | C_2 | y_2 | ... | C_k | y_k ]

i.e. the k-fold horizontal concatenation of the single-sample augmented
matrices [C_i | y_i].  This is a natural linear-algebraic invariant:
* rank = n  means the noise component is linearly explained by the public
  matrix (the generalisation of the W=0 spike);
* rank < n  captures additional rank collapse from a low-rank B.

For k independent samples drawn with a fresh marginal-uniform B each time,
the k-sample rank is the sum of k independent single-sample ranks.  We
compute the exact distribution of this sum and its statistical distance to
the same statistic under matched-rate LPN.

Key finding (Track CC): even this richer structural statistic does not leak
at a rate bounded away from zero in n.  Its single-sample distinguishing
advantage is driven by the event rank([C|y])=n, whose probability tends to
q_graph(n) = (3/4)^n as m grows; q_graph(n) -> 0.  By the tensorization of
statistical distance, the k-sample advantage is at most k times the
single-sample advantage, so fixed-k structural rank tests are a NO-GO for an
asymptotic lem:m2 break.

Families
--------
* uniform-B-per-A : B ~ Unif(F_2^{m x 2n}) drawn independently for each A
  (and, in the k-sample product model, independently for each sample).

Comparison distribution (L4)
----------------------------
Matched-rate LPN_{p_eff(n)} with
    p_eff(n) = (1 - (1-p)^{2n}) / 2,   p = 1/4.
For n=2 this is 175/512; for n=3 it is 3367/8192.  The LPN target is the
standard product distribution over k independent (C_i, y_i) tuples.  It is
never transformed.

Standing guards
---------------
L1 exact arithmetic: all probabilities are derived from integer counts;
    JSON stores string fractions and SDs are exact Fractions.
L2 J-twist duality: output distribution inspected directly in the (C,y)
    space; no Fourier/J-twist dual rewriting is used.
L3 query-class hygiene: the statistic is the "augmented-matrix rank" on k
    independent samples -- a structural/linear-algebraic distinguisher.  It
    is not an unrestricted full-joint or SQ claim.
L4 never transform the comparison distribution: P_lpn is the standard
    matched-rate LPN k-product; no reweighting or conditioning is applied.

PRE-REGISTER interpretation guards
----------------------------------
* Statistic: rank_F2([C_1|y_1|...|C_k|y_k]).
* Sampling model for k samples: independent fresh B per sample (the natural
  marginal-adaptive model; B may depend on A but is not reused across
  samples).  This makes the k-sample distribution a product.
* Comparison distribution: matched-rate LPN product, never transformed.
* n-axis: n=2 primary, plus an n=3 spot.
* m-axis: small m (2..6 for n=2, 2..4 for n=3).
* k-axis: small k (1..3 for n=2, 1..2 for n=3).
* CLOSURE-GRADE: fixed-n finite computations; asymptotic rate claims are
  labelled EVIDENCE/OPEN.
"""

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    enumerate_lagrangian_bases_n,
    lpn_target_counts_n,
    randomized_uniform_B_counts_n,
)


# ---------------------------------------------------------------------------
# Matched LPN noise rate
# ---------------------------------------------------------------------------

def p_eff(n: int, p: Fraction = Fraction(1, 4)) -> Fraction:
    """Matched per-coordinate output noise rate for ambient noise p."""
    return Fraction(1 - (Fraction(1) - p) ** (2 * n), 2)


# ---------------------------------------------------------------------------
# q_graph(n): probability that e ~ Ber(p)^{2n} lies in a fixed Lagrangian
# ---------------------------------------------------------------------------

def q_graph(n: int, p: Fraction = Fraction(1, 4)) -> Fraction:
    """Return Pr[e in L] for a fixed Lagrangian L <= F_2^{2n}.

    Because Sp(2n,F_2) acts transitively on Lagrangians and the Ber(p)^{2n}
    weight is coordinate-wise, the sum is the same for every Lagrangian.  We
    compute it on the standard Lagrangian spanned by the first n basis
    vectors, where membership simply forces the last n coordinates to be 0.
    """
    return (Fraction(1) - p) ** n


# ---------------------------------------------------------------------------
# Rank of the single-sample augmented matrix [C | y]
# ---------------------------------------------------------------------------

def rank_augmented(m: int, n: int, C_key: int, y: int) -> int:
    """F_2-rank of the m x (n+1) matrix [C | y].

    C_key encodes the m x n matrix C in little-endian column order:
        C_key = c_{n-1} << ((n-1)*m) | ... | c_1 << m | c_0.
    """
    mask = (1 << m) - 1
    cols = [(C_key >> (j * m)) & mask for j in range(n)]
    cols.append(y)
    pivots = {}
    for col in cols:
        x = col & mask
        if x == 0:
            continue
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return len(pivots)


def rank_distribution(m: int, n: int, counts: list[int], denom: int) -> dict[int, Fraction]:
    """Exact distribution of rank([C|y]) from integer counts over (C,y)."""
    size = 1 << ((n + 1) * m)
    mask_y = (1 << m) - 1
    raw = Counter()
    for key in range(size):
        cnt = counts[key]
        if cnt == 0:
            continue
        C_key = key >> m
        y = key & mask_y
        raw[rank_augmented(m, n, C_key, y)] += cnt
    return {r: Fraction(c, denom) for r, c in raw.items()}


# ---------------------------------------------------------------------------
# k-fold convolution for independent samples
# ---------------------------------------------------------------------------

def convolve_k(dist: dict[int, Fraction], k: int) -> dict[int, Fraction]:
    """Return the exact distribution of the sum of k i.i.d. rank draws."""
    cur = {0: Fraction(1)}
    for _ in range(k):
        nxt = Counter()
        for r1, p1 in cur.items():
            for r2, p2 in dist.items():
                nxt[r1 + r2] += p1 * p2
        cur = dict(nxt)
    return cur


def sd_between(d1: dict[int, Fraction], d2: dict[int, Fraction]) -> Fraction:
    """Exact statistical distance between two distributions on the integers."""
    keys = set(d1.keys()) | set(d2.keys())
    return sum(abs(d1.get(k, Fraction(0)) - d2.get(k, Fraction(0))) for k in keys) / 2


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(
    n2_m_max: int = 6,
    n2_k_max: int = 3,
    n3_m_max: int = 4,
    n3_k_max: int = 2,
    output_dir: Path | None = None,
) -> dict:
    results = {
        "track": "CC",
        "experiment": 620,
        "statistic": "rank_F2([C_1|y_1|...|C_k|y_k])",
        "sampling_model": "independent fresh marginal-uniform B per sample (product distribution)",
        "standing_guards": ["L1 exact arithmetic", "L2 J-twist duality", "L3 query-class hygiene", "L4 never transform LPN"],
        "q_graph_formula": "(3/4)^n",
        "tables": [],
    }

    results["tables"].append(
        run_for_n(2, n2_m_max, n2_k_max, enumerate_lagrangian_bases())
    )
    results["tables"].append(
        run_for_n(3, n3_m_max, n3_k_max, enumerate_lagrangian_bases_n(3))
    )

    if output_dir is None:
        output_dir = Path("experiments/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / (
        f"620-trackCC-k-sample-augmented-rank-"
        f"n2m{n2_m_max}k{n2_k_max}-n3m{n3_m_max}k{n3_k_max}.json"
    )
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)
    return results


def run_for_n(n: int, m_max: int, k_max: int, bases) -> dict:
    """Compute exact rank-sum laws for one value of n."""
    p = p_eff(n)
    qg = q_graph(n)
    table = {
        "n": n,
        "p_eff": str(p),
        "q_graph(n)": str(qg),
        "float_q_graph": float(qg),
        "rows": [],
    }

    for m in range(2, m_max + 1):
        print(f"n={n}, m={m}", file=sys.stderr)
        red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
        lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)

        red_rank = rank_distribution(m, n, red_counts, red_denom)
        lpn_rank = rank_distribution(m, n, lpn_counts, lpn_denom)

        row = {
            "m": m,
            "single_sample": {
                "reduction": frac_dict(red_rank),
                "lpn": frac_dict(lpn_rank),
                "sd_rank": str(sd_between(red_rank, lpn_rank)),
                "sd_rank_float": float(sd_between(red_rank, lpn_rank)),
            },
            "k_sample": [],
        }

        for k in range(2, k_max + 1):
            red_k = convolve_k(red_rank, k)
            lpn_k = convolve_k(lpn_rank, k)
            sd_k = sd_between(red_k, lpn_k)
            row["k_sample"].append({
                "k": k,
                "sd_rank_sum": str(sd_k),
                "sd_rank_sum_float": float(sd_k),
                "upper_bound_k_times_single": str(
                    min(Fraction(1), k * sd_between(red_rank, lpn_rank))
                ),
            })

        table["rows"].append(row)

    return table


def frac_dict(d: dict[int, Fraction]) -> dict[str, str]:
    """Serialize a distribution with integer keys to string fractions."""
    return {str(k): str(v) for k, v in sorted(d.items())}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Track CC: k-sample augmented-matrix rank")
    parser.add_argument("--n2-m-max", type=int, default=6)
    parser.add_argument("--n2-k-max", type=int, default=3)
    parser.add_argument("--n3-m-max", type=int, default=4)
    parser.add_argument("--n3-k-max", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    results = run_experiment(
        n2_m_max=args.n2_m_max,
        n2_k_max=args.n2_k_max,
        n3_m_max=args.n3_m_max,
        n3_k_max=args.n3_k_max,
        output_dir=args.output_dir,
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
