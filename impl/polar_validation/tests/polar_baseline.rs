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
    fixed_schedule_top_l_i64, fixed_schedule_top_l_selection_plan,
    fixed_scl_binary_child_write_domain_check, fixed_scl_child_write_domain_failure_label,
    fixed_scl_child_write_parity_check, fixed_scl_integer_metric_deltas,
    fixed_scl_integer_round_build_certificate, fixed_scl_integer_round_build_parity_check,
    fixed_scl_integer_round_run_plan_certificate, fixed_scl_integer_round_run_shape_certificate,
    fixed_scl_integer_round_schedule, fixed_scl_integer_round_schedule_build_plan,
    fixed_scl_integer_round_schedule_plan, fixed_scl_integer_round_schedule_shape_plan,
    fixed_scl_integer_schedule_domain_check, fixed_scl_integer_schedule_domain_failure_label,
    fixed_scl_integer_schedule_shape_failure_family,
    fixed_scl_integer_schedule_shape_failure_label, fixed_scl_integer_schedule_shape_parity_check,
    fixed_scl_integer_shape_parity_check, fixed_scl_one_bit_run_plan_certificate,
    fixed_scl_one_bit_shape_parity_check, fixed_scl_path_buffer_schedule_domain_check,
    fixed_scl_path_domain_failure_label, fixed_scl_public_round_run_shape_certificate,
    fixed_scl_public_round_schedule_plan, fixed_scl_public_round_schedule_shape_failure_family,
    fixed_scl_public_round_schedule_shape_failure_label,
    fixed_scl_public_round_schedule_shape_plan, fixed_scl_public_round_shape_parity_check,
    fixed_scl_public_round_work_counts, fixed_scl_public_round_work_counts_with_capacities,
    fixed_scl_public_round_work_shape_plan, fixed_scl_round_schedule_plan,
    fixed_scl_round_schedule_plan_certificate, fixed_scl_round_schedule_plan_parity_check,
    fixed_scl_round_schedule_shape_parity_check, fixed_scl_round_schedule_shape_plan,
    fixed_scl_round_schedule_shape_plan_certificate, fixed_top_l_selection_domain_failure_label,
    high_noise_control_configs, importance_results_to_json, polar_rate_row,
    polar_rate_rows_to_json, results_to_json, results_to_json_with_decoder,
    scl_work_shape_audit_json, simulate_bsc_sc, simulate_bsc_scl, simulate_bsc_scl_fast,
    simulate_bsc_scl_fast_importance, target_n2048_configs, try_fixed_scl_integer_round_schedule,
    two_public_bits_run_shape_certificate, two_public_bits_shape_parity_check,
    zero_error_upper_bound, FixedScheduleTopLSelectionDomainFailureLabel,
    FixedScheduleTopLSelectionPlan, FixedSclBinaryChildWriteDomainCheck,
    FixedSclChildWriteDomainFailureLabel, FixedSclChildWriteParityCheck,
    FixedSclIntegerRoundScheduleBuild, FixedSclIntegerRoundScheduleBuildParityCheck,
    FixedSclIntegerRoundScheduleBuildPlan, FixedSclIntegerRoundSchedulePlan,
    FixedSclIntegerRoundScheduleShapePlan, FixedSclIntegerScheduleDomainCheck,
    FixedSclIntegerScheduleDomainFailureLabel, FixedSclIntegerScheduleShapeFailureLabel,
    FixedSclIntegerScheduleShapeParityCheck, FixedSclIntegerShapeParityCheck, FixedSclMetricDeltas,
    FixedSclOneBitExpansionRun, FixedSclOneBitShapeParityCheck, FixedSclPathBuffer,
    FixedSclPathBufferIntegerScheduleRun, FixedSclPathBufferScheduleDomainCheck,
    FixedSclPathDomainFailureLabel, FixedSclPublicRoundSchedulePlan,
    FixedSclPublicRoundScheduleRun, FixedSclPublicRoundScheduleShapeFailureLabel,
    FixedSclPublicRoundScheduleShapePlan, FixedSclPublicRoundShapeParityCheck,
    FixedSclPublicRoundWorkCounts, FixedSclPublicRoundWorkShapePlan, FixedSclRound,
    FixedSclRoundSchedulePlanParityCheck, FixedSclRoundScheduleShapeParityCheck, FixedTopLEntry,
    PolarCode, FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX, FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY,
    FIXED_SCL_CHILD_WRITE_DOMAIN_FAILURE_LABELS, FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
    FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT, FIXED_SCL_FORBIDDEN_METRIC_DELTA,
    FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_FAILURE_LABELS, FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
    FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE, FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
    FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN,
    FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK,
    FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN,
    FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE,
    FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_LABELS, FIXED_SCL_NO_INVALID_ROUND,
    FIXED_SCL_PATH_DOMAIN_BIT_INDEX, FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE,
    FIXED_SCL_PATH_DOMAIN_FAILURE_LABELS, FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY,
    FIXED_SCL_PATH_DOMAIN_OK, FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY,
    FIXED_SCL_PATH_DOMAIN_TOP_L_WIDTH, FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK,
    FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN,
    FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE,
    FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_LABELS,
    FIXED_TOP_L_SELECTION_DOMAIN_FAILURE_LABELS, FIXED_TOP_L_SELECTION_DOMAIN_OK,
    FIXED_TOP_L_SELECTION_DOMAIN_WIDTH,
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
    assert!(json.contains("\"top_l_selection_domain_failure_codes\""));
    assert!(json.contains("\"width\""));
    assert!(json.contains("negative metric deltas are diagnostic-only"));
    assert!(
        json.contains("future active integer SCL rail requires fixed-width non-negative penalties")
    );
    assert!(json.contains("forbidden sentinel must remain terminal"));
    assert!(json.contains("fixed_schedule_top_l_i64"));
    assert!(json.contains("fixed_schedule_top_l_selection_plan"));
    assert!(json.contains("execution-free top-L selection preflight"));
    assert!(json.contains("FixedSclPathBuffer"));
    assert!(json.contains("fixed_scl_binary_child_write_domain_check"));
    assert!(json.contains("public child-write domain validator"));
    assert!(json.contains("fixed_scl_child_write_parity_check"));
    assert!(json.contains("child-write run/preflight parity record"));
    assert!(json.contains("\"public_child_write_failure_codes\""));
    assert!(json.contains("\"dst_capacity\""));
    assert!(json.contains("\"parent_slot\""));
    assert!(json.contains("try_write_binary_children_from"));
    assert!(json.contains("non-panicking child-write wrapper"));
    assert!(json.contains("write_binary_children_from"));
    assert!(json.contains("integer child expansion"));
    assert!(json.contains("expand_then_compact_one_bit"));
    assert!(json.contains("one-bit expand then compact"));
    assert!(json.contains("try_expand_then_compact_one_bit"));
    assert!(json.contains("non-panicking one-bit expand then compact wrapper"));
    assert!(json.contains("fixed_scl_one_bit_run_plan_certificate"));
    assert!(json.contains("one-bit run/preflight plan certificate adapter"));
    assert!(json.contains("fixed_scl_one_bit_shape_parity_check"));
    assert!(json.contains("one-bit run/preflight shape parity record"));
    assert!(json.contains("expand_then_compact_two_public_bits"));
    assert!(json.contains("two-round public-bit loop"));
    assert!(json.contains("two_public_bits_run_shape_certificate"));
    assert!(json.contains("two-public-bits run/preflight shape certificate adapter"));
    assert!(json.contains("two_public_bits_shape_parity_check"));
    assert!(json.contains("two-public-bits run/preflight shape parity record"));
    assert!(json.contains("FixedSclRound"));
    assert!(json.contains("expand_then_compact_public_rounds"));
    assert!(json.contains("public round schedule"));
    assert!(json.contains("try_expand_then_compact_two_public_bits"));
    assert!(json.contains("non-panicking two-round public-bit helper"));
    assert!(json.contains("try_expand_then_compact_public_rounds"));
    assert!(json.contains("non-panicking multi-round public schedule wrapper"));
    assert!(json.contains("fixed_scl_public_round_run_shape_certificate"));
    assert!(json.contains("public run-shape certificate adapter"));
    assert!(json.contains("fixed_scl_public_round_shape_parity_check"));
    assert!(json.contains("public run/preflight shape parity record"));
    assert!(json.contains("fixed_scl_round_schedule_plan"));
    assert!(json.contains("execution-free FixedSclRound schedule preflight"));
    assert!(json.contains("fixed_scl_round_schedule_plan_parity_check"));
    assert!(json.contains("FixedSclRound schedule/public preflight parity record"));
    assert!(json.contains("fixed_scl_round_schedule_shape_parity_check"));
    assert!(json.contains("FixedSclRound schedule/public shape parity record"));
    assert!(json.contains("fixed_scl_public_round_schedule_plan"));
    assert!(json.contains("execution-free public schedule preflight"));
    assert!(json.contains("fixed_scl_public_round_schedule_shape_plan"));
    assert!(json.contains("execution-free public schedule shape certificate"));
    assert!(json.contains("fixed_scl_public_round_schedule_shape_failure_family"));
    assert!(json.contains("public schedule-shape failure-family classifier"));
    assert!(json.contains("fixed_scl_integer_round_schedule_plan"));
    assert!(json.contains("execution-free integer schedule preflight"));
    assert!(json.contains("fixed_scl_integer_round_schedule_build_plan"));
    assert!(json.contains("execution-free integer schedule-build preflight"));
    assert!(json.contains("fixed_scl_integer_round_build_parity_check"));
    assert!(json.contains("integer schedule-build run/preflight parity record"));
    assert!(json.contains("fixed_scl_integer_round_run_plan_certificate"));
    assert!(json.contains("integer run/preflight plan certificate adapter"));
    assert!(json.contains("fixed_scl_integer_shape_parity_check"));
    assert!(json.contains("integer run/preflight shape parity record"));
    assert!(json.contains("fixed_scl_integer_schedule_shape_parity_check"));
    assert!(json.contains("integer schedule/run shape parity record"));
    assert!(json.contains("fixed_scl_integer_schedule_shape_failure_family"));
    assert!(json.contains("integer schedule-shape failure-family classifier"));
    assert!(json.contains("fixed_scl_public_round_work_counts"));
    assert!(json.contains("public work-count audit"));
    assert!(json.contains("fixed_scl_public_round_work_shape_plan"));
    assert!(json.contains("execution-free public round work-shape plan"));
    assert!(json.contains("fixed_scl_integer_metric_deltas"));
    assert!(json.contains("integer metric delta audit"));
    assert!(json.contains("fixed_scl_integer_round_schedule"));
    assert!(json.contains("public integer round schedule audit"));
    assert!(json.contains("fixed_scl_integer_schedule_domain_check"));
    assert!(json.contains("active integer schedule domain validator"));
    assert!(json.contains("\"integer_schedule_domain_failure_codes\""));
    assert!(json.contains("\"hard_bit\""));
    assert!(json.contains("\"magnitude\""));
    assert!(json.contains("try_fixed_scl_integer_round_schedule"));
    assert!(json.contains("non-panicking integer schedule builder"));
    assert!(json.contains("FixedSclIntegerRoundScheduleBuild.round_slots_written"));
    assert!(json.contains("fixed_scl_path_buffer_schedule_domain_check"));
    assert!(json.contains("public path-buffer shape validator"));
    assert!(json.contains("\"public_path_domain_failure_codes\""));
    assert!(json.contains("\"repeated_child_capacity\""));
    assert!(json.contains("\"top_l_width\""));
    assert!(json.contains("\"non_panicking_wrapper_failure_code_map\""));
    assert!(json.contains("\"wrapper\": \"try_write_binary_children_from\""));
    assert!(json.contains("\"failure_family\": \"public_child_write_failure_codes\""));
    assert!(json.contains(
        "\"work_count_field\": \"FixedSclBinaryChildWriteDomainCheck.child_slots_written\""
    ));
    assert!(json.contains("\"work_count_field\": \"FixedSclOneBitExpansionRun.work_counts\""));
    assert!(json.contains("\"wrapper\": \"try_fixed_scl_integer_round_schedule\""));
    assert!(json.contains(
        "\"status_field\": \"FixedSclIntegerRoundScheduleBuild.domain_check.failure_code\""
    ));
    assert!(json.contains("\"wrapper\": \"try_expand_then_compact_integer_round_schedule\""));
    assert!(json.contains("\"work_count_field\": \"FixedSclPublicRoundScheduleRun.work_counts\""));
    assert!(json.contains("\"integer_status_family\": \"integer_schedule_domain_failure_codes\""));
    assert!(json.contains(
        "\"path_status_field\": \"FixedSclPathBufferIntegerScheduleRun.path_domain_check.failure_code\""
    ));
    assert!(json.contains(
        "\"integer_status_field\": \"FixedSclPathBufferIntegerScheduleRun.domain_check.failure_code\""
    ));
    assert!(
        json.contains("\"work_count_field\": \"FixedSclPathBufferIntegerScheduleRun.work_counts\"")
    );
    assert!(json.contains("try_expand_then_compact_integer_round_schedule"));
    assert!(json.contains("non-panicking path-buffer schedule wrapper"));
    assert!(json.contains("expand_then_compact_integer_round_schedule"));
    assert!(json.contains("integer schedule source-level loop"));
    assert!(json.contains("\"public_work_count_examples\""));
    assert!(json.contains("\"top_l_compare_exchanges\": 18"));
    assert!(json.contains("\"child_slots_written\": 12"));
    assert!(json.contains("\"compacted_slots_written\": 6"));
    assert!(json.contains("fixed_scl_public_round_work_counts_with_capacities"));
    assert!(json.contains("\"first_child_capacity\": 6"));
    assert!(json.contains("\"repeated_child_capacity\": 4"));
    assert!(json.contains("\"top_l_compare_exchanges\": 27"));
    assert!(json.contains("\"child_slots_written\": 14"));
    assert!(json.contains("zero_rounds_no_expansion_work"));
    assert!(json.contains("\"top_l_compare_exchanges\": 0"));
    assert!(json.contains("\"child_slots_written\": 0"));
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
fn fixed_top_l_selection_domain_failure_labels_cover_public_codes() {
    assert_eq!(
        FIXED_TOP_L_SELECTION_DOMAIN_FAILURE_LABELS,
        [
            FixedScheduleTopLSelectionDomainFailureLabel {
                code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
                name: "ok",
                meaning: "valid public top-L selection shape",
            },
            FixedScheduleTopLSelectionDomainFailureLabel {
                code: FIXED_TOP_L_SELECTION_DOMAIN_WIDTH,
                name: "width",
                meaning: "list size must be no larger than selection width",
            },
        ]
    );
    assert_eq!(
        fixed_top_l_selection_domain_failure_label(FIXED_TOP_L_SELECTION_DOMAIN_WIDTH),
        "width"
    );
    assert_eq!(fixed_top_l_selection_domain_failure_label(255), "unknown");
}

#[test]
fn fixed_scl_child_write_domain_failure_labels_cover_public_codes() {
    assert_eq!(
        FIXED_SCL_CHILD_WRITE_DOMAIN_FAILURE_LABELS,
        [
            FixedSclChildWriteDomainFailureLabel {
                code: FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
                name: "ok",
                meaning: "valid public fixed child-write domain",
            },
            FixedSclChildWriteDomainFailureLabel {
                code: FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT,
                name: "parent_slot",
                meaning: "parent slot must be inside the fixed parent buffer",
            },
            FixedSclChildWriteDomainFailureLabel {
                code: FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY,
                name: "dst_capacity",
                meaning: "destination child buffer must have room for both children",
            },
            FixedSclChildWriteDomainFailureLabel {
                code: FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX,
                name: "bit_index",
                meaning: "public bit index must be inside the path bit width",
            },
        ]
    );
    assert_eq!(
        fixed_scl_child_write_domain_failure_label(FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY),
        "dst_capacity"
    );
    assert_eq!(fixed_scl_child_write_domain_failure_label(255), "unknown");
}

#[test]
fn fixed_scl_integer_schedule_domain_failure_labels_cover_public_codes() {
    assert_eq!(
        FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_FAILURE_LABELS,
        [
            FixedSclIntegerScheduleDomainFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
                name: "ok",
                meaning: "valid public integer schedule inputs",
            },
            FixedSclIntegerScheduleDomainFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
                name: "hard_bit",
                meaning: "hard decisions must be public bits",
            },
            FixedSclIntegerScheduleDomainFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
                name: "magnitude",
                meaning: "integer metric magnitudes must be non-negative",
            },
        ]
    );
    assert_eq!(
        fixed_scl_integer_schedule_domain_failure_label(FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT),
        "hard_bit"
    );
    assert_eq!(
        fixed_scl_integer_schedule_domain_failure_label(255),
        "unknown"
    );
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
fn fixed_schedule_top_l_selection_plan_reports_public_shape_without_sorting() {
    assert_eq!(
        fixed_schedule_top_l_selection_plan(8, 4),
        FixedScheduleTopLSelectionPlan {
            width: 8,
            list_size: 4,
            valid: true,
            failure_code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
            compare_exchanges: 28,
        }
    );
    assert_eq!(
        fixed_schedule_top_l_selection_plan(2, 3),
        FixedScheduleTopLSelectionPlan {
            width: 2,
            list_size: 3,
            valid: false,
            failure_code: FIXED_TOP_L_SELECTION_DOMAIN_WIDTH,
            compare_exchanges: 0,
        }
    );
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
            child_slots_written: 2,
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
            child_slots_written: 0,
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
            child_slots_written: 0,
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
            child_slots_written: 0,
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
            child_slots_written: 2,
            valid: true,
            failure_code: FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
        }
    );
    assert_eq!(children.active_count(), 2);
    assert_eq!(children.bits(2), [1, 0, 0, 0, 0, 0, 0, 0]);
    assert_eq!(children.bits(3), [1, 0, 0, 1, 0, 0, 0, 0]);
}

#[test]
fn fixed_scl_child_write_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [1, 0, 0, 0, 0, 0, 0, 0]);

    let mut children = FixedSclPathBuffer::<4, 8>::new();
    let run_domain_check = children.try_write_binary_children_from(&parents, 0, 2, 3, 5, 9);
    let expected_domain_check = fixed_scl_binary_child_write_domain_check::<2, 4, 8>(0, 2, 3);

    assert_eq!(
        fixed_scl_child_write_parity_check(run_domain_check, expected_domain_check),
        FixedSclChildWriteParityCheck {
            matches: true,
            run_domain_check: expected_domain_check,
            expected_domain_check,
        }
    );

    let mut altered_run_domain_check = run_domain_check;
    altered_run_domain_check.child_slots_written = 0;

    assert_eq!(
        fixed_scl_child_write_parity_check(altered_run_domain_check, expected_domain_check),
        FixedSclChildWriteParityCheck {
            matches: false,
            run_domain_check: altered_run_domain_check,
            expected_domain_check,
        }
    );
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
            child_slots_written: 0,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 3,
                rounds: 1,
                top_l_compare_exchanges: 6,
                child_slots_written: 4,
                compacted_slots_written: 3,
            },
            children,
            top,
        }
    );
}

#[test]
fn fixed_scl_one_bit_shape_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_one_bit::<4, 3>(2, 5, -1);
    let expected_plan = fixed_scl_public_round_schedule_plan::<2, 8, 4, 4, 3, 1>([2]);

    assert_eq!(
        fixed_scl_one_bit_shape_parity_check(&run, expected_plan),
        FixedSclOneBitShapeParityCheck {
            matches: true,
            run_plan_certificate: expected_plan,
            expected_plan,
        }
    );

    let mut altered_run = run;
    altered_run.work_counts.rounds = 0;
    let altered_certificate = fixed_scl_one_bit_run_plan_certificate(&altered_run);

    assert_eq!(
        fixed_scl_one_bit_shape_parity_check(&altered_run, expected_plan),
        FixedSclOneBitShapeParityCheck {
            matches: false,
            run_plan_certificate: altered_certificate,
            expected_plan,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 3,
                repeated_child_capacity: 3,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 2,
                top_l_compare_exchanges: 12,
                child_slots_written: 8,
                compacted_slots_written: 4,
            },
            paths,
            top,
        }
    );
}

#[test]
fn fixed_scl_two_public_bits_shape_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_two_public_bits::<4, 4, 2>((2, 5, -1), (4, 7, 0));
    let expected_shape_plan =
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 2>([2, 4]);

    assert_eq!(
        two_public_bits_shape_parity_check(&run, expected_shape_plan),
        FixedSclPublicRoundShapeParityCheck {
            matches: true,
            run_shape_certificate: expected_shape_plan,
            expected_shape_plan,
        }
    );

    let mut altered_run = run;
    altered_run.work_counts.rounds = 0;
    let altered_certificate = two_public_bits_run_shape_certificate(&altered_run);

    assert_eq!(
        two_public_bits_shape_parity_check(&altered_run, expected_shape_plan),
        FixedSclPublicRoundShapeParityCheck {
            matches: false,
            run_shape_certificate: altered_certificate,
            expected_shape_plan,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 18,
                child_slots_written: 12,
                compacted_slots_written: 6,
            },
            paths,
            top,
        }
    );
    assert_eq!(
        fixed_scl_public_round_run_shape_certificate(&run),
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5])
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
    assert_eq!(
        fixed_scl_public_round_run_shape_certificate(&run),
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 2>([2, 8])
    );
}

#[test]
fn fixed_scl_public_round_shape_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];
    let run = parents.try_expand_then_compact_public_rounds::<4, 4, 2, 3>(rounds);
    let expected_shape_plan =
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]);

    assert_eq!(
        fixed_scl_public_round_shape_parity_check(&run, expected_shape_plan),
        FixedSclPublicRoundShapeParityCheck {
            matches: true,
            run_shape_certificate: expected_shape_plan,
            expected_shape_plan,
        }
    );

    let mut altered_run = run;
    altered_run.work_counts.rounds = 0;
    let altered_certificate = fixed_scl_public_round_run_shape_certificate(&altered_run);

    assert_eq!(
        fixed_scl_public_round_shape_parity_check(&altered_run, expected_shape_plan),
        FixedSclPublicRoundShapeParityCheck {
            matches: false,
            run_shape_certificate: altered_certificate,
            expected_shape_plan,
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
fn fixed_scl_public_round_schedule_plan_reports_status_and_work_counts_without_running() {
    assert_eq!(
        fixed_scl_public_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]),
        FixedSclPublicRoundSchedulePlan {
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 18,
                child_slots_written: 12,
                compacted_slots_written: 6,
            },
        }
    );

    assert_eq!(
        fixed_scl_public_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5]).work_counts,
        FixedSclPublicRoundWorkCounts {
            parent_capacity: 2,
            first_child_capacity: 4,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 0,
            top_l_compare_exchanges: 0,
            child_slots_written: 0,
            compacted_slots_written: 0,
        }
    );
}

#[test]
fn fixed_scl_public_round_schedule_shape_plan_pairs_path_domain_with_top_l_work_shape() {
    assert_eq!(
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]),
        FixedSclPublicRoundScheduleShapePlan {
            valid: true,
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
            work_shape_plan: FixedSclPublicRoundWorkShapePlan {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                valid: true,
                first_top_l_plan: FixedScheduleTopLSelectionPlan {
                    width: 4,
                    list_size: 2,
                    valid: true,
                    failure_code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
                    compare_exchanges: 6,
                },
                repeated_top_l_plan: FixedScheduleTopLSelectionPlan {
                    width: 4,
                    list_size: 2,
                    valid: true,
                    failure_code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
                    compare_exchanges: 6,
                },
                work_counts: FixedSclPublicRoundWorkCounts {
                    parent_capacity: 2,
                    first_child_capacity: 4,
                    repeated_child_capacity: 4,
                    list_size: 2,
                    rounds: 3,
                    top_l_compare_exchanges: 18,
                    child_slots_written: 12,
                    compacted_slots_written: 6,
                },
            },
        }
    );

    let invalid = fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5]);

    assert!(!invalid.valid);
    assert_eq!(
        invalid.path_domain_check.failure_code,
        FIXED_SCL_PATH_DOMAIN_BIT_INDEX
    );
    assert!(invalid.work_shape_plan.valid);
    assert_eq!(invalid.work_shape_plan.work_counts.rounds, 0);
    assert_eq!(
        invalid.work_shape_plan.work_counts.top_l_compare_exchanges,
        0
    );
}

#[test]
fn fixed_scl_public_round_schedule_shape_failure_family_labels_status_sources() {
    assert_eq!(
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_LABELS,
        [
            FixedSclPublicRoundScheduleShapeFailureLabel {
                code: FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK,
                name: "ok",
                meaning: "valid public schedule-shape preflight",
            },
            FixedSclPublicRoundScheduleShapeFailureLabel {
                code: FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN,
                name: "path_domain",
                meaning: "public path-buffer schedule domain failed first",
            },
            FixedSclPublicRoundScheduleShapeFailureLabel {
                code: FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE,
                name: "work_shape",
                meaning: "public top-L work-shape envelope failed after path-domain checks",
            },
        ]
    );

    let valid_plan = fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]);
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_family(valid_plan),
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK
    );
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_label(
            FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK
        ),
        "ok"
    );

    let invalid_path_plan =
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5]);
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_family(invalid_path_plan),
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN
    );
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_label(
            FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN
        ),
        "path_domain"
    );

    let mut invalid_work_shape_plan = valid_plan;
    invalid_work_shape_plan.valid = false;
    invalid_work_shape_plan.work_shape_plan = fixed_scl_public_round_work_shape_plan(2, 1, 1, 2, 1);
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_family(invalid_work_shape_plan),
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE
    );
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_label(
            FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE
        ),
        "work_shape"
    );
    assert_eq!(
        fixed_scl_public_round_schedule_shape_failure_label(99),
        "unknown"
    );
}

#[test]
fn fixed_scl_round_schedule_plan_reads_round_bit_indices_without_expansion() {
    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];

    assert_eq!(
        fixed_scl_round_schedule_plan::<2, 8, 4, 4, 2, 3>(rounds),
        FixedSclPublicRoundSchedulePlan {
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 18,
                child_slots_written: 12,
                compacted_slots_written: 6,
            },
        }
    );

    let invalid = fixed_scl_round_schedule_plan::<2, 8, 4, 4, 2, 2>([
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(8, 7, 0),
    ]);
    assert_eq!(
        invalid.path_domain_check.failure_code,
        FIXED_SCL_PATH_DOMAIN_BIT_INDEX
    );
    assert_eq!(invalid.path_domain_check.first_invalid_round, 1);
    assert_eq!(invalid.work_counts.rounds, 0);
}

#[test]
fn fixed_scl_round_schedule_plan_parity_check_reports_match_and_mismatch() {
    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];
    let expected_public_plan = fixed_scl_public_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]);

    assert_eq!(
        fixed_scl_round_schedule_plan_parity_check::<2, 8, 4, 4, 2, 3>(
            rounds,
            expected_public_plan,
        ),
        FixedSclRoundSchedulePlanParityCheck {
            matches: true,
            round_schedule_plan: expected_public_plan,
            expected_public_plan,
        }
    );

    let altered_expected_public_plan =
        fixed_scl_public_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5]);
    let round_schedule_plan = fixed_scl_round_schedule_plan_certificate::<2, 8, 4, 4, 2, 3>(rounds);

    assert_eq!(
        fixed_scl_round_schedule_plan_parity_check::<2, 8, 4, 4, 2, 3>(
            rounds,
            altered_expected_public_plan,
        ),
        FixedSclRoundSchedulePlanParityCheck {
            matches: false,
            round_schedule_plan,
            expected_public_plan: altered_expected_public_plan,
        }
    );
}

#[test]
fn fixed_scl_round_schedule_shape_parity_check_reports_match_and_mismatch() {
    let rounds = [
        FixedSclRound::new(2, 5, -1),
        FixedSclRound::new(4, 7, 0),
        FixedSclRound::new(5, 4, -2),
    ];
    let expected_shape_plan =
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5]);

    assert_eq!(
        fixed_scl_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(rounds),
        expected_shape_plan,
    );

    assert_eq!(
        fixed_scl_round_schedule_shape_parity_check::<2, 8, 4, 4, 2, 3>(
            rounds,
            expected_shape_plan,
        ),
        FixedSclRoundScheduleShapeParityCheck {
            matches: true,
            round_shape_plan: expected_shape_plan,
            expected_shape_plan,
        }
    );

    let altered_expected_shape_plan =
        fixed_scl_public_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5]);
    let round_shape_plan =
        fixed_scl_round_schedule_shape_plan_certificate::<2, 8, 4, 4, 2, 3>(rounds);

    assert_eq!(
        fixed_scl_round_schedule_shape_parity_check::<2, 8, 4, 4, 2, 3>(
            rounds,
            altered_expected_shape_plan,
        ),
        FixedSclRoundScheduleShapeParityCheck {
            matches: false,
            round_shape_plan,
            expected_shape_plan: altered_expected_shape_plan,
        }
    );
}

#[test]
fn fixed_scl_integer_round_schedule_plan_reports_dual_status_and_work_counts_without_running() {
    assert_eq!(
        fixed_scl_integer_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5], [1, 1, 1], [5, 7, 4],),
        FixedSclIntegerRoundSchedulePlan {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 3,
                valid: true,
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 18,
                child_slots_written: 12,
                compacted_slots_written: 6,
            },
        }
    );

    let invalid_integer =
        fixed_scl_integer_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5], [1, 1, 1], [5, -7, 4]);
    assert_eq!(
        invalid_integer.domain_check,
        FixedSclIntegerScheduleDomainCheck {
            rounds: 3,
            valid: false,
            failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
            first_invalid_round: 1,
        }
    );
    assert_eq!(
        invalid_integer.path_domain_check.failure_code,
        FIXED_SCL_PATH_DOMAIN_OK
    );
    assert_eq!(
        invalid_integer.work_counts,
        FixedSclPublicRoundWorkCounts {
            parent_capacity: 2,
            first_child_capacity: 4,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 0,
            top_l_compare_exchanges: 0,
            child_slots_written: 0,
            compacted_slots_written: 0,
        }
    );

    let invalid_path =
        fixed_scl_integer_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 8, 5], [1, 1, 1], [5, 7, 4]);
    assert_eq!(
        invalid_path.domain_check.failure_code,
        FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK
    );
    assert_eq!(
        invalid_path.path_domain_check.failure_code,
        FIXED_SCL_PATH_DOMAIN_BIT_INDEX
    );
    assert_eq!(invalid_path.path_domain_check.first_invalid_round, 1);
    assert_eq!(invalid_path.work_counts.rounds, 0);
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
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 18,
                child_slots_written: 12,
                compacted_slots_written: 6,
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
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
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
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 2,
                first_child_capacity: 4,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 0,
                top_l_compare_exchanges: 0,
                child_slots_written: 0,
                compacted_slots_written: 0,
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
fn fixed_scl_integer_shape_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
        [2, 4, 5],
        [false, false, true],
        [1, 1, 1],
        [5, 7, 4],
    );
    let expected_plan =
        fixed_scl_integer_round_schedule_plan::<2, 8, 4, 4, 2, 3>([2, 4, 5], [1, 1, 1], [5, 7, 4]);

    assert_eq!(
        fixed_scl_integer_shape_parity_check(&run, expected_plan),
        FixedSclIntegerShapeParityCheck {
            matches: true,
            run_plan_certificate: expected_plan,
            expected_plan,
        }
    );

    let mut altered_run = run;
    altered_run.work_counts.rounds = 0;
    let altered_certificate = fixed_scl_integer_round_run_plan_certificate(&altered_run);

    assert_eq!(
        fixed_scl_integer_shape_parity_check(&altered_run, expected_plan),
        FixedSclIntegerShapeParityCheck {
            matches: false,
            run_plan_certificate: altered_certificate,
            expected_plan,
        }
    );
}

#[test]
fn fixed_scl_integer_schedule_shape_parity_check_reports_match_and_mismatch() {
    let mut parents = FixedSclPathBuffer::<2, 8>::new();
    parents.set_candidate(0, 10, [0; 8]);
    parents.set_candidate(1, 3, [1; 8]);

    let run = parents.try_expand_then_compact_integer_round_schedule::<4, 4, 2, 3>(
        [2, 4, 5],
        [false, false, true],
        [1, 1, 1],
        [5, 7, 4],
    );
    let expected_shape_plan = fixed_scl_integer_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(
        [2, 4, 5],
        [1, 1, 1],
        [5, 7, 4],
    );

    assert_eq!(
        fixed_scl_integer_schedule_shape_parity_check(&run, expected_shape_plan),
        FixedSclIntegerScheduleShapeParityCheck {
            matches: true,
            run_shape_certificate: expected_shape_plan,
            expected_shape_plan,
        }
    );

    let invalid_integer_shape_plan = fixed_scl_integer_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(
        [2, 4, 5],
        [1, 1, 1],
        [5, -7, 4],
    );
    assert_eq!(
        invalid_integer_shape_plan,
        FixedSclIntegerRoundScheduleShapePlan {
            valid: false,
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 3,
                valid: false,
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
                first_invalid_round: 1,
            },
            path_domain_check: expected_shape_plan.path_domain_check,
            work_shape_plan: fixed_scl_public_round_work_shape_plan(2, 4, 4, 2, 0),
        }
    );

    let altered_certificate = fixed_scl_integer_round_run_shape_certificate(&run);

    assert_eq!(
        fixed_scl_integer_schedule_shape_parity_check(&run, invalid_integer_shape_plan),
        FixedSclIntegerScheduleShapeParityCheck {
            matches: false,
            run_shape_certificate: altered_certificate,
            expected_shape_plan: invalid_integer_shape_plan,
        }
    );
}

#[test]
fn fixed_scl_integer_schedule_shape_failure_family_labels_status_sources() {
    assert_eq!(
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_LABELS,
        [
            FixedSclIntegerScheduleShapeFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK,
                name: "ok",
                meaning: "valid integer schedule-shape preflight",
            },
            FixedSclIntegerScheduleShapeFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN,
                name: "integer_domain",
                meaning: "integer hard-bit or metric-magnitude domain failed first",
            },
            FixedSclIntegerScheduleShapeFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN,
                name: "path_domain",
                meaning: "public path-buffer schedule domain failed first",
            },
            FixedSclIntegerScheduleShapeFailureLabel {
                code: FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE,
                name: "work_shape",
                meaning: "public top-L work-shape envelope failed after domain checks",
            },
        ]
    );

    let valid_plan = fixed_scl_integer_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(
        [2, 4, 5],
        [1, 1, 1],
        [5, 7, 4],
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_family(valid_plan),
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_label(
            FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK
        ),
        "ok"
    );

    let invalid_integer_plan = fixed_scl_integer_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(
        [2, 4, 5],
        [1, 2, 1],
        [5, 7, 4],
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_family(invalid_integer_plan),
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_label(
            FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN
        ),
        "integer_domain"
    );

    let invalid_path_plan = fixed_scl_integer_round_schedule_shape_plan::<2, 8, 4, 4, 2, 3>(
        [2, 8, 5],
        [1, 1, 1],
        [5, 7, 4],
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_family(invalid_path_plan),
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_label(
            FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN
        ),
        "path_domain"
    );

    let mut invalid_work_shape_plan = valid_plan;
    invalid_work_shape_plan.valid = false;
    invalid_work_shape_plan.work_shape_plan = fixed_scl_public_round_work_shape_plan(2, 1, 1, 2, 1);
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_family(invalid_work_shape_plan),
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_label(
            FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE
        ),
        "work_shape"
    );
    assert_eq!(
        fixed_scl_integer_schedule_shape_failure_label(99),
        "unknown"
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

    let mixed_counts = fixed_scl_public_round_work_counts_with_capacities(3, 6, 4, 2, 3);

    assert_eq!(mixed_counts.parent_capacity, 3);
    assert_eq!(mixed_counts.rounds, 3);
    assert_eq!(mixed_counts.first_child_capacity, 6);
    assert_eq!(mixed_counts.repeated_child_capacity, 4);
    assert_eq!(mixed_counts.list_size, 2);
    assert_eq!(mixed_counts.top_l_compare_exchanges, 27);
    assert_eq!(mixed_counts.child_slots_written, 14);
    assert_eq!(mixed_counts.compacted_slots_written, 6);

    let empty_counts = fixed_scl_public_round_work_counts_with_capacities(3, 6, 4, 2, 0);

    assert_eq!(empty_counts.parent_capacity, 3);
    assert_eq!(empty_counts.rounds, 0);
    assert_eq!(empty_counts.first_child_capacity, 6);
    assert_eq!(empty_counts.repeated_child_capacity, 4);
    assert_eq!(empty_counts.list_size, 2);
    assert_eq!(empty_counts.top_l_compare_exchanges, 0);
    assert_eq!(empty_counts.child_slots_written, 0);
    assert_eq!(empty_counts.compacted_slots_written, 0);
}

#[test]
fn fixed_scl_public_round_work_shape_plan_pairs_top_l_plans_with_counts() {
    assert_eq!(
        fixed_scl_public_round_work_shape_plan(3, 6, 4, 2, 3),
        FixedSclPublicRoundWorkShapePlan {
            parent_capacity: 3,
            first_child_capacity: 6,
            repeated_child_capacity: 4,
            list_size: 2,
            rounds: 3,
            valid: true,
            first_top_l_plan: FixedScheduleTopLSelectionPlan {
                width: 6,
                list_size: 2,
                valid: true,
                failure_code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
                compare_exchanges: 15,
            },
            repeated_top_l_plan: FixedScheduleTopLSelectionPlan {
                width: 4,
                list_size: 2,
                valid: true,
                failure_code: FIXED_TOP_L_SELECTION_DOMAIN_OK,
                compare_exchanges: 6,
            },
            work_counts: FixedSclPublicRoundWorkCounts {
                parent_capacity: 3,
                first_child_capacity: 6,
                repeated_child_capacity: 4,
                list_size: 2,
                rounds: 3,
                top_l_compare_exchanges: 27,
                child_slots_written: 14,
                compacted_slots_written: 6,
            },
        }
    );

    let invalid = fixed_scl_public_round_work_shape_plan(3, 1, 4, 2, 3);

    assert!(!invalid.valid);
    assert_eq!(
        invalid.first_top_l_plan.failure_code,
        FIXED_TOP_L_SELECTION_DOMAIN_WIDTH
    );
    assert_eq!(
        invalid.repeated_top_l_plan.failure_code,
        FIXED_TOP_L_SELECTION_DOMAIN_OK
    );
    assert_eq!(invalid.work_counts.rounds, 0);
    assert_eq!(invalid.work_counts.top_l_compare_exchanges, 0);
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
            failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
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
            failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
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
            failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
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
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            round_slots_written: 2,
            rounds: [
                FixedSclRound::new(0, 3, 0),
                FixedSclRound::new(1, 5, FIXED_SCL_FORBIDDEN_METRIC_DELTA),
            ],
        }
    );
}

#[test]
fn fixed_scl_integer_round_build_parity_check_reports_match_and_mismatch() {
    let build = try_fixed_scl_integer_round_schedule([0, 1], [false, true], [1, 1], [3, 5]);
    let expected_plan = fixed_scl_integer_round_schedule_build_plan([1, 1], [3, 5]);

    assert_eq!(
        fixed_scl_integer_round_build_parity_check(&build, expected_plan),
        FixedSclIntegerRoundScheduleBuildParityCheck {
            matches: true,
            run_build_certificate: expected_plan,
            expected_plan,
        }
    );

    let mut altered_build = build;
    altered_build.round_slots_written = 0;
    let altered_certificate = fixed_scl_integer_round_build_certificate(&altered_build);

    assert_eq!(
        fixed_scl_integer_round_build_parity_check(&altered_build, expected_plan),
        FixedSclIntegerRoundScheduleBuildParityCheck {
            matches: false,
            run_build_certificate: altered_certificate,
            expected_plan,
        }
    );

    assert_eq!(
        expected_plan,
        FixedSclIntegerRoundScheduleBuildPlan {
            domain_check: FixedSclIntegerScheduleDomainCheck {
                rounds: 2,
                valid: true,
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
                first_invalid_round: FIXED_SCL_NO_INVALID_ROUND,
            },
            round_slots_written: 2,
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
                failure_code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
                first_invalid_round: 1,
            },
            round_slots_written: 0,
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
