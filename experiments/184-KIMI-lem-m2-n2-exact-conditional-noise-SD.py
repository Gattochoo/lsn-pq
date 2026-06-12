#!/usr/bin/env python3
"""184: lem:m2 exact conditional noise SD for n=2.

Enumerate all B in F_2^{m x 4}, all Lagrangian A, and all noise e,
then compute exact SD(P(e' | C), Bernoulli(p')^m).

This runner uses optimized exact integer counting rather than literal
triple enumeration over (A, B, e).  For fixed A and e the linear map
B -> (C=BA, e'=Be) is affine, so the number of B consistent with a
given (C, e') is constant and can be added in bulk.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    apply_matrix,
    enumerate_lagrangian_bases,
)


N = 4  # number of physical bits for n=2


def parse_args():
    """Parse and validate command-line arguments.

    Returns an argparse.Namespace with the original fields plus a validated
    list of p-grid values as Fractions in ``args.p_values``.
    """
    p = argparse.ArgumentParser(
        description="Exact conditional noise SD for lem:m2 with n=2."
    )
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument(
        "--pgrid",
        type=str,
        default="0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5",
        help="comma-separated list of p' values (probabilities)",
    )
    p.add_argument("--output", type=str, default=None, help="output JSON path")
    args = p.parse_args()

    if args.m < 1:
        p.error("--m must be at least 1")

    p_values = []
    for x in args.pgrid.split(","):
        try:
            frac = Fraction(x)
        except Exception:
            p.error(f"invalid probability in --pgrid: {x!r}")
        if not (0 <= frac <= 1):
            p.error(f"--pgrid values must be in [0,1], got {x!r}")
        p_values.append(frac)

    args.p_values = p_values
    return args


def main():
    """Run the exact enumeration and write the results to JSON."""
    args = parse_args()
    m = args.m
    p_values = args.p_values
    bases = list(enumerate_lagrangian_bases())
    num_bases = len(bases)

    # Precompute noise vectors and integer weights 3^{N-w}.
    # P(e) = (1/4)^w (3/4)^{N-w}; clearing the common denominator 4^N
    # gives integer weight 3^{N-w} for each noise vector.
    noise_info = []
    for e in range(1 << N):
        w = e.bit_count()
        noise_info.append((e, 3 ** (N - w)))

    total_weight_per_B = sum(w for _, w in noise_info) * num_bases  # 15 * 4^N = 3840

    num_ep = 1 << m
    num_C = 1 << (2 * m)
    mask = num_ep - 1

    # Sum over all noise vectors of 3^{N-|e|} = (3+1)^N = 4^N.  This is the
    # common denominator of the noise distribution and appears in every per-B SD.
    NOISE_WEIGHT_SUM = 4 ** N

    # Precompute Bernoulli(p)^m as integer numerators q_int[p][ep] / D[p].
    q_int = {}
    D = {}
    for p in p_values:
        D[p] = p.denominator ** m
        q_int[p] = [0] * num_ep
        for ep in range(num_ep):
            w = ep.bit_count()
            q_int[p][ep] = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))

    # Global joint/marginal over all B, accumulated via (A,e) counting.
    # For fixed A and e, the linear constraints BA=C, Be=e' on B have a constant
    # number of solutions for each feasible (C,e'), so we update in bulk.
    global_joint = [0] * (num_C * num_ep)
    global_marginal_C = [0] * num_C

    for a0, a1 in bases:
        span = {0: (0, 0), a0: (1, 0), a1: (0, 1), a0 ^ a1: (1, 1)}
        for e, w_e in noise_info:
            if e in span:
                # e lies in span(A), so e = alpha*a0 + beta*a1.  Then
                # Be = alpha*c0 + beta*c1 is completely determined by C=BA;
                # for each C there is exactly one feasible e'(C).  The 2m free
                # bits of B give 2^{2m} matrices for each (C, e'(C)).
                alpha, beta = span[e]
                count_B = 1 << (2 * m)
                add = count_B * w_e
                for C_key in range(num_C):
                    c0 = C_key >> m
                    c1 = C_key & mask
                    eprime = 0
                    if alpha:
                        eprime ^= c0
                    if beta:
                        eprime ^= c1
                    idx = C_key * num_ep + eprime
                    global_joint[idx] += add
                    global_marginal_C[C_key] += add
            else:
                # e is outside span(A), so Be is independent of C=BA.  For each
                # C every e' in F_2^m is feasible, and the m linear constraints
                # Be=e' leave m free bits in B: 2^m solutions per (C, e').
                count_B = 1 << m
                add = count_B * w_e
                for C_key in range(num_C):
                    base = C_key * num_ep
                    for ep in range(num_ep):
                        global_joint[base + ep] += add
                    global_marginal_C[C_key] += add * num_ep

    # Per-B enumeration: P(e' | C, B) = P(e' | B) because the noise e is
    # independent of A (and therefore of C=BA).  Hence the per-B average
    # conditional SD over C reduces to the unconditional SD(P(e'|B), Q).
    num_B = 1 << (4 * m)
    total_weight = num_B * total_weight_per_B

    best_B = None
    best_avg_sd = Fraction(2)
    worst_avg_sd = Fraction(-1)

    # Accumulate e' marginal for unconditional SD (without the uniform A factor,
    # which is reintroduced when normalising).
    global_uncond_weight = [0] * num_ep

    p25 = Fraction(1, 4)
    D25 = D[p25]
    q25 = q_int[p25]
    denom25 = 2 * NOISE_WEIGHT_SUM * D25

    for bits in range(num_B):
        b0 = bits & mask
        b1 = (bits >> m) & mask
        b2 = (bits >> (2 * m)) & mask
        b3 = (bits >> (3 * m)) & mask
        B_cols = [b0, b1, b2, b3]

        eprime_weight = [0] * num_ep
        for e, w_e in noise_info:
            eprime = apply_matrix(B_cols, e)
            eprime_weight[eprime] += w_e

        for ep in range(num_ep):
            global_uncond_weight[ep] += eprime_weight[ep]

        sd_num = 0
        for ep in range(num_ep):
            sd_num += abs(eprime_weight[ep] * D25 - q25[ep] * NOISE_WEIGHT_SUM)
        avg_sd_p25 = Fraction(sd_num, denom25)

        if avg_sd_p25 < best_avg_sd:
            best_avg_sd = avg_sd_p25
            best_B = B_cols[:]
        if avg_sd_p25 > worst_avg_sd:
            worst_avg_sd = avg_sd_p25

    result = {
        "n": 2,
        "m": m,
        "num_lagrangian": num_bases,
        "num_B": num_B,
        "p_grid": [str(p) for p in p_values],
        "best_B_p25": best_B,
        "best_avg_sd_p25": str(best_avg_sd),
        "worst_avg_sd_p25": str(worst_avg_sd),
    }

    # Conditional SD averaged over C (computed from global aggregates).
    for p in p_values:
        Dp = D[p]
        q = q_int[p]
        sd_sum_num = 0
        for C_key in range(num_C):
            marg = global_marginal_C[C_key]
            if marg == 0:
                continue
            base = C_key * num_ep
            for ep in range(num_ep):
                joint = global_joint[base + ep]
                sd_sum_num += abs(joint * Dp - q[ep] * marg)
        result[f"global_avg_conditional_sd_p{p}"] = str(Fraction(sd_sum_num, 2 * Dp * total_weight))

    # Unconditional SD(P(e'), Q).
    for p in p_values:
        Dp = D[p]
        q = q_int[p]
        # eprime_marginal includes the factor num_bases from summing over A.
        eprime_marginal = [num_bases * w for w in global_uncond_weight]
        sd_num = 0
        for ep in range(num_ep):
            sd_num += abs(eprime_marginal[ep] * Dp - q[ep] * total_weight)
        result[f"global_unconditional_sd_p{p}"] = str(Fraction(sd_num, 2 * Dp * total_weight))

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"184-lem-m2-n2-exact-conditional-noise-SD-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
