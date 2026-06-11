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
LSN workstream B, step 1 — why the matchgate/fermion band has NO inhabitant.

thin-band VII §4 left ONE open sub-question: is there a discrete fermionic-code
decoding that sits in the band (escapes Pfaffian-easy without going #P)?  The
structural claim: matchgate simulability is CONTINUOUS (Gaussian covariance / R),
so its natural "learning with noise" is mean-estimation -> noise AVERAGES OUT ->
easy (F-1 cliff).  Clifford simulability is DISCRETE (F2 symplectic tableau), so
its noise has no averaging escape -> LPN-hard (LSN).  That is why the band has
exactly one inhabitant.  Demonstrate the dichotomy directly: matched linear
"learning with noise", once over R (matchgate analog) and once over F2 (LSN
analog), and watch the error-vs-samples scaling.
"""
import numpy as np
rng = np.random.default_rng(7)

d = 24                                  # secret dimension
Ns = [50, 100, 200, 400, 800, 1600, 3200, 6400]

print("== R / matchgate analog: Gaussian-covariance learning with noise ==")
print("   secret theta in R^d, y = A theta + N(0,sigma);  recover by least squares")
theta = rng.standard_normal(d)
sigma = 1.0
print(f"{'N':>6} {'rel.L2 error':>13} {'~ c/sqrt(N)?':>14}")
for N in Ns:
    A = rng.standard_normal((N, d))
    y = A @ theta + sigma * rng.standard_normal(N)
    th_hat, *_ = np.linalg.lstsq(A, y, rcond=None)
    err = np.linalg.norm(th_hat - theta) / np.linalg.norm(theta)
    print(f"{N:>6} {err:>13.4f} {err*np.sqrt(N):>14.3f}")
print("   => error decays ~ 1/sqrt(N): continuous noise averages out. EASY (F-1).\n")

print("== F2 / Clifford-LSN analog: LPN, same shape, noise rate p=0.25 ==")
print("   secret s in F2^d, b = A s XOR Bern(p);  try the analog 'averaging' decode")
p = 0.25
s = rng.integers(0, 2, d)
print(f"{'N':>6} {'corr-decode Ham':>16} {'LS-relax+round':>15}")
for N in Ns:
    A = rng.integers(0, 2, (N, d))
    e = (rng.random(N) < p).astype(int)
    b = (A @ s + e) % 2
    # (i) per-coordinate correlation/majority -- the F2 analog of "averaging"
    pm_b = 1 - 2 * b                                   # +-1
    pm_A = 1 - 2 * A
    corr = (pm_A * pm_b[:, None]).mean(axis=0)         # correlation of each col with b
    s_corr = (corr < 0).astype(int)                    # sign decode
    ham_corr = np.mean(s_corr != s)
    # (ii) least-squares relax over R then round (pretend F2 is R)
    bf = b.astype(float)
    s_ls, *_ = np.linalg.lstsq(A.astype(float), bf, rcond=None)
    ham_ls = np.mean((s_ls > 0.5).astype(int) != s)
    print(f"{N:>6} {ham_corr:>16.3f} {ham_ls:>15.3f}")
print("   => Hamming error stays ~0.5 (random) for BOTH naive decoders, ALL N: F2")
print("      XOR-noise does NOT average out. Recovery needs an LPN solver (sub-exp")
print("      BKW at best). HARD (the LSN layer).\n")

print("VERDICT (workstream B core): the matchgate/fermion formalism's natural")
print("'learning with noise' is CONTINUOUS mean-estimation -> averages out -> easy,")
print("so it cannot carry the band's discrete hard-decoding layer. The discreteness")
print("that DOES carry hardness (higher-Majorana stabilizers) is Jordan-Wigner-equal")
print("to qubit Clifford = LSN itself, not a second inhabitant. Continuous=archimedean")
print("=averaging-easy is the SAME geometry wall as the rest of the no-go map.")
