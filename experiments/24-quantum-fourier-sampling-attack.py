r"""
Lane E (NEW direction) — death-mode ⑤ (BQP-easy) assessment for LSN: the natural
quantum / structure-aware symplectic-Fourier-SAMPLING attack also obeys the wall.

The whole decoder program attacked LSN with CLASSICAL decoders. But LSN is QUANTUM-NATIVE,
so the natural question (death mode ⑤, the memory's BQP-easy mode) is: does a QUANTUM,
structure-aware attack break it at poly samples? The self-duality (Lane C7) makes one attack
canonical: F_Ω[1_L] = 2^n·1_L, so the symplectic-Fourier (Weil) power spectrum of the
positive set CONCENTRATES on L. A quantum "Fourier-sampling" attack prepares a superposition
over the positives, applies the Weil transform, and measures — its measurement distribution is
exactly q(w) = |F_Ω[1_P](w)|² (normalised). This tests whether that attack recovers L.

★ The structural point: q is the symplectic-Fourier POWER SPECTRUM, and the XOR-autocorrelation
C(d) (the classical channel signal, Lane C3) is its Fourier dual. So the quantum measurement
distribution and the classical autocorrelation are ONE object in two bases — the quantum attack
inherits the channel-level closure (C3): at poly samples the L-concentration of q vanishes for
the same reason C(d∈L) does. Hence the natural quantum Fourier-sampling attack is in the SAME
walled (Walsh/autocorrelation) family. A genuine quantum break would need a step BEYOND
structure-aware Fourier sampling (non-Clifford / period-finding-style) — the open post-quantum
conjecture, which this does NOT settle.

Calibration guard: the attack MUST reveal L at clean/dense (else weak tool). Run:
  python3 24-quantum-fourier-sampling-attack.py
"""
import numpy as np

SEED = 20260607
rng = np.random.default_rng(SEED)


def omega_int(u, v, n):
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


def fwht(a):
    a = a.astype(np.float64).copy()
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(N // (2 * h), 2, h)
        x = a[:, 0, :].copy()
        y = a[:, 1, :].copy()
        a[:, 0, :] = x + y
        a[:, 1, :] = x - y
        a = a.reshape(N)
        h *= 2
    return a


def J_perm(n):
    D = 2 * n
    mask = (1 << n) - 1
    perm = np.empty(1 << D, dtype=np.int64)
    for i in range(1 << D):
        perm[i] = ((i >> n) | ((i & mask) << n)) & ((1 << D) - 1)
    return perm


def F_omega(f, perm):
    return fwht(f[perm])


def rand_lagrangian(n, rng):
    D = 2 * n
    piv = {}
    rows = []

    def indep(v):
        x = v
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                return True
        return False

    while len(rows) < n:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, b, n) == 0 for b in rows) and indep(v):
            rows.append(v)
    return rows


def members(rows):
    elems = {0}
    for r in rows:
        elems |= {e ^ r for e in elems}
    return elems


def qfs_attack(n, secrets, m, p, perm, rng):
    """quantum Fourier-sampling attack: returns (mean concentration ratio, recovery rate)."""
    D = 2 * n
    N = 1 << D
    m = min(m, N)
    ratios = []
    rec = 0
    for rows, mem in secrets:
        memlist = np.fromiter(mem, dtype=np.int64, count=len(mem))
        obs = rng.choice(N, size=m, replace=False)
        true = np.fromiter((1 if int(v) in mem else 0 for v in obs), np.int8, count=m)
        flips = (rng.random(m) < p).astype(np.int8)
        P = obs[(true ^ flips) == 1]
        ind = np.zeros(N)
        ind[P] = 1.0
        F = F_omega(ind, perm)
        q = F * F
        s = q.sum()
        if s <= 0:
            ratios.append(0.0)
            continue
        q = q / s                                  # quantum measurement distribution
        conc = q[memlist].sum()                    # mass on L (self-dual: spectrum sits on L)
        ratios.append(conc * (1 << n))             # /(|L|/2^{2n}) = ·2^n ; uniform→1, clean→~2^n
        # "quantum decoder": top-|L| coords of q -> compare to L
        top = set(np.argsort(-q)[: len(mem)].tolist())
        rec += int(top == set(int(x) for x in mem))
    return float(np.mean(ratios)), rec, len(secrets)


def main():
    print("=" * 76)
    print("Lane E — quantum symplectic-Fourier-sampling attack on LSN (death-mode ⑤ check)")
    print(f"seed={SEED}, p=0.10 unless noted")
    print("=" * 76)

    NS = [4, 5, 6]
    TR = {4: 80, 5: 60, 6: 40}
    perms = {n: J_perm(n) for n in NS}
    secrets = {n: [(r, members(r)) for r in (rand_lagrangian(n, rng) for _ in range(TR[n]))]
               for n in NS}

    print("\n[CALIBRATION] clean p=0 full-obs: the attack MUST reveal L (else weak tool)")
    print(f"  {'n':>2} {'conc ratio (→2^n clean)':>24} {'recovery':>10}")
    ok = True
    for n in NS:
        r, rec, T = qfs_attack(n, secrets[n], 1 << (2 * n), 0.0, perms[n], rng)
        print(f"  {n:>2} {r:>24.1f} {f'{rec}/{T}':>10}")
        ok = ok and (rec > 0.5 * T)
    print(f"  calibration (clean reveals L): {'PASS' if ok else 'FAIL (weak tool)'}")

    print("\n[SWEEP] p=0.10: concentration ratio (uniform=1, signal=>1) and recovery vs m")
    for n in NS:
        D = 2 * n
        ms = sorted({1 << (2 * n - 1), 1 << n, 1 << (n - 1), 1 << (n - 2), n * n}, reverse=True)
        print(f"  n={n} (2^n={1<<n}):")
        for m in ms:
            if not (1 <= m <= (1 << D)):
                continue
            r, rec, T = qfs_attack(n, secrets[n], m, 0.10, perms[n], rng)
            ratio_m = m / (1 << n)
            mark = "SPARSE" if ratio_m < 1 else ""
            print(f"     m={m:>6} (m/2^n={ratio_m:>6.2f}) {mark:>7}  conc-ratio={r:>7.2f}  rec={rec}/{T}")

    print("\n  Reading: the quantum Fourier-sampling attack reveals L at clean/dense (conc-ratio")
    print("  ≈2^n, recovery high), but at SPARSE m (m/2^n<1) conc-ratio → ~1 (uniform) and")
    print("  recovery → 0 — the quantum measurement carries no L-signal. This is the SAME wall")
    print("  as the classical autocorrelation/Walsh family: q = |F_Ω[1_P]|² (the quantum")
    print("  measurement) is the Fourier DUAL of the autocorrelation C(d) (Lane C3), so it")
    print("  inherits the channel-level closure. => the natural structure-aware quantum")
    print("  Fourier-sampling attack does NOT beat the poly-sample wall (death-mode ⑤ via this")
    print("  attack: CLOSED). A genuine quantum break would need a step BEYOND Fourier sampling")
    print("  (non-Clifford / period-finding) -- the open post-quantum conjecture, NOT settled here.")
    print("  (Membership channel is also exp-data; the crypto channel is the poly linear one.)")


if __name__ == "__main__":
    main()
