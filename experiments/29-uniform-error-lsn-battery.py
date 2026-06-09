"""
Experiment 29: Uniform-Error LSN Decoder Battery

Context (P4):
- Standard LSN: per-sample Bernoulli noise (i.i.d.)
- Question: does replacing Bernoulli with uniform (exact-count) noise retain hardness?
- Uniform noise: exactly floor(m*p) samples are flipped, chosen uniformly at random
  (gives adversary exact noise count info, slight negative correlation between bits)
- If decoders succeed under uniform noise where they fail under Bernoulli,
  LSN hardness is noise-model-sensitive.

Decoders tested:
1. Walsh / Symplectic Fourier (1st-order)
2. Stress-margin pair (2nd-order)
3. ML classifier (logistic)
4. Random baseline

Run: python3 29-uniform-error-lsn-battery.py
"""

import numpy as np
from collections import defaultdict

SEED = 2026060829
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
    def contains(self, v):
        while v:
            h = v.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                return False
            v ^= r
        return True


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
    """Standard per-sample Bernoulli noise."""
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
    """Uniform noise: exactly floor(m*p) samples flipped."""
    D = 2 * n
    N = 1 << D
    xs = [int(rng.integers(0, N)) for _ in range(m)]
    true_labels = [1 if x in L_elems else 0 for x in xs]
    num_flip = int(m * p)
    flip_idx = set(rng.choice(m, size=num_flip, replace=False))
    labels = [1 - t if i in flip_idx else t for i, t in enumerate(true_labels)]
    return list(zip(xs, labels))


def decode_walsh(samples, n):
    """Walsh-Hadamard decoder: find frequency with max power."""
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
    """Stress-margin pair decoder: score z = a+b by isotropy."""
    D = 2 * n
    N = 1 << D
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
    """Simple logistic regression baseline."""
    D = 2 * n
    N = 1 << D
    # Feature: binary vector of length D
    X = np.zeros((len(samples), D))
    y = np.zeros(len(samples))
    for i, (x, label) in enumerate(samples):
        for j in range(D):
            X[i, j] = (x >> j) & 1
        y[i] = label
    # Ridge regression closed form
    lam = 0.1
    XtX = X.T @ X + lam * np.eye(D)
    Xty = X.T @ y
    try:
        w = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return None
    # Predict
    preds = (X @ w) > 0.5
    return float(np.mean(preds == y))


def evaluate_decoder(decoder_fn, samples, L_elems, n):
    """Evaluate decoder. Returns success metric."""
    result = decoder_fn(samples, n)
    if result is None:
        return 0.0
    if isinstance(result, int):
        # For Walsh: check if result is in L
        return 1.0 if result in L_elems else 0.0
    elif isinstance(result, float):
        return result
    return 0.0


def run_battery(L, n, m, p, num_trials, rng):
    L_elems = subspace_elems(L)
    results = {'bernoulli': {}, 'uniform': {}}
    
    for noise_type, sampler in [('bernoulli', sample_bernoulli), ('uniform', sample_uniform)]:
        walsh_scores = []
        stress_scores = []
        ml_scores = []
        
        for _ in range(num_trials):
            samples = sampler(L_elems, n, m, p, rng)
            walsh_scores.append(evaluate_decoder(decode_walsh, samples, L_elems, n))
            stress_scores.append(evaluate_decoder(decode_stress_margin, samples, L_elems, n))
            ml_scores.append(evaluate_decoder(decode_ml_logistic, samples, L_elems, n))
        
        results[noise_type]['walsh'] = np.mean(walsh_scores)
        results[noise_type]['stress'] = np.mean(stress_scores)
        results[noise_type]['ml'] = np.mean(ml_scores)
    
    return results


def main():
    print("=" * 76)
    print("Experiment 29: Uniform-Error LSN Decoder Battery")
    print(f"seed={SEED}")
    print("=" * 76)
    
    p = 0.10
    m = 5000
    num_pairs = 20
    trials_per_pair = 10
    
    print(f"\nParameters: p={p}, m={m}, num_pairs={num_pairs}, trials={trials_per_pair}")
    print("Comparing Bernoulli vs Uniform noise across decoder families\n")
    
    for n in [3, 4, 5, 6, 7]:
        D = 2 * n
        N = 1 << D
        print(f"\n--- n={n}, N=2^{D}={N} ---")
        
        bern = {'walsh': [], 'stress': [], 'ml': []}
        unif = {'walsh': [], 'stress': [], 'ml': []}
        
        for _ in range(num_pairs):
            L = rand_lagrangian(n, rng)
            results = run_battery(L, n, m, p, trials_per_pair, rng)
            for dec in ['walsh', 'stress', 'ml']:
                bern[dec].append(results['bernoulli'][dec])
                unif[dec].append(results['uniform'][dec])
        
        for dec in ['walsh', 'stress', 'ml']:
            b_mean = np.mean(bern[dec])
            u_mean = np.mean(unif[dec])
            print(f"  {dec:8s}: Bernoulli={b_mean:.4f} | Uniform={u_mean:.4f} | delta={u_mean-b_mean:+.4f}")
    
    print("\n" + "=" * 76)
    print("Interpretation:")
    print("  If Uniform > Bernoulli for any decoder, uniform noise is WEAKER.")
    print("  If Uniform ≈ Bernoulli, LSN hardness is noise-model-ROBUST.")
    print("  If Uniform < Bernoulli, uniform noise is STRONGER (harder).")
    print("=" * 76)


if __name__ == "__main__":
    main()
