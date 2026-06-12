# lem:m2 deterministic adaptive bound — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a verification script and proof note that establish and check the deterministic adaptive $B=g(A)$ lower bound $\mathrm{SD}((C,y),\mathrm{LPN}) \ge 1 - |\mathrm{Lagr}(2n,\F_2)| / 2^{mn}$.

**Architecture:** Add a `num_lagrangian_subspaces(n)` helper to the existing helper module with a test. A small script computes the bound for $n=2$, $m=2..6$, loads experiment 185 JSON minima for $m=3,4$, and saves a JSON. A meta note states the theorem and interprets the comparison.

**Tech Stack:** Python 3, `fractions.Fraction`, `json`, `pathlib`.

---

## File Structure

- **Modify:** `experiments/lib/lem_m2_exact.py` — add `num_lagrangian_subspaces(n)`.
- **Modify:** `tests/test_lem_m2_exact.py` — add test for the new helper.
- **Create:** `experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py` — verification script.
- **Create:** `experiments/output/186-lem-m2-deterministic-adaptive-bound.json` — results.
- **Create:** `meta/2026-06-13-KIMI-lem-m2-deterministic-adaptive-bound.md` — proof/interpretation note.

---

## Task 1: Add Lagrangian count helper

**Files:**
- Modify: `experiments/lib/lem_m2_exact.py`
- Test: `tests/test_lem_m2_exact.py`

- [ ] **Step 1.1: Write failing test**

Append to `tests/test_lem_m2_exact.py`:

```python
from experiments.lib.lem_m2_exact import num_lagrangian_subspaces


def test_num_lagrangian_subspaces():
    assert num_lagrangian_subspaces(1) == 3
    assert num_lagrangian_subspaces(2) == 15
    assert num_lagrangian_subspaces(3) == 135
```

- [ ] **Step 1.2: Run tests to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py::test_num_lagrangian_subspaces -v
```
Expected: `AttributeError` or `ImportError`.

- [ ] **Step 1.3: Implement helper**

Append to `experiments/lib/lem_m2_exact.py`:

```python
def num_lagrangian_subspaces(n: int) -> int:
    """Number of Lagrangian subspaces of F_2^{2n}."""
    if n < 1:
        raise ValueError("n must be >= 1")
    total = 1
    for i in range(1, n + 1):
        total *= (2 ** i + 1)
    return total
```

- [ ] **Step 1.4: Run tests**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
```
Expected: all tests PASS.

- [ ] **Step 1.5: Commit**

```bash
git add experiments/lib/lem_m2_exact.py tests/test_lem_m2_exact.py
git commit -m "feat(lem-m2): Lagrangian subspace count helper"
```

---

## Task 2: Verification script

**Files:**
- Create: `experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py`
- Create: `experiments/output/186-lem-m2-deterministic-adaptive-bound.json`

- [ ] **Step 2.1: Write script**

```python
#!/usr/bin/env python3
"""186: Verify deterministic adaptive B lower bound for lem:m2.

Theorem: for deterministic B=g(A), SD((C,y), LPN) >= 1 - |Lagr(2n,F2)| / 2^{mn}.
For n=2 this is 1 - 15 / 4^m.
"""
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import num_lagrangian_subspaces


def main():
    n = 2
    num_lag = num_lagrangian_subspaces(n)

    results = {
        "n": n,
        "num_lagrangian": num_lag,
        "theorem": "SD((C,y), LPN) >= 1 - |Lagr| / 2^{mn} for deterministic B=g(A)",
        "bounds": [],
    }

    for m in range(2, 7):
        C_space_size = 1 << (m * n)
        bound = Fraction(C_space_size - num_lag, C_space_size)
        entry = {
            "m": m,
            "C_space_size": C_space_size,
            "lower_bound": str(bound),
            "lower_bound_float": float(bound),
        }

        # Compare with experiment 185 min SD if available
        json_path = Path("experiments/output") / f"185-lem-m2-n2-full-joint-SD-m{m}.json"
        if json_path.exists():
            data = json.loads(json_path.read_text())
            entry["exp185_min_sd"] = data.get("min_sd")
            entry["matches_bound"] = (data.get("min_sd") == str(bound))

        results["bounds"].append(entry)

    out_path = Path("experiments/output") / "186-lem-m2-deterministic-adaptive-bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.2: Run script**

```bash
PYTHONPATH=. python3 experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py
```
Expected: creates `experiments/output/186-lem-m2-deterministic-adaptive-bound.json` and prints the saved path.

- [ ] **Step 2.3: Verify output**

```bash
PYTHONPATH=. python3 - <<'PY'
import json
p = Path('experiments/output/186-lem-m2-deterministic-adaptive-bound.json')
data = json.loads(p.read_text())
assert data['num_lagrangian'] == 15
for e in data['bounds']:
    if e['m'] in (3, 4):
        assert e['matches_bound'] is True
print(json.dumps(data, indent=2))
PY
```

- [ ] **Step 2.4: Commit**

```bash
git add experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py \
        experiments/output/186-lem-m2-deterministic-adaptive-bound.json
git commit -m "feat(lem-m2): deterministic adaptive B lower bound verification"
```

---

## Task 3: Proof/interpretation note

**Files:**
- Create: `meta/2026-06-13-KIMI-lem-m2-deterministic-adaptive-bound.md`

- [ ] **Step 3.1: Write note**

Use the spec text as the basis. Include:
- Statement of the theorem.
- Proof (support size + data processing).
- Verification table for $m=3,4$.
- General $n$ formula.
- Limitation: deterministic only.

- [ ] **Step 3.2: Commit**

```bash
git add meta/2026-06-13-KIMI-lem-m2-deterministic-adaptive-bound.md
git commit -m "docs(lem-m2): deterministic adaptive B lower bound note"
```

---

## Task 4: Final review and branch finish

- [ ] **Step 4.1: Run tests and script**

```bash
PYTHONPATH=. python3 -m pytest tests/test_lem_m2_exact.py -v
PYTHONPATH=. python3 experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py
```

- [ ] **Step 4.2: Final review subagent**

Dispatch a reviewer to check helper, script, output, and note.

- [ ] **Step 4.3: Merge/push**

Use `superpowers:finishing-a-development-branch` to merge to `main` and push.

---

## Self-Review Checklist

- **Spec coverage:**
  - Lagrangian count helper: Task 1.
  - Lower bound computation: Task 2.
  - Comparison with 185: Task 2.
  - Proof note: Task 3.
- **Placeholder scan:** No TBD/TODO.
- **Type consistency:** `num_lagrangian_subspaces(n: int) -> int` used consistently.
