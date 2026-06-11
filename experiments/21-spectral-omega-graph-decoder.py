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

r"""
Lane C6 — a 3rd structural decoder family: SPECTRAL on the symplectic-orthogonality graph.

Kimi's symplectic-clique note (clique-drowning) flagged, honest caveat #3: "a decoder that
uses Ω differently (e.g. SPECTRAL methods on the symplectic-orthogonal graph ...) is not ruled
out by this analysis." This tests exactly that named-open route — a genuinely different family
from autocorrelation (pair counts) and greedy-clique (combinatorial search).

Decoder (spectral):
  P = positive-labeled vectors. Graph G on P: edge (v,w) iff Ω(v,w)=0. True members of L are
  mutually Ω-orthogonal (L isotropic) => they form a PLANTED CLIQUE; false positives are random
  (Ω=0 w.p. 1/2) => background ~ G(|P|, 1/2). Recover the planted clique spectrally: top
  eigenvector of the centered adjacency M = A − ½(J−I) concentrates on the clique. Rank vertices
  by that eigenvector; greedily build an ISOTROPIC F₂ span from the top-ranked vertices (add v
  iff it stays Ω-orthogonal to the accepted set AND raises rank); stop at rank n; accept iff
  isotropic rank-n; exact recovery = span == L.

★ Calibration guard (avoid "weak tool failing ≠ hardness", check #13): the decoder MUST recover
at clean/low-noise (else its poly-sample failure is meaningless). We calibrate at p=0 (full) and
p=0.02/0.05 (half-obs) before reading the p=0.10 sweep.

Run: python3 21-spectral-omega-graph-decoder.py
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
        x = v
        while x:
            h = x.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                self.piv[h] = x
                return True
            x ^= r
        return False

    def rank(self):
        return len(self.piv)


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


def bits_matrix(ints, D):
    """rows = vectors as bit arrays (len D), low bit first."""
    out = np.zeros((len(ints), D), dtype=np.int8)
    for i, v in enumerate(ints):
        for b in range(D):
            out[i, b] = (v >> b) & 1
    return out


def spectral_decode(P_ints, n, L_xb):
    """spectral Ω-graph decoder. Returns True iff exact recovery (span == L)."""
    D = 2 * n
    if len(P_ints) < n:
        return False
    Pm = bits_matrix(P_ints, D)
    top = Pm[:, :n].astype(np.int64)
    bot = Pm[:, n:].astype(np.int64)
    gram = (top @ bot.T + bot @ top.T) % 2           # Ω(v_i,v_j)
    A = (1 - gram).astype(np.float64)                # edge iff Ω=0
    np.fill_diagonal(A, 0.0)
    N = A.shape[0]
    M = A - 0.5 * (np.ones((N, N)) - np.eye(N))      # centered adjacency
    # top eigenvector
    w, V = np.linalg.eigh(M)
    u = V[:, -1]
    if u.sum() < 0:
        u = -u                                        # orient toward the clique (positive mass)
    order = np.argsort(-u)                            # high eigenvector weight first
    # greedily build an isotropic F₂ span from top-ranked vertices
    basis = XorBasis()
    accepted = []
    for idx in order:
        v = P_ints[idx]
        if v == 0:
            continue
        if all(omega_int(v, a, n) == 0 for a in accepted):   # keep isotropic
            if basis.add(v):
                accepted.append(v)
                if basis.rank() == n:
                    break
    if basis.rank() != n:
        return False
    # span == L ?  (all accepted in L, and rank n)
    rows = list(basis.piv.values())
    return all(_in_span(L_xb, r) for r in rows)


def _in_span(xb, v):
    x = v
    while x:
        h = x.bit_length() - 1
        r = xb.get(h)
        if r is None:
            return False
        x ^= r
    return True


def L_basis_dict(rows):
    xb = {}
    for v in rows:
        x = v
        while x:
            h = x.bit_length() - 1
            if h in xb:
                x ^= xb[h]
            else:
                xb[h] = x
                break
    return xb


def run_cell(n, secrets, m, p, rng):
    D = 2 * n
    N = 1 << D
    m = min(m, N)
    ok = 0
    for rows, mem in secrets:
        Lxb = L_basis_dict(rows)
        obs = rng.choice(N, size=m, replace=False)
        true = np.fromiter((1 if int(v) in mem else 0 for v in obs), np.int8, count=m)
        flips = (rng.random(m) < p).astype(np.int8)
        P = [int(v) for v in obs[(true ^ flips) == 1]]
        ok += spectral_decode(P, n, Lxb)
    return ok, len(secrets)


def main():
    print("=" * 74)
    print("Lane C6 — spectral Ω-graph decoder (3rd structural family)")
    print(f"seed={SEED}")
    print("=" * 74)

    NS = [4, 5, 6, 7]
    TR = {4: 80, 5: 80, 6: 60, 7: 40}
    secrets = {n: [(r, subspace_elems(r)) for r in (rand_lagrangian(n, rng) for _ in range(TR[n]))]
               for n in NS}

    print("\n[CALIBRATION] (must recover at clean/low-noise, else weak tool -> failure meaningless)")
    print(f"  {'n':>2} {'p=0 full':>10} {'p=.02 half':>11} {'p=.05 half':>11} {'p=.10 half':>11}")
    calib_ok = {}
    for n in NS:
        c0 = run_cell(n, secrets[n], 1 << (2 * n), 0.0, rng)
        c2 = run_cell(n, secrets[n], 1 << (2 * n - 1), 0.02, rng)
        c5 = run_cell(n, secrets[n], 1 << (2 * n - 1), 0.05, rng)
        c10 = run_cell(n, secrets[n], 1 << (2 * n - 1), 0.10, rng)
        calib_ok[n] = (c0[0] / c0[1] > 0.5)
        f = lambda c: f"{c[0]}/{c[1]}"
        print(f"  {n:>2} {f(c0):>10} {f(c2):>11} {f(c5):>11} {f(c10):>11}")
    passed = all(calib_ok.values())
    print(f"  calibration (p=0 full recovers >50%): {'PASS' if passed else 'FAIL (weak tool)'}")

    print("\n[SWEEP] p=0.10, exact recovery vs m (SPARSE = m/2^n < 1)")
    for n in NS:
        D = 2 * n
        ms = sorted({1 << (2 * n - 1), 1 << n, 1 << (n - 1), 1 << (n - 2), n * n}, reverse=True)
        print(f"  n={n} (2^n={1<<n}):")
        for m in ms:
            if m < 1 or m > (1 << D):
                continue
            ok, T = run_cell(n, secrets[n], m, 0.10, rng)
            ratio = m / (1 << n)
            mark = "SPARSE" if ratio < 1 else ""
            print(f"     m={m:>6} (m/2^n={ratio:>6.2f}) {mark:>7}  {ok}/{T}")

    print("\n  Verdict: if calibration PASSED and every SPARSE (m/2^n<1) cell is 0, the spectral")
    print("  Ω-graph decoder (3rd family) ALSO obeys the wall at poly-sample constant rate --")
    print("  confirming the closure is not specific to autocorrelation/clique. If a SPARSE cell")
    print("  recovers, that is a ★REDUCES flag (≈0): re-verify 10x and escalate. If calibration")
    print("  FAILED, this decoder is too weak to be informative (weak tool ≠ hardness).")


if __name__ == "__main__":
    main()
