#!/usr/bin/env python3
"""155: CLAUDE check of Kimi OP8-final §3(i) claim.

Kimi §3(i): "their noisy codeword w = [A|B][r;y]+e is uniform over F_2^{2n}
(since [A|B] is full-rank and r is uniform), so marginal uniformity is
satisfiable: we can set a_i = w_i."

Claim under test: for a FIXED public [A|B] and FIXED secret y, with r~Unif(F_2^n)
and e small depolarizing noise, is w marginally uniform over F_2^{2n}?

Linear-algebra prediction: NO. With y fixed and only r varying, the noiseless
part A·r + B·y lives in the n-dim affine coset colspan(A) + B·y (2^n points),
not all of F_2^{2n} (2^{2n} points). Full-rank [A|B] would give uniformity only
if the WHOLE [r;y] ranged over F_2^{n+k}; fixing y kills that.

We enumerate n=2,3 (fixed isotropic A, full-rank [A|B], fixed y), tabulate the
support of w with e=0 and with small depolarizing e, and report support size vs
ambient 2^{2n}.
Output: experiments/155-CLAUDE-op8-locus-i-uniformity-check.json
"""
import json, itertools

def popcount(x): return bin(x).count("1")

def make_omega(n):
    mask = (1 << n) - 1
    def omega(u, v):
        ua, ub = u & mask, u >> n
        va, vb = v & mask, v >> n
        return (popcount(ua & vb) ^ popcount(ub & va)) & 1
    return omega

def find_isotropic_basis(n):
    """greedy: n vectors in F_2^{2n}, pairwise symplectic-orthogonal, independent."""
    omega = make_omega(n)
    N = 2 * n
    basis = []
    def indep(vs, w):
        # gaussian check over F_2
        rows = list(vs) + [w]
        piv = []
        mat = rows[:]
        r = 0
        cols = 2 * n
        mm = mat[:]
        # rank by elimination
        tmp = mm[:]
        rank = 0
        used = [False]*len(tmp)
        for c in range(cols):
            prow = None
            for i in range(len(tmp)):
                if not used[i] and (tmp[i] >> c) & 1:
                    prow = i; break
            if prow is None: continue
            used[prow] = True; rank += 1
            for i in range(len(tmp)):
                if i != prow and (tmp[i] >> c) & 1:
                    tmp[i] ^= tmp[prow]
        return rank == len(rows)
    for v in range(1, 1 << N):
        if all(omega(v, b) == 0 for b in basis) and (not basis or indep(basis, v)):
            basis.append(v)
            if len(basis) == n:
                break
    return basis  # list of n column-vectors (as ints in F_2^{2n})

def find_B(n, A_cols):
    """find k=1 column b s.t. [A|b] full rank (b independent of colspan(A))."""
    N = 2 * n
    def rank(vs):
        tmp = list(vs); used=[False]*len(tmp); r=0
        for c in range(N):
            p=None
            for i in range(len(tmp)):
                if not used[i] and (tmp[i]>>c)&1: p=i;break
            if p is None: continue
            used[p]=True; r+=1
            for i in range(len(tmp)):
                if i!=p and (tmp[i]>>c)&1: tmp[i]^=tmp[p]
        return r
    base_rank = rank(A_cols)
    for b in range(1, 1 << N):
        if rank(A_cols + [b]) == base_rank + 1:
            return b
    return None

def depol_noise_support(n, p_weight_cap=2):
    """all e with symplectic weight (#nonzero qubit-blocks*... ) small; here
    enumerate all e of Hamming weight <= cap as a proxy for low-noise support."""
    N = 2 * n
    out = []
    for e in range(1 << N):
        if popcount(e) <= p_weight_cap:
            out.append(e)
    return out

out = {"experiment": "155-CLAUDE-op8-locus-i-uniformity-check",
       "claim_under_test": "Kimi OP8-final §3(i): w uniform over F_2^{2n} for fixed y",
       "results": []}

for n in (2, 3):
    N = 2 * n
    A = find_isotropic_basis(n)
    b = find_B(n, A)
    y = 1  # fixed secret bit (k=1)
    By = b if y else 0
    # noiseless support: { A·r + B·y : r in F_2^n }
    colspanA = set()
    for r in range(1 << n):
        v = 0
        for i in range(n):
            if (r >> i) & 1:
                v ^= A[i]
        colspanA.add(v)
    noiseless_support = set(v ^ By for v in colspanA)
    # with small noise: union over e of (noiseless + e)
    noise_es = depol_noise_support(n, p_weight_cap=2)
    noisy_support = set()
    for w0 in noiseless_support:
        for e in noise_es:
            noisy_support.add(w0 ^ e)
    out["results"].append({
        "n": n, "ambient_2^{2n}": 1 << N,
        "A_cols": A, "B_col": b, "y_fixed": y,
        "noiseless_support_size": len(noiseless_support),
        "noiseless_expected_2^n": 1 << n,
        "noiseless_is_uniform": len(noiseless_support) == (1 << N),
        "noisy_support_size_wt<=2": len(noisy_support),
        "noisy_is_uniform": len(noisy_support) == (1 << N),
        "verdict": ("NOT uniform — w confined to n-dim coset (+noise); "
                    "Kimi §3(i) 'uniform since full-rank & r uniform' is FALSE")
                   if len(noiseless_support) < (1 << N) else "uniform",
    })

with open("experiments/155-CLAUDE-op8-locus-i-uniformity-check.json", "w") as f:
    json.dump(out, f, indent=1)

for r in out["results"]:
    print(f"n={r['n']}: ambient={r['ambient_2^{2n}']}, "
          f"noiseless support={r['noiseless_support_size']} (=2^n={r['noiseless_expected_2^n']}), "
          f"uniform={r['noiseless_is_uniform']}; "
          f"noisy(wt<=2) support={r['noisy_support_size_wt<=2']}, uniform={r['noisy_is_uniform']}")
    print("  ->", r["verdict"])
