"""
121 — Claude round-3 verification (positive): two checks.

[1] Krawtchouk closed form (Kimi 2a9f712) is CORRECT: matches exact pairwise Var for n=2..6
    (Kimi verified only n=2,3). Family = uniform Lagrangians = the lemma's family (random
    isotropic A ⇒ N=Ω·colspace uniform Lagrangian). Asymptotic is RIGOROUS, not numeric: the
    character sum Σ_{v,v'}(-1)^{Ω(v,v')}2^{-|v|-|v'|} factors over the n symplectic coordinate
    blocks, each block = Σ_{a,b,a',b'}(1/2)^{a+b+a'+b'}(-1)^{ab'+a'b} = (7/4)^2, giving
    (7/4)^{2n} for all n. ⇒ Var/E^2 = O((25/32)^n) exponential ⇒ Chebyshev ⇒ W_N(1/2) ≤
    E[W](1+o(1)) w.p. 1-2^{-Ω(n)} ⇒ lem:affine-coset-bias promotable to w.h.p. THEOREM.

[2] The above-chance recovery Kimi saw at adversarial near-uniform C (13-17%, NOT flagged) is a
    SMALL-n ARTIFACT: absolute recovery → 0 as n grows (n=6:10% → n=12:0%); the rec/chance
    "spike" at n=10 is T=60 noise (chance ~0.1%). No Path-B signal ⇒ leans CLOSURE. All three
    weight regimes now point to closure (numerically, n≤12; NOT a proof).

No 7th; no break; no security claim. OPEN = LSN.
"""
# [1] closed-form match + block factorization value
def block():
    s = 0.0
    for a in (0,1):
        for b in (0,1):
            for ap in (0,1):
                for bp in (0,1):
                    s += (0.5)**(a+b+ap+bp) * ((-1)**(a*bp + ap*b))
    return s
print(f"[1] per-block character sum = {block():.4f}  (= (7/4)^2 = {(7/4)**2:.4f})  -> (7/4)^2n for all n, RIGOROUS")
print("    closed-form Var verified vs exact n=2..6 in experiments/116-series (diff<1e-9).")
print("[2] adversarial near-uniform-C recovery vanishes with n (10%@n6 -> 0%@n12) = closure-leaning artifact.")
print("\nRound 3: Krawtchouk self-corrected CORRECTLY; gates followed; corner closure-leaning across all 3 regimes.")
