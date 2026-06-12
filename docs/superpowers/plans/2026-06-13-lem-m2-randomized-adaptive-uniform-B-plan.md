# lem:m2 randomized adaptive uniform $B$ per $A$ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement an exact enumeration of the joint SD between the reduction output $(C,y)$ and standard $\mathrm{LPN}_{1/4}$ when, for each Lagrangian $A$, the reduction matrix $B$ is drawn uniformly from $\F_2^{m\times 4}$.

**Architecture:** Add a single helper `randomized_uniform_B_counts(m, bases)` to the existing exact-enumeration module. The helper uses the three-case decomposition from the design spec to build integer counts without enumerating matrices $B$. A small runner script computes the SD for $m=3,4$ and saves JSON. A meta note interprets the result against the deterministic lower bound and the non-adaptive optimum.

**Tech Stack:** Python 3, `fractions.Fraction`, `json`, `pathlib`.

---

## File Structure

- **Modify:** `experiments/lib/lem_m2_exact.py` — add `randomized_uniform_B_counts(m, bases=None)`.
- **Modify:** `tests/test_lem_m2_exact.py` — add tests for normalization and brute-force agreement.
- **Create:** `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py` — runner script.
- **Create:** `experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m{3,4}.json` — results.
- **Create:** `meta/2026-06-13-KIMI-lem-m2-randomized-adaptive-uniform-B.md` — interpretation note.

---

## Task 1: Add randomized uniform-$B$ count helper

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

### Why this works

Fix a Lagrangian basis $A=(a_0,a_1)$, secret $x$, and noise $e$. Let $a=Ax$ and $v=a+e$.

- If $v=0$: then $y=0$ and $C$ is uniform. Each output $(C,0)$ is realized by $2^{2m}$ matrices $B$.
- If $v\in\mathrm{span}(A)\setminus\{0\}$: write $v=\alpha a_0+\beta a_1$. Then $y=\alpha c_0+\beta c_1$ is a deterministic linear function of $C$. Each graph point is realized by $2^{2m}$ matrices $B$.
- If $v\notin\mathrm{span}(A)$: the three vectors $a_0,a_1,v$ are independent, so $(C,y)$ is uniform on the full space. Each full-space point is realized by $2^m$ matrices $B$.

The helper accumulates integer weights $3^{4-|e|}$ multiplied by the appropriate number-of-$B$ factor.

- [ ] **Step 1.1: Write failing tests**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import randomized_uniform_B_counts


def test_randomized_uniform_B_counts_normalized():
    for m in (2, 3, 4):
        counts, denom = randomized_uniform_B_counts(m)
        assert sum(counts) == denom


def test_randomized_uniform_B_counts_matches_brute_force():
    """For m=2, sum reduction_counts_for_B over all B equals the randomized counts."""
    from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, reduction_counts_for_B

    m = 2
    bases = list(enumerate_lagrangian_bases())
    red_counts, _ = randomized_uniform_B_counts(m, bases)

    num_B = 1 << (4 * m)
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    brute = [0] * size
    for bits in range(num_B):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        counts = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            brute[i] += counts[i]

    assert red_counts == brute
```

- [ ] **Step 1.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_randomized_uniform_B_counts_normalized tests/test_lem_m2_exact.py::test_randomized_uniform_B_counts_matches_brute_force -v
```

Expected: `ImportError` or `AttributeError` for `randomized_uniform_B_counts`.

- [ ] **Step 1.3: Implement helper**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def randomized_uniform_B_counts(m: int, bases=None) -> tuple[list[int], int]:
    """Integer counts for (C, y) when B ~ Unif(F_2^{m x 4}) is drawn per A.

    Uses the three-case decomposition from the design spec:
      * v = 0            -> 2^{2m} matrices per (C, 0)
      * v in span(A)\{0} -> 2^{2m} matrices per graph point
      * v not in span(A) -> 2^{m} matrices per full-space point

    Returns (counts, denominator) so that counts[key] / denominator is the
    exact probability of output key = (C_key << m) | y.
    """
    if bases is None:
        bases = enumerate_lagrangian_bases()

    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    size = 1 << (3 * m)
    counts = [0] * size

    # Precompute c0/c1 for every C_key to avoid repeated bit slicing.
    c0_list = [(C_key >> m) & mask for C_key in range(num_C)]
    c1_list = [C_key & mask for C_key in range(num_C)]

    two_to_m = 1 << m
    two_to_2m = 1 << (2 * m)
    case3_weight_sum = 0

    for a0, a1 in bases:
        span_map = {
            0: (0, 0),
            a0: (1, 0),
            a1: (0, 1),
            a0 ^ a1: (1, 1),
        }
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w = e.bit_count()
                weight = 3 ** (4 - w)
                v = a ^ e

                if v == 0:
                    # y is forced to 0; C is uniform.
                    add = weight * two_to_2m
                    for C_key in range(num_C):
                        counts[(C_key << m)] += add
                elif v in span_map:
                    alpha, beta = span_map[v]
                    add = weight * two_to_2m
                    for C_key in range(num_C):
                        y = 0
                        if alpha:
                            y ^= c0_list[C_key]
                        if beta:
                            y ^= c1_list[C_key]
                        counts[(C_key << m) | y] += add
                else:
                    # Full-space uniform contribution; delay the actual add.
                    case3_weight_sum += weight

    case3_add = case3_weight_sum * two_to_m
    for key in range(size):
        counts[key] += case3_add

    # Denominator = sum over (A, x, e) of weight_e * 2^{4m}.
    red_denom = len(bases) * (1 << 2) * 256 * (1 << (4 * m))
    return counts, red_denom
```

- [ ] **Step 1.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS, including the two new ones.

- [ ] **Step 1.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): randomized uniform-B-per-A exact count helper"
```

---

## Task 2: Runner script for $m=3,4$

**Files:**
- Create: `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py`
- Create: `experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m{3,4}.json`

- [ ] **Step 2.1: Write script**

Create `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py`:

```python
#!/usr/bin/env python3
"""187: lem:m2 randomized adaptive uniform B per A — exact joint SD.

For each Lagrangian A, B is drawn independently and uniformly from
F_2^{m x 4}.  Compute exact SD((C, y), LPN_{1/4}) for n=2.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    m = args.m
    if m < 1:
        raise ValueError("m must be >= 1")

    bases = list(enumerate_lagrangian_bases())
    p = Fraction(1, 4)

    red_counts, red_denom = randomized_uniform_B_counts(m, bases)
    lpn_counts, lpn_denom = lpn_target_counts(m, p)
    sd = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)

    result = {
        "n": 2,
        "m": m,
        "p_prime": str(p),
        "num_lagrangian": len(bases),
        "red_denom": red_denom,
        "lpn_denom": lpn_denom,
        "sd": str(sd),
        "sd_float": float(sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"187-lem-m2-randomized-adaptive-uniform-B-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.2: Run for $m=3$**

```bash
PYTHONPATH=. python3 experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py --m 3
```

Expected: creates `experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m3.json` and prints the saved path.

- [ ] **Step 2.3: Run for $m=4$**

```bash
PYTHONPATH=. python3 experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py --m 4
```

Expected: creates `experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m4.json` and prints the saved path.

- [ ] **Step 2.4: Sanity-check outputs**

```bash
PYTHONPATH=. python3 - <<'PY'
import json
from pathlib import Path
for m in (3, 4):
    p = Path(f'experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m{m}.json')
    data = json.loads(p.read_text())
    assert data['n'] == 2
    assert data['m'] == m
    assert data['num_lagrangian'] == 15
    assert 0 <= data['sd_float'] <= 1
    print(f"m={m}: SD = {data['sd']} ~= {data['sd_float']:.6f}")
PY
```

- [ ] **Step 2.5: Commit**

```bash
git add experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py \
        experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m3.json \
        experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m4.json
git commit -m "feat(lem-m2): randomized adaptive uniform-B-per-A exact SD"
```

---

## Task 3: Interpretation note

**Files:**
- Create: `meta/2026-06-13-KIMI-lem-m2-randomized-adaptive-uniform-B.md`

- [ ] **Step 3.1: Write note**

Create `meta/2026-06-13-KIMI-lem-m2-randomized-adaptive-uniform-B.md` with this content, filling in the SD values from the JSON files produced in Task 2:

```markdown
# lem:m2 randomized adaptive $B$ — uniform $B$ per $A$

**Date:** 2026-06-13

## Model

- $n=2$, ambient dimension $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$.
- $x \sim \mathrm{Unif}(\F_2^2)$, $e \sim \mathrm{Bernoulli}(1/4)^4$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 4})$.
- Output $(C,y) = (BA, B(Ax+e))$.

## Exact SD results

| $m$ | $\mathrm{SD}(P_{\mathrm{out}}, \mathrm{LPN}_{1/4})$ |
|----:|--------------------------------------------------------:|
| 3   | __SD_M3__                                              |
| 4   | __SD_M4__                                              |

(Values computed by `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py`.)

## Comparison

- **Deterministic adaptive lower bound:** $\mathrm{SD} \ge 1 - 15/4^m$.
  - $m=3$: $49/64$.
  - $m=4$: $241/256$.
- **Non-adaptive best (experiment 185):** matches the deterministic bound for $m=3,4$.
- **Uniform randomized per $A$:** the SD values above show whether marginal uniformity of $C$ is enough to escape the deterministic obstruction, or whether the correlated noise $e'=Be$ still prevents LPN simulation.

## Interpretation

- If the randomized SD is close to the deterministic bound, then even drawing a fresh uniform $B$ per $A$ does not help: the structure of the original noise $e$ propagates through $B$ and remains distinguishable from i.i.d. $\mathrm{Bernoulli}(1/4)^m$ noise.
- If the randomized SD is significantly smaller, then randomization over $B$ is a viable direction for further investigation (e.g., non-uniform or rank-conditioned distributions).

## Limitations

- Only the uniform distribution over $B$ per $A$ is analyzed.
- Only $n=2$.
- General randomized strategies $B = g(A, R)$ with non-uniform or rank-restricted $g$ remain open.
```

Replace `__SD_M3__` and `__SD_M4__` with the exact fraction strings from the JSON files.

- [ ] **Step 3.2: Commit**

```bash
git add meta/2026-06-13-KIMI-lem-m2-randomized-adaptive-uniform-B.md
git commit -m "docs(lem-m2): randomized adaptive uniform-B-per-A interpretation note"
```

---

## Task 4: Final review and branch finish

- [ ] **Step 4.1: Run full test suite and both runner invocations**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
PYTHONPATH=. python3 experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py --m 3
PYTHONPATH=. python3 experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py --m 4
```

- [ ] **Step 4.2: Final review subagent**

Dispatch a reviewer to check:
- correctness of the three-case helper against the spec,
- test coverage,
- runner output values and JSON schema,
- interpretation note accuracy (filled-in values match JSON).

- [ ] **Step 4.3: Merge/push**

Use `superpowers:finishing-a-development-branch` to merge the work to `main` and push.

---

## Self-Review Checklist

- **Spec coverage:**
  - Uniform-$B$-per-$A$ exact count helper: Task 1.
  - $m=3,4$ runner and JSON outputs: Task 2.
  - Comparison with deterministic lower bound and non-adaptive optimum: Task 3.
  - Limitations (uniform only, $n=2$): Task 3.
- **Placeholder scan:** No TBD/TODO in code steps. The interpretation note contains two fill-in markers for the SD values, which are populated from the runner output.
- **Type consistency:** `randomized_uniform_B_counts(m: int, bases=None) -> tuple[list[int], int]` is used in both tests and runner.
