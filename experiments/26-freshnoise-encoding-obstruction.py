r"""
Lane G (#2) — the fresh-noise-encoding worst→avg route: the precise discrete obstruction.

The adjudicator left ONE open route for a LSN worst→avg (the symmetry/subspace route being
closed by Sp-irreducibility): a Regev-style FRESH-NOISE encoding — add fresh noise to a
worst-case instance to produce average-case samples. This attempts the natural version and
extracts the precise obstruction.

Regev/LWE: adding a discrete GAUSSIAN of width σ ≥ smoothing-parameter maps a worst-case BDD
instance to the (instance-independent) average LWE distribution AT A USABLE rate — because the
Gaussian is a CONTINUOUS, TUNABLE family (you pick σ large enough to smooth yet small enough to
decode). The F₂ analog adds fresh Bernoulli(q) (depolarizing) noise. For the encoding to map a
worst-case error to the average (worst-case-INDEPENDENT) distribution, two worst-case errors
differing by Δ (weight w) must become statistically indistinguishable:
        leak(q,w) := TV( Bern(q)^w ,  Bern(1−q)^w )   →ε ?
This measures leak(q,w) vs q and asks whether any USABLE q (below a decoding threshold p*<1/2)
achieves leak<ε. Prediction (the obstruction): discrete smoothing is ALL-OR-NOTHING — leak→0
only as q→1/2 (unusable), so no usable q smooths. This is the discrete shadow of the C7
self-dual-noise rigidity (the self-dual point = q→1/2).

Run: python3 26-freshnoise-encoding-obstruction.py
"""
import numpy as np
from math import comb


def leak(q, w):
    """TV( Bern(q)^w , Bern(1-q)^w ) = (1/2) Σ_j C(w,j)|q^j(1-q)^{w-j} − q^{w-j}(1-q)^j|."""
    s = 0.0
    for j in range(w + 1):
        a = (q ** j) * ((1 - q) ** (w - j))
        b = (q ** (w - j)) * ((1 - q) ** j)
        s += comb(w, j) * abs(a - b)
    return 0.5 * s


def main():
    print("=" * 74)
    print("Lane G (#2) — fresh-noise-encoding obstruction: discrete smoothing is all-or-nothing")
    print("=" * 74)

    qs = [0.05, 0.10, 0.20, 0.30, 0.40, 0.45, 0.49]
    print("\n  leak(q,w) = TV(Bern(q)^w, Bern(1-q)^w)   (must → 0 to smooth a worst-case diff Δ)")
    print("  (a USABLE encoding needs q below a decoding threshold p* < 1/2, e.g. q ≤ 0.25)")
    print(f"\n  {'w\\q':>5} " + "".join(f"{q:>8.2f}" for q in qs))
    for w in [1, 2, 4, 8]:
        row = "".join(f"{leak(q, w):>8.3f}" for q in qs)
        print(f"  {w:>5} {row}")

    # the smoothing q needed for leak < 0.01, per w; and whether it's usable (q* < 0.25?)
    print("\n  smallest q with leak(q,w) < 0.01  (the q you'd NEED to smooth), vs usable cap 0.25:")
    print(f"  {'w':>3} {'q_smooth(leak<0.01)':>20} {'usable (q_smooth ≤ 0.25)?':>26}")
    for w in [1, 2, 4, 8, 16]:
        qg = None
        for qi in range(1, 500):
            q = qi / 1000.0
            if leak(q, w) < 0.01:
                qg = q
                break
        usable = (qg is not None and qg <= 0.25)
        print(f"  {w:>3} {(f'{qg:.3f}' if qg else '>0.499'):>20} {('YES' if usable else 'NO'):>26}")

    print("\n  Reading: leak(q,w) → 0 only as q → 1/2 (e.g. even w=1 needs q ≈ 0.495 for leak<0.01).")
    print("  A worst-case error difference Δ is smoothed into the average distribution ONLY at")
    print("  near-total noise q→1/2 — which is UNUSABLE for decoding (above every converse). At")
    print("  any usable rate (q ≤ 0.25) the leak is large: the worst-case instance shows through,")
    print("  so the encoded samples are NOT the worst-case-independent average distribution.")
    print("  => the NATURAL (i.i.d. Bernoulli/depolarizing) fresh-noise encoding CANNOT")
    print("  simultaneously smooth AND stay usable. This is the discrete shadow of the C7")
    print("  self-dual-noise rigidity (self-dual point = q→1/2): LWE's Gaussian is a continuous")
    print("  tunable family that smooths at a usable width; F₂ depolarizing is all-or-nothing.")
    print("  HONEST scope: this obstructs the NATURAL fresh-noise encoding; a clever non-i.i.d./")
    print("  correlated ('exotic') encoding is NOT ruled out -- that remains the open ≈0 route.")
    print("  No worst→avg reduction; no 7th; no security claim.")


if __name__ == "__main__":
    main()
