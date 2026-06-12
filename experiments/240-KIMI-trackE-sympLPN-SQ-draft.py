#!/usr/bin/env python3
"""Track E: OP1 SDA/SQ draft for the sympLPN formulation.

Computes exact quantities needed for a paper-grade DRAFT meta note:
- subset moments m_j from thm:mj-general (exact fractions),
- bundle moments V_k from cor:bundle and V_{2n} from prop:vmax,
- sympLPN pairwise correlations for k-row bundle parity queries,
- SDA parameters and Feldman VSTAT bounds.

All arithmetic uses fractions.Fraction.  Output is written as JSON with
string-encoded fractions.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction
from math import comb
from pathlib import Path


# ---------------------------------------------------------------------------
# Moment machinery (thm:mj-general, prop:vmax, cor:bundle)
# ---------------------------------------------------------------------------

def mj_general(n: int, j: int) -> Fraction:
    """Exact j-th subset moment of the isotropic row ensemble (thm:mj-general)."""
    if j == 0:
        return Fraction(1)
    if j > 2 * n:
        return Fraction(0)
    D_j = 2 ** (2 * n - j)
    P = (2 ** (2 * n) - 1) * (2 ** (2 * n - 1) - 2)
    term = Fraction(1, 2) * D_j * D_j - D_j
    even_adjust = Fraction(0)
    if j % 2 == 0:
        even_adjust = Fraction(comb(n, j // 2) * D_j, 2)
    numerator = comb(2 * n, j) * term + even_adjust
    denominator = comb(2 * n, j) * P
    return Fraction(numerator, denominator)


def sigma_sq(p: Fraction) -> Fraction:
    """χ^2 coefficient κ = (1-2p)^2 / (p(1-p))."""
    return Fraction((1 - 2 * p) ** 2, p * (1 - p))


def Vk_bundle(n: int, k: int, p: Fraction) -> Fraction:
    """k-row bundle moment V_k = Σ_j C(k,j) σ^{2j} m_j (cor:bundle)."""
    s2 = sigma_sq(p)
    total = Fraction(0)
    for j in range(k + 1):
        total += Fraction(comb(k, j)) * (s2 ** j) * mj_general(n, j)
    return total


def V2n_closed(n: int, p: Fraction) -> Fraction:
    """Closed form for V_{2n} (prop:vmax)."""
    s2 = sigma_sq(p)
    X = 4 ** n
    P = Fraction((X - 1) * (X - 4), 2)
    term1 = Fraction(X * X, 2) * ((Fraction(1) + s2 / 4) ** (2 * n) - 1)
    term2 = X * ((Fraction(1) + s2 / 2) ** (2 * n) - 1)
    term3 = Fraction(X, 2) * ((Fraction(1) + s2 * s2 / 4) ** n - 1)
    return Fraction(1) + (term1 - term2 + term3) / P


# ---------------------------------------------------------------------------
# SympLPN pairwise correlations
# ---------------------------------------------------------------------------

def tau(p: Fraction) -> Fraction:
    """τ = (1-2p)^2, the LPN likelihood-ratio coefficient per row."""
    return Fraction((1 - 2 * p) ** 2)


def symplpn_diagonal_corr(n: int, p: Fraction) -> Fraction:
    """Likelihood-ratio self-correlation ⟨D_x,D_x⟩ for one sympLPN sample."""
    return (Fraction(1) + tau(p)) ** (2 * n) - 1


def symplpn_offdiag_corr(n: int, p: Fraction) -> Fraction:
    """Likelihood-ratio off-diagonal correlation ⟨D_x,D_x'⟩, x≠x'."""
    return -(symplpn_diagonal_corr(n, p)) / Fraction(2 ** (2 * n) - 1)


def symplpn_offdiag_abs(n: int, p: Fraction) -> Fraction:
    return abs(symplpn_offdiag_corr(n, p))


def average_pairwise_corr_full_secret_space(n: int, p: Fraction) -> Fraction:
    """Average |⟨D_x,D_x'⟩| over all x,x' in F_2^n."""
    N = 2 ** n
    diag = symplpn_diagonal_corr(n, p)
    off = symplpn_offdiag_abs(n, p)
    return Fraction(N * diag + (N * N - N) * off, N * N)


def k_row_bundle_average_corr(n: int, k: int, p: Fraction) -> Fraction:
    """Average |pairwise correlation| of the k-row bundle parity query over all secrets.

    For fixed non-empty S, |S|=k, the diagonal is (1-2p)^{2k} and every
    off-diagonal equals -(1-2p)^{2k}/(2^{2n}-1).  Averaging over F_2^n gives
    (1-2p)^{2k} * (2^n + 2) / [2^n (2^n + 1)].
    """
    d = Fraction((1 - 2 * p) ** (2 * k))
    N = 2 ** n
    return d * Fraction(N + 2, N * (N + 1))


# ---------------------------------------------------------------------------
# SDA / Feldman parameters
# ---------------------------------------------------------------------------

def sda_params(n: int, t: int, p: Fraction) -> dict[str, Fraction]:
    """SDA parameters for subset size 2^{n-t} using full likelihood ratio."""
    subset_size = 2 ** (n - t)
    chi2_self = symplpn_diagonal_corr(n, p)
    chi2_off = symplpn_offdiag_abs(n, p)
    # diagonal-inclusive average absolute correlation
    rho_avg = Fraction(
        subset_size * chi2_self + (subset_size * subset_size - subset_size) * chi2_off,
        subset_size * subset_size,
    )
    # double it to leave slack for Feldman's theorem
    gamma = 2 * rho_avg
    # Feldman: q >= (2α-1)d with α=2/3, and VSTAT(1/(3γ))
    alpha = Fraction(2, 3)
    d = subset_size
    q_lower = (2 * alpha - 1) * d
    vstat_inv = 3 * gamma
    return {
        "subset_size": Fraction(subset_size),
        "rho_avg": rho_avg,
        "gamma": gamma,
        "sda_d": d,
        "query_lower_bound": q_lower,
        "vstat_param_inv": vstat_inv,
    }


def k_bundle_sda_params(n: int, k: int, t: int, p: Fraction) -> dict[str, Fraction]:
    """SDA parameters for k-row bundle parity queries on subset size 2^{n-t}."""
    subset_size = 2 ** (n - t)
    d_per_row = Fraction((1 - 2 * p) ** (2 * k))
    # ρ_avg ≤ 2 d_per_row / subset_size (using 1+(|S|-1)/(2^{2n}-1) ≤ 2)
    gamma = 2 * d_per_row / subset_size
    alpha = Fraction(2, 3)
    d = subset_size
    q_lower = (2 * alpha - 1) * d
    vstat_inv = 3 * gamma
    return {
        "k": k,
        "subset_size": Fraction(subset_size),
        "gamma": gamma,
        "sda_d": d,
        "query_lower_bound": q_lower,
        "vstat_param_inv": vstat_inv,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    p = Fraction(1, 4)
    output: dict[str, dict] = {}

    for n in [2, 3]:
        record: dict[str, str | dict | list] = {}
        record["p"] = str(p)

        # m_j
        record["mj"] = [str(mj_general(n, j)) for j in range(2 * n + 1)]

        # V_k for k=0..2n and closed-form V_{2n}
        record["Vk"] = [str(Vk_bundle(n, k, p)) for k in range(2 * n + 1)]
        record["V2n_closed"] = str(V2n_closed(n, p))
        record["V2n_sum_agrees"] = (
            Vk_bundle(n, 2 * n, p) == V2n_closed(n, p)
        )

        # SympLPN correlations
        record["symplpn"] = {
            "chi2_self": str(symplpn_diagonal_corr(n, p)),
            "chi2_off": str(symplpn_offdiag_corr(n, p)),
            "chi2_off_abs": str(symplpn_offdiag_abs(n, p)),
            "avg_abs_over_F2n": str(average_pairwise_corr_full_secret_space(n, p)),
            "k_row_bundle_avg": {
                str(k): str(k_row_bundle_average_corr(n, k, p))
                for k in range(1, 2 * n + 1)
            },
        }

        # SDA / Feldman for t=0 (full secret space) and t=n-1
        record["sda"] = {
            "t=0": {k: str(v) for k, v in sda_params(n, 0, p).items()},
            "t=n-1": {k: str(v) for k, v in sda_params(n, n - 1, p).items()},
        }

        # k-row bundle SDA for k=1 and full secret space
        record["k_bundle_sda"] = {
            f"k={k}": {kk: str(vv) for kk, vv in k_bundle_sda_params(n, k, 0, p).items()}
            for k in [1, 2]
        }

        output[f"n={n}"] = record

    out_path = Path(__file__).with_suffix("").name
    out_file = Path("experiments/output") / f"{out_path}.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
