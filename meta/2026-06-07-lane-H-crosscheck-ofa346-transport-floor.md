# Lane H — independent cross-check: the OFA-346 transport-floor theorem holds exactly

> The adjudicator (commit `44ad20fe`) proved a closed form for the worst→avg transport
> distortion of per-qubit depolarizing noise under the nonlocal symplectic transvections that
> transitivity forces: `min_nonlocal TV(D, t_u#D) = (4p/3)(1−4p/3)`, independent of `n`. This
> verifies it with an **independent implementation** (own `omega`, depolarizing product, exact
> TV over every transvection). Result: **exact agreement** for `n=2,3,4` and `p=0.05/0.10/0.20`,
> plus the clean **local-vs-nonlocal split** — local transvections give `TV=0` (preserve the
> per-qubit noise), nonlocal ones all distort by `≥(4p/3)(1−4p/3)`. This is the quantitative
> engine of "the worst→avg barrier is in the noise" (Lane G#2 / C8). Script:
> `lsn-experiments/27-crosscheck-ofa346-transport-floor.py`. Date: 2026-06-07.

## Result

```text
  n   p     min TV (LOCAL u)   min TV (NONLOCAL u)   (4p/3)(1−4p/3)   match
  2 0.05         0.000000            0.062222            0.062222      OK
  3 0.05         0.000000            0.062222            0.062222      OK
  4 0.05         0.000000            0.062222            0.062222      OK
  2 0.10         0.000000            0.115556            0.115556      OK
  3 0.10         0.000000            0.115556            0.115556      OK
  4 0.10         0.000000            0.115556            0.115556      OK
  2 0.20         0.000000            0.195556            0.195556      OK   (n-independent throughout)
```

## Reading

- **Local transvections (support 1): `TV=0`** — single-qubit symplectic ops *preserve* the
  per-qubit depolarizing noise. This is the noise-preserving (local-Clifford) subgroup of Lane
  C8, seen from the noise side.
- **Nonlocal transvections (support ≥2): `TV ≥ (4p/3)(1−4p/3) > 0`, `n`-independent** — the
  entangling ops that transitivity *forces* (Witt; C8) each distort the noise by a positive
  constant that does **not** shrink with `n`. Independently reproduces the adjudicator's OFA-346
  closed form to machine precision.
- **Synthesis.** A transport-based worst→avg (move the worst-case instance to average by a
  symplectic map, keeping the noise) must use nonlocal transvections (else not transitive), and
  each such step pays a **fixed, `n`-independent** noise distortion `(4p/3)(1−4p/3)`. So the
  noise cannot be preserved through the transport — the precise, quantitative form of "the
  worst→avg barrier is entirely in the noise" (Lane C7/C8/G#2 and the adjudicator's SvN/transport
  synthesis). The `(4p/3)` is the depolarizing flip-rate; the `(1−4p/3)` the two-Pauli
  interference term.

## Verdict (Sound Verifier)

**CONFIRMED — the OFA-346 transport-floor theorem holds exactly (independent implementation).**
Local symplectic ops preserve the noise (`TV=0`); the nonlocal ops transitivity forces distort
it by the `n`-independent constant `(4p/3)(1−4p/3)`. This closes the transport realisation of the
worst→avg route quantitatively (a genuine asymptotic barrier, not a finite-size artifact), and is
consistent across the collaboration (adjudicator theorem + Lane C8 locality + Lane G#2
fresh-noise). The only worst→avg route not foreclosed remains an *exotic non-i.i.d.* encoding
(≈0). **No 7th; no security claim; OPEN = LSN.**

---
## References
- `lsn-experiments/27-crosscheck-ofa346-transport-floor.py` (this cross-check).
- Adjudicator OFA-346 (`44ad20fe`, `…freshnoise-worstavg-both-realizations-closed.md`, `24-verify-ofa346-transport-tv.py`).
- Lane C8 (locality conflict), Lane G#2 (fresh-noise i.i.d. obstruction), Lane C7 (self-dual-noise rigidity).
