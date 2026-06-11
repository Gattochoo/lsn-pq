"""
124 — Claude round-5 verification + threat-model catch.

[1] Kimi's per-row Krawtchouk closed form phi_w(d) = K_w(d;2n)/C(2n,w) is CORRECT (verified at
    n=6, beyond Kimi's n<=5; phi_n(2) = -1/(2n-1) confirmed). The TV(P_C,U)=Omega(1/n) lower
    bound (single weight-2 test, phi_n(2)!=0) is rigorous.

[2] THREAT-MODEL MISFRAMING (propagated from the round-4 Fisher draft, which I under-flagged):
    the Fisher/TV route bounds I(x;y) in a model where "the adversary sees y but NOT C". But in
    the LPN reduction the solver sees (C,y) — C=BA is the PUBLIC LPN matrix. The relevant
    quantity is I(x; y | C). By the chain rule I(x;y) <= I(x;C,y) = I(x;y|C), so bounding I(x;y)
    (via TV(P_C,U)) does NOT bound I(x;y|C) from above. Resolving TV(P_C,U) — vanishing or not —
    does NOT close the corner. The real residue is I(x;y|C): whether the <=2n-dim noise Be is
    recovery-useless GIVEN the public C. That is the original M2 question, still OPEN.

    The empirical recovery->0 (experiments/122) IS in the correct model (max-agreement uses C),
    so the closure-leaning evidence stands; only the THEORETICAL Fisher/TV route was mis-aimed.

No 7th; no break; no security claim. OPEN = LSN.
"""
import itertools, math
def Kraw(w,d,N): return sum((-1)**j*math.comb(d,j)*math.comb(N-d,w-j) for j in range(w+1))
def phi_exact(n,w,d):
    D=2*n; tot=cnt=0
    for combo in itertools.combinations(range(D),w):
        s=set(combo); tot+=(-1)**(sum(1 for j in range(d) if (n+j) in s)%2); cnt+=1
    return tot/cnt
if __name__=="__main__":
    n=6; ok=True
    for w in [2,6,8]:
        for d in [1,2,4]:
            ok &= abs(Kraw(w,d,2*n)/math.comb(2*n,w)-phi_exact(n,w,d))<1e-9
    print(f"phi_w(d) closed form correct at n=6: {ok}; phi_n(2)={Kraw(6,2,12)/math.comb(12,6):+.5f}=-1/(2n-1)")
    print("Threat model: solver sees C ⇒ target I(x;y|C) (≥ I(x;y)); TV(P_C,U) bounds the wrong quantity.")
