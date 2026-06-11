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

"""
92e — A5 n-scaling reconciled summary.

Reconciles 90 (full n=5), 92c (subset sweep n=5), 92 (100K n=6), 92d (200K n=6).
Key finding: subset-size inflation is the dominant source of discrepancy.
- n=5 full (32,768): c = δ·2^n/m ≈ 0.03
- n=5 10K subset (30%): c ≈ 0.05 (1.7× inflation)
- n=5 1K subset (3%): c ≈ 0.10 (3.3× inflation)
- n=6 200K subset (10%): c ≈ 0.015
- n=6 100K subset (5%): c ≈ 0.017

Extrapolated n=6 full: c ≈ 0.01–0.02.
The n=5→n=6 ratio is ≈ 2–3×, consistent with δ∝2^{-n} up to a prior-dependent constant.

Output: JSON + human-readable summary.
"""
import json

data = {
    "n5_full": {
        "n": 5,
        "subset_size": 32768,
        "subset_fraction": 1.0,
        "results": [
            {"m": 8, "delta_over_m": 0.00112, "c": 0.036},
            {"m": 12, "delta_over_m": 0.00109, "c": 0.035},
            {"m": 16, "delta_over_m": 0.00096, "c": 0.031},
            {"m": 20, "delta_over_m": 0.00095, "c": 0.030},
            {"m": 24, "delta_over_m": 0.00094, "c": 0.030},
        ]
    },
    "n5_10k": {
        "n": 5,
        "subset_size": 10000,
        "subset_fraction": 0.305,
        "results": [
            {"m": 8, "delta_over_m": 0.00146, "c": 0.047},
            {"m": 12, "delta_over_m": 0.00132, "c": 0.042},
            {"m": 16, "delta_over_m": 0.00115, "c": 0.037},
            {"m": 20, "delta_over_m": 0.00112, "c": 0.036},
            {"m": 24, "delta_over_m": 0.00102, "c": 0.033},
        ]
    },
    "n6_200k": {
        "n": 6,
        "subset_size": 200000,
        "subset_fraction": 0.095,
        "results": [
            {"m": 8, "delta_over_m": 0.000373, "c": 0.024},
            {"m": 16, "delta_over_m": 0.000280, "c": 0.018},
            {"m": 24, "delta_over_m": 0.000235, "c": 0.015},
            {"m": 32, "delta_over_m": 0.000202, "c": 0.013},
            {"m": 40, "delta_over_m": 0.000199, "c": 0.013},
            {"m": 48, "delta_over_m": 0.000179, "c": 0.011},
        ]
    },
    "reconciliation": {
        "finding": "Subset-size inflation is the dominant source of discrepancy between 90 and 92.",
        "n5_full_c": 0.03,
        "n6_extrapolated_full_c": 0.01,
        "scaling_law": "delta ≈ c · m · 2^{-n}",
        "c_range": "0.01–0.03 for full population; 0.01–0.10 depending on subset size",
        "chi_squared_upper_bound": 0.7,
    },
    "security_implication": "At n=65, m=22528, delta <= 2^{-50} — negligible enrichment."
}

with open("experiments/92e-nscaling-reconciled.json", "w") as f:
    json.dump(data, f, indent=2)

print("=" * 60)
print("A5 n-scaling reconciled summary")
print("=" * 60)
print()
print("Subset-size effect:")
print("  n=5 full (100%):  c ≈ 0.030")
print("  n=5 30% subset:   c ≈ 0.042 (+40%)")
print("  n=5 3% subset:    c ≈ 0.100 (+230%)")
print()
print("n=6 (corrected for subset effect):")
print("  200K subset (10%): c ≈ 0.015")
print("  Extrapolated full: c ≈ 0.01–0.02")
print()
print("Reconciled scaling law:")
print("  delta ≈ c · m · 2^{-n}")
print("  Full-population c: 0.01–0.03 (prior-dependent)")
print("  Chi-squared upper bound: c ≈ 0.7")
print()
print("Saved to experiments/92e-nscaling-reconciled.json")
