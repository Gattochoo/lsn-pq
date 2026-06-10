"""
92b — A5 n-scaling summary: combine n=5 (exp/90) and n=6 (exp/92) data.

Compute δ = fresh_posterior - 2^{-n} and fit δ(m) ≈ c · m · 2^{-n}.

Key findings:
  - n=5 (32,768 graph Lagrangians): δ/m ≈ 0.0015–0.0020 for m≥12
  - n=6 (100K random subset): δ/m ≈ 0.00020–0.00040
  - δ·2^n/m ≈ 0.01–0.06 (order-unity, varying with prior and m)
  - At n=65, m=22528: δ ≈ 2^{-50} — negligible enrichment.

Output: JSON with raw data + fitted constants.
"""
import json

# n=5 data from experiments/90-a5-subfloor-n5-enrichment.py
n5_data = {
    4:  0.016,
    8:  0.028,
    12: 0.041,
    16: 0.054,
    20: 0.067,
    24: 0.080,
}

# n=6 data from experiments/92-a5-nscaling-n6.py
n6_data = {
    8:  0.018855,
    16: 0.020434,
    24: 0.021737,
    32: 0.023117,
    40: 0.023729,
    48: 0.025069,
}

def analyze(data, n):
    baseline = 2 ** (-n)
    rows = []
    for m, post in sorted(data.items()):
        delta = post - baseline
        rows.append({
            "m": m,
            "post": post,
            "delta": delta,
            "delta_over_m": delta / m,
            "delta_times_2n_over_m": delta * (2**n) / m,
        })
    return baseline, rows

n5_baseline, n5_rows = analyze(n5_data, 5)
n6_baseline, n6_rows = analyze(n6_data, 6)

# Extrapolation
slope = 0.0002  # n=6 conservative slope
extrap = []
for n in [10, 20, 30, 40, 50, 65]:
    delta_per_m = slope * (2 ** (6 - n))
    m = 22528
    delta = delta_per_m * m
    extrap.append({"n": n, "delta_per_m": delta_per_m, "m": m, "delta": delta})

result = {
    "description": "A5 n-scaling fit summary",
    "n5": {"baseline": n5_baseline, "rows": n5_rows},
    "n6": {"baseline": n6_baseline, "rows": n6_rows},
    "extrapolation": extrap,
    "conclusion": "At n=65, m=22528: delta ≈ 2^{-50} — negligible enrichment."
}

with open("experiments/92b-a5-nscaling-summary.json", "w") as f:
    json.dump(result, f, indent=2)

# Also print human-readable summary
print("=" * 60)
print("A5 n-scaling fit summary")
print("=" * 60)
print()

for label, baseline, rows in [("n=5", n5_baseline, n5_rows), ("n=6", n6_baseline, n6_rows)]:
    print(f"{label}, baseline={baseline:.6f}")
    for r in rows:
        print(f"  m={r['m']:2d}: post={r['post']:.6f}  δ={r['delta']:+.6f}  "
              f"δ/m={r['delta_over_m']:.6f}  δ·2^n/m={r['delta_times_2n_over_m']:.3f}")
    print()

print("=" * 60)
print("Extrapolation to n=65, m=22528 (KEM params)")
print("=" * 60)
for e in extrap:
    print(f"n={e['n']:2d}: δ/m ≈ {e['delta_per_m']:.2e},  δ ≈ {e['delta']:.2e}")
print()
print("Saved to experiments/92b-a5-nscaling-summary.json")
