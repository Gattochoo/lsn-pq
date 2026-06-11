#!/usr/bin/env python3

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
"""Analyze off-diagonal term sign and magnitude for n=2..20."""



for n in range(2, 21):

    p = 1.0 / (2**n + 1)

    q = 1.0 / ((2**(n-1) + 1) * (2**n + 1))

    

    D = (5/4)**(2*n) - 1

    T = ((3/2)**(2*n) - 1)**2 - D

    C_full = (7/4)**(2*n) - 2*(3/2)**(2*n) + 1 - D

    S_0 = (T + C_full) / 2

    

    diagonal = p * (1 - p) * D

    offdiag = q * S_0 - p * p * T

    var = diagonal + offdiag

    

    mean = 1.0 + p * ((3/2)**(2*n) - 1)

    ratio = var / (mean ** 2)

    

    print(f"n={n:2d}: diag={diagonal:.6f}, off={offdiag:+.6f}, Var={var:.6f}, "

          f"E={mean:.4f}, V/E²={ratio:.6f}")
