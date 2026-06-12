# lem:m2 $n=3$ uniform-$B$ exact scaling — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement exact helpers and a runner that compute the joint SD between $(C,y)$ and $\mathrm{LPN}_{1/4}$ for $n=3$ under uniform randomized $B$ per $A$, for $m=3$ and $m=4$.

**Architecture:** Generalize the exact-enumeration helpers to arbitrary $n$: symplectic form, Lagrangian basis enumerator, LPN target counts, and uniform-$B$ count helper. Keep the existing $n=2$ helpers unchanged for backward compatibility. A runner script computes the SD for $n=3$, compares with the $n=2$ results from experiment 187, and saves JSON plus a meta note.

**Tech Stack:** Python 3, `fractions.Fraction`, `json`, `pathlib`.

---

## File Structure

- **Modify:** `experiments/lib/lem_m2_exact.py` — add `symplectic_form_n`, `enumerate_lagrangian_bases_n`, `lpn_target_counts_n`, `randomized_uniform_B_counts_n`.
- **Modify:** `tests/test_lem_m2_exact.py` — add tests for the new helpers.
- **Create:** `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py` — runner.
- **Create:** `experiments/output/189-lem-m2-n3-uniform-B-exact-m{3,4}.json` — results.
- **Create:** `meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md` — interpretation note.

---

## Task 1: Generalized symplectic form and Lagrangian enumerator

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 1.1: Write failing tests**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import symplectic_form_n, enumerate_lagrangian_bases_n


def test_symplectic_form_n_matches_existing():
    for u in range(1 << 4):
        for v in range(1 << 4):
            assert symplectic_form_n(u, v, 2) == symplectic_form(u, v)


def test_enumerate_lagrangian_bases_n_counts():
    assert len(enumerate_lagrangian_bases_n(1)) == 3
    assert len(enumerate_lagrangian_bases_n(2)) == 15
    assert len(enumerate_lagrangian_bases_n(3)) == 135
```

- [ ] **Step 1.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_symplectic_form_n_matches_existing tests/test_lem_m2_exact.py::test_enumerate_lagrangian_bases_n_counts -v
```

Expected: `ImportError` or `AttributeError` for `symplectic_form_n` / `enumerate_lagrangian_bases_n`.

- [ ] **Step 1.3: Implement helpers**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def symplectic_form_n(u: int, v: int, n: int) -> int:
    """Standard symplectic form on F_2^{2n}: omega(u, v)."""
    res = 0
    for i in range(n):
        ui = (u >> i) & 1
        vi = (v >> i) & 1
        ui2 = (u >> (i + n)) & 1
        vi2 = (v >> (i + n)) & 1
        res ^= (ui * vi2) ^ (ui2 * vi)
    return res & 1


def enumerate_lagrangian_bases_n(n: int) -> list[tuple[int, ...]]:
    """Return one ordered basis per Lagrangian subspace of F_2^{2n}.

    For n=2 this returns the same 15 subspaces as enumerate_lagrangian_bases.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    dim = 2 * n
    vectors = list(range(1, 1 << dim))
    subspaces = {}

    def is_isotropic(basis):
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                if symplectic_form_n(basis[i], basis[j], n) != 0:
                    return False
        return True

    # Recursively build ordered isotropic bases of size n.
    def extend(basis, start):
        if len(basis) == n:
            if not is_isotropic(basis):
                return
            span = [0]
            for v in basis:
                span += [s ^ v for s in span]
            span_set = frozenset(span)
            canon = tuple(sorted(basis))
            subspaces.setdefault(span_set, canon)
            return
        for idx in range(start, len(vectors)):
            v = vectors[idx]
            ok = True
            for b in basis:
                if symplectic_form_n(b, v, n) != 0:
                    ok = False
                    break
            if not ok:
                continue
            # Also require linear independence from existing span.
            for s in span_of(basis):
                if s == v:
                    ok = False
                    break
            if not ok:
                continue
            extend(basis + [v], idx + 1)

    def span_of(basis):
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        return set(span)

    extend([], 0)
    return [c for _, c in sorted(subspaces.items())]
```

- [ ] **Step 1.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS.

- [ ] **Step 1.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): generalized symplectic form and Lagrangian enumerator"
```

---

## Task 2: Generalized LPN target counts

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 2.1: Write failing test**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import lpn_target_counts_n


def test_lpn_target_counts_n_matches_existing():
    for m in (2, 3):
        counts_old, denom_old = lpn_target_counts(m, Fraction(1, 4))
        counts_new, denom_new = lpn_target_counts_n(m, 2, Fraction(1, 4))
        assert counts_old == counts_new
        assert denom_old == denom_new


def test_lpn_target_counts_n_normalized():
    for n in (2, 3):
        for m in (2, 3):
            counts, denom = lpn_target_counts_n(m, n, Fraction(1, 4))
            assert sum(counts) == denom
```

- [ ] **Step 2.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_lpn_target_counts_n_matches_existing tests/test_lem_m2_exact.py::test_lpn_target_counts_n_normalized -v
```

Expected: `ImportError` or `AttributeError` for `lpn_target_counts_n`.

- [ ] **Step 2.3: Implement helper**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def lpn_target_counts_n(m: int, n: int, p: Fraction) -> tuple[list[int], int]:
    """Integer counts and denominator for LPN_p distribution over (C, y) with C in F_2^{m x n}."""
    mask = (1 << m) - 1
    num_C = 1 << (n * m)
    size = 1 << ((n + 1) * m)
    counts = [0] * size
    D = p.denominator ** m
    total_denom = num_C * (1 << n) * D

    # Precompute c_j for each C_key and basis index j.
    c_lists = [[0] * num_C for _ in range(n)]
    for C_key in range(num_C):
        tmp = C_key
        for j in range(n):
            c_lists[j][C_key] = tmp & mask
            tmp >>= m

    for C_key in range(num_C):
        for x in range(1 << n):
            cx = 0
            for j in range(n):
                if (x >> j) & 1:
                    cx ^= c_lists[j][C_key]
            for eprime in range(1 << m):
                w = eprime.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx ^ eprime
                key = (C_key << m) | y
                counts[key] += num
    return counts, total_denom
```

- [ ] **Step 2.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS.

- [ ] **Step 2.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): generalized LPN target counts for arbitrary n"
```

---

## Task 3: Generalized uniform-$B$ count helper

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 3.1: Write failing test**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import randomized_uniform_B_counts_n


def test_randomized_uniform_B_counts_n_matches_n2_helper():
    for m in (2, 3):
        bases_n2 = enumerate_lagrangian_bases()
        counts_old, denom_old = randomized_uniform_B_counts(m, bases_n2)
        counts_new, denom_new = randomized_uniform_B_counts_n(m, 2, bases_n2)
        assert counts_old == counts_new
        assert denom_old == denom_new


def test_randomized_uniform_B_counts_n_normalized():
    for n in (2, 3):
        for m in (2, 3):
            counts, denom = randomized_uniform_B_counts_n(m, n)
            assert sum(counts) == denom
```

- [ ] **Step 3.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_randomized_uniform_B_counts_n_matches_n2_helper tests/test_lem_m2_exact.py::test_randomized_uniform_B_counts_n_normalized -v
```

Expected: `ImportError` or `AttributeError` for `randomized_uniform_B_counts_n`.

- [ ] **Step 3.3: Implement helper**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def randomized_uniform_B_counts_n(
    m: int, n: int, bases: list[tuple[int, ...]] | None = None
) -> tuple[list[int], int]:
    """Exact counts for (C, y) when B ~ Unif(F_2^{m x 2n}) is drawn per A.

    Generalizes randomized_uniform_B_counts to arbitrary n using the same
    three-case decomposition:
      * v = 0            -> uniform on {(C, 0)}, 2^{n m} matrices per point
      * v in span(A)\{0} -> uniform on graph of linear map, 2^{n m} matrices/point
      * v not in span(A) -> uniform on full (C, y) space, 2^{(n-1)m} matrices/point
    """
    if bases is None:
        bases = enumerate_lagrangian_bases_n(n)

    mask = (1 << m) - 1
    num_C = 1 << (n * m)
    size = 1 << ((n + 1) * m)
    counts = [0] * size

    # Precompute c_j for each C_key.
    c_lists = [[0] * num_C for _ in range(n)]
    for C_key in range(num_C):
        tmp = C_key
        for j in range(n):
            c_lists[j][C_key] = tmp & mask
            tmp >>= m

    two_to_nm = 1 << (n * m)
    two_to_nminus1_m = 1 << ((n - 1) * m)
    case3_weight_sum = 0
    total_error_weight = sum(3 ** (2 * n - e.bit_count()) for e in range(1 << (2 * n)))

    for basis in bases:
        # Build span_map: span vector -> coefficient tuple over the basis.
        span_map = {0: tuple([0] * n)}
        for s in range(1, 1 << n):
            v = 0
            coeffs = [0] * n
            for j in range(n):
                if (s >> j) & 1:
                    v ^= basis[j]
                    coeffs[j] = 1
            span_map[v] = tuple(coeffs)

        for x in range(1 << n):
            a = 0
            for j in range(n):
                if (x >> j) & 1:
                    a ^= basis[j]
            for e in range(1 << (2 * n)):
                w_e = 3 ** (2 * n - e.bit_count())
                v = a ^ e

                if v == 0:
                    add = w_e * two_to_nm
                    for C_key in range(num_C):
                        counts[C_key << m] += add
                elif v in span_map:
                    coeffs = span_map[v]
                    add = w_e * two_to_nm
                    for C_key in range(num_C):
                        y = 0
                        for j in range(n):
                            if coeffs[j]:
                                y ^= c_lists[j][C_key]
                        counts[(C_key << m) | y] += add
                else:
                    case3_weight_sum += w_e

    case3_add = case3_weight_sum * two_to_nminus1_m
    for key in range(size):
        counts[key] += case3_add

    red_denom = len(bases) * (1 << n) * total_error_weight * (1 << (2 * n * m))
    return counts, red_denom
```

- [ ] **Step 3.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS.

- [ ] **Step 3.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): generalized uniform-B-per-A exact count helper"
```

---

## Task 4: Runner script

**Files:**
- Create: `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py`
- Create: `experiments/output/189-lem-m2-n3-uniform-B-exact-m{3,4}.json`

- [ ] **Step 4.1: Write script**

Create `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py`:

```python
#!/usr/bin/env python3
"""189: lem:m2 n=3 exact uniform-B-per-A joint SD.

For each Lagrangian A in F_2^6, B is drawn uniformly from F_2^{m x 6}.
Compute exact SD((C, y), LPN_{1/4}) for n=3, m=3,4.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases_n,
    exact_sd_counts,
    lpn_target_counts_n,
    randomized_uniform_B_counts_n,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    m = args.m
    if m not in (3, 4):
        raise ValueError("this experiment supports m=3 or m=4")

    n = 3
    bases = list(enumerate_lagrangian_bases_n(n))
    p = Fraction(1, 4)

    red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
    lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)
    sd = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)

    result = {
        "n": n,
        "m": m,
        "p_lpn": str(p),
        "num_lagrangian": len(bases),
        "red_denom": red_denom,
        "lpn_denom": lpn_denom,
        "sd": str(sd),
        "sd_float": float(sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"189-lem-m2-n3-uniform-B-exact-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4.2: Run for $m=3$**

```bash
PYTHONPATH=. python3 experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py --m 3
```

Expected: creates `experiments/output/189-lem-m2-n3-uniform-B-exact-m3.json`.

- [ ] **Step 4.3: Run for $m=4$**

```bash
PYTHONPATH=. python3 experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py --m 4
```

Expected: creates `experiments/output/189-lem-m2-n3-uniform-B-exact-m4.json`.

- [ ] **Step 4.4: Sanity-check outputs**

```bash
PYTHONPATH=. python3 - <<'PY'
import json
from fractions import Fraction
from pathlib import Path
for m in (3, 4):
    p = Path(f'experiments/output/189-lem-m2-n3-uniform-B-exact-m{m}.json')
    data = json.loads(p.read_text())
    assert data['n'] == 3 and data['m'] == m
    assert data['num_lagrangian'] == 135
    sd = Fraction(data['sd'])
    assert 0 <= sd <= 1
    print(f"n=3, m={m}: SD = {data['sd']} ~= {data['sd_float']:.6f}")
PY
```

- [ ] **Step 4.5: Commit**

```bash
git add experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py \
        experiments/output/189-lem-m2-n3-uniform-B-exact-m3.json \
        experiments/output/189-lem-m2-n3-uniform-B-exact-m4.json \
    && git commit -m "feat(lem-m2): n=3 uniform-B-per-A exact SD"
```

---

## Task 5: Interpretation note

**Files:**
- Create: `meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md`

- [ ] **Step 5.1: Write note**

Create `meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md` with this content. Replace `__SD_M3__`, `__SD_M4__`, `__FLOAT_M3__`, `__FLOAT_M4__` with values from the JSON files and from experiment 187.

```markdown
# lem:m2 $n=3$ uniform-$B$ exact scaling

**Date:** 2026-06-14

## Model

- $n=3$, ambient dimension $2n=6$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(6,\F_2))$, $|A|=135$.
- $x \sim \mathrm{Unif}(\F_2^3)$, $e \sim \mathrm{Bernoulli}(1/4)^6$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 6})$.
- Output $(C,y) = (BA, B(Ax+e))$.

## Exact SD results

| $n$ | $m$ | $\mathrm{SD}(P_{\mathrm{out}}, \mathrm{LPN}_{1/4})$ |
|----:|----:|--------------------------------------------------------:|
| 2   | 3   | $3225/32768 \approx 0.0984$                             |
| 2   | 4   | $5903/32768 \approx 0.1801$                             |
| 3   | 3   | __SD_M3__ (__FLOAT_M3__)                                |
| 3   | 4   | __SD_M4__ (__FLOAT_M4__)                                |

(Values computed by `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py`.)

## Interpretation

- If the $n=3$ SD values remain small and comparable to $n=2$, then uniform $B$ per $A$ scales beyond the minimal case and `lem:m2` is threatened by this randomized reduction.
- If the SD values jump significantly, the $n=2$ result was an artifact of the small ambient dimension and the strategy does not scale.

## Limitations

- Only uniform $B$ per $A$ is analyzed.
- Only $n=3$, $m=3,4$.
- Larger $n$ or $m$ will require sampling or symbolic methods.
```

- [ ] **Step 5.2: Commit**

```bash
git add meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md
git commit -m "docs(lem-m2): n=3 uniform-B-per-A exact scaling note"
```

---

## Task 6: Final review and branch finish

- [ ] **Step 6.1: Run full test suite and both runner invocations**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
PYTHONPATH=. python3 experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py --m 3
PYTHONPATH=. python3 experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py --m 4
```

- [ ] **Step 6.2: Final review subagent**

Dispatch a reviewer to check:
- generalized helpers agree with existing $n=2$ helpers,
- $n=3$ Lagrangian count is 135,
- runner output values and JSON schema,
- interpretation note accuracy.

- [ ] **Step 6.3: Merge/push**

Use `superpowers:finishing-a-development-branch` to merge the work to `main` and push.

---

## Self-Review Checklist

- **Spec coverage:**
  - Generalized symplectic form and Lagrangian enumerator: Task 1.
  - Generalized LPN target counts: Task 2.
  - Generalized uniform-$B$ count helper: Task 3.
  - Runner and JSON outputs for $n=3$, $m=3,4$: Task 4.
  - Comparison note with $n=2$ results: Task 5.
  - Limitations: Task 5.
- **Placeholder scan:** No TBD/TODO in code steps. The interpretation note contains fill-in markers for the SD values, populated from the runner output.
- **Type consistency:** `symplectic_form_n(u, v, n)`, `enumerate_lagrangian_bases_n(n)`, `lpn_target_counts_n(m, n, p)`, `randomized_uniform_B_counts_n(m, n, bases)` used consistently.
