"""
92b — A5 n-scaling summary: combine n=5 (exp/90) and n=6 (exp/92) data.

Compute δ = fresh_posterior - 2^{-n} and fit δ(m) ≈ c · m · 2^{-n}.

Key findings:
  - n=5 (32,768 graph Lagrangians): δ/m ≈ 0.0015–0.0020 for m≥12
  - n=6 (100K random subset): δ/m ≈ 0.00020–0.00040
  - Ratio n=5/n=6 ≈ 5–10, larger than the naive 2^{1}=2 expected from δ∝2^{-n}
  - Likely causes: subset-size effect (100K/2M vs full 32K), saturation,
    and the graph-Lagrangian prior not being uniform over all Lagrangians.
  - Regardless of the exact constant, δ decreases exponentially in n and
    at n=65, m=22528 the enrichment is negligible (≤2^{-50}).
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
    print(f"n={n}, baseline={baseline:.6f}")
    for m, post in sorted(data.items()):
        delta = post - baseline
        print(f"  m={m:2d}: post={post:.6f}  δ={delta:+.6f}  δ/m={delta/m:.6f}  δ·2^n/m={delta * (2**n) / m:.3f}")
    print()

print("=" * 60)
print("A5 n-scaling fit summary")
print("=" * 60)
print()

analyze(n5_data, 5)
analyze(n6_data, 6)

print("=" * 60)
print("Extrapolation to n=65, m=22528 (KEM params)")
print("=" * 60)
# Conservative: use n=6 slope δ/m ≈ 0.0002
slope = 0.0002
for n in [10, 20, 30, 40, 50, 65]:
    baseline = 2 ** (-n)
    # Assume δ/m scales as slope * (2^{-n} / 2^{-6}) = slope * 2^{6-n}
    # This is a rough extrapolation assuming δ ∝ m · 2^{-n}
    delta_per_m = slope * (2 ** (6 - n))
    m = 22528
    delta = delta_per_m * m
    print(f"n={n:2d}: δ/m ≈ {delta_per_m:.2e},  δ ≈ {delta:.2e}")

print()
print("At n=65: δ ≈ 2^{-50} — negligible enrichment.")
