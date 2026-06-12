# lem:m2 randomized adaptive $B$ distribution sweep — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement an exact enumeration script that compares the joint SD between $(C,y)$ and $\mathrm{LPN}_{1/4}$ for several randomized adaptive $B$ distributions: uniform full-rank, rank-deficient, and Bernoulli($p$) rows with $p$ optimization.

**Architecture:** Add two helpers to the exact-enumeration module. `rank_conditioned_counts` enumerates all matrices of a given rank and aggregates deterministic counts. `bernoulli_rows_B_counts` uses an analytic row-pattern composition to compute the exact distribution when rows are i.i.d. $\mathrm{Bernoulli}(p)^4$. A runner sweeps the distributions for $m=3,4$, finds the best $p$, and saves JSON plus a meta note.

**Tech Stack:** Python 3, `fractions.Fraction`, `json`, `pathlib`.

---

## File Structure

- **Modify:** `experiments/lib/lem_m2_exact.py` — add `matrix_rank_f2`, `rank_conditioned_counts`, and `bernoulli_rows_B_counts`.
- **Modify:** `tests/test_lem_m2_exact.py` — add tests for rank counts and Bernoulli-row counts.
- **Create:** `experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py` — runner.
- **Create:** `experiments/output/188-lem-m2-randomized-B-distribution-sweep-m{3,4}.json` — results.
- **Create:** `meta/2026-06-14-KIMI-lem-m2-randomized-B-distribution-sweep.md` — interpretation note.

---

## Task 1: Add rank-conditioned count helper

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 1.1: Write failing tests**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import matrix_rank_f2, rank_conditioned_counts


def test_matrix_rank_f2():
    # rows of identity-like matrix in F2^4
    rows = [1, 2, 4, 8]
    assert matrix_rank_f2(rows, 4) == 4
    rows = [1, 2, 3, 0]
    assert matrix_rank_f2(rows, 4) == 2
    rows = [0, 0, 0]
    assert matrix_rank_f2(rows, 4) == 0


def test_rank_conditioned_counts_full_rank_m3():
    m = 3
    counts, denom = rank_conditioned_counts(m, rank=m)
    # sum of counts must equal number of full-rank 3x4 matrices * 15360
    num_full_rank = (2 ** 4 - 1) * (2 ** 4 - 2) * (2 ** 4 - 4)
    assert denom == num_full_rank * 15360
    assert sum(counts) == denom
```

- [ ] **Step 1.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_matrix_rank_f2 tests/test_lem_m2_exact.py::test_rank_conditioned_counts_full_rank_m3 -v
```

Expected: `ImportError` or `AttributeError` for the new names.

- [ ] **Step 1.3: Implement helpers**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def matrix_rank_f2(rows: list[int], n_cols: int) -> int:
    """Rank of a matrix over F_2 given as a list of row bitmasks."""
    pivots = {}
    for r in rows:
        x = r & ((1 << n_cols) - 1)
        if x == 0:
            continue
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return len(pivots)


def _rows_to_columns(rows: list[int], n_cols: int) -> list[int]:
    """Convert row representation to column representation for apply_matrix."""
    m = len(rows)
    cols = [0] * n_cols
    for j in range(n_cols):
        col_val = 0
        for i, r in enumerate(rows):
            if (r >> j) & 1:
                col_val |= 1 << i
        cols[j] = col_val
    return cols


def rank_conditioned_counts(m: int, rank: int, bases=None) -> tuple[list[int], int]:
    """Exact counts for (C, y) when B is uniform over m x 4 matrices of given rank."""
    if bases is None:
        bases = enumerate_lagrangian_bases()
    if rank > min(m, 4):
        raise ValueError("rank cannot exceed min(m, 4)")

    size = 1 << (3 * m)
    counts = [0] * size
    num_B = 1 << (4 * m)
    row_mask = (1 << 4) - 1
    matched = 0

    for bits in range(num_B):
        rows = [((bits >> (j * 4)) & row_mask) for j in range(m)]
        if matrix_rank_f2(rows, 4) != rank:
            continue
        matched += 1
        B_cols = _rows_to_columns(rows, 4)
        c = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            counts[i] += c[i]

    denom = matched * 15360
    return counts, denom
```

- [ ] **Step 1.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS.

- [ ] **Step 1.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): rank-conditioned randomized B count helper"
```

---

## Task 2: Add Bernoulli-row count helper

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 2.1: Write failing test**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import bernoulli_rows_B_counts


def test_bernoulli_rows_B_counts_matches_brute_force():
    """For m=2, p=1/3, compare analytic helper with full B enumeration."""
    from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, reduction_counts_for_B

    m = 2
    p = Fraction(1, 3)
    bases = list(enumerate_lagrangian_bases())
    red_counts, red_denom = bernoulli_rows_B_counts(m, p, bases)
    assert sum(red_counts) == red_denom

    # Brute-force weighted sum over all B.
    num_B = 1 << (4 * m)
    row_mask = (1 << 4) - 1
    size = 1 << (3 * m)
    brute = [0] * size
    D = p.denominator ** (4 * m)
    for bits in range(num_B):
        rows = [((bits >> (j * 4)) & row_mask) for j in range(m)]
        weight_num = 1
        for r in rows:
            w = r.bit_count()
            weight_num *= (p.numerator ** w) * ((p.denominator - p.numerator) ** (4 - w))
        B_cols = []
        for j in range(4):
            col_val = 0
            for i, r in enumerate(rows):
                if (r >> j) & 1:
                    col_val |= 1 << i
            B_cols.append(col_val)
        counts = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            brute[i] += counts[i] * weight_num

    assert red_counts == brute
```

- [ ] **Step 2.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_bernoulli_rows_B_counts_matches_brute_force -v
```

Expected: `ImportError` or `AttributeError` for `bernoulli_rows_B_counts`.

- [ ] **Step 2.3: Implement helper**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def bernoulli_rows_B_counts(m: int, p: Fraction, bases=None) -> tuple[list[int], int]:
    """Exact counts for (C, y) when each row of B is i.i.d. Bernoulli(p)^4.

    For each (A, x, e) triple we enumerate all assignments of m rows to the
    eight possible output-bit patterns (s0, s1, s2) = (r·a0, r·a1, r·v).  The
    per-row weight numerator is accumulated analytically, so we never iterate
    over the full 2^{4m} matrix space.
    """
    if bases is None:
        bases = enumerate_lagrangian_bases()
    if not (0 <= p <= 1):
        raise ValueError("p must be in [0, 1]")

    size = 1 << (3 * m)
    counts = [0] * size
    num_row_patterns = 1 << 4

    # Numerator of row-pattern weight, denominator is p.denominator^4.
    pattern_weights = [0] * num_row_patterns
    for r in range(num_row_patterns):
        w = r.bit_count()
        pattern_weights[r] = (
            p.numerator ** w
        ) * ((p.denominator - p.numerator) ** (4 - w))

    # Bits of the 8 output patterns: t = (s0<<2) | (s1<<1) | s2.
    t_bits = [((t >> 2) & 1, (t >> 1) & 1, t & 1) for t in range(8)]
    num_assignments = 8 ** m

    for a0, a1 in bases:
        span_map = {0: (0, 0), a0: (1, 0), a1: (0, 1), a0 ^ a1: (1, 1)}
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w_e = 3 ** (4 - e.bit_count())
                v = a ^ e

                # W[t] = total row-pattern weight producing output pattern t.
                W = [0] * 8
                if v == 0:
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        t = (s0 << 2) | (s1 << 1)
                        W[t] += pattern_weights[r]
                elif v in span_map:
                    alpha, beta = span_map[v]
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        s2 = ((alpha * s0) ^ (beta * s1)) & 1
                        t = (s0 << 2) | (s1 << 1) | s2
                        W[t] += pattern_weights[r]
                else:
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        s2 = (r & v).bit_count() & 1
                        t = (s0 << 2) | (s1 << 1) | s2
                        W[t] += pattern_weights[r]

                # Enumerate all row-to-output-pattern assignments.
                for assignment in range(num_assignments):
                    tmp = assignment
                    c0 = 0
                    c1 = 0
                    y = 0
                    prod = 1
                    for i in range(m):
                        t = tmp & 7
                        tmp >>= 3
                        prod *= W[t]
                        s0, s1, s2 = t_bits[t]
                        if s0:
                            c0 |= 1 << i
                        if s1:
                            c1 |= 1 << i
                        if s2:
                            y |= 1 << i
                    key = ((c0 << m) | c1) << m | y
                    counts[key] += w_e * prod

    red_denom = 15360 * (p.denominator ** (4 * m))
    return counts, red_denom
```

- [ ] **Step 2.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```

Expected: all tests PASS.

- [ ] **Step 2.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): Bernoulli-row randomized B count helper"
```

---

## Task 3: Runner script

**Files:**
- Create: `experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py`
- Create: `experiments/output/188-lem-m2-randomized-B-distribution-sweep-m{3,4}.json`

- [ ] **Step 3.1: Write script**

Create `experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py`:

```python
#!/usr/bin/env python3
"""188: Sweep randomized adaptive B distributions for lem:m2 exact SD.

Compares uniform full-rank, rank-deficient, and Bernoulli(p)-row distributions
against standard LPN_{1/4} for n=2, m=3,4.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    bernoulli_rows_B_counts,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    rank_conditioned_counts,
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

    bases = list(enumerate_lagrangian_bases())
    p_lpn = Fraction(1, 4)
    lpn_counts, lpn_denom = lpn_target_counts(m, p_lpn)

    # Uniform over all matrices == Bernoulli(1/2) rows.
    uniform_counts, uniform_denom = bernoulli_rows_B_counts(m, Fraction(1, 2), bases)
    uniform_sd = exact_sd_counts(uniform_counts, uniform_denom, lpn_counts, lpn_denom)

    # Uniform full-rank.
    full_rank_counts, full_rank_denom = rank_conditioned_counts(m, rank=m, bases=bases)
    full_rank_sd = exact_sd_counts(
        full_rank_counts, full_rank_denom, lpn_counts, lpn_denom
    )

    # Rank-deficient only meaningful for m=4 (rank 3).
    rank3_sd = None
    if m == 4:
        rank3_counts, rank3_denom = rank_conditioned_counts(m, rank=3, bases=bases)
        rank3_sd = exact_sd_counts(
            rank3_counts, rank3_denom, lpn_counts, lpn_denom
        )

    # Bernoulli(p) rows for fixed p values.
    bernoulli_sd = {}
    for p_str in ("1/4", "1/3", "1/2"):
        p = Fraction(p_str)
        counts, denom = bernoulli_rows_B_counts(m, p, bases)
        sd = exact_sd_counts(counts, denom, lpn_counts, lpn_denom)
        bernoulli_sd[p_str] = str(sd)

    # Search for best p in [0.05, 0.5] with step 0.05.
    best_p = None
    best_sd = Fraction(2)
    for k in range(1, 11):  # 0.05, 0.10, ..., 0.50
        p = Fraction(k, 20)
        counts, denom = bernoulli_rows_B_counts(m, p, bases)
        sd = exact_sd_counts(counts, denom, lpn_counts, lpn_denom)
        if sd < best_sd:
            best_sd = sd
            best_p = p

    result = {
        "n": 2,
        "m": m,
        "p_lpn": str(p_lpn),
        "num_lagrangian": len(bases),
        "uniform_sd": str(uniform_sd),
        "uniform_full_rank_sd": str(full_rank_sd),
        "rank3_sd": str(rank3_sd) if rank3_sd is not None else None,
        "bernoulli_p_sd": bernoulli_sd,
        "best_p": str(best_p),
        "best_p_sd": str(best_sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"188-lem-m2-randomized-B-distribution-sweep-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3.2: Run for $m=3$**

```bash
PYTHONPATH=. python3 experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py --m 3
```

Expected: creates `experiments/output/188-lem-m2-randomized-B-distribution-sweep-m3.json`.

- [ ] **Step 3.3: Run for $m=4$**

```bash
PYTHONPATH=. python3 experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py --m 4
```

Expected: creates `experiments/output/188-lem-m2-randomized-B-distribution-sweep-m4.json`.

- [ ] **Step 3.4: Sanity-check outputs**

```bash
PYTHONPATH=. python3 - <<'PY'
import json
from pathlib import Path
for m in (3, 4):
    p = Path(f'experiments/output/188-lem-m2-randomized-B-distribution-sweep-m{m}.json')
    data = json.loads(p.read_text())
    assert data['n'] == 2 and data['m'] == m
    assert 0 <= float(data['uniform_sd']) <= 1
    print(f"m={m}: uniform={data['uniform_sd']}, full-rank={data['uniform_full_rank_sd']}, best_p={data['best_p']}->{data['best_p_sd']}")
PY
```

- [ ] **Step 3.5: Commit**

```bash
git add experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py \
        experiments/output/188-lem-m2-randomized-B-distribution-sweep-m3.json \
        experiments/output/188-lem-m2-randomized-B-distribution-sweep-m4.json
git commit -m "feat(lem-m2): randomized B distribution sweep"
```

---

## Task 4: Interpretation note

**Files:**
- Create: `meta/2026-06-14-KIMI-lem-m2-randomized-B-distribution-sweep.md`

- [ ] **Step 4.1: Write note**

Create `meta/2026-06-14-KIMI-lem-m2-randomized-B-distribution-sweep.md` with this content. Replace the placeholders `__...__` with the exact values from the JSON files produced in Task 3.

```markdown
# lem:m2 randomized adaptive $B$ — distribution sweep

**Date:** 2026-06-14

## Model

- $n=2$, ambient dimension $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$.
- $B$ is drawn per $A$ from one of the candidate distributions.
- Output $(C,y) = (BA, B(Ax+e))$.

## Results

### $m=3$

| Distribution | SD |
|--------------|---:|
| Uniform (all $B$) | __UNIFORM_SD_M3__ |
| Uniform full-rank | __FULL_RANK_SD_M3__ |
| Bernoulli($1/4$) rows | __P1_4_SD_M3__ |
| Bernoulli($1/3$) rows | __P1_3_SD_M3__ |
| Bernoulli($1/2$) rows | __P1_2_SD_M3__ |
| Best $p^*$ | __BEST_P_M3__ -> __BEST_P_SD_M3__ |

### $m=4$

| Distribution | SD |
|--------------|---:|
| Uniform (all $B$) | __UNIFORM_SD_M4__ |
| Uniform full-rank | __FULL_RANK_SD_M4__ |
| Uniform rank-3 | __RANK3_SD_M4__ |
| Bernoulli($1/4$) rows | __P1_4_SD_M4__ |
| Bernoulli($1/3$) rows | __P1_3_SD_M4__ |
| Bernoulli($1/2$) rows | __P1_2_SD_M4__ |
| Best $p^*$ | __BEST_P_M4__ -> __BEST_P_SD_M4__ |

## Interpretation

- If uniform full-rank $B$ is materially smaller than uniform all-$B$, rank conditioning helps.
- If a Bernoulli($p^*$) with $p^* \neq 1/2$ is smaller than uniform, biasing row sparsity helps.
- If nothing beats uniform $B$ by much, the correlated noise $e'=Be$ is already close to i.i.d. for $n=2$, and the next step is scaling to $n=3$.

## Limitations

- Only $n=2$.
- Only $m=3,4$.
- Distributions are independent per $A$.
```

- [ ] **Step 4.2: Commit**

```bash
git add meta/2026-06-14-KIMI-lem-m2-randomized-B-distribution-sweep.md
git commit -m "docs(lem-m2): randomized B distribution sweep note"
```

---

## Task 5: Final review and branch finish

- [ ] **Step 5.1: Run full test suite and both runner invocations**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
PYTHONPATH=. python3 experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py --m 3
PYTHONPATH=. python3 experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py --m 4
```

- [ ] **Step 5.2: Final review subagent**

Dispatch a reviewer to check:
- correctness of rank helper against brute-force counts,
- correctness of Bernoulli helper against brute-force weighted sum,
- runner output values and JSON schema,
- interpretation note accuracy (filled-in values match JSON).

- [ ] **Step 5.3: Merge/push**

Use `superpowers:finishing-a-development-branch` to merge the work to `main` and push.

---

## Self-Review Checklist

- **Spec coverage:**
  - Rank-conditioned exact count helper: Task 1.
  - Bernoulli-row exact count helper: Task 2.
  - Distribution sweep runner and JSON outputs: Task 3.
  - Comparison table and interpretation note: Task 4.
  - Limitations ($n=2$, $m=3,4$): Task 4.
- **Placeholder scan:** No TBD/TODO in code steps. The interpretation note contains fill-in markers for the SD values, which are populated from the runner output.
- **Type consistency:** `matrix_rank_f2(rows, n_cols)`, `rank_conditioned_counts(m, rank, bases)`, `bernoulli_rows_B_counts(m, p, bases)` used consistently.
