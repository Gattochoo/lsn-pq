#!/usr/bin/env python3
"""R2a: LSN sample-complexity brute-force for n=3 (fast)."""
import itertools, random, json, time

def symplectic_form(x, y, n):
    s = 0
    for i in range(n):
        s ^= (((x >> (2*i)) & 1) * ((y >> (2*i + 1)) & 1)) ^ (((x >> (2*i + 1)) & 1) * ((y >> (2*i)) & 1))
    return s

def gf2_rank(matrix):
    m = list(matrix)
    rank = 0
    row = 0
    col = max(m).bit_length() if m else 0
    for c in range(col - 1, -1, -1):
        pivot = None
        for r in range(row, len(m)):
            if (m[r] >> c) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        for r in range(len(m)):
            if r != row and ((m[r] >> c) & 1):
                m[r] ^= m[row]
        rank += 1
        row += 1
        if row >= len(m):
            break
    return rank

def basis_is_isotropic(basis, n):
    for i in range(len(basis)):
        for j in range(i, len(basis)):
            if symplectic_form(basis[i], basis[j], n) != 0:
                return False
    return True

def enumerate_lagrangians_fast(n):
    total_dim = 2 * n
    all_v = list(range(1, 2 ** total_dim))
    lagr = []
    seen = set()
    for combo in itertools.combinations(all_v, n):
        if gf2_rank(list(combo)) < n:
            continue
        if not basis_is_isotropic(combo, n):
            continue
        span = {0}
        for v in combo:
            span |= {s ^ v for s in span}
        key = tuple(sorted(span))
        if key in seen:
            continue
        seen.add(key)
        lagr.append(frozenset(span))
    return lagr

def sample_lsn(L_set, m, p, n, total_dim):
    samples = []
    for _ in range(m):
        a = random.randint(0, 2 ** total_dim - 1)
        e = 1 if random.random() < p else 0
        b = (1 if a in L_set else 0) ^ e
        samples.append((a, b))
    return samples

def brute_force_decode(samples, lagrangians):
    best_L = None
    best_score = -1
    for L in lagrangians:
        score = sum(1 for a, b in samples if ((1 if a in L else 0) == b))
        if score > best_score:
            best_score = score
            best_L = L
    return best_L, best_score

def run_trials(n, m, num_trials, p, lagrangians):
    total_dim = 2 * n
    success = 0
    for t in range(num_trials):
        L = random.choice(lagrangians)
        samples = sample_lsn(L, m, p, n, total_dim)
        L_guess, _ = brute_force_decode(samples, lagrangians)
        if L_guess == L:
            success += 1
    return success / num_trials

def main():
    random.seed(42)
    p = 0.25
    n = 3
    print(f"=== n={n} ===")
    t0 = time.time()
    lagrangians = enumerate_lagrangians_fast(n)
    print(f"  Enumerated {len(lagrangians)} Lagrangians in {time.time()-t0:.1f}s")
    expected = 1
    for i in range(1, n+1):
        expected *= (2**i + 1)
    assert len(lagrangians) == expected
    
    base = 2 ** (2 * n)
    m_values = [int(base * r) for r in [0.25, 0.5, 1.0, 2.0, 4.0]]
    print(f"  Testing m values: {m_values}")
    num_trials = 200
    
    success_rates = []
    for m in m_values:
        t0 = time.time()
        rate = run_trials(n, m, num_trials, p, lagrangians)
        elapsed = time.time() - t0
        success_rates.append(rate)
        print(f"    m={m:5d} (ratio={m/base:.2f}*2^{{2n}}): success={rate:.2%} ({elapsed:.1f}s)")
    
    results = {
        n: {
            "m_values": m_values,
            "success_rates": success_rates,
            "num_trials": num_trials,
            "p": p,
            "num_lagrangians": len(lagrangians)
        }
    }
    out = "/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/lsn-experiments/71-lsn-sample-complexity-results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out}")

if __name__ == "__main__":
    main()
