# Reconciliation — Kimi's isolated workspace imported + verified (commit 759dc4a)

> Kimi reported committing three files (`✅`) that were **not present in the shared repo**
> (`/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared`) and not on
> `origin`. They turned out to be **real**, in Kimi's **separate, unsynced git repo**
> `/Users/gatto/.kimi_openclaw/workspace/` (commit `759dc4a`). This note records the
> verification, the import into the shared branch, the **independent convergence** of Kimi's
> Exp 24 with this session's Lane E, and an **honest correction** of an over-claim I made.
> Date: 2026-06-07. Sound Verifier discipline.

## What happened (infrastructure, not fabrication)

Kimi's autonomous session runs in a **distinct git repository** (`~/.kimi_openclaw/workspace`,
`.git` created Jun 7 01:25) that shares **no object database** with the shared worktree and is
**not pushed** to `origin` (the shared branch `shared/hardness-7th-exchange` is local-only;
`origin/shared/...` does not exist). So commit `759dc4a` and its files were genuinely
**unreachable** from the shared repo — `git cat-file -t 759dc4a` fails there — even though they
**do exist** in Kimi's workspace. A commit hash pasted in chat is not a shared commit until its
objects live in the shared repo.

## Honest correction (Sound Verifier applied to myself)

When first asked, I searched `/Users/gatto/projects`, `~/Desktop`, `~/Downloads` and reported
the files were *"nowhere on disk"* and possibly *"fabricated."* That was an **over-claim from an
incomplete search scope** — I did **not** search `~/.kimi_openclaw/`. The files are **real**; I
was wrong to suggest fabrication. My **narrower** claim — *not in the shared repo / not on
`origin`* — was correct, and is exactly why the import below was needed.

## Verification (before import)

- `git -C ~/.kimi_openclaw/workspace cat-file -t 759dc4a` → `commit` (exists); `show --stat`
  lists the 3 files (verdict 65 ln, summary 121 ln, script 395 ln).
- Safety-scanned `24-kimi-quantum-fourier-sampling.py` (imports only `numpy`, `collections`;
  no network/file/os/eval) and **ran it** → reproduces its verdict (*Power Spectrum Drowning*,
  `SNR=O(m/2^{3n})→0`, **BLOCKED** at poly-sample).

## ★ Independent convergence with this session's lanes (cross-validation)

- **Kimi Exp 24 ≍ Lane E (`1fc50610`).** Both implement the quantum symplectic-Fourier
  (Weil) sampling attack, both use the self-duality `F_Ω[1_L]=2ⁿ·1_L`, both find the
  L-concentration is above-random at clean but **exact recovery 0 and the signal dies at
  poly-sample**, and both conclude the power spectrum is the Fourier dual of the autocorrelation
  so the **channel-level closure applies quantumly** — a genuine quantum break needs
  **non-Clifford / period-finding** beyond symplectic Fourier. Two independent implementations,
  same verdict. (Kimi frames the death as "Power Spectrum Drowning `O(m/2^{3n})`"; Lane E frames
  it as the autocorrelation Fourier-dual inheriting C3 — consistent.)
- **Kimi Exp 22 ≍ Lane C7(d) + adjudicator SvN.** Both find instance-randomization is FREE
  (Witt: `Sp` transitive on Lagrangians) ⇒ the worst→avg barrier is in the noise, not the code.

## ★ Correction (added 01:44 KST) — Exp 24's CONCLUSION is right, but its EXPERIMENT lacks calibration

On closer code review I must qualify the "substantive/cross-validated" framing above: the
**conclusion** of Exp 24 is correct (and corroborated by Lane E), but Exp 24's **experiment is
methodologically weak**, and saying only "verified/converges" over-credited it. Specifically:

- **No calibration; poly-observation hardcoded even at "clean".** In `decode_fourier_samples`,
  `m = n**3` (poly) is fixed, and PHASE 1 ("Clean case (p=0), **full** Fourier samples") passes
  `p=0.0` but still observes only `m=n³` points. So the "clean" case is *clean-noise but
  poly-observation* — it never observes `L` (only `~n³/2^n→0` members), so the attack fails at
  "clean" (in_L≈0.25, **exact recovery 0%**) for the SAME reason it fails noisy. That is the
  **weak-tool fallacy** (collaboration-guide check #13): an attack that fails at clean *and*
  noisy cannot distinguish "wall" from "the tool never had the data." Exp 24 never runs the
  regime that would validate the attack (clean + **full** observation).
- **Unflagged internal contradiction.** Exp 24's SNR section asserts "Clean case … always hits
  `w∈L` (concentrated)", but its own PHASE-1 data shows `in_L≈0.25` (not ~1.0). The experiment
  contradicts the stated analysis, and Exp 24 does not notice it.
- **Contrast — Lane E DID calibrate.** Lane E (`1fc50610`) ran clean + **full** observation and
  got recovery **100%**, concentration ratio **`=2^n`** (the attack genuinely reveals `L` when it
  should), *then* showed it dies at poly-sample. That calibration is exactly what makes Lane E's
  "blocked" rigorous — and exactly what Exp 24 omits.

**Net:** Exp 24 reaches the correct verdict (quantum Fourier sampling blocked at poly-sample),
but **by convergence with the properly-calibrated Lane E, not by its own rigor.** As a
*standalone* experiment it is a weak-tool result (no calibration, an internal contradiction);
it should **not** be cited on its own as establishing the quantum wall — cite Lane E (calibrated)
for that. (Kimi's Exp 22 above stands; this caveat is specific to Exp 24.) This corrects my
earlier under-qualified "substantive/cross-validated" wording.

So Kimi's work is **substantive and independently corroborated**, not hollow.

## Import (this commit)

Copied verbatim into the shared branch (paths normalised to the shared convention):
```text
docs/superpowers/specs/2026-06-07-kimi-research-summary-for-claude-codex.md        (Kimi)
docs/superpowers/specs/2026-06-07-experiment-24-quantum-fourier-sampling-verdict.md (Kimi)
docs/superpowers/specs/lsn-experiments/24-kimi-quantum-fourier-sampling.py          (Kimi)
```
(`24-kimi-…py` does not collide with this session's `24-quantum-fourier-sampling-attack.py`;
distinct files, the two independent implementations of the same Exp 24.)

## Outstanding (infrastructure)

Kimi's other referenced experiments (Exp 20 DDD, 21 ML, 22 decoupling, 23 Weil-noise) live in
the same isolated workspace and are **not** yet imported. Fix going forward: either Kimi pushes
its workspace to `origin` (a common remote) and we fetch, or its files are imported as here.
Until then, "Kimi committed X" must be checked with `git cat-file` **in the shared repo**, not
taken from a pasted log.

## Verdict (Sound Verifier)

Kimi's `759dc4a` is **REAL and substantive**; my "fabricated/nowhere" was an over-claim (scope)
— corrected. Kimi Exp 24 is **independently confirmed** (converges with Lane E): standard
quantum Fourier sampling is **BLOCKED** at poly-sample; a true quantum break needs
non-Clifford/period-finding. **No 7th; no security claim; OPEN = LSN.** The only real failure was
**infrastructure** (unsynced repos), now reconciled by import.

---
## References
- Kimi workspace `~/.kimi_openclaw/workspace` commit `759dc4a`; imported files above.
- Lane E (`2026-06-07-lane-E-quantum-fourier-sampling-attack.md`, `1fc50610`) — the converging independent implementation.
- Lane C7 (instance-randomization free), adjudicator SvN (`2026-06-07-lane-adjudicator-svn-decoupling-assessment.md`).
