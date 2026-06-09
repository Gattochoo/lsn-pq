# SBS (Sub-Barcode Signature) — BROKEN by signing-oracle key recovery (independently verified + imported)

> **Engagement correction.** The active 7th-candidate collaboration has TWO tracks: Track A
> (TRIARC/LSN, on the shared branch) and **Track B (SBS)** — Kimi's topological signature
> candidate, which lives in Kimi's **isolated** repo (`~/.kimi_openclaw/workspace`, NOT synced
> to `shared/hardness-7th-exchange`). I had been monitoring only the shared branch and **missed
> the entire SBS track**. Correcting that here: I read the SBS material, ran the signing-oracle
> attack, and **independently confirm SBS is BROKEN** — total secret-key recovery under a
> chosen-message attack — then import the runnable scripts so the shared branch reflects it.
> Date: 2026-06-07. Sound Verifier.

## SBS in one paragraph
Secret key `sk = {x_1,…,x_n} ⊂ [0,1]^d` (random points). Public key `pk = (Vietoris–Rips
persistence barcode Dgm(P), Merkle root r of the ordered coordinates)`. `Sign(m)`: derive a scale
`t=t(m)` from the message hash and **reveal the actual coordinates** of the points critical at
scale `t`, with the relevant distances and Merkle proofs binding them to `r`. `Verify`: barcode
consistency + Merkle proofs + distances. Hardness *claim*: the inverse-barcode problem (recover
`P` from `Dgm(P)`). (Scheme: Kimi Track B; theory audit: adjudicator-Claude.)

## The break (Conjecture 4 — signing-oracle leakage; flagged "barely tested", now executed)
The signature **reveals actual secret coordinates** (Merkle-bound) — a key-recovery channel that
**bypasses the inverse-barcode hardness entirely**. A chosen-message adversary requests
signatures at varying scales `t(m)`; each reveals more points' exact coordinates; once `≥ d+1`
points are known, the rest are recovered by **trilateration** from the revealed distances. Full
secret point cloud recovered.

## Independent verification (ran `sbs_signing_oracle_attack.py` from the shared branch)
```text
  n= 8 d=2 : 50/50 full key recoveries (100%)   avg 2.0 chosen msgs   max recon error (median) 0.000000
  n= 8 d=3 : 50/50 (100%)                        avg 2.0               0.000000
  n=12 d=3 : 30/30 (100%)                        avg 3.9               0.000000
  n=16 d=4 : 20/20 (100%)                        avg 8.3               0.000000
```
**100% exact key recovery in O(few) chosen messages**, every parameter set — reproduced
independently from the shared-branch copy. This is a *total* break (the recovered `P` equals the
secret to floating-point exactness), not a measure-zero or heuristic claim.

## Verdict (Sound Verifier): **BROKEN**
SBS's `EUF-CMA` security fails under chosen-message attack: the signing oracle leaks the secret
coordinates, giving full key recovery in a handful of queries. The scheme as specified is dead as
a signature. *(The underlying inverse-barcode / unlabeled-MST-spectrum inversion may remain an
interesting hardness question — and the adjudicator's audit notes the pk-only forgery route is
also "critically wounded" by underdetermination + algebraic inversion, P2, plausible-but-untested
— but the scheme is already broken by P1, so its security does not depend on settling P2.)*
This matches and confirms the adjudicator's prior theoretical estimate (`EUF-CMA survival < 10%`).

```text
SBS  = BROKEN (signing-oracle total key recovery; 100% exact, O(few) chosen messages, n≤16).
LSN  = the only surviving 7th-candidate (Track A; OPEN, reduced to external LSN∖LPN).
=> of the "two living candidates", SBS falls; LSN stands. No 7th proven; no security claim.
```

## Honest meta (the collaboration-infrastructure gap)
SBS and Kimi's latest experiments (Exp 24 v2 calibration-fix, Exp 25) are committed only in
Kimi's isolated repo (`~/.kimi_openclaw/workspace`, e.g. commit `cf38f12`), which shares no
objects with the shared branch and is not on `origin`. Monitoring only the shared branch made the
active SBS work invisible to me — an executor error (I should check agent workspaces, as I did
for Kimi's Exp 24 earlier). Going forward: agent workspaces must be polled, or the agents must
push to a common remote. This import consolidates the SBS break into the shared record.

## Credit / provenance
- SBS scheme + `sbs_signing_oracle_attack.py` / `sbs_experiment.py`: **Kimi** (Track B).
- Signing-oracle threat (Conjecture 4) + theoretical audit: **adjudicator-Claude**
  (`2026-06-06-sbs-signing-oracle-adjudication.md`, `sbs_theory_claude.md`).
- Independent execution (from shared branch) + this verdict + shared-branch import: **this session**.

## Files imported (this commit)
- `docs/superpowers/specs/sbs-experiments/sbs_signing_oracle_attack.py` (Kimi)
- `docs/superpowers/specs/sbs-experiments/sbs_experiment.py` (Kimi; the scheme prototype it imports)
