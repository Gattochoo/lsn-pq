// Copyright 2026 Kwanghoo Choo
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use polar_validation::{
    baseline_reproduction_configs, bhattacharyya_reliabilities, build_frozen_natural, decode_scl,
    decode_scl_fast, decode_successive_cancellation, encode, fixed_schedule_top_l_compare_count,
    fixed_schedule_top_l_i64, high_noise_control_configs, importance_results_to_json,
    polar_rate_row, polar_rate_rows_to_json, results_to_json, results_to_json_with_decoder,
    scl_work_shape_audit_json, simulate_bsc_sc, simulate_bsc_scl, simulate_bsc_scl_fast,
    simulate_bsc_scl_fast_importance, target_n2048_configs, zero_error_upper_bound,
    FixedSclPathBuffer, FixedTopLEntry, PolarCode,
};

#[test]
fn natural_order_frozen_set_matches_small_reference() {
    let frozen = build_frozen_natural(8, 4, 0.0706);
    assert_eq!(frozen, vec![4, 2, 1, 0]);
}

#[test]
fn bhattacharyya_reliabilities_preserve_natural_frozen_order() {
    let z = bhattacharyya_reliabilities(8, 0.0706);
    let mut order = (0..8).collect::<Vec<_>>();
    order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));

    assert_eq!(&order[4..], build_frozen_natural(8, 4, 0.0706).as_slice());
}

#[test]
fn polar_rate_row_marks_target_bound_status() {
    let weak_channel = polar_rate_row(2048, 256, 0.0706, -128.0);
    let strong_channel = polar_rate_row(2048, 256, 0.0343, -128.0);

    assert!(!weak_channel.passes_half_sum_target);
    assert!(strong_channel.passes_half_sum_target);
    assert!(strong_channel.half_sum_bound < weak_channel.half_sum_bound);
}

#[test]
fn polar_rate_json_records_target_and_log_bounds() {
    let row = polar_rate_row(128, 16, 0.0343, -40.0);
    let json = polar_rate_rows_to_json("codex-polar-rate-smoke", -40.0, &[row]);

    assert!(json.contains("\"experiment\": \"codex-polar-rate-smoke\""));
    assert!(json.contains("\"target_log2_half_sum_bound\": -40.000000"));
    assert!(json.contains("\"log2_half_sum_bound\""));
    assert!(json.contains("\"passes_half_sum_target\""));
}

#[test]
fn noiseless_successive_cancellation_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(8, 4, 0.0706);
    let msg = vec![1, 0, 1, 1];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_successive_cancellation(&code, &llr);
    assert_eq!(decoded, msg);
}

#[test]
fn noiseless_scl_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(16, 8, 0.0706);
    let msg = vec![1, 0, 1, 1, 0, 0, 1, 0];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_scl(&code, &llr, 8);
    assert_eq!(decoded, msg);
}

#[test]
fn noiseless_fast_scl_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(16, 8, 0.0706);
    let msg = vec![1, 0, 1, 1, 0, 0, 1, 0];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_scl_fast(&code, &llr, 8);
    assert_eq!(decoded, msg);
}

#[test]
fn short_bsc_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_sc(128, 16, 0.0343, 25, 0x5eed);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn short_bsc_scl_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_scl(128, 16, 0.0706, 25, 0x51c1, 8);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn short_bsc_fast_scl_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_scl_fast(128, 16, 0.0706, 25, 0xF451C1, 8);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn baseline_reproduction_configs_cover_paper_short_lengths() {
    let configs = baseline_reproduction_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(
        triples,
        vec![
            (128, 16, 0.0706),
            (128, 16, 0.0343),
            (256, 32, 0.0706),
            (256, 32, 0.0343),
            (512, 64, 0.0706),
            (512, 64, 0.0343),
        ]
    );
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn target_n2048_configs_cover_paper_design_points() {
    let configs = target_n2048_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(triples, vec![(2048, 256, 0.0706), (2048, 256, 0.0343)]);
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn high_noise_control_configs_cover_failure_points() {
    let configs = high_noise_control_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(
        triples,
        vec![(2048, 256, 0.3), (2048, 256, 0.4), (2048, 256, 0.5),]
    );
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn high_noise_fast_scl_smoke_fails_when_channel_is_random() {
    let result = simulate_bsc_scl_fast(128, 16, 0.5, 25, 0xBAD5EED, 8);
    assert_eq!(result.trials, 25);
    assert!(
        result.errors >= 20,
        "expected high-noise BLER near 1, got {result:?}"
    );
}

#[test]
fn scl_work_shape_audit_records_non_constant_time_surfaces() {
    let json = scl_work_shape_audit_json();

    assert!(json.contains("\"experiment\": \"codex-polar-scl-workshape-audit\""));
    assert!(json.contains("\"ct_surface\": \"ct-003\""));
    assert!(json.contains("\"current_verdict\": \"not_constant_time\""));
    assert!(json.contains("\"production_constant_time_claim\": false"));
    assert!(json.contains("path metric sort"));
    assert!(json.contains("Vec growth"));
    assert!(json.contains("floating-point path metrics"));
    assert!(json.contains("fixed-schedule integer decoder plan required"));
    assert!(json.contains("fixed_schedule_top_l_i64"));
    assert!(json.contains("FixedSclPathBuffer"));
    assert!(json.contains("source-level fixed schedule only"));
    assert!(json.contains("not wired into decode_scl"));
}

#[test]
fn fixed_schedule_top_l_selects_lowest_metrics_with_stable_ties() {
    let top = fixed_schedule_top_l_i64::<8, 4>([7, -2, 5, -2, 9, 0, 5, -3]);

    assert_eq!(
        top,
        [
            FixedTopLEntry {
                metric: -3,
                index: 7,
            },
            FixedTopLEntry {
                metric: -2,
                index: 1,
            },
            FixedTopLEntry {
                metric: -2,
                index: 3,
            },
            FixedTopLEntry {
                metric: 0,
                index: 5,
            },
        ]
    );
    assert_eq!(fixed_schedule_top_l_compare_count(8), 28);
}

#[test]
#[should_panic(expected = "top-L selector requires L <= WIDTH")]
fn fixed_schedule_top_l_rejects_invalid_width() {
    let _ = fixed_schedule_top_l_i64::<2, 3>([0, 1]);
}

#[test]
fn fixed_scl_path_buffer_uses_fixed_capacity_slots_and_top_l_view() {
    let mut buffer = FixedSclPathBuffer::<4, 8>::new();

    assert_eq!(buffer.capacity(), 4);
    assert_eq!(buffer.bit_width(), 8);
    assert_eq!(buffer.active_count(), 0);
    assert_eq!(
        buffer.metric_entries()[0],
        FixedTopLEntry {
            metric: i64::MAX,
            index: 0
        }
    );

    buffer.set_candidate(0, 42, [1, 0, 1, 0, 1, 0, 1, 0]);
    buffer.set_candidate(1, -7, [0; 8]);
    buffer.set_candidate(2, -7, [1; 8]);

    assert_eq!(buffer.active_count(), 3);
    assert_eq!(buffer.bits(2), [1; 8]);
    assert_eq!(
        buffer.top_l_entries::<2>(),
        [
            FixedTopLEntry {
                metric: -7,
                index: 1,
            },
            FixedTopLEntry {
                metric: -7,
                index: 2,
            },
        ]
    );

    buffer.clear_slot(1);

    assert_eq!(buffer.active_count(), 2);
    assert_eq!(
        buffer.top_l_entries::<2>(),
        [
            FixedTopLEntry {
                metric: -7,
                index: 2,
            },
            FixedTopLEntry {
                metric: 42,
                index: 0,
            },
        ]
    );
}

#[test]
fn result_json_records_bler_and_seed() {
    let result = simulate_bsc_sc(128, 16, 0.0343, 5, 12345);
    let json = results_to_json("codex-p1-smoke", &[result]);
    assert!(json.contains("\"experiment\": \"codex-p1-smoke\""));
    assert!(json.contains("\"seed\": 12345"));
    assert!(json.contains("\"bler\": 0"));
}

#[test]
fn result_json_can_label_scl_decoder() {
    let result = simulate_bsc_scl(128, 16, 0.0706, 5, 67890, 8);
    let json = results_to_json_with_decoder("codex-p1-scl-smoke", "scl_l8_exact_llr", &[result]);
    assert!(json.contains("\"decoder\": \"scl_l8_exact_llr\""));
}

#[test]
fn zero_error_upper_bound_matches_one_sided_binomial_formula() {
    let upper = zero_error_upper_bound(2000, 0.05);
    assert!((upper - 0.001496).abs() < 0.000001);
}

#[test]
fn importance_sampler_matches_plain_mc_when_proposal_equals_target() {
    let plain = simulate_bsc_scl_fast(128, 16, 0.4, 20, 0x1A5E_2026, 8);
    let tilted = simulate_bsc_scl_fast_importance(128, 16, 0.4, 0.4, 20, 0x1A5E_2026, 8);

    assert_eq!(tilted.proposal_errors, plain.errors);
    assert!((tilted.weighted_bler_estimate - plain.bler()).abs() < 1e-12);
    assert!((tilted.mean_likelihood_ratio - 1.0).abs() < 1e-12);
    assert!((tilted.effective_sample_size - 20.0).abs() < 1e-12);
}

#[test]
fn importance_json_records_proposal_and_weight_diagnostics() {
    let result = simulate_bsc_scl_fast_importance(128, 16, 0.4, 0.4, 5, 0x1515, 8);
    let json = importance_results_to_json("codex-p1b-importance-smoke", "scl_l8", &[result]);

    assert!(json.contains("\"sampling\": \"tilted_bsc_proposal_reweighted_to_target_bsc\""));
    assert!(json.contains("\"target_p\": 0.4000000000"));
    assert!(json.contains("\"proposal_p\": 0.4000000000"));
    assert!(json.contains("\"weighted_bler_estimate\""));
    assert!(json.contains("\"effective_sample_size\""));
}
