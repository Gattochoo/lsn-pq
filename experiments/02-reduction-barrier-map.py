# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LSN workstream A, step 1 — map the non-linear reduction barrier (convention-free).

The open question (7th vs 6.5th): can a NON-LINEAR reduction sympLPN -> LPN close
the C(n,2)-bit entropy deficiency (result #1) WITHOUT blowing the error past the
Shannon converse?  Appendix D kills the *linear* class. We probe the two natural
non-linear escapes and show where each one hits a wall. These two measurements do
NOT depend on the paper's exact matrix convention (which we deliberately avoid
re-deriving) -- they are the underlying information-theoretic mechanisms.

  2A. Linear/dense-mixing escape -> piling-up lemma wall (error -> 1/2).
  2B. Degree-2 (Veronese) escape -> Segre/rank-1 wall (deficiency gets WORSE).
"""
import math, numpy as np

rng = np.random.default_rng(12345)

# ---------------------------------------------------------------------------
# 2A. The piling-up error wall (mechanism behind Thm D.2).
# Any reduction that builds a new error bit as the XOR of w original Bern(p)
# error bits has effective noise eta(w) = (1-(1-2p)^w)/2 -> 1/2.  Uniformizing an
# entropy-deficient A demands dense mixing (large w) => error is destroyed.
# ---------------------------------------------------------------------------
print("== 2A. piling-up error wall (p=0.10) ==")
print(f"{'w (mixed err bits)':>18} {'eta_emp':>8} {'eta_formula':>12} {'decodable?':>11}")
p = 0.10
T = 400_000
for w in [1, 2, 3, 5, 8, 12, 20]:
    E = (rng.random((T, w)) < p).astype(np.int8)
    eta_emp = (E.sum(axis=1) & 1).mean()
    eta_f = (1 - (1 - 2 * p) ** w) / 2
    decodable = "yes" if eta_f < 0.25 else ("marginal" if eta_f < 0.45 else "NO (->1/2)")
    print(f"{w:>18} {eta_emp:>8.4f} {eta_f:>12.4f} {decodable:>11}")
print("  => to inject the missing ~n^2/2 bits, B must mix ~Theta(n) error bits per")
print("     output; eta(w)->1/2 long before that. Linear escape is walled.\n")

# ---------------------------------------------------------------------------
# 2B. The degree-2 (Veronese) escape makes uniformity WORSE, not better.
# A degree-2 reduction expresses b' as quadratic forms in s: b'_ij ~ <s,a_i><s,a_j>
# = <s(x)s, a_i (x) a_j>.  So the lifted LPN matrix has columns a_i (x) a_j = RANK-1
# tensors (the Segre variety).  Count how deficient that is vs uniform.
# ---------------------------------------------------------------------------
print("== 2B. degree-2 lift lands on rank-1 tensors (Segre wall) ==")
print(f"{'n':>2} {'N=2n':>5} {'iso H/unif':>11} {'lift H':>8} {'lift unif=N^2':>13} {'lift H/unif':>11}")
for n in [2, 3, 4, 5]:
    N = 2 * n
    iso_ratio = (1.5 * n * n) / (2.0 * n * n)            # result #1: (3/2)n^2 / 2n^2 = 0.75
    rank1 = (2 ** N - 1) ** 2                            # # nonzero rank-1 NxN over F2 = u v^T
    lift_H = math.log2(rank1)
    lift_unif = N * N
    print(f"{n:>2} {N:>5} {iso_ratio:>11.3f} {lift_H:>8.2f} {lift_unif:>13} {lift_H/lift_unif:>11.3f}")
print("  => isotropic A keeps 75% of uniform entropy; its degree-2 lift keeps only")
print("     ~2N/N^2 = 1/n -> collapses to ~0. The natural non-linear escape moves the")
print("     problem into a FAR more structured space, not a uniform one.\n")

print("VERDICT (Sound Verifier): OPEN, unchanged. Both natural reduction routes")
print("(linear dense-mix; degree-2 Veronese) hit information-theoretic walls. This is")
print("a BARRIER MAP (7th-evidence direction), not a proof. Sharpened target for Codex")
print("OFA: a reduction injecting the missing C(n,2) bits with error-mixing SUB-linear")
print("in w AND keeping b' linear in s (or a secret-lift that stays uniform). Search it")
print("on Sp(2n,F2)-on-Lagrangians at scale, seed-stable.")
