# CODEX ct-003: fixed top-L entry-less flag

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The fixed top-L compare-exchange helper now uses `entry_less_flag` returning a `0/1` word instead of converting a bool returned by `entry_less`. The helper keeps the same ordering rule: lower metric wins, and equal metrics keep the lower source index as the stable tie-breaker. The resulting flag is still fed into `select_i64` and `select_usize` masks for the compare-exchange swap.

## RED/GREEN

- RED: added `fixed_top_l_compare_exchange_source_uses_entry_less_flag`, which failed while `fixed_compare_exchange` used `usize::from(entry_less(b, a))`.
- GREEN: replaced the bool helper with `entry_less_flag`, computing `metric_lt | (metric_eq & index_lt)`.
- Regression: `fixed_schedule_top_l_selects_lowest_metrics_with_stable_ties` still preserves stable top-L ordering.

## Adjudication

This is a decoder-body source-level implementation step only. It is not a production constant-time, security, PQ, or 7th-source claim. The active decoder remains `not_constant_time` until the complete fixed schedule, generated-code review, memory-access review, and platform timing story are closed.
