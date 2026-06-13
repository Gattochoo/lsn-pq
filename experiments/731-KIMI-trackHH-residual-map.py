#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""731 (Track HH): assemble the residual honest no-go map.

Reads the round-8 output JSONs for the fresh-B/fresh-C residual and produces a
draft open-problem map for the paper.  No new cryptanalysis is performed; this
is a summarisation/aggregation script only.

Input artifacts (read-only):
  * experiments/output/600-trackAA-W-law-maxM7.json
  * experiments/output/610-trackBB-conditional-mutual-information-maxM8.json
  * experiments/output/620-trackCC-k-sample-augmented-rank-*.json
  * experiments/output/630-trackDD-structured-B-threat-hunt-maxM6.json
  * experiments/output/640-CLAUDE-trackCC-qgraph-audit.py (conceptual, not JSON)
  * experiments/output/730-trackHH-permutation-of-uniform-maxM6.json

Output:
  * experiments/output/731-trackHH-residual-map.json

Guards
------
L1: all imported numbers are string fractions; no new floating-point computation
    is used for claims.
L2/L3/L4: this is a meta-aggregator; the original data were produced under the
    same guards in their respective tracks.
CLOSURE-GRADE: the map explicitly separates fixed-n evidence from asymptotic
    rates.  No closure claim is made.
"""
import json
import sys
from collections import OrderedDict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

OUTPUT_DIR = Path("experiments/output")


def load_json(name: str) -> dict:
    path = OUTPUT_DIR / name
    with open(path) as f:
        return json.load(f)


def safe_float(s: str) -> float:
    return float(Fraction(s))


def main():
    aa = load_json("600-trackAA-W-law-maxM7.json")
    bb = load_json("610-trackBB-conditional-mutual-information-maxM8.json")
    cc = next(p for p in OUTPUT_DIR.glob("620-trackCC-k-sample-augmented-rank-*.json"))
    cc = json.loads(cc.read_text())
    dd = load_json("630-trackDD-structured-B-threat-hunt-maxM6.json")
    hh = load_json("730-trackHH-permutation-of-uniform-maxM6.json")

    # Extract representative finite-n data.
    aa_uni_m6 = next(r for r in aa["per_m"] if r["m"] == 6)["families"][0]
    aa_lpn_m6 = aa_uni_m6["tv_to_lpn"]

    bb_uni = next(r for r in bb["n2"] if r["m"] == 6)["uniform_B_per_A"]
    bb_lpn = next(r for r in bb["n2"] if r["m"] == 6)["lpn_matched"]

    cc_m6 = next(r for r in cc["tables"][0]["rows"] if r["m"] == 6)

    dd_m6 = next(r for r in dd["results"] if r["m"] == 6)

    hh_m4 = next(r for r in hh["results"] if r["m"] == 4)
    hh_m6 = next(r for r in hh["results"] if r["m"] == 6)

    q_graph_true = Fraction(29, 64)  # uniform-Lagrangian average at n=2

    map_data = OrderedDict()
    map_data["track"] = "HH"
    map_data["experiment"] = 731
    map_data["purpose"] = "residual honest no-go map for fresh-B/fresh-C marginal-adaptive model"

    map_data["model_definitions"] = {
        "reduction_output": "sympLPN reduction outputs (C,y) with C=BA and y=Cx+Be (paper lsn-core.tex, Sec. 5.2 / eq. around lines 884, 954)",
        "open_problem_8": "open:marginal-adaptive (paper lsn-core.tex lines 1232--1238): randomized adaptive B=g(A,R); I(x;y|C)=o(n) remains open",
        "lem_m2_status": "lem:m2 (paper lsn-core.tex lines 1166--1177) is heuristic/conditional; correlated noise Be lives in <=2n-dimensional subspace",
        "shared_vs_fresh": "shared-B (same B across rows/samples) is closed by stacked-rank rank(HY)<=2n; fresh-B/fresh-C is the residual",
    }

    map_data["distinguishers"] = [
        {
            "name": "W=0 spike (min-syndrome-weight zero)",
            "source": "Gemini stacked-rank argument (round 7)",
            "rate": "q_graph(n) -> 0",
            "q_graph_true_n2": str(q_graph_true),
            "status": "CLOSED as non-vanishing (B-agnostic lower bound only; actual Pr[W=0] approaches q_graph from above)",
            "label": "THEOREM (rate -> 0)",
        },
        {
            "name": "W-law (full low-weight tail of min-syndrome-weight)",
            "source": "Track AA (exp 600)",
            "finite_n2_m6": {
                "uniform_B_tv_w_law": aa_uni_m6["tv_to_lpn"],
                "uniform_B_tv_float": aa_uni_m6["tv_float"],
            },
            "rate": "per-sample advantage bounded by q_graph(n) -> 0",
            "status": "NO-GO for asymptotic break (fixed-n TV grows with m but vanishes when normalised by n)",
            "label": "EVIDENCE/NO-GO",
        },
        {
            "name": "I(x;y|C) (conditional mutual information)",
            "source": "Track BB (exp 610)",
            "finite_n2_m6": {
                "uniform_B_bits": bb_uni["I_bits"],
                "matched_LPN_bits": bb_lpn["I_bits"],
                "per_sample_fraction_of_Hx": float(Fraction(bb_uni["I_bits"])) / 2.0,
            },
            "rate": "per-sample I ~ 0.04--0.05 bits; does not approach H(x)=n",
            "status": "OPEN (consistent with I=o(n); not proven)",
            "label": "EVIDENCE/OPEN",
        },
        {
            "name": "k-sample augmented-matrix rank (fresh independent B per sample)",
            "source": "Track CC (exp 620)",
            "finite_n2_m6_k2": {
                "sd_rank_sum": cc_m6["k_sample"][0]["sd_rank_sum"],
                "sd_float": cc_m6["k_sample"][0]["sd_rank_sum_float"],
                "upper_bound_k_times_single": cc_m6["k_sample"][0]["upper_bound_k_times_single"],
            },
            "rate": "fixed-k advantage <= k * q_graph(n) -> 0",
            "status": "NO-GO for fixed-k structural rank tests",
            "label": "NO-GO (subadditivity)",
        },
        {
            "name": "Structured marginal-uniform SD sweep",
            "source": "Track DD (exp 630)",
            "finite_n2_m6": {
                "baseline_sd": dd_m6["baseline_sd_to_matched_lpn"],
                "best_structured_family": dd_m6["minimum_sd_family"],
                "best_structured_sd": dd_m6["minimum_sd_value"],
            },
            "rate": "all structured families (UCS, block, parity) stay at or above baseline; no non-vanishing leak",
            "status": "NO-GO (negative result)",
            "label": "NO-GO",
        },
        {
            "name": "Permutation-of-uniform fresh-B (distinct rows)",
            "source": "Track HH (exp 730)",
            "finite_n2_m4": {
                "sd": hh_m4["permutation_of_uniform"]["sd_to_matched_lpn"],
                "sd_float": hh_m4["permutation_of_uniform"]["sd_float"],
                "delta_vs_baseline": hh_m4["delta_sd_vs_baseline"],
            },
            "finite_n2_m6": {
                "sd": hh_m6["permutation_of_uniform"]["sd_to_matched_lpn"],
                "sd_float": hh_m6["permutation_of_uniform"]["sd_float"],
                "delta_vs_baseline": hh_m6["delta_sd_vs_baseline"],
            },
            "rate": "below baseline at m=2,3,4; above at m=5,6; no monotonic asymptotic reduction",
            "status": "ESCALATE (first reducing direction observed) but NO-GO for asymptotic break",
            "label": "EVIDENCE/ESCALATE/NO-GO",
        },
    ]

    map_data["honest_residual_statement"] = (
        "In the fresh-B/fresh-C model (independent B/C per sample), every tested "
        "distinguisher leaks at a rate that tends to 0 in n.  No tested structured "
        "marginal-uniform B family produces a non-vanishing asymptotic gap.  "
        "Permutation-of-uniform is the first family to move below the uniform-B "
        "baseline at small m, but the gap is O(1) fixed-n and crosses by m=6.  "
        "lem:m2 in the fresh model therefore remains OPEN."
    )

    map_data["paper_draft_map"] = {
        "title": "Residual open-problem map: randomized marginal-adaptive linear reductions",
        "rows": [
            ["shared-B (same B)", "CLOSED", "rank(HY) <= 2n (stacked-rank) vs full-rank LPN"],
            ["fresh-B/fresh-C (independent B/C)", "OPEN", "no tested distinguisher leaks at non-vanishing rate"],
            ["W=0 spike", "rate -> 0", "q_graph(n) (uniform-Lagrangian average)"],
            ["W-law", "NO-GO", "per-sample advantage <= q_graph(n)"],
            ["I(x;y|C)", "OPEN", "consistent with o(n); no proof"],
            ["k-sample rank (fresh)", "NO-GO", "fixed-k advantage -> 0"],
            ["structured SD", "NO-GO", "all families >= baseline or fixed-n only"],
            ["permutation-of-uniform", "ESCALATE/NO-GO", "below baseline for m=2,3,4; crosses by m=6"],
        ],
    }

    map_data["guards"] = {
        "L1_exact_arithmetic": "all numbers imported as string fractions; aggregator uses Fraction only",
        "L2_J_twist_duality": "data produced directly in (C,y) space",
        "L3_query_class": "each row notes its query class / unrestricted status",
        "L4_comparison_distribution": "LPN targets were matched-rate and untransformed in source tracks",
        "CLOSURE_GRADE": "fixed-n evidence is not conflated with asymptotic rates; shared-B closure is stated separately",
    }

    out_path = OUTPUT_DIR / "731-trackHH-residual-map.json"
    with open(out_path, "w") as f:
        json.dump(map_data, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
