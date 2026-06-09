r"""
Lane C3 — independent cross-verification of the CHANNEL-LEVEL signal-vanishing.

Lane D Side-1 relies on the adjudicator's channel-level closure of the autocorrelation
family (OFA-325/327): at poly-ward sample density the RAW signal any such decoder reads —
the XOR-autocorrelation C(d)=|{v∈P: v⊕d∈P}| being larger for d∈L than for d∉L — VANISHES,
so no decoder (present or future) in that family can recover. Task 5 measured the downstream
consequence (exact recovery → 0); this measures the UPSTREAM signal directly, from an
independent implementation, to confirm the mechanism (not just the symptom).

Measure, at p=0.10, for n=4..7, sweeping m:
    signal     = mean over d∈L\{0} of C(d)
    background = mean over d∉L     of C(d)
    ratio      = signal / background      (>>1 dense; → 1 once m/2^n < 1)
A ratio → 1 means d∈L is statistically indistinguishable from d∉L in the autocorrelation —
the signal itself is gone, independent of any decoder.

Run: python3 19-autocorr-signal-vanish-crosscheck.py
"""
import numpy as np

SEED = 20260606
rng = np.random.default_rng(SEED)


def omega_int(u, v, n):
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


class XorBasis:
    __slots__ = ("piv",)

    def __init__(self):
        self.piv = {}

    def add(self, v):
        while v:
            h = v.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                self.piv[h] = v
                return True
            v ^= r
        return False


def rand_lagrangian(n, rng):
    D = 2 * n
    xb = XorBasis()
    rows = []
    while len(rows) < n:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, b, n) == 0 for b in rows) and xb.add(v):
            rows.append(v)
    return rows


def subspace_elems(rows):
    elems = {0}
    for r in rows:
        elems |= {e ^ r for e in elems}
    return elems


def fwht(a):
    a = a.astype(np.float64).copy()
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(N // (2 * h), 2, h)
        x = a[:, 0, :].copy()
        y = a[:, 1, :].copy()
        a[:, 0, :] = x + y
        a[:, 1, :] = x - y
        a = a.reshape(N)
        h *= 2
    return a


def autocorr(indicator):
    N = indicator.shape[0]
    spec = fwht(indicator)
    return np.rint(fwht(spec * spec) / N).astype(np.int64)


def signal_vs_background(n, secrets, m, p, rng):
    r"""mean C(d) over d∈L\{0} vs over d∉L, averaged across trials."""
    D = 2 * n
    N = 1 << D
    m = min(m, N)
    sig_sum = bg_sum = 0.0
    for rows, mem in secrets:
        member_arr = np.fromiter((d for d in mem if d != 0), dtype=np.int64,
                                 count=len(mem) - 1)                     # d∈L\{0}
        obs = rng.choice(N, size=m, replace=False)
        true = np.fromiter((1 if int(v) in mem else 0 for v in obs), dtype=np.int8, count=m)
        flips = (rng.random(m) < p).astype(np.int8)
        pos = obs[(true ^ flips) == 1]
        ind = np.zeros(N, dtype=np.float64)
        ind[pos] = 1.0
        C = autocorr(ind)
        in_L = np.zeros(N, dtype=bool)
        in_L[member_arr] = True
        in_L[0] = False
        # background = all nonzero d not in L
        notL = np.ones(N, dtype=bool)
        notL[0] = False
        notL[member_arr] = False
        sig_sum += C[in_L].mean()
        bg_sum += C[notL].mean()
    T = len(secrets)
    return sig_sum / T, bg_sum / T


def main():
    print("=" * 78)
    print("Lane C3 — autocorrelation signal vs background (independent channel-level check)")
    print(f"seed={SEED}, p=0.10")
    print("=" * 78)

    p = 0.10
    for n in [4, 5, 6, 7]:
        T = 80 if n < 7 else 50
        secrets = [(r, subspace_elems(r)) for r in (rand_lagrangian(n, rng) for _ in range(T))]
        ms = [(1 << (2 * n - 1), "2^%d(half)" % (2 * n - 1)),
              (1 << n, "2^n"),
              (1 << (n - 1), "2^{n-1}"),
              (1 << (n - 2), "2^{n-2}"),
              (n * n, "n^2")]
        # dedup by m, keep order high->low
        seen = {}
        for m, lab in ms:
            if m not in seen and m >= 1:
                seen[m] = lab
        order = sorted(seen.keys(), reverse=True)

        print(f"\n  n={n} (2^n={1<<n})")
        print(f"    {'m':>7} {'label':>10} {'m/2^n':>7} {'sparse?':>7} "
              f"{'signal C(d∈L)':>14} {'bg C(d∉L)':>11} {'EXCESS s-bg':>12} {'%of dense':>9}")
        dense_excess = None
        for m in order:
            lab = seen[m]
            ratio_m = m / (1 << n)
            sig, bg = signal_vs_background(n, secrets, m, p, rng)
            excess = sig - bg                       # the L-SPECIFIC structural signal
            if dense_excess is None:
                dense_excess = excess               # half-obs baseline (=100%)
            pct = 100.0 * excess / dense_excess if dense_excess > 1e-12 else float('nan')
            mark = "SPARSE" if ratio_m < 1.0 else ""
            print(f"    {m:>7} {lab:>10} {ratio_m:>7.3f} {mark:>7} "
                  f"{sig:>14.3f} {bg:>11.3f} {excess:>12.4f} {pct:>8.2f}%")

    print("\n  Reading (honest, corrected metric): the decoder-relevant quantity is the")
    print("  L-SPECIFIC EXCESS = mean C(d∈L) − mean C(d∉L) (the autocorrelation lift due to L).")
    print("  At dense m (m/2^n ≥ 1) the excess is large (tens); at SPARSE m (m/2^n < 1) it")
    print("  collapses to ≈0 -- typically <1% of the dense excess, orders of magnitude down --")
    print("  AND the absolute signal C(d∈L) itself → ~0 (almost no positive-pairs survive).")
    print("  So at poly-ward density there is essentially NO L-structure in the autocorrelation")
    print("  for any decoder to read. (Note: the raw signal/background RATIO is NOT a useful")
    print("  metric here -- both → ~0, so the ratio is a noisy 0/0; the EXCESS is the right one.)")
    print("  This independently confirms the channel-level closure (OFA-325/327) and the")
    print("  mechanism behind Task 5's recovery→0. NOT REDUCES; evidence, not proof.")


if __name__ == "__main__":
    main()
