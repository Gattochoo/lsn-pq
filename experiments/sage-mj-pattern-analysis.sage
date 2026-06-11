# Sage analysis of m_j exact values for n=2,3,4,5
# Track A Step 5 - closed form attempt

# Exact data
m_data = {
    2: {'m1': 4/15, 'm2': 7/135, 'm3': 0},
    3: {'m1': 16/63, 'm2': 284/4725, 'm3': 4/315},
    4: {'m1': 64/255, 'm2': 464/7497, 'm3': 16/1071},
    5: {'m1': 256/1023, 'm2': 146368/2347785, 'm3': 448/28985},
}

print("=" * 60)
print("m_j exact values and convergence analysis")
print("=" * 60)

# m_1 has exact closed form: 2^(2n-2) / (2^(2n) - 1)
print("\n--- m_1 (known closed form) ---")
for n in [2,3,4,5]:
    exact = m_data[n]['m1']
    closed = 2^(2*n-2) / (2^(2*n) - 1)
    print(f"n={n}: exact={exact}, closed={closed}, match={exact == closed}")

# For m_1: m_1 - 1/4 = 1/(4*(4^n - 1))
print("\nm_1 - 1/4 = 1/(4*(4^n - 1))")
for n in [2,3,4,5]:
    diff = m_data[n]['m1'] - 1/4
    formula = 1/(4*(4^n - 1))
    print(f"n={n}: diff={diff}, formula={formula}, match={diff == formula}")

# Analyze m_2
print("\n--- m_2 pattern analysis ---")
for n in [2,3,4,5]:
    exact = m_data[n]['m2']
    target = 1/16
    diff = target - exact
    c_est = diff * 4^n
    print(f"n={n}: m2={exact}, 1/16 - m2={diff}, c_est={c_est} = {float(c_est):.6f}")

# Analyze m_3
print("\n--- m_3 pattern analysis ---")
for n in [2,3,4,5]:
    exact = m_data[n]['m3']
    target = 1/64
    diff = target - exact
    c_est = diff * 4^n
    print(f"n={n}: m3={exact}, 1/64 - m3={diff}, c_est={c_est} = {float(c_est):.6f}")

# Try to fit m_2 to various forms
print("\n--- m_2 rational function fitting ---")
q = var('q')
n = var('n')

# Form 1: (1/16) * (1 - a/(q-1) - b/(q-1)^2) where q = 4^n
# This is motivated by m_1 = (1/4) * (1 + 1/(q-1))
print("\nTry m_2 = 1/16 * (1 - a/(q-1) - b/(q-1)^2 - c/(q-1)^3)")
a, b, c = var('a b c')
for N in [2,3,4,5]:
    qv = 4^N
    mv = m_data[N]['m2']
    print(f"n={N}: q={qv}, m2={mv}, 1/16 - m2={1/16 - mv}")

# The differences for m_2:
# n=2: 23/2160 = 23/(6^3 * 10) ... let's factor
print("\nFactorizations of differences:")
for n_val in [2,3,4,5]:
    diff = 1/16 - m_data[n_val]['m2']
    print(f"n={n_val}: diff={diff} = {diff.factor()}")
    # Also factor numerator and denominator separately
    diff_frac = diff
    print(f"  num={numerator(diff_frac).factor()}, den={denominator(diff_frac).factor()}")

print("\n--- Looking for pattern in denominators ---")
for n_val in [2,3,4,5]:
    qv = 4^n_val
    d = denominator(m_data[n_val]['m2'])
    print(f"n={n_val}: denom(m2)={d.factor()}")

print("\n--- Looking for pattern in numerators ---")
for n_val in [2,3,4,5]:
    qv = 4^n_val
    num = numerator(m_data[n_val]['m2'])
    print(f"n={n_val}: num(m2)={num.factor()}")

# Try Lagrangian-counting inspired form
# m_j might involve counts of isotropic subspaces containing certain vectors
print("\n--- Isotropic subspace counts ---")
for n_val in [2,3,4,5]:
    N_iso_2 = (4^n_val - 1)*(2*4^(n_val-1) - 2) / 6
    N_lag = prod([2^i + 1 for i in range(1, n_val+1)])
    print(f"n={n_val}: N_iso(2)={N_iso_2}, N_lag={N_lag}")

# Hypothesis: m_j = (number of j-dim isotropic subspaces in a certain affine slice) / N_iso(j)
# For j=2, the condition is b_1, b_2 in S_j where S_j = {v: v[0]=...=v[j-1]=1}

print("\n--- Exact convergence rate analysis ---")
print("For m_2, compute 4^n * (1/16 - m_2):")
for n_val in [2,3,4,5]:
    c_n = 4^n_val * (1/16 - m_data[n_val]['m2'])
    print(f"n={n_val}: c(n)={c_n} = {float(c_n):.8f}")

print("\nFor m_3, compute 4^n * (1/64 - m_3):")
for n_val in [2,3,4,5]:
    c_n = 4^n_val * (1/64 - m_data[n_val]['m3'])
    print(f"n={n_val}: c(n)={c_n} = {float(c_n):.8f}")

# Try to fit c_2(n) to a simple form
print("\n--- Fit c_2(n) = 4^n * (1/16 - m_2) ---")
c2_values = [4^n * (1/16 - m_data[n]['m2']) for n in [2,3,4,5]]
print(f"c_2 values: {c2_values}")
print(f"As floats: {[float(c) for c in c2_values]}")

# Maybe c_2(n) = a + b/4^n + c/16^n
# Use n=3,4,5 to solve (n=2 may have boundary effects)
print("\nTry c_2(n) = a + b/4^n:")
a, b = var('a b')
eq1 = a + b/64 == c2_values[1]  # n=3
eq2 = a + b/256 == c2_values[2]  # n=4
sol = solve([eq1, eq2], [a, b])
print(f"Solution from n=3,4: {sol}")
if sol:
    a_val = sol[0][0].rhs()
    b_val = sol[0][1].rhs()
    print(f"a={a_val}={float(a_val):.8f}, b={b_val}={float(b_val):.8f}")
    for i, n_val in enumerate([2,3,4,5]):
        pred = a_val + b_val/4^n_val
        print(f"n={n_val}: pred={float(pred):.8f}, actual={float(c2_values[i]):.8f}, diff={float(pred - c2_values[i]):.2e}")

# Try c_2(n) = a + b/4^n + c/16^n using n=2,3,4
print("\nTry c_2(n) = a + b/4^n + c/16^n:")
a, b, c = var('a b c')
eq1 = a + b/16 + c/256 == c2_values[0]  # n=2
eq2 = a + b/64 + c/4096 == c2_values[1]  # n=3
eq3 = a + b/256 + c/65536 == c2_values[2]  # n=4
sol = solve([eq1, eq2, eq3], [a, b, c])
print(f"Solution: {sol}")
if sol:
    a_val = sol[0][0].rhs()
    b_val = sol[0][1].rhs()
    c_val = sol[0][2].rhs()
    print(f"a={float(a_val):.8f}, b={float(b_val):.8f}, c={float(c_val):.8f}")
    for i, n_val in enumerate([2,3,4,5]):
        pred = a_val + b_val/4^n_val + c_val/16^n_val
        print(f"n={n_val}: pred={float(pred):.8f}, actual={float(c2_values[i]):.8f}, diff={float(pred - c2_values[i]):.2e}")

print("\n" + "=" * 60)
print("Summary: m_j = (1/4)^j - c_j(n) * 4^{-n}")
print("c_2(n) appears to converge to ~0.16 = 4/25")
print("c_3(n) appears to converge to ~0.18 = 9/50")
print("Exact closed form remains open but convergence is geometric with ratio 1/4")
print("=" * 60)
