# Adjudication — Codex OFA-319/320 (closure-autocorrelation decoder): the structurally-different door, NOT REDUCES

> Codex attempted the one remaining REDUCES door — a **structurally-different**
> decoder (XOR-closure autocorrelation, not top-k Walsh) — exactly the Task-4-style
> probe. It finds an interesting full-observation/low-rate signal, but it **fails
> under partial observation + constant rate + n-scaling**, like Walsh. **NOT REDUCES;
> the door stays shut.** Codex's honest end: "We have not found the 7th source." This
> closes one more structural family; the genuinely-novel ones (Plücker, BP, list) of
> Kimi Task 4 remain.

## What the closure-autocorrelation decoder is (genuinely different)

`C(d) = |{x : x∈P and x+d∈P}|` (XOR autocorrelation of the noisy positive set `P`,
via FWHT), take the top `2^n` shifts as the proposed support. This exploits that the
Lagrangian `L` is **closed under XOR** — a structurally distinct signal from top-k
Walsh / support-span / ISD. A legitimate member of the "structurally-different"
family.

## OFA-319/320: it obeys the same wall

```text
OFA-319 (full observation): an interesting low-rate structural signal exists.
OFA-320 (partial observation -- the realistic public model):
  half-sampling,  n=6: 88/144 (p=0) -> 30/144 (9/256) -> 2/144 (13/256)   SHRINKS
  quarter-sampling, n=6: 18/144 even at p=0, 0/144 at p>=5/256            FAILS
```

The closure-autocorrelation signal **shrinks with noise and with sparser observation
and with n** — the same wall that broke support-span and top-k Walsh. It does **not**
hold a constant-rate threshold under n-scaling, so it is **NOT REDUCES**. Codex's
verdict — "interesting full-coordinate/low-rate signal, but OFA-320 prevents
upgrading it to REDUCES; status returns to OPEN evidence" — is exactly right.

## Verdict: NOT REDUCES, door stays shut; one more structural family closed

```text
Structurally-different decoders now tried and failing the wall:
  support-span (bounded-distance)            break ~p=0.02
  top-k Walsh / Fourier (OFA-315-318)         threshold shrinks with n
  XOR-closure autocorrelation (OFA-319/320)   shrinks with noise/sparsity/n
  closure-span COMPLETION repair (OFA-321)    also shrinks with noise (n=4 half:
                                              132/144 @p=0 -> 31/144 @13/256)  <-- new
=> the symplectic structure still yields no public poly constant-rate decoder.
   7th-evidence unchanged (OPEN), now with one more family ruled out.
```

## Honest scope — the door is narrower, not yet fully closed

Codex tried **one** structurally-different family (closure autocorrelation). It
failed. But the genuinely-novel members of Kimi Task 4 are **untested**:

```text
F1 BP / message-passing ML on the isotropic Tanner graph        -- untested
F2 Plücker / Lagrangian-Grassmannian decoding (symplectic-specific) -- untested  <-- the novel one
F3 list-decode + isotropy prune                                 -- untested
```

Codex's closure-autocorrelation is adjacent to F3 (a structural signal + top-support
selection) and it failed; F2 (the Plücker/Grassmannian angle that *uses the
symplectic relations directly*) is the one genuinely-different shot still open. So
the right division: **Codex closed the autocorrelation/closure family; Kimi Task 4
should focus on F2 (Plücker) and F1 (BP)**, the families Codex did not try.

## Net

```text
in-house verdict: 7th-EVIDENCE, unchanged. The last door is NARROWER:
  - 3 structurally-different decoder families now obey the n-scaling/partial wall
    (support-span, Walsh, closure-autocorrelation)
  - remaining open: F2 Plücker/Grassmannian + F1 BP + F3 list (Kimi Task 4)
  - and the external proof LSN ⊀ LPN
```

Codex's discipline was, again, exact: it tried the remaining door, found a real
low-rate signal, refused to over-claim when it failed the partial/n-scaling wall, and
restated "we have not found the 7th source." The in-house verdict is unmoved — every
new structural decoder converges to the same wall — and the only genuinely-open
in-house shot left is the Plücker/Grassmannian decoder of Kimi Task 4, with the
external proof beyond it.
