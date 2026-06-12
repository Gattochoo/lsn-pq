# lem:m2 n=2 exact conditional noise SD — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a SageMath-backed exact enumeration script that computes, for $n=2$ and small $m$, the conditional statistical distance $\mathrm{SD}(P(e'\mid C), \mathrm{Bernoulli}(p')^m)$ where $e'=Be$ and $C=BA$, over all Lagrangian $A$ and all $B\in\F_2^{m\times 4}$.

**Architecture:** A small reusable helper module (`experiments/lib/lem_m2_exact.py`) handles Lagrangian enumeration, bit-packed matrix arithmetic, and SD computation. A runner script (`experiments/184-...`) enumerates all $(A,B,e)$ triples with integer weights, builds exact joint/marginal distributions, evaluates SD for a grid of $p'$, and saves JSON. Unit tests guard the helper invariants.

**Tech Stack:** Python 3, SageMath 10.9 (`sage -python`), `fractions.Fraction`, `itertools.product`, `collections.Counter`, `json`, `pathlib`.

---

## File Structure

- **Create:** `experiments/lib/lem_m2_exact.py` — helper functions (Lagrangian enumeration, bit ops, SD, Bernoulli product).
- **Create:** `experiments/lib/__init__.py` — make `experiments.lib` a regular package.
- **Create:** `tests/test_lem_m2_exact.py` — unit tests for helper invariants.
- **Create:** `experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py` — main enumeration runner.
- **Create:** `experiments/output/184-lem-m2-n2-exact-conditional-noise-SD.json` — results.
- **Create:** `meta/2026-06-13-KIMI-lem-m2-n2-exact-conditional-noise-SD-DRAFT.md` — interpretation note.

---

## Background Bits (used throughout)

- $n=2$, so $2n=4$. A Lagrangian $A$ is a 2-dimensional isotropic subspace of $\F_2^4$, represented by two column basis vectors $a_0,a_1\in\F_2^4$.
- $B\in\F_2^{m\times 4}$ is represented by four $m$-bit integers $b_0,b_1,b_2,b_3$ (its columns).
- $C = BA$ is $m\times 2$ with columns $c_0 = B a_0 = \bigoplus_j a_{0,j}\, b_j$ and $c_1 = B a_1$.
- $e' = B e = \bigoplus_j e_j\, b_j$.
- Key packing: `C_key = (c0 << m) | c1` uses $2m$ bits; `e_key = eprime` uses $m$ bits.
- Noise weight $w=|e|$ gets integer weight $3^{4-w}$ after clearing denominators. This comes from $P(e)=(1/4)^w(3/4)^{4-w}$ and the uniform $A$ factor $1/15$; total denominator $15\cdot 4^4 = 3840$, and $3840/15/4^4 \cdot 3^{4-w} \cdot 1^w = 3^{4-w}$.

---

## Task 1: Helper module — Lagrangian enumeration and bit ops

**Files:**
- Create: `experiments/lib/lem_m2_exact.py`
- Create: `experiments/lib/__init__.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 1.1: Write failing tests**

```python
# tests/test_lem_m2_exact.py
from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, symplectic_form

def test_lagrangian_count():
    bases = enumerate_lagrangian_bases()
    assert len(bases) == 15

def test_symplectic_form_basis():
    # standard basis: e1=1, e2=2, f1=4, f2=8
    assert symplectic_form(1, 4) == 1
    assert symplectic_form(2, 8) == 1
    assert symplectic_form(1, 2) == 0
    assert symplectic_form(4, 8) == 0
```

- [ ] **Step 1.2: Run tests to verify they fail**

Run:
```bash
python3 -m pytest tests/test_lem_m2_exact.py -v
```
Expected: `ModuleNotFoundError: No module named 'experiments.lib.lem_m2_exact'`.

- [ ] **Step 1.3: Create package marker**

```bash
touch experiments/lib/__init__.py
```

- [ ] **Step 1.4: Implement helpers**

```python
# experiments/lib/lem_m2_exact.py
"""Exact small-n helpers for lem:m2 noise-side enumeration."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product


def symplectic_form(u: int, v: int) -> int:
    """Standard symplectic form on F_2^4: omega(u,v)."""
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def enumerate_lagrangian_bases():
    """Return list of Lagrangian subspaces of F_2^4 as (col0,col1) basis pairs."""
    subspaces = set()
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            span = frozenset({0, v1, v2, v1 ^ v2})
            # canonical basis: smallest non-zero and its symplectic partner
            canon = tuple(sorted([v1, v2]))
            subspaces.add((span, canon))
    return [c for _, c in sorted(subspaces)]


def apply_matrix(B_cols, x):
    """B * x over F_2; B_cols is list of m-bit column ints, x is 4-bit int."""
    y = 0
    for j, col in enumerate(B_cols):
        if (x >> j) & 1:
            y ^= col
    return y


def bernoulli_product(p: Fraction, m: int):
    """Return dict {e_prime: probability} for Bernoulli(p)^m."""
    q = Fraction(1) - p
    dist = {}
    for v in range(1 << m):
        w = v.bit_count()
        dist[v] = (p ** w) * (q ** (m - w))
    return dist


def sd_to_product(dist, product_dist):
    """Exact SD between dict dist (sums to 1) and product_dist."""
    keys = set(dist.keys()) | set(product_dist.keys())
    total = Fraction(0)
    for k in keys:
        total += abs(Fraction(dist.get(k, 0)) - Fraction(product_dist.get(k, 0)))
    return total / 2
```

- [ ] **Step 1.5: Run tests**

Run:
```bash
python3 -m pytest tests/test_lem_m2_exact.py -v
```
Expected: both tests PASS.

- [ ] **Step 1.6: Commit**

```bash
git add experiments/lib/lem_m2_exact.py experiments/lib/__init__.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): exact n=2 noise enumeration helpers"
```

---

## Task 2: Main enumeration runner

**Files:**
- Create: `experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py`
- Create: `experiments/output/184-lem-m2-n2-exact-conditional-noise-SD.json`

- [ ] **Step 2.1: Write runner skeleton with argparse**

```python
#!/usr/bin/env python3
"""184: lem:m2 exact conditional noise SD for n=2.

Enumerate all B in F_2^{m x 4}, all Lagrangian A, and all noise e,
then compute exact SD(P(e' | C), Bernoulli(p')^m).
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    apply_matrix,
    bernoulli_product,
    enumerate_lagrangian_bases,
    sd_to_product,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--pgrid", type=str, default="0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    m = args.m
    p_values = [Fraction(x) for x in args.pgrid.split(",")]
    bases = enumerate_lagrangian_bases()
    num_bases = len(bases)

    # Precompute noise vectors and integer weights 3^{4-w}
    noise_info = []
    for e in range(1 << 4):
        w = e.bit_count()
        noise_info.append((e, 3 ** (4 - w)))

    total_weight_per_B = sum(w for _, w in noise_info) * num_bases  # 3840

    global_joint = Counter()   # (C_key, eprime) -> weight
    global_marginal_C = Counter()  # C_key -> weight

    best_B = None
    best_avg_sd = Fraction(2)
    worst_avg_sd = Fraction(-1)
    num_B = 1 << (4 * m)

    for bits in range(num_B):
        B_cols = [((bits >> (j * m)) & ((1 << m) - 1)) for j in range(4)]
        joint_B = Counter()
        marginal_C_B = Counter()
        for a0, a1 in bases:
            c0 = apply_matrix(B_cols, a0)
            c1 = apply_matrix(B_cols, a1)
            C_key = (c0 << m) | c1
            for e, w_e in noise_info:
                eprime = apply_matrix(B_cols, e)
                joint_B[(C_key, eprime)] += w_e
                marginal_C_B[C_key] += w_e
                global_joint[(C_key, eprime)] += w_e
                global_marginal_C[C_key] += w_e

        # per-B average SD over p'=1/4 (primary) and best p'
        avg_sds = {}
        for p in p_values:
            Q = bernoulli_product(p, m)
            sd_sum = Fraction(0)
            for C_key, marg in marginal_C_B.items():
                cond = {ep: joint_B[(C_key, ep)] / marg for ep in range(1 << m) if joint_B[(C_key, ep)]}
                sd_sum += marg * sd_to_product(cond, Q)
            avg_sds[str(p)] = Fraction(sd_sum, total_weight_per_B)

        avg_sd_p25 = avg_sds["1/4"]
        if avg_sd_p25 < best_avg_sd:
            best_avg_sd = avg_sd_p25
            best_B = B_cols[:]
        if avg_sd_p25 > worst_avg_sd:
            worst_avg_sd = avg_sd_p25

    # global aggregates
    total_weight = num_B * total_weight_per_B
    result = {
        "n": 2,
        "m": m,
        "num_lagrangian": num_bases,
        "num_B": num_B,
        "p_grid": [str(p) for p in p_values],
        "best_B_p25": best_B,
        "best_avg_sd_p25": str(best_avg_sd),
        "worst_avg_sd_p25": str(worst_avg_sd),
    }

    # conditional SD averaged over C
    for p in p_values:
        Q = bernoulli_product(p, m)
        sd_sum = Fraction(0)
        for C_key, marg in global_marginal_C.items():
            cond = {ep: global_joint[(C_key, ep)] / marg for ep in range(1 << m) if global_joint[(C_key, ep)]}
            sd_sum += marg * sd_to_product(cond, Q)
        result[f"global_avg_conditional_sd_p{p}"] = str(Fraction(sd_sum, total_weight))

    # unconditional SD(P(e'), Q)
    for p in p_values:
        Q = bernoulli_product(p, m)
        eprime_marginal = Counter()
        for (C_key, ep), w in global_joint.items():
            eprime_marginal[ep] += w
        result[f"global_unconditional_sd_p{p}"] = str(sd_to_product(
            {ep: Fraction(w, total_weight) for ep, w in eprime_marginal.items()}, Q))

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"184-lem-m2-n2-exact-conditional-noise-SD-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.2: Run for $m=3$**

Run:
```bash
python3 experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py --m 3
```
Expected: finishes in seconds, creates `experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m3.json`.

- [ ] **Step 2.3: Verify $m=3$ output sanity**

Run:
```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path('experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m3.json')
data = json.loads(p.read_text())
assert data['m'] == 3
assert data['num_lagrangian'] == 15
assert data['num_B'] == 2**12
print(json.dumps(data, indent=2)[:1500])
PY
```
Expected: assertion passes, snippet prints.

- [ ] **Step 2.4: Run for $m=4$ and $m=5$**

Run:
```bash
python3 experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py --m 4
python3 experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py --m 5
```
Expected: $m=4$ finishes in ~10 seconds; $m=5$ finishes in a few minutes.

- [ ] **Step 2.5: Commit runner and outputs**

```bash
git add experiments/184-KIMI-lem-m2-n2-exact-conditional-noise-SD.py \
        experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m3.json \
        experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m4.json \
        experiments/output/184-lem-m2-n2-exact-conditional-noise-SD-m5.json
git commit -m "feat(lem-m2): exact n=2 conditional noise SD enumeration for m=3,4,5"
```

---

## Task 3: Independent sanity checks

**Files:**
- Create: `experiments/184b-KIMI-lem-m2-n2-sanity-checks.py`

- [ ] **Step 3.1: Write sanity script**

The script should:
1. Check that for $B=0$, $e'=0$ always, so $\mathrm{SD}$ to any non-degenerate product is large.
2. Check that for $B=I_{4\times 4}$ (with $m=4$), $e'=e\sim\mathrm{Bernoulli}(1/4)^4$, so $\mathrm{SD}$ to $Q_{1/4}$ is 0.
3. Re-derive the integer weight formula $3^{4-w}$ independently.

```python
#!/usr/bin/env python3
"""184b: Independent sanity checks for 184 exact enumeration."""
from collections import Counter
from fractions import Fraction

from experiments.lib.lem_m2_exact import apply_matrix, enumerate_lagrangian_bases


def check_zero_B():
    m = 3
    B_cols = [0, 0, 0, 0]
    eprime_counts = Counter()
    total = 0
    for a0, a1 in enumerate_lagrangian_bases():
        for e in range(1 << 4):
            w = e.bit_count()
            weight = 3 ** (4 - w)
            eprime = apply_matrix(B_cols, e)
            assert eprime == 0
            eprime_counts[eprime] += weight
            total += weight
    assert eprime_counts[0] == total
    print("zero-B sanity: OK")


def check_identity_B():
    m = 4
    B_cols = [1, 2, 4, 8]  # identity columns
    eprime_counts = Counter()
    total = 0
    for a0, a1 in enumerate_lagrangian_bases():
        for e in range(1 << 4):
            w = e.bit_count()
            weight = 3 ** (4 - w)
            eprime = apply_matrix(B_cols, e)
            eprime_counts[eprime] += weight
            total += weight
    # each e maps to itself; marginal should equal Bernoulli(1/4)^4
    for e in range(1 << 4):
        w = e.bit_count()
        expected = Fraction(3 ** (4 - w), 256)
        got = Fraction(eprime_counts[e], total // 15)  # per-B total = 3840, divide by 15 bases
        assert got == expected, f"e={e}: got {got}, expected {expected}"
    print("identity-B sanity: OK")


if __name__ == "__main__":
    check_zero_B()
    check_identity_B()
```

- [ ] **Step 3.2: Run sanity checks**

Run:
```bash
python3 experiments/184b-KIMI-lem-m2-n2-sanity-checks.py
```
Expected:
```
zero-B sanity: OK
identity-B sanity: OK
```

- [ ] **Step 3.3: Commit**

```bash
git add experiments/184b-KIMI-lem-m2-n2-sanity-checks.py
git commit -m "test(lem-m2): independent sanity checks for exact enumeration"
```

---

## Task 4: Interpretation note

**Files:**
- Create: `meta/2026-06-13-KIMI-lem-m2-n2-exact-conditional-noise-SD-DRAFT.md`

- [ ] **Step 4.1: Draft interpretation note**

Template contents:
- State what was computed.
- Include the $m=3,4,5$ key numbers from JSON.
- Interpret against `lem:m2`:
  - If $\min_B \mathrm{avg\_sd}$ is bounded away from 0, interpret as evidence that even non-adaptive $B$ cannot fake i.i.d. noise.
  - If some $B$ gives small SD, flag as candidate and describe its structure.
- List caveats ($n=2$, non-adaptive $B$, $p'$ grid).

- [ ] **Step 4.2: Commit note**

```bash
git add meta/2026-06-13-KIMI-lem-m2-n2-exact-conditional-noise-SD-DRAFT.md
git commit -m "docs(lem-m2): interpretation draft for n=2 exact conditional noise SD"
```

---

## Task 5: Push and handoff

- [ ] **Step 5.1: Push**

```bash
git push
```

- [ ] **Step 5.2: Report to user**

Summarize results with exact SD numbers and ask whether to:
1. Extend to $m=6$ via sampling/optimization.
2. Add adaptive $B=g(A)$ families.
3. Return to OP7.

---

## Self-Review Checklist

- **Spec coverage:**
  - $n=2$ exact enumeration: Task 2.
  - Conditional $P(e'\mid C)$: Task 2 algorithm.
  - Comparison to $\mathrm{Bernoulli}(p')^m$: Task 2 `bernoulli_product` + SD.
  - $m=3,4,5$ runs: Task 2.
  - Output JSON: Task 2.
  - Interpretation note: Task 4.
- **Placeholder scan:** No TBD/TODO; all code blocks concrete.
- **Type consistency:** `B_cols` is always a list of 4 $m$-bit ints; `C_key` is `(c0 << m) | c1`; keys match across tasks.
