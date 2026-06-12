# lem:m2 full joint SD — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python script that computes, for $n=2$ and $m=3,4$, the exact full joint statistical distance $\mathrm{SD}((C,y), \mathrm{LPN}_{1/4})$ over all non-adaptive $B\in\F_2^{m\times 4}$.

**Architecture:** The existing helper module `experiments/lib/lem_m2_exact.py` is extended with functions for LPN target counts, reduction output counts, and exact cross-denominator SD. A runner script `experiments/185-...` enumerates all $B$, computes per-$B$ SD, and saves JSON. A separate sanity-check script verifies extreme cases.

**Tech Stack:** Python 3, `fractions.Fraction`, `collections.Counter`, `json`, `pathlib`. SageMath is not required for this small exact enumeration.

---

## File Structure

- **Modify:** `experiments/lib/lem_m2_exact.py` — add `lpn_target_counts`, `reduction_counts_for_B`, `exact_sd_counts`.
- **Modify:** `tests/test_lem_m2_exact.py` — add tests for the new helpers.
- **Create:** `experiments/185-KIMI-lem-m2-n2-full-joint-SD.py` — main enumeration runner.
- **Create:** `experiments/185b-KIMI-lem-m2-n2-full-joint-sanity.py` — sanity checks.
- **Create:** `experiments/output/185-lem-m2-n2-full-joint-SD-m{3,4}.json` — results.
- **Create:** `meta/2026-06-13-KIMI-lem-m2-n2-full-joint-SD-DRAFT.md` — interpretation note.

---

## Background

Key sizes for $n=2$:
- $|A| = 15$, $|x| = 4$, $|e| = 16$.
- $|B| = 2^{4m}$.
- $(C,y)$ key space size: $2^{2m} \cdot 2^m = 2^{3m}$.

Integer weights:
- Reduction per-$B$ total weight: $15 \cdot 4 \cdot 256 = 3840$.
- LPN target denominator: $4^m \cdot 4 \cdot 4^m = 4^{2m+1}$.

---

## Task 1: Extend helper module

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 1.1: Write failing tests**

Append to `tests/test_lem_m2_exact.py`:

```python
from fractions import Fraction
from experiments.lib.lem_m2_exact import (
    apply_matrix,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
)


def test_lpn_target_counts_normalized():
    counts, denom = lpn_target_counts(m=3, p=Fraction(1, 4))
    assert sum(counts) == denom


def test_reduction_counts_zero_B():
    m = 3
    B_cols = [0, 0, 0, 0]
    counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
    assert sum(counts) == 3840
    assert counts[0] == 3840  # only C=0, y=0
    assert all(c == 0 for c in counts[1:])


def test_exact_sd_identical():
    counts = [0, 2, 1]
    denom = 3
    sd = exact_sd_counts(counts, denom, counts, denom)
    assert sd == Fraction(0)
```

- [ ] **Step 1.2: Run tests to verify they fail**

Run:
```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```
Expected: `AttributeError` or `ImportError` for the new functions.

- [ ] **Step 1.3: Implement helpers**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def lpn_target_counts(m: int, p: Fraction) -> tuple[list[int], int]:
    """Integer counts and denominator for LPN_p distribution over (C, y)."""
    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    num_y = 1 << m
    size = num_C * num_y
    counts = [0] * size
    D = p.denominator ** m
    total_denom = num_C * 4 * D  # |C| * |x| * 4^m
    for C_key in range(num_C):
        c0 = (C_key >> m) & mask
        c1 = C_key & mask
        for x in range(1 << 2):  # n = 2
            cx = 0
            if x & 1:
                cx ^= c0
            if x & 2:
                cx ^= c1
            for eprime in range(num_y):
                w = eprime.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx ^ eprime
                key = (C_key << m) | y
                counts[key] += num
    return counts, total_denom


def reduction_counts_for_B(B_cols: list[int], bases: list[tuple[int, int]], m: int) -> list[int]:
    """Integer counts for reduction output (C, y) for a fixed B."""
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    counts = [0] * size
    for a0, a1 in bases:
        c0 = apply_matrix(B_cols, a0) & mask
        c1 = apply_matrix(B_cols, a1) & mask
        C_key = (c0 << m) | c1
        for x in range(1 << 2):  # n = 2
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):  # 2n = 4
                w = e.bit_count()
                v = a ^ e
                y = apply_matrix(B_cols, v) & mask
                key = (C_key << m) | y
                counts[key] += 3 ** (4 - w)
    return counts


def exact_sd_counts(counts1: list[int], denom1: int, counts2: list[int], denom2: int) -> Fraction:
    """Exact SD between two integer-count distributions with different denominators."""
    num = 0
    for c1, c2 in zip(counts1, counts2):
        num += abs(c1 * denom2 - c2 * denom1)
    return Fraction(num, 2 * denom1 * denom2)
```

- [ ] **Step 1.4: Run tests**

Run:
```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```
Expected: all tests PASS.

- [ ] **Step 1.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): helpers for full joint SD"
```

---

## Task 2: Main enumeration runner

**Files:**
- Create: `experiments/185-KIMI-lem-m2-n2-full-joint-SD.py`
- Create: `experiments/output/185-lem-m2-n2-full-joint-SD-m{3,4}.json`

- [ ] **Step 2.1: Write runner**

```python
#!/usr/bin/env python3
"""185: lem:m2 exact full joint SD((C,y), LPN_{1/4}) for n=2, m=3,4.

Enumerates all B in F_2^{m x 4} and computes the exact statistical distance
between the reduction output distribution and standard LPN.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
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

    lpn_counts, lpn_denom = lpn_target_counts(m, p)

    num_B = 1 << (4 * m)
    mask = (1 << m) - 1

    best_B = None
    best_sd = Fraction(2)
    worst_B = None
    worst_sd = Fraction(-1)
    sd_sum = Fraction(0)

    for bits in range(num_B):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        red_counts = reduction_counts_for_B(B_cols, bases, m)
        sd = exact_sd_counts(red_counts, 3840, lpn_counts, lpn_denom)
        sd_sum += sd
        if sd < best_sd:
            best_sd = sd
            best_B = B_cols[:]
        if sd > worst_sd:
            worst_sd = sd
            worst_B = B_cols[:]

    result = {
        "n": 2,
        "m": m,
        "p_prime": str(p),
        "num_lagrangian": len(bases),
        "num_B": num_B,
        "min_sd": str(best_sd),
        "max_sd": str(worst_sd),
        "avg_sd": str(Fraction(sd_sum, num_B)),
        "best_B": best_B,
        "worst_B": worst_B,
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"185-lem-m2-n2-full-joint-SD-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.2: Run for $m=3$**

```bash
PYTHONPATH=. python3 experiments/185-KIMI-lem-m2-n2-full-joint-SD.py --m 3
```
Expected: finishes in seconds, creates `experiments/output/185-lem-m2-n2-full-joint-SD-m3.json`.

- [ ] **Step 2.3: Run for $m=4$**

```bash
PYTHONPATH=. python3 experiments/185-KIMI-lem-m2-n2-full-joint-SD.py --m 4
```
Expected: finishes in under a few minutes, creates `experiments/output/185-lem-m2-n2-full-joint-SD-m4.json`.

- [ ] **Step 2.4: Verify outputs**

```bash
PYTHONPATH=. python3 - <<'PY'
import json
for m in (3, 4):
    p = Path(f'experiments/output/185-lem-m2-n2-full-joint-SD-m{m}.json')
    data = json.loads(p.read_text())
    assert data['n'] == 2 and data['m'] == m
    assert data['p_prime'] == '1/4'
    print(m, data['min_sd'], data['max_sd'], data['avg_sd'])
PY
```

- [ ] **Step 2.5: Commit**

```bash
git add experiments/185-KIMI-lem-m2-n2-full-joint-SD.py \
        experiments/output/185-lem-m2-n2-full-joint-SD-m3.json \
        experiments/output/185-lem-m2-n2-full-joint-SD-m4.json
git commit -m "feat(lem-m2): exact n=2 full joint SD for m=3,4"
```

---

## Task 3: Sanity checks

**Files:**
- Create: `experiments/185b-KIMI-lem-m2-n2-full-joint-sanity.py`

- [ ] **Step 3.1: Write sanity script**

```python
#!/usr/bin/env python3
"""185b: Sanity checks for full joint SD enumeration."""
from fractions import Fraction

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
)


def check_zero_B_is_far():
    m = 3
    B_cols = [0, 0, 0, 0]
    red_counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
    lpn_counts, lpn_denom = lpn_target_counts(m, Fraction(1, 4))
    sd = exact_sd_counts(red_counts, 3840, lpn_counts, lpn_denom)
    assert sd > Fraction(9, 10), f"zero-B SD unexpectedly small: {sd}"
    print(f"zero-B SD for m={m}: {sd} (OK)")


def check_bounds():
    m = 3
    lpn_counts, lpn_denom = lpn_target_counts(m, Fraction(1, 4))
    best = Fraction(2)
    worst = Fraction(-1)
    mask = (1 << m) - 1
    for bits in range(1 << (4 * m)):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        red_counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
        sd = exact_sd_counts(red_counts, 3840, lpn_counts, lpn_denom)
        assert 0 <= sd <= 1
        if sd < best:
            best = sd
        if sd > worst:
            worst = sd
    print(f"m={m} SD bounds: [{best}, {worst}] (OK)")


if __name__ == "__main__":
    check_zero_B_is_far()
    check_bounds()
```

- [ ] **Step 3.2: Run sanity checks**

```bash
PYTHONPATH=. python3 experiments/185b-KIMI-lem-m2-n2-full-joint-sanity.py
```
Expected:
```
zero-B SD for m=3: ... (OK)
m=3 SD bounds: [..., ...] (OK)
```

- [ ] **Step 3.3: Commit**

```bash
git add experiments/185b-KIMI-lem-m2-n2-full-joint-sanity.py
git commit -m "test(lem-m2): sanity checks for full joint SD"
```

---

## Task 4: Interpretation note

**Files:**
- Create: `meta/2026-06-13-KIMI-lem-m2-n2-full-joint-SD-DRAFT.md`

- [ ] **Step 4.1: Write note**

Template contents:
- What was computed.
- $m=3,4$ results for $\min/\max/\mathrm{avg}\;\mathrm{SD}$.
- Interpretation:
  - If $\min_B \mathrm{SD} > 0$: no non-adaptive $B$ perfectly simulates $\mathrm{LPN}_{1/4}$ for $n=2$ → evidence for `lem:m2`.
  - If $\min_B \mathrm{SD} = 0$: candidate counterexample.
- Compare with the earlier noise-only result (best noise SD was 0, but full joint is not).
- Limitations: $n=2$, non-adaptive $B$, $p'=1/4$.

- [ ] **Step 4.2: Commit**

```bash
git add meta/2026-06-13-KIMI-lem-m2-n2-full-joint-SD-DRAFT.md
git commit -m "docs(lem-m2): interpretation draft for full joint SD"
```

---

## Task 5: Final review and branch finish

- [ ] **Step 5.1: Run all tests and sanity checks**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
PYTHONPATH=. python3 experiments/185b-KIMI-lem-m2-n2-full-joint-sanity.py
```

- [ ] **Step 5.2: Final review subagent**

Dispatch a final reviewer to check all files, outputs, and note.

- [ ] **Step 5.3: Merge/push**

Use `superpowers:finishing-a-development-branch` to merge to `main` and push.

---

## Self-Review Checklist

- **Spec coverage:**
  - Full joint SD formula: Task 2 `exact_sd_counts`.
  - LPN target distribution: Task 1 `lpn_target_counts`.
  - Reduction output counts: Task 1 `reduction_counts_for_B`.
  - $m=3,4$ runs: Task 2.
  - Output JSON: Task 2.
  - Sanity checks: Task 3.
  - Interpretation note: Task 4.
- **Placeholder scan:** No TBD/TODO; all code blocks concrete.
- **Type consistency:** `B_cols` always list of 4 $m$-bit ints; combined key `(C_key << m) | y`; `counts` length `1 << (3*m)` consistent across helpers and runner.
