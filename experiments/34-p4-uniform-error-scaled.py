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
Experiment 34: P4 Uniform-Error LSN Decoder Battery — Scaled to n=6,7
Reduced parameters for feasibility: num_pairs=5, trials=3, m=2000.
n=7 skips Walsh (O(2^{2n} * m) too slow).
"""

import numpy as np
from collections import defaultdict
import time

SEED = 2026060834
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
    return tuple(rows)


def subspace_elems(rows):
    elems = {0}
    for v in rows:
        elems |= {e ^ v for e in elems}
    return elems


def sample_bernoulli(L_elems, n, m, p, rng):
    D = 2 * n
    N = 1 << D
    samples = []
    for _ in range(m):
        x = int(rng.integers(0, N))
        true_label = 1 if x in L_elems else 0
        if true_label == 1:
            y = 0 if rng.random() < p else 1
        else:
            y = 1 if rng.random() < p else 0
        samples.append((x, y))
    return samples


def sample_uniform(L_elems, n, m, p, rng):
    D = 2 * n
    N = 1 << D
    xs = [int(rng.integers(0, N)) for _ in range(m)]
    true_labels = [1 if x in L_elems else 0 for x in xs]
    num_flip = int(m * p)
    flip_idx = set(rng.choice(m, size=num_flip, replace=False))
    labels = [1 - t if i in flip_idx else t for i, t in enumerate(true_labels)]
    return list(zip(xs, labels))


def decode_walsh(samples, n):
    D = 2 * n
    N = 1 << D
    spectrum = np.zeros(N)
    for x, y in samples:
        if y == 1:
            for w in range(N):
                spectrum[w] += (-1) ** bin(x & w).count('1')
    best_w = np.argmax(np.abs(spectrum))
    return best_w


def decode_stress_margin(samples, n):
    pos = [x for x, y in samples if y == 1]
    if len(pos) < 2:
        return None
    score = defaultdict(int)
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            z = pos[i] ^ pos[j]
            o = omega_int(pos[i], pos[j], n)
            score[z] += 1 if o == 0 else -1
    if not score:
        return None
    best_z = max(score, key=lambda k: score[k])
    return best_z


def decode_ml_logistic(samples, n):
    D = 2 * n
    X = np.zeros((len(samples), D))
    y = np.zeros(len(samples))
    for i, (x, label) in enumerate(samples):
        for j in range(D):
            X[i, j] = (x >> j) & 1
        y[i] = label
    lam = 0.1
    XtX = X.T @ X + lam * np.eye(D)
    Xty = X.T @ y
    try:
        w = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return None
    preds = (X @ w) > 0.5
    return float(np.mean(preds == y))


def evaluate_decoder(decoder_fn, samples, L_elems, n):
    result = decoder_fn(samples, n)
    if result is None:
        return 0.0
    if isinstance(result, int):
        return 1.0 if result in L_elems else 0.0
    elif isinstance(result, float):
        return result
    return 0.0


def run_battery(L, n, m, p, num_trials, rng, use_walsh=True):
    L_elems = subspace_elems(L)
    results = {'bernoulli': {}, 'uniform': {}}
    
    decoders = []
    if use_walsh:
        decoders.append(('walsh', decode_walsh))
    decoders.extend([('stress', decode_stress_margin), ('ml', decode_ml_logistic)])
    
    for noise_type, sampler in [('bernoulli', sample_bernoulli), ('uniform', sample_uniform)]:
        scores = {name: [] for name, _ in decoders}
        
        for _ in range(num_trials):
            samples = sampler(L_elems, n, m, p, rng)
            for name, fn in decoders:
                scores[name].append(evaluate_decoder(fn, samples, L_elems, n))
        
        for name, _ in decoders:
            results[noise_type][name] = np.mean(scores[name])
    
    return results


def main():
    print("=" * 76)
    print("Experiment 34: P4 Uniform-Error LSN Battery (Scaled)")
    print(f"seed={SEED}")
    print("=" * 76)
    
    p = 0.10
    m = 2000
    num_pairs = 5
    trials_per_pair = 3
    
    print(f"\nParameters: p={p}, m={m}, num_pairs={num_pairs}, trials={trials_per_pair}")
    
    for n in [3, 4, 5, 6, 7]:
        D = 2 * n
        N = 1 << D
        use_walsh = (n <= 6)
        print(f"\n--- n={n}, N=2^{D}={N} ---")
        
        dec_list = ['stress', 'ml']
        if use_walsh:
            dec_list = ['walsh'] + dec_list
        
        bern = {d: [] for d in dec_list}
        unif = {d: [] for d in dec_list}
        
        t0 = time.time()
        for pair_idx in range(num_pairs):
            L = rand_lagrangian(n, rng)
            results = run_battery(L, n, m, p, trials_per_pair, rng, use_walsh=use_walsh)
            for dec in dec_list:
                bern[dec].append(results['bernoulli'][dec])
                unif[dec].append(results['uniform'][dec])
        elapsed = time.time() - t0
        
        for dec in dec_list:
            b_mean = np.mean(bern[dec])
            u_mean = np.mean(unif[dec])
            print(f"  {dec:8s}: Bernoulli={b_mean:.4f} | Uniform={u_mean:.4f} | delta={u_mean-b_mean:+.4f}")
        print(f"  (elapsed: {elapsed:.1f}s)")
    
    print("\n" + "=" * 76)
    print("Interpretation:")
    print("  |delta| < 0.05 → noise-model-robust")
    print("  Uniform > Bernoulli → uniform noise is weaker")
    print("  Uniform < Bernoulli → uniform noise is stronger")
    print("=" * 76)


if __name__ == "__main__":
    main()
