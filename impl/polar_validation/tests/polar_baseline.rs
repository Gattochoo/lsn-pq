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
    fixed_schedule_top_l_i64, fixed_scl_binary_child_write_domain_check,
    fixed_scl_integer_metric_deltas, fixed_scl_integer_round_schedule,
    fixed_scl_integer_schedule_domain_check, fixed_scl_path_buffer_schedule_domain_check,
    fixed_scl_path_domain_failure_label, fixed_scl_public_round_work_counts,
    high_noise_control_configs, importance_results_to_json, polar_rate_row,
    polar_rate_rows_to_json, results_to_json, results_to_json_with_decoder,
    scl_work_shape_audit_json, simulate_bsc_sc, simulate_bsc_scl, simulate_bsc_scl_fast,
    simulate_bsc_scl_fast_importance, target_n2048_configs, try_fixed_scl_integer_round_schedule,
    zero_error_upper_bound, FixedSclBinaryChildWriteDomainCheck, FixedSclIntegerRoundScheduleBuild,
    FixedSclIntegerScheduleDomainCheck, FixedSclMetricDeltas, FixedSclOneBitExpansionRun,
    FixedSclPathBuffer, FixedSclPathBufferIntegerScheduleRun,
    FixedSclPathBufferScheduleDomainCheck, FixedSclPathDomainFailureLabel,
    FixedSclPublicRoundScheduleRun, FixedSclRound, FixedTopLEntry, PolarCode,
    FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX, FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY,
    FIXED_SCL_CHILD_WRITE_DOMAIN_OK, FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT,
    FIXED_SCL_FORBIDDEN_METRIC_DELTA, FIXED_SCL_NO_INVALID_ROUND, FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
    FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE, FIXED_SCL_PATH_DOMAIN_FAILURE_LABELS,
    FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY, FIXED_SCL_PATH_DOMAIN_OK,
    FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY, FIXED_SCL_PATH_DOMAIN_TOP_L_WIDTH,
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
    assert!(json.contains("\"metric_domain_assumptions\""));
    assert!(json.contains("negative metric deltas are diagnostic-only"));
    assert!(
        json.contains("future active integer SCL rail requires fixed-width non-negative penalties")
    );
    assert!(json.contains("forbidden sentinel must remain terminal"));
    assert!(json.contains("fixed_schedule_top_l_i64"));
    assert!(json.contains("FixedSclPathBuffer"));
    assert!(json.contains("fixed_scl_binary_child_write_domain_check"));
    assert!(json.contains("public child-write domain validator"));
    assert!(json.contains("try_write_binary_children_from"));
    assert!(json.contains("non-panicking child-write wrapper"));
    assert!(json.contains("write_binary_children_from"));
    assert!(json.contains("integer child expansion"));
    assert!(json.contains("expand_then_compact_one_bit"));
    assert!(json.contains("one-bit expand then compact"));
    assert!(json.contains("try_expand_then_compact_one_bit"));
    assert!(json.contains("non-panicking one-bit expand then compact wrapper"));
    assert!(json.contains("expand_then_compact_two_public_bits"));
    assert!(json.contains("two-round public-bit loop"));
    assert!(json.contains("FixedSclRound"));
    assert!(json.contains("expand_then_compact_public_rounds"));
    assert!(json.contains("public round schedule"));
    assert!(json.contains("try_expand_then_compact_two_public_bits"));
    assert!(json.contains("non-panicking two-round public-bit helper"));
    assert!(json.contains("try_expand_then_compact_public_rounds"));
    assert!(json.contains("non-panicking multi-round public schedule wrapper"));
    assert!(json.contains("fixed_scl_public_round_work_counts"));
    assert!(json.contains("public work-count audit"));
    assert!(json.contains("fixed_scl_integer_metric_deltas"));
    assert!(json.contains("integer metric delta audit"));
    assert!(json.contains("fixed_scl_integer_round_schedule"));
    assert!(json.contains("public integer round schedule audit"));
    assert!(json.contains("fixed_scl_integer_schedule_domain_check"));
    assert!(json.contains("active integer schedule domain validator"));
    assert!(json.contains("try_fixed_scl_integer_round_schedule"));
    assert!(json.contains("non-panicking integer schedule builder"));
    assert!(json.contains("fixed_scl_path_buffer_schedule_domain_check"));
    assert!(json.contains("public path-buffer shape validator"));
    assert!(json.contains("\"public_path_domain_failure_codes\""));
    assert!(json.contains("\"repeated_child_capacity\""));
    assert!(json.contains("\"top_l_width\""));
    assert!(json.contains("try_expand_then_compact_integer_round_schedule"));
    assert!(json.contains("non-panicking path-buffer schedule wrapper"));
    assert!(json.contains("expand_then_compact_integer_round_schedule"));
    assert!(json.contains("integer schedule source-level loop"));
    assert!(json.contains("\"public_work_count_examples\""));
    assert!(json.contains("\"top_l_compare_exchanges\": 18"));
    assert!(json.contains("\"child_slots_written\": 12"));
    assert!(json.contains("\"compacted_slots_written\": 6"));
    assert!(json.contains("source-level fixed schedule only"));
    assert!(json.contains("not wired into decode_scl"));
}

#[test]
fn fixed_scl_path_domain_failure_labels_cover_public_codes() {
    assert_eq!(
        FIXED_SCL_PATH_DOMAIN_FAILURE_LABELS,
        [
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_OK,
                name: "ok",
                meaning: "valid public path-buffer schedule shape",
            },
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE,
                name: "empty_schedule",
                meaning: "round schedule must contain at least one public round",
            },
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY,
                name: "first_child_capacity",
                meaning: "first child buffer must hold two children per parent slot",
            },
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY,
                name: "repeated_child_capacity",
                meaning: "repeated child buffer must hold two children per compacted path",
            },
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_TOP_L_WIDTH,
                name: "top_l_width",
                meaning: "list size must fit the parent and child selection widths",
            },
            FixedSclPathDomainFailureLabel {
                code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
                name: "bit_index",
                meaning: "every public bit index must be inside the path bit width",
            },
        ]
    );
    assert_eq!(
        fixed_scl_path_domain_failure_label(FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY),
        "repeated_child_capacity"
    );
    assert_eq!(fixed_scl_path_domain_failure_label(255), "unknown");
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
fn fixed_scl_path_buffer_writes_binary_children_into_fixed_slots() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [1, 0, 0, 0, 0, 0, 0, 0]);

    let mut children = FixedSclPathBuffer::<4, 8>::new();
    children.write_binary_children_from(&parents, 0, 2, 3, 5, 9);

    assert_eq!(children.active_count(), 2);
    assert_eq!(children.bits(2), [1, 0, 0, 0, 0, 0, 0, 0]);
    assert_eq!(children.bits(3), [1, 0, 0, 1, 0, 0, 0, 0]);
    assert_eq!(
        children.top_l_entries::<2>(),
        [
            FixedTopLEntry {
                metric: 15,
                index: 2,
            },
            FixedTopLEntry {
                metric: 19,
                index: 3,
            },
        ]
    );
}

#[test]
fn fixed_scl_binary_child_write_domain_check_accepts_public_inputs() {
    assert_eq!(
        fixed_scl_binary_child_write_domain_check::<2, 4, 8>(0, 2, 3),
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 0,
            dst_start: 2,
            bit_index: 3,
            valid: true,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
        }
    );
}

#[test]
fn fixed_scl_binary_child_write_domain_check_rejects_parent_slot() {
    assert_eq!(
        fixed_scl_binary_child_write_domain_check::<2, 4, 8>(2, 0, 3),
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 2,
            dst_start: 0,
            bit_index: 3,
            valid: false,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT,
        }
    );
}

#[test]
fn fixed_scl_binary_child_write_domain_check_rejects_destination_overflow() {
    assert_eq!(
        fixed_scl_binary_child_write_domain_check::<2, 4, 8>(1, 3, 3),
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 1,
            dst_start: 3,
            bit_index: 3,
            valid: false,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY,
        }
    );
}

#[test]
fn fixed_scl_binary_child_write_domain_check_rejects_bit_index() {
    assert_eq!(
        fixed_scl_binary_child_write_domain_check::<2, 4, 8>(1, 2, 8),
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 1,
            dst_start: 2,
            bit_index: 8,
            valid: false,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_writes_binary_children_from_valid_parent() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [1, 0, 0, 0, 0, 0, 0, 0]);

    let mut children = FixedSclPathBuffer::<4, 8>::new();
    let check = children.try_write_binary_children_from(&parents, 0, 2, 3, 5, 9);

    assert_eq!(
        check,
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 0,
            dst_start: 2,
            bit_index: 3,
            valid: true,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
        }
    );
    assert_eq!(children.active_count(), 2);
    assert_eq!(children.bits(2), [1, 0, 0, 0, 0, 0, 0, 0]);
    assert_eq!(children.bits(3), [1, 0, 0, 1, 0, 0, 0, 0]);
}

#[test]
fn fixed_scl_path_buffer_try_write_rejects_invalid_parent_without_writing() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [1, 0, 0, 0, 0, 0, 0, 0]);

    let mut children = FixedSclPathBuffer::<4, 8>::new();
    children.set_candidate(0, 99, [1; 8]);
    let before = children;

    let check = children.try_write_binary_children_from(&parents, 2, 2, 3, 5, 9);

    assert_eq!(
        check,
        FixedSclBinaryChildWriteDomainCheck {
            parent_capacity: 2,
            child_capacity: 4,
            bit_width: 8,
            parent_slot: 2,
            dst_start: 2,
            bit_index: 3,
            valid: false,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT,
        }
    );
    assert_eq!(children, before);
}

#[test]
fn fixed_scl_forbidden_delta_survives_negative_parent_metric() {
    let mut parents = FixedSclPathBuffer::<1, 4>::new();
    parents.set_candidate(0, -100, [0; 4]);

    let mut children = FixedSclPathBuffer::<2, 4>::new();
    children.write_binary_children_from(&parents, 0, 0, 1, 0, FIXED_SCL_FORBIDDEN_METRIC_DELTA);

    let entries = children.metric_entries();
    assert_eq!(entries[0].metric, -100);
    assert_eq!(entries[1].metric, FIXED_SCL_FORBIDDEN_METRIC_DELTA);
}

#[test]
#[should_panic(expected = "binary child destination requires two slots")]
fn fixed_scl_path_buffer_rejects_child_slot_overflow() {
    let parents = FixedSclPathBuffer::<1, 4>::new();
    let mut children = FixedSclPathBuffer::<2, 4>::new();
    children.write_binary_children_from(&parents, 0, 1, 0, 0, 0);
}

#[test]
fn fixed_scl_path_buffer_expands_then_compacts_one_bit() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let (children, top) = parents.expand_then_compact_one_bit::<4, 3>(2, 5, -1);

    assert_eq!(children.active_count(), 4);
    assert_eq!(children.bits(0), [0; 8]);
    assert_eq!(children.bits(1), [0, 0, 1, 0, 0, 0, 0, 0]);
    assert_eq!(children.bits(2), [1, 1, 0, 1, 1, 1, 1, 1]);
    assert_eq!(children.bits(3), [1; 8]);
    assert_eq!(
        top,
        [
            FixedTopLEntry {
                metric: 2,
                index: 3,
            },
            FixedTopLEntry {
                metric: 8,
                index: 2,
            },
            FixedTopLEntry {
                metric: 9,
                index: 1,
            },
        ]
    );
}

#[test]
fn fixed_scl_path_buffer_try_expand_then_compact_one_bit_matches_valid_expansion() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_one_bit::<4, 3>(2, 5, -1);
    let (children, top) = parents.expand_then_compact_one_bit::<4, 3>(2, 5, -1);

    assert_eq!(
        run,
        FixedSclOneBitExpansionRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 3,
                rounds: 1,
                bit_width: 8,
                valid: true,
                failure_code: FIXED_SCL_PATH_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            children,
            top,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_expand_then_compact_one_bit_rejects_small_child_buffer() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_one_bit::<3, 2>(2, 5, -1);

    assert_eq!(
        run,
        FixedSclOneBitExpansionRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 3,
                repeated_child_capacity: 3,
                list_size: 2,
                rounds: 1,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            children: FixedSclPathBuffer::<3, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_expand_then_compact_one_bit_rejects_bit_index() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_one_bit::<4, 2>(8, 5, -1);

    assert_eq!(
        run,
        FixedSclOneBitExpansionRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 1,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
                first_invalid_round: 0,
            },
            children: FixedSclPathBuffer::<4, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
#[should_panic(expected = "expand-then-compact child capacity requires two slots per parent")]
fn fixed_scl_path_buffer_expand_then_compact_rejects_small_child_buffer() {
    let parents = FixedSclPathBuffer::<2, 4>::new();
    let _ = parents.expand_then_compact_one_bit::<3, 2>(0, 0, 0);
}

#[test]
fn fixed_scl_path_buffer_expands_then_compacts_two_public_bits() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let (final_paths, final_top) =
        parents.expand_then_compact_two_public_bits::<4, 4, 2>((2, 5, -1), (4, 7, 0));

    assert_eq!(final_paths.active_count(), 2);
    assert_eq!(final_paths.bits(0), [1; 8]);
    assert_eq!(final_paths.bits(1), [1, 1, 0, 1, 1, 1, 1, 1]);
    assert_eq!(
        final_top,
        [
            FixedTopLEntry {
                metric: 2,
                index: 1,
            },
            FixedTopLEntry {
                metric: 8,
                index: 3,
            },
        ]
    );
}

#[test]
fn fixed_scl_path_buffer_try_two_public_bits_matches_valid_helper() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_two_public_bits::<4, 4, 2>((2, 5, -1), (4, 7, 0));
    let (paths, top) =
        parents.expand_then_compact_two_public_bits::<4, 4, 2>((2, 5, -1), (4, 7, 0));

    assert_eq!(
        run,
        FixedSclPublicRoundScheduleRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 2,
                bit_width: 8,
                valid: true,
                failure_code: FIXED_SCL_PATH_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            paths,
            top,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_two_public_bits_rejects_invalid_second_bit() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);

    let run = parents.try_expand_then_compact_two_public_bits::<4, 4, 2>((2, 5, -1), (8, 7, 0));

    assert_eq!(
        run,
        FixedSclPublicRoundScheduleRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 2,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
                first_invalid_round: 1,
            },
            paths: FixedSclPathBuffer::<2, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_runs_public_round_schedule() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];
    let (final_paths, final_top) = parents.expand_then_compact_public_rounds::<4, 4, 2, 3>(rounds);

    assert_eq!(final_paths.active_count(), 2);
    assert_eq!(final_paths.bits(0), [1; 8]);
    assert_eq!(final_paths.bits(1), [1, 1, 1, 1, 1, 0, 1, 1]);
    assert_eq!(
        final_top,
        [
            FixedTopLEntry {
                metric: 0,
                index: 1,
            },
            FixedTopLEntry {
                metric: 6,
                index: 0,
            },
        ]
    );
}

#[test]
fn fixed_scl_path_buffer_try_public_round_schedule_matches_valid_schedule() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];
    let run = parents.try_expand_then_compact_public_rounds::<4, 4, 2, 3>(rounds);
    let (paths, top) = parents.expand_then_compact_public_rounds::<4, 4, 2, 3>(rounds);

    assert_eq!(
        run,
        FixedSclPublicRoundScheduleRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                bit_width: 8,
                valid: true,
                failure_code: FIXED_SCL_PATH_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            paths,
            top,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_public_round_schedule_rejects_empty_schedule() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);

    let run = parents.try_expand_then_compact_public_rounds::<4, 4, 2, 0>([]);

    assert_eq!(
        run,
        FixedSclPublicRoundScheduleRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            paths: FixedSclPathBuffer::<2, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_public_round_schedule_rejects_invalid_bit_index() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);

    let rounds = [FixedSclRound::new(2, 5, -1), FixedSclRound::new(8, 7, 0)];
    let run = parents.try_expand_then_compact_public_rounds::<4, 4, 2, 2>(rounds);

    assert_eq!(
        run,
        FixedSclPublicRoundScheduleRun {
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 2,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
                first_invalid_round: 1,
            },
            paths: FixedSclPathBuffer::<2, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_runs_generated_integer_round_schedule() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let (final_paths, final_top) = parents
        .expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
            [2, 4, 5],
            [false, false, true],
            [1, 1, 1],
            [5, 7, 4],
        );

    assert_eq!(final_paths.active_count(), 2);
    assert_eq!(final_paths.bits(0), [1, 1, 1, 1, 1, 0, 1, 1]);
    assert_eq!(final_paths.bits(1), [1, 1, 0, 1, 1, 0, 1, 1]);
    assert_eq!(
        final_top,
        [
            FixedTopLEntry {
                metric: 7,
                index: 0,
            },
            FixedTopLEntry {
                metric: 12,
                index: 2,
            },
        ]
    );
}

#[test]
fn fixed_scl_path_buffer_schedule_domain_check_accepts_public_shape() {
    assert_eq!(
        fixed_scl_path_buffer_schedule_domain_check::<2, 8, 4, 4, 2, 3>([2, 4, 5]),
        FixedSclPathBufferScheduleDomainCheck {
            parent_capacity: 2,
            first_child_capacity: 4,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 3,
            bit_width: 8,
            valid: true,
            failure_code: FIXED_SCL_PATH_DOMAIN_OK,
            first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_schedule_domain_check_rejects_small_first_child_capacity() {
    assert_eq!(
        fixed_scl_path_buffer_schedule_domain_check::<2, 8, 3, 4, 2, 3>([2, 4, 5]),
        FixedSclPathBufferScheduleDomainCheck {
            parent_capacity: 2,
            first_child_capacity: 3,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 3,
            bit_width: 8,
            valid: false,
            failure_code: FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY,
            first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_schedule_domain_check_rejects_bit_index_outside_width() {
    assert_eq!(
        fixed_scl_path_buffer_schedule_domain_check::<2, 8, 4, 4, 2, 3>([2, 8, 5]),
        FixedSclPathBufferScheduleDomainCheck {
            parent_capacity: 2,
            first_child_capacity: 4,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 3,
            bit_width: 8,
            valid: false,
            failure_code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
            first_invalid_round: 1,
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_integer_round_schedule_matches_valid_schedule() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
        [2, 4, 5],
        [false, false, true],
        [1, 1, 1],
        [5, 7, 4],
    );

    assert_eq!(
        run,
        FixedSclPathBufferIntegerScheduleRun {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 3,
                valid: true,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                bit_width: 8,
                valid: true,
                failure_code: FIXED_SCL_PATH_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            paths: {
                let (paths, _) = parents.expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
                    [2, 4, 5],
                    [false, false, true],
                    [1, 1, 1],
                    [5, 7, 4],
                );
                paths
            },
            top: [
                FixedTopLEntry {
                    metric: 7,
                    index: 0,
                },
                FixedTopLEntry {
                    metric: 12,
                    index: 2,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_integer_round_schedule_reports_invalid_without_expansion() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
        [2, 4, 5],
        [false, false, true],
        [1, 1, 1],
        [5, -7, 4],
    );

    assert_eq!(
        run,
        FixedSclPathBufferIntegerScheduleRun {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 3,
                valid: false,
                first_invalid_round: 1,
            },
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                bit_width: 8,
                valid: true,
                failure_code: FIXED_SCL_PATH_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            paths: FixedSclPathBuffer::<2, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_path_buffer_try_integer_round_schedule_reports_invalid_bit_index_without_expansion() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
        [2, 8, 5],
        [false, false, true],
        [1, 1, 1],
        [5, 7, 4],
    );

    assert_eq!(
        run,
        FixedSclPathBufferIntegerScheduleRun {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 3,
                valid: true,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            path_domain_check: FixedSclPathBufferScheduleDomainCheck {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                bit_width: 8,
                valid: false,
                failure_code: FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
                first_invalid_round: 1,
            },
            paths: FixedSclPathBuffer::<2, 8>::new(),
            top: [
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
                FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                },
            ],
        }
    );
}

#[test]
fn fixed_scl_public_round_work_counts_are_public_parameters() {
    let counts = fixed_scl_public_round_work_counts(2, 4, 2, 3);

    assert_eq!(counts.rounds, 3);
    assert_eq!(counts.first_child_capacity, 4);
    assert_eq!(counts.repeated_child_capacity, 4);
    assert_eq!(counts.list_size, 2);
    assert_eq!(counts.top_l_compare_exchanges, 18);
    assert_eq!(counts.child_slots_written, 12);
    assert_eq!(counts.compacted_slots_written, 6);
}

#[test]
fn fixed_scl_integer_metric_deltas_penalize_llr_mismatch() {
    assert_eq!(
        fixed_scl_integer_metric_deltas(false, 0, 7),
        FixedSclMetricDeltas {
            bit0_metric_delta: 0,
            bit1_metric_delta: 7,
        }
    );
    assert_eq!(
        fixed_scl_integer_metric_deltas(false, 1, 7),
        FixedSclMetricDeltas {
            bit0_metric_delta: 7,
            bit1_metric_delta: 0,
        }
    );
}

#[test]
fn fixed_scl_integer_metric_deltas_forbid_frozen_one_branch() {
    assert_eq!(
        fixed_scl_integer_metric_deltas(true, 1, 7),
        FixedSclMetricDeltas {
            bit0_metric_delta: 7,
            bit1_metric_delta: FIXED_SCL_FORBIDDEN_METRIC_DELTA,
        }
    );
}

#[test]
fn fixed_scl_integer_metric_deltas_saturate_large_penalty() {
    assert_eq!(
        fixed_scl_integer_metric_deltas(false, 0, i64::MAX),
        FixedSclMetricDeltas {
            bit0_metric_delta: 0,
            bit1_metric_delta: i64::MAX,
        }
    );
}

#[test]
fn fixed_scl_integer_schedule_domain_check_accepts_active_inputs() {
    assert_eq!(
        fixed_scl_integer_schedule_domain_check([0, 1, 1], [0, 5, 7]),
        FixedSclIntegerScheduleDomainCheck {
            rounds: 3,
            valid: true,
            first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
        }
    );
}

#[test]
fn fixed_scl_integer_schedule_domain_check_rejects_negative_magnitude() {
    assert_eq!(
        fixed_scl_integer_schedule_domain_check([0, 1, 1], [0, -5, 7]),
        FixedSclIntegerScheduleDomainCheck {
            rounds: 3,
            valid: false,
            first_invalid_round: 1,
        }
    );
}

#[test]
fn fixed_scl_integer_schedule_domain_check_rejects_non_bit_hard_decision() {
    assert_eq!(
        fixed_scl_integer_schedule_domain_check([0, 2, 1], [0, 5, 7]),
        FixedSclIntegerScheduleDomainCheck {
            rounds: 3,
            valid: false,
            first_invalid_round: 1,
        }
    );
}

#[test]
fn try_fixed_scl_integer_round_schedule_builds_valid_rounds() {
    assert_eq!(
        try_fixed_scl_integer_round_schedule([0, 1], [false, true], [1, 1], [3, 5]),
        FixedSclIntegerRoundScheduleBuild {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 2,
                valid: true,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            rounds: [
                FixedSclRound::new(0, 3, 0),
                FixedSclRound::new(1, 5, FIXED_SCL_FORBIDDEN_METRIC_DELTA),
            ],
        }
    );
}

#[test]
fn try_fixed_scl_integer_round_schedule_reports_invalid_without_panicking() {
    assert_eq!(
        try_fixed_scl_integer_round_schedule([0, 1], [false, true], [1, 1], [3, -5]),
        FixedSclIntegerRoundScheduleBuild {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 2,
                valid: false,
                first_invalid_round: 1,
            },
            rounds: [FixedSclRound::new(0, 0, 0), FixedSclRound::new(0, 0, 0)],
        }
    );
}

#[test]
fn fixed_scl_integer_round_schedule_maps_public_arrays_to_rounds() {
    let rounds =
        fixed_scl_integer_round_schedule([0, 1, 2], [true, false, false], [1, 0, 1], [3, 5, 7]);

    assert_eq!(
        rounds,
        [
            FixedSclRound::new(0, 3, FIXED_SCL_FORBIDDEN_METRIC_DELTA),
            FixedSclRound::new(1, 0, 5),
            FixedSclRound::new(2, 7, 0),
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
