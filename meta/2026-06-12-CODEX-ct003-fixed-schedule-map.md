# CODEX ct-003 fixed-schedule map

Date: 2026-06-12

## Scope

This is a Codex handoff note for the `ct-003` polar SCL line. It maps the
known variable-shape surfaces in the current reference decoder to the
audit-only fixed-schedule prototypes added so far.

This note does not modify `paper/`, does not wire any prototype into
`decode_scl` or `decode_scl_fast`, and does not make a constant-time,
production, or security claim. The active decoder verdict remains
`not_constant_time`.

## Current Variable-Shape Surfaces

| Surface | Current source | Prototype rail | Remaining obligation |
|---|---|---|---|
| Path metric sort | `prune_paths` | `fixed_schedule_top_l_i64` | generated-code review of compare-exchange schedule; replace float ordering |
| Vec growth/truncate | `prune_paths` | `FixedSclPathBuffer` | eliminate dynamic allocation in active path |
| Candidate bit expansion | SCL path extension | `write_binary_children_from` | define masked/integer metric update for frozen vs information bits |
| One-bit prune boundary | path extension + prune | `expand_then_compact_one_bit` | connect only after integer metric design is fixed |
| Multi-round carry-forward | recursive node composition | `expand_then_compact_public_rounds` | prove public schedule covers only public control flow |
| Public work accounting | implicit in code | `fixed_scl_public_round_work_counts` and `public_work_count_examples` | compare with generated code and timing/leakage audit |
| Floating-point metrics | `decode_scl` / `decode_scl_fast` | none yet | replace with fixed-width integer or masked metric domain |
| Frozen-mask branching | decoder traversal | none yet | convert to public schedule or masked update; classify public vs secret inputs |

## Next Bounded Implementation Step

The next code increment should not wire the rail into `decode_scl`. A safer
next step is to add an audit-only integer metric update primitive:

- public inputs: branch bit, frozen flag, integer LLR sign/magnitude class;
- output: two integer deltas or masked single-path delta;
- constraints: no floating point, no allocation, no secret-dependent sort;
- tests: RED/GREEN for saturation, stable branch ordering, and frozen-bit
  behavior.

That would close one remaining gap in the rail without crossing into a
production constant-time claim.

## Verification

This note is documentation-only. Verification before commit:

- `git diff --check` on this file.
- `git status --short --branch` to ensure Kimi/Claude WIP remains unstaged.

## Interpretation

The SCL rail is now coherent enough to guide implementation, but it is still a
source-level audit scaffold. The necessary next proof objects are generated-code
inspection and timing/leakage evidence, not more positive wording.
