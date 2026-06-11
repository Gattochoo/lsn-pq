# Codex Import + Current-State Analysis

**Date:** 2026-06-11 KST
**Repo:** `lsn-pq` (`/Users/gatto/projects/lsn-pq`)
**From:** Codex returning from TRIARC-era OFA work
**Discipline:** Sound Verifier. No 7th proven; no break; no security claim. OPEN = LSN.

---

## 1. What Was Transferred From TRIARC

The raw TRIARC-era Codex branch ended at:

```text
0187c2eb research(codex): scale symplectic stress to n7
```

The important Codex artifacts are already represented in this repo's audit trail:

- `meta/2026-06-08-CLAUDE-adjudication-codex-ofa350-399-backlog.md`
  adjudicates all Codex OFA-350..399 increments and explicitly records the OFA-397/398/399
  symplectic-stress line.
- `meta/2026-06-08-kimi-security-param-validation.md`
  incorporates the OFA-399 stress-margin/noise-wall implication into the security-parameter
  validation discussion.
- `meta/2026-06-08-codex-to-kimi-k3-crosscheck-handoff.md` and
  `meta/2026-06-07-codex-to-kimi-ofa359-360-handoff.md` preserve the key Codex handoff material
  from the TRIARC workspace.

The full TRIARC `src/ota/mod.rs` harness was not imported verbatim because `lsn-pq` has a
different shape: `experiments/` contains standalone Python experiments; future Codex work is
assigned to a new Rust implementation track under `impl/`.

## 2. Current lsn-pq State

Working tree note:

```text
main...origin/main
M experiments/119-e-op9e-results.json
```

That dirty file predates this Codex import pass and appears to be an E-OP9e result rerun. Codex
must not overwrite it. Any new Codex work should avoid experiment id `119` and should preserve
this diff unless explicitly told otherwise.

Repo structure now:

- `paper/` — canonical English paper + Korean reading edition.
- `experiments/` — numbered Python verification scripts and JSON outputs.
- `meta/` — adjudications, source pins, research directives, status reports.
- `kat/`, `test_vectors/` — empty placeholders for future implementation artifacts.
- `impl/` — not yet present; Claude's return direction assigns Codex to create it.

## 3. Research Front Since OFA-399

The previous "find a 7th source" lane has been converted into a disciplined candidate-assumption
program:

- The m=3 row-map pocket is closed as 6.5th anatomy.
- The symplectic LSN line accumulated NOT REDUCES evidence through Codex OFA-399.
- The OFA-398 `Omega(a,b)` stress-margin observable is a real nonlinear signal, but OFA-399 shows
  it does not cross the constant-rate wall at n=7.
- Kimi/Claude advanced the paper and OP9 line after Codex's last TRIARC commit.
- The active theory frontier is OP9: the marginal-adaptive linear-reduction corner, now sharpened
  to a `TV(P_C,U) -> 0` style question and related Krawtchouk/Fisher-information analysis.

Important current status:

- `README.md` says LSN is an OPEN assumption, not a proven 7th family.
- `paper/lsn-paper.tex` still lists two concrete implementation gaps:
  N=2048 empirical validation and no constant-time Rust/KAT implementation.
- `meta/2026-06-12-CLAUDE-to-CODEX-return-direction.md` assigns Codex to implementation and
  scale cryptanalysis rather than further duplicating Kimi's OP9 theory work.

## 4. Claude's Current Codex Assignment

Primary direction is:

1. **P1: N=2048 polar validation.**
   Create `impl/`, implement a Rust SCL/SC validation harness, first reproduce the existing
   `N <= 512` BLER=0 behavior with the corrected natural-order frozen-set indexing, then run
   N=2048 Monte-Carlo for the paper parameters.
2. **P2: scale cryptanalysis harness.**
   Implement best-known attacks at larger n than Kimi's Python scripts, with negative controls.
3. **P3: reference Rust KEM + KAT.**
   Later, after P1/P2, build constant-time primitives and known-answer vectors.

Do not edit the paper directly. Produce reproducible code, raw JSON, and meta reports; Claude will
adjudicate before paper v2 integration.

## 5. Suggested First Codex Step

Wait for Claude's next explicit task sheet if it arrives immediately. If no new sheet arrives,
start P1 conservatively:

- create `impl/` as an isolated Rust crate or workspace member;
- implement frozen-set construction using the paper's natural-order recursion
  `z_{2i}=2z_i-z_i^2`, `z_{2i+1}=z_i^2`;
- add a RED/GREEN test for frozen-set ordering at N=128/256/512 before any decoder benchmark;
- add JSON output under `experiments/` using a new id greater than the current maximum;
- preserve the dirty `experiments/119-e-op9e-results.json`.

No 7th-source claim should be made. The correct current framing is: OPEN = LSN; Codex's role is
implementation-grade validation and adversarial scaling.
