#!/usr/bin/env python3
"""Debug Lagrangian generation for n=2."""

from itertools import combinations

def wt(v):
    return v.bit_count()

def omega(v, vp, n):
    a = v & ((1 << n) - 1)
    b = v >> n
    x = vp & ((1 << n) - 1)
    y = vp >> n
    return ((a & y).bit_count() + (b & x).bit_count()) & 1

def generate_lagrangians(n):
    N = 1 << (2 * n)
    all_vectors = list(range(N))
    
    def is_isotropic(S):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if omega(S[i], S[j], n) != 0:
                    return False
        return True
    
    def closure(S):
        S = set(S)
        changed = True
        while changed:
            changed = False
            current = list(S)
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    s = current[i] ^ current[j]
                    if s not in S:
                        S.add(s)
                        changed = True
        return sorted(S)
    
    def rank(vecs, n):
        m = len(vecs)
        if m == 0:
            return 0
        M = [list(map(int, format(v, f'0{2*n}b'))) for v in vecs]
        r = 0
        for col in range(2 * n):
            pivot = None
            for i in range(r, m):
                if M[i][col] == 1:
                    pivot = i
                    break
            if pivot is None:
                continue
            M[r], M[pivot] = M[pivot], M[r]
            for i in range(m):
                if i != r and M[i][col] == 1:
                    for j in range(col, 2 * n):
                        M[i][j] ^= M[r][j]
            r += 1
            if r == m:
                break
        return r
    
    lagrangians = []
    for basis in combinations(range(1, N), n):
        if not is_isotropic(basis):
            continue
        closed = closure(basis)
        if len(closed) != (1 << n):
            continue
        if rank(closed, n) != n:
            continue
        lagrangians.append(tuple(closed))
    
    return list(set(lagrangians))

n = 2
lags = generate_lagrangians(n)
print(f"n={n}, num_lagrangians={len(lags)}")
for i, N in enumerate(lags[:3]):
    print(f"  L{i}: {N}")
