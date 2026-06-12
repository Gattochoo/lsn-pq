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

use std::collections::HashSet;

pub const FIXED_I64_VALIDATION_METRIC_SCALE: f64 = 1024.0;

#[derive(Clone, Debug)]
pub struct PolarCode {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub frozen: Vec<usize>,
    pub info_set: Vec<usize>,
    frozen_mask: Vec<bool>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct SimulationResult {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub trials: usize,
    pub errors: usize,
    pub seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct FixedI64DecoderAgreement {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub trials: usize,
    pub decoded_mismatches: usize,
    pub fast_errors: usize,
    pub fixed_errors: usize,
    pub seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ImportanceSamplingResult {
    pub n: usize,
    pub k: usize,
    pub target_p: f64,
    pub proposal_p: f64,
    pub trials: usize,
    pub proposal_errors: usize,
    pub weighted_bler_estimate: f64,
    pub mean_likelihood_ratio: f64,
    pub effective_sample_size: f64,
    pub seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PolarRateRow {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub rate: f64,
    pub bhattacharyya_sum_bound: f64,
    pub half_sum_bound: f64,
    pub log2_bhattacharyya_sum_bound: f64,
    pub log2_half_sum_bound: f64,
    pub target_log2_half_sum_bound: f64,
    pub passes_half_sum_target: bool,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedTopLEntry {
    pub metric: i64,
    pub index: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclCandidate<const N: usize> {
    pub metric: i64,
    pub bits: [u8; N],
    pub active: u8,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclRound {
    pub bit_index: usize,
    pub bit0_metric_delta: i64,
    pub bit1_metric_delta: i64,
}

pub const FIXED_SCL_FORBIDDEN_METRIC_DELTA: i64 = i64::MAX;
pub const FIXED_SCL_NO_INVALID_ROUND: usize = usize::MAX;
pub const FIXED_SCL_PATH_DOMAIN_OK: u8 = 0;
pub const FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE: u8 = 1;
pub const FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY: u8 = 2;
pub const FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY: u8 = 3;
pub const FIXED_SCL_PATH_DOMAIN_TOP_L_WIDTH: u8 = 4;
pub const FIXED_SCL_PATH_DOMAIN_BIT_INDEX: u8 = 5;
pub const FIXED_SCL_CHILD_WRITE_DOMAIN_OK: u8 = 0;
pub const FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT: u8 = 1;
pub const FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY: u8 = 2;
pub const FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX: u8 = 3;
pub const FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK: u8 = 0;
pub const FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT: u8 = 1;
pub const FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE: u8 = 2;
pub const FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK: u8 = 0;
pub const FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN: u8 = 1;
pub const FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN: u8 = 2;
pub const FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE: u8 = 3;
pub const FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK: u8 = 0;
pub const FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN: u8 = 1;
pub const FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE: u8 = 2;
pub const FIXED_TOP_L_SELECTION_DOMAIN_OK: u8 = 0;
pub const FIXED_TOP_L_SELECTION_DOMAIN_WIDTH: u8 = 1;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedScheduleTopLSelectionDomainFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_TOP_L_SELECTION_DOMAIN_FAILURE_LABELS:
    [FixedScheduleTopLSelectionDomainFailureLabel; 2] = [
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
];

pub fn fixed_top_l_selection_domain_failure_label(code: u8) -> &'static str {
    for label in FIXED_TOP_L_SELECTION_DOMAIN_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerScheduleDomainFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_FAILURE_LABELS:
    [FixedSclIntegerScheduleDomainFailureLabel; 3] = [
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
];

pub fn fixed_scl_integer_schedule_domain_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerMetricDomainFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_INTEGER_METRIC_DOMAIN_FAILURE_LABELS:
    [FixedSclIntegerMetricDomainFailureLabel; 3] = [
    FixedSclIntegerMetricDomainFailureLabel {
        code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
        name: "ok",
        meaning: "valid public integer metric inputs",
    },
    FixedSclIntegerMetricDomainFailureLabel {
        code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
        name: "hard_bit",
        meaning: "hard decisions must be public bits",
    },
    FixedSclIntegerMetricDomainFailureLabel {
        code: FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
        name: "magnitude",
        meaning: "integer metric magnitudes must be non-negative",
    },
];

pub fn fixed_scl_integer_metric_domain_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_INTEGER_METRIC_DOMAIN_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerScheduleShapeFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_LABELS:
    [FixedSclIntegerScheduleShapeFailureLabel; 4] = [
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
];

pub fn fixed_scl_integer_schedule_shape_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundScheduleShapeFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_LABELS:
    [FixedSclPublicRoundScheduleShapeFailureLabel; 3] = [
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
];

pub fn fixed_scl_public_round_schedule_shape_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclChildWriteDomainFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_CHILD_WRITE_DOMAIN_FAILURE_LABELS: [FixedSclChildWriteDomainFailureLabel; 4] = [
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
];

pub fn fixed_scl_child_write_domain_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_CHILD_WRITE_DOMAIN_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPathDomainFailureLabel {
    pub code: u8,
    pub name: &'static str,
    pub meaning: &'static str,
}

pub const FIXED_SCL_PATH_DOMAIN_FAILURE_LABELS: [FixedSclPathDomainFailureLabel; 6] = [
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
];

pub fn fixed_scl_path_domain_failure_label(code: u8) -> &'static str {
    for label in FIXED_SCL_PATH_DOMAIN_FAILURE_LABELS {
        if label.code == code {
            return label.name;
        }
    }
    "unknown"
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclMetricDeltas {
    pub bit0_metric_delta: i64,
    pub bit1_metric_delta: i64,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerMetricDomainCheck {
    pub valid: bool,
    pub failure_code: u8,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerMetricDeltaRun {
    pub domain_check: FixedSclIntegerMetricDomainCheck,
    pub deltas: FixedSclMetricDeltas,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedScheduleTopLSelectionPlan {
    pub width: usize,
    pub list_size: usize,
    pub valid: bool,
    pub failure_code: u8,
    pub compare_exchanges: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerScheduleDomainCheck {
    pub rounds: usize,
    pub valid: bool,
    pub failure_code: u8,
    pub first_invalid_round: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerRoundScheduleBuild<const ROUNDS: usize> {
    pub domain_check: FixedSclIntegerScheduleDomainCheck,
    pub round_slots_written: usize,
    pub rounds: [FixedSclRound; ROUNDS],
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerRoundScheduleBuildPlan {
    pub domain_check: FixedSclIntegerScheduleDomainCheck,
    pub round_slots_written: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerRoundScheduleBuildParityCheck {
    pub matches: bool,
    pub run_build_certificate: FixedSclIntegerRoundScheduleBuildPlan,
    pub expected_plan: FixedSclIntegerRoundScheduleBuildPlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPathBufferScheduleDomainCheck {
    pub parent_capacity: usize,
    pub first_child_capacity: usize,
    pub repeated_child_capacity: usize,
    pub list_size: usize,
    pub rounds: usize,
    pub bit_width: usize,
    pub valid: bool,
    pub failure_code: u8,
    pub first_invalid_round: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundSchedulePlan {
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_counts: FixedSclPublicRoundWorkCounts,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclRoundSchedulePlanParityCheck {
    pub matches: bool,
    pub round_schedule_plan: FixedSclPublicRoundSchedulePlan,
    pub expected_public_plan: FixedSclPublicRoundSchedulePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclRoundScheduleShapeParityCheck {
    pub matches: bool,
    pub round_shape_plan: FixedSclPublicRoundScheduleShapePlan,
    pub expected_shape_plan: FixedSclPublicRoundScheduleShapePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundScheduleShapePlan {
    pub valid: bool,
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_shape_plan: FixedSclPublicRoundWorkShapePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundShapeParityCheck {
    pub matches: bool,
    pub run_shape_certificate: FixedSclPublicRoundScheduleShapePlan,
    pub expected_shape_plan: FixedSclPublicRoundScheduleShapePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclOneBitShapeParityCheck {
    pub matches: bool,
    pub run_plan_certificate: FixedSclPublicRoundSchedulePlan,
    pub expected_plan: FixedSclPublicRoundSchedulePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerRoundSchedulePlan {
    pub domain_check: FixedSclIntegerScheduleDomainCheck,
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_counts: FixedSclPublicRoundWorkCounts,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerRoundScheduleShapePlan {
    pub valid: bool,
    pub domain_check: FixedSclIntegerScheduleDomainCheck,
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_shape_plan: FixedSclPublicRoundWorkShapePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerShapeParityCheck {
    pub matches: bool,
    pub run_plan_certificate: FixedSclIntegerRoundSchedulePlan,
    pub expected_plan: FixedSclIntegerRoundSchedulePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclIntegerScheduleShapeParityCheck {
    pub matches: bool,
    pub run_shape_certificate: FixedSclIntegerRoundScheduleShapePlan,
    pub expected_shape_plan: FixedSclIntegerRoundScheduleShapePlan,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclBinaryChildWriteDomainCheck {
    pub parent_capacity: usize,
    pub child_capacity: usize,
    pub bit_width: usize,
    pub parent_slot: usize,
    pub dst_start: usize,
    pub bit_index: usize,
    pub child_slots_written: usize,
    pub valid: bool,
    pub failure_code: u8,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclChildWriteParityCheck {
    pub matches: bool,
    pub run_domain_check: FixedSclBinaryChildWriteDomainCheck,
    pub expected_domain_check: FixedSclBinaryChildWriteDomainCheck,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclOneBitExpansionRun<const CHILD_CAP: usize, const L: usize, const N: usize> {
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_counts: FixedSclPublicRoundWorkCounts,
    pub children: FixedSclPathBuffer<CHILD_CAP, N>,
    pub top: [FixedTopLEntry; L],
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundScheduleRun<const L: usize, const N: usize> {
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_counts: FixedSclPublicRoundWorkCounts,
    pub paths: FixedSclPathBuffer<L, N>,
    pub top: [FixedTopLEntry; L],
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPathBufferIntegerScheduleRun<const L: usize, const N: usize> {
    pub domain_check: FixedSclIntegerScheduleDomainCheck,
    pub path_domain_check: FixedSclPathBufferScheduleDomainCheck,
    pub work_counts: FixedSclPublicRoundWorkCounts,
    pub paths: FixedSclPathBuffer<L, N>,
    pub top: [FixedTopLEntry; L],
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundWorkCounts {
    pub parent_capacity: usize,
    pub first_child_capacity: usize,
    pub repeated_child_capacity: usize,
    pub list_size: usize,
    pub rounds: usize,
    pub top_l_compare_exchanges: usize,
    pub child_slots_written: usize,
    pub compacted_slots_written: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPublicRoundWorkShapePlan {
    pub parent_capacity: usize,
    pub first_child_capacity: usize,
    pub repeated_child_capacity: usize,
    pub list_size: usize,
    pub rounds: usize,
    pub valid: bool,
    pub first_top_l_plan: FixedScheduleTopLSelectionPlan,
    pub repeated_top_l_plan: FixedScheduleTopLSelectionPlan,
    pub work_counts: FixedSclPublicRoundWorkCounts,
}

impl FixedSclRound {
    pub const fn new(bit_index: usize, bit0_metric_delta: i64, bit1_metric_delta: i64) -> Self {
        Self {
            bit_index,
            bit0_metric_delta,
            bit1_metric_delta,
        }
    }
}

impl<const N: usize> FixedSclCandidate<N> {
    pub const EMPTY: Self = Self {
        metric: i64::MAX,
        bits: [0; N],
        active: 0,
    };

    pub fn effective_metric(self) -> i64 {
        let active = self.active & 1;
        let active_i64_mask = 0i64.wrapping_sub(i64::from(active));
        select_i64(active_i64_mask, i64::MAX, self.metric)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FixedSclPathBuffer<const CAP: usize, const N: usize> {
    slots: [FixedSclCandidate<N>; CAP],
}

impl<const CAP: usize, const N: usize> FixedSclPathBuffer<CAP, N> {
    pub fn new() -> Self {
        Self {
            slots: [FixedSclCandidate::EMPTY; CAP],
        }
    }

    pub fn capacity(&self) -> usize {
        CAP
    }

    pub fn bit_width(&self) -> usize {
        N
    }

    pub fn active_count(&self) -> usize {
        self.slots
            .iter()
            .map(|candidate| usize::from(candidate.active & 1))
            .sum()
    }

    pub fn set_candidate(&mut self, slot: usize, metric: i64, bits: [u8; N]) {
        assert!(slot < CAP, "SCL fixed path slot is outside capacity");
        self.slots[slot] = FixedSclCandidate {
            metric,
            bits,
            active: 1,
        };
    }

    pub fn clear_slot(&mut self, slot: usize) {
        assert!(slot < CAP, "SCL fixed path slot is outside capacity");
        self.slots[slot] = FixedSclCandidate::EMPTY;
    }

    pub fn bits(&self, slot: usize) -> [u8; N] {
        assert!(slot < CAP, "SCL fixed path slot is outside capacity");
        self.slots[slot].bits
    }

    pub fn metric_entries(&self) -> [FixedTopLEntry; CAP] {
        let mut entries = [FixedTopLEntry {
            metric: i64::MAX,
            index: usize::MAX,
        }; CAP];
        for (index, entry) in entries.iter_mut().enumerate() {
            *entry = FixedTopLEntry {
                metric: self.slots[index].effective_metric(),
                index,
            };
        }
        entries
    }

    pub fn top_l_entries<const L: usize>(&self) -> [FixedTopLEntry; L] {
        let entries = self.metric_entries();
        let mut metrics = [i64::MAX; CAP];
        for (index, metric) in metrics.iter_mut().enumerate() {
            *metric = entries[index].metric;
        }
        fixed_schedule_top_l_i64::<CAP, L>(metrics)
    }

    pub fn write_binary_children_from<const SRC_CAP: usize>(
        &mut self,
        parents: &FixedSclPathBuffer<SRC_CAP, N>,
        parent_slot: usize,
        dst_start: usize,
        bit_index: usize,
        bit0_metric_delta: i64,
        bit1_metric_delta: i64,
    ) {
        assert!(
            parent_slot < SRC_CAP,
            "binary child parent slot is outside capacity"
        );
        assert!(
            dst_start + 1 < CAP,
            "binary child destination requires two slots"
        );
        assert!(bit_index < N, "binary child bit index is outside width");

        let parent = parents.slots[parent_slot];
        let mut bit0 = parent.bits;
        let mut bit1 = parent.bits;
        bit0[bit_index] = 0;
        bit1[bit_index] = 1;

        let active = parent.active & 1;
        let active_i64_mask = 0i64.wrapping_sub(i64::from(active));
        let active_u8_mask = 0u8.wrapping_sub(active);

        self.slots[dst_start] = FixedSclCandidate {
            metric: select_i64(
                active_i64_mask,
                i64::MAX,
                fixed_scl_metric_add(parent.metric, bit0_metric_delta),
            ),
            bits: mask_bits(bit0, active_u8_mask),
            active,
        };
        self.slots[dst_start + 1] = FixedSclCandidate {
            metric: select_i64(
                active_i64_mask,
                i64::MAX,
                fixed_scl_metric_add(parent.metric, bit1_metric_delta),
            ),
            bits: mask_bits(bit1, active_u8_mask),
            active,
        };
    }

    pub fn try_write_binary_children_from<const SRC_CAP: usize>(
        &mut self,
        parents: &FixedSclPathBuffer<SRC_CAP, N>,
        parent_slot: usize,
        dst_start: usize,
        bit_index: usize,
        bit0_metric_delta: i64,
        bit1_metric_delta: i64,
    ) -> FixedSclBinaryChildWriteDomainCheck {
        let domain_check = fixed_scl_binary_child_write_domain_check::<SRC_CAP, CAP, N>(
            parent_slot,
            dst_start,
            bit_index,
        );
        if domain_check.valid {
            self.write_binary_children_from(
                parents,
                parent_slot,
                dst_start,
                bit_index,
                bit0_metric_delta,
                bit1_metric_delta,
            );
        }
        domain_check
    }

    pub fn expand_then_compact_one_bit<const CHILD_CAP: usize, const L: usize>(
        &self,
        bit_index: usize,
        bit0_metric_delta: i64,
        bit1_metric_delta: i64,
    ) -> (FixedSclPathBuffer<CHILD_CAP, N>, [FixedTopLEntry; L]) {
        assert!(
            CAP.saturating_mul(2) <= CHILD_CAP,
            "expand-then-compact child capacity requires two slots per parent"
        );
        let mut children = FixedSclPathBuffer::<CHILD_CAP, N>::new();
        for parent_slot in 0..CAP {
            children.write_binary_children_from(
                self,
                parent_slot,
                parent_slot * 2,
                bit_index,
                bit0_metric_delta,
                bit1_metric_delta,
            );
        }
        let top = children.top_l_entries::<L>();
        (children, top)
    }

    pub fn try_expand_then_compact_one_bit<const CHILD_CAP: usize, const L: usize>(
        &self,
        bit_index: usize,
        bit0_metric_delta: i64,
        bit1_metric_delta: i64,
    ) -> FixedSclOneBitExpansionRun<CHILD_CAP, L, N> {
        let path_domain_check =
            fixed_scl_path_buffer_schedule_domain_check::<CAP, N, CHILD_CAP, CHILD_CAP, L, 1>([
                bit_index,
            ]);
        let zero_work_counts =
            fixed_scl_public_round_work_counts_with_capacities(CAP, CHILD_CAP, CHILD_CAP, L, 0);
        if !path_domain_check.valid {
            return FixedSclOneBitExpansionRun {
                path_domain_check,
                work_counts: zero_work_counts,
                children: FixedSclPathBuffer::<CHILD_CAP, N>::new(),
                top: [FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                }; L],
            };
        }

        let mut children = FixedSclPathBuffer::<CHILD_CAP, N>::new();
        for parent_slot in 0..CAP {
            let _ = children.try_write_binary_children_from(
                self,
                parent_slot,
                parent_slot * 2,
                bit_index,
                bit0_metric_delta,
                bit1_metric_delta,
            );
        }
        let top = children.top_l_entries::<L>();
        FixedSclOneBitExpansionRun {
            path_domain_check,
            work_counts: fixed_scl_public_round_work_counts_with_capacities(
                CAP, CHILD_CAP, CHILD_CAP, L, 1,
            ),
            children,
            top,
        }
    }

    fn from_top_entries<const SRC_CAP: usize>(
        source: &FixedSclPathBuffer<SRC_CAP, N>,
        top: [FixedTopLEntry; CAP],
    ) -> Self {
        let mut compacted = Self::new();
        for (dst_slot, entry) in top.iter().enumerate() {
            let mut selected = FixedSclCandidate::<N>::EMPTY;
            for source_slot in 0..SRC_CAP {
                let take_source = usize::from(source_slot == entry.index);
                let take_i64_mask = 0i64.wrapping_sub(take_source as i64);
                let take_u8_mask = 0u8.wrapping_sub(take_source as u8);
                selected = select_candidate(
                    take_i64_mask,
                    take_u8_mask,
                    selected,
                    source.slots[source_slot],
                );
            }
            compacted.slots[dst_slot] = sanitize_candidate_active(selected);
        }
        compacted
    }

    pub fn expand_then_compact_two_public_bits<
        const FIRST_CHILD_CAP: usize,
        const SECOND_CHILD_CAP: usize,
        const L: usize,
    >(
        &self,
        first_round: (usize, i64, i64),
        second_round: (usize, i64, i64),
    ) -> (FixedSclPathBuffer<L, N>, [FixedTopLEntry; L]) {
        let (first_bit, first_bit0_delta, first_bit1_delta) = first_round;
        let (first_children, first_top) = self.expand_then_compact_one_bit::<FIRST_CHILD_CAP, L>(
            first_bit,
            first_bit0_delta,
            first_bit1_delta,
        );
        let first_compacted =
            FixedSclPathBuffer::<L, N>::from_top_entries(&first_children, first_top);

        let (second_bit, second_bit0_delta, second_bit1_delta) = second_round;
        let (second_children, second_top) = first_compacted
            .expand_then_compact_one_bit::<SECOND_CHILD_CAP, L>(
                second_bit,
                second_bit0_delta,
                second_bit1_delta,
            );
        let second_compacted =
            FixedSclPathBuffer::<L, N>::from_top_entries(&second_children, second_top);
        (second_compacted, second_top)
    }

    pub fn try_expand_then_compact_two_public_bits<
        const FIRST_CHILD_CAP: usize,
        const SECOND_CHILD_CAP: usize,
        const L: usize,
    >(
        &self,
        first_round: (usize, i64, i64),
        second_round: (usize, i64, i64),
    ) -> FixedSclPublicRoundScheduleRun<L, N> {
        let (first_bit, first_bit0_delta, first_bit1_delta) = first_round;
        let (second_bit, second_bit0_delta, second_bit1_delta) = second_round;
        self.try_expand_then_compact_public_rounds::<FIRST_CHILD_CAP, SECOND_CHILD_CAP, L, 2>([
            FixedSclRound::new(first_bit, first_bit0_delta, first_bit1_delta),
            FixedSclRound::new(second_bit, second_bit0_delta, second_bit1_delta),
        ])
    }

    pub fn expand_then_compact_public_rounds<
        const FIRST_CHILD_CAP: usize,
        const CHILD_CAP: usize,
        const L: usize,
        const ROUNDS: usize,
    >(
        &self,
        rounds: [FixedSclRound; ROUNDS],
    ) -> (FixedSclPathBuffer<L, N>, [FixedTopLEntry; L]) {
        assert!(
            ROUNDS > 0,
            "public round schedule requires at least one round"
        );

        let first_round = rounds[0];
        let (first_children, first_top) = self.expand_then_compact_one_bit::<FIRST_CHILD_CAP, L>(
            first_round.bit_index,
            first_round.bit0_metric_delta,
            first_round.bit1_metric_delta,
        );
        let mut compacted =
            FixedSclPathBuffer::<L, N>::from_top_entries(&first_children, first_top);
        let mut final_top = first_top;

        for round in rounds.iter().skip(1) {
            let (children, top) = compacted.expand_then_compact_one_bit::<CHILD_CAP, L>(
                round.bit_index,
                round.bit0_metric_delta,
                round.bit1_metric_delta,
            );
            compacted = FixedSclPathBuffer::<L, N>::from_top_entries(&children, top);
            final_top = top;
        }

        (compacted, final_top)
    }

    pub fn try_expand_then_compact_public_rounds<
        const FIRST_CHILD_CAP: usize,
        const CHILD_CAP: usize,
        const L: usize,
        const ROUNDS: usize,
    >(
        &self,
        rounds: [FixedSclRound; ROUNDS],
    ) -> FixedSclPublicRoundScheduleRun<L, N> {
        let plan =
            fixed_scl_round_schedule_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(rounds);
        if !plan.path_domain_check.valid {
            return FixedSclPublicRoundScheduleRun {
                path_domain_check: plan.path_domain_check,
                work_counts: plan.work_counts,
                paths: FixedSclPathBuffer::<L, N>::new(),
                top: [FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                }; L],
            };
        }

        let Some(first_round) = rounds.first().copied() else {
            return FixedSclPublicRoundScheduleRun {
                path_domain_check: plan.path_domain_check,
                work_counts: plan.work_counts,
                paths: FixedSclPathBuffer::<L, N>::new(),
                top: [FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                }; L],
            };
        };

        let first_run = self.try_expand_then_compact_one_bit::<FIRST_CHILD_CAP, L>(
            first_round.bit_index,
            first_round.bit0_metric_delta,
            first_round.bit1_metric_delta,
        );
        let mut compacted =
            FixedSclPathBuffer::<L, N>::from_top_entries(&first_run.children, first_run.top);
        let mut final_top = first_run.top;

        for round in rounds.iter().skip(1) {
            let run = compacted.try_expand_then_compact_one_bit::<CHILD_CAP, L>(
                round.bit_index,
                round.bit0_metric_delta,
                round.bit1_metric_delta,
            );
            compacted = FixedSclPathBuffer::<L, N>::from_top_entries(&run.children, run.top);
            final_top = run.top;
        }

        FixedSclPublicRoundScheduleRun {
            path_domain_check: plan.path_domain_check,
            work_counts: plan.work_counts,
            paths: compacted,
            top: final_top,
        }
    }

    pub fn expand_then_compact_integer_round_schedule<
        const FIRST_CHILD_CAP: usize,
        const CHILD_CAP: usize,
        const L: usize,
        const ROUNDS: usize,
    >(
        &self,
        bit_indices: [usize; ROUNDS],
        frozen_bits: [bool; ROUNDS],
        hard_bits: [u8; ROUNDS],
        magnitudes: [i64; ROUNDS],
    ) -> (FixedSclPathBuffer<L, N>, [FixedTopLEntry; L]) {
        let rounds =
            fixed_scl_integer_round_schedule(bit_indices, frozen_bits, hard_bits, magnitudes);
        self.expand_then_compact_public_rounds::<FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(rounds)
    }

    pub fn try_expand_then_compact_integer_round_schedule<
        const FIRST_CHILD_CAP: usize,
        const CHILD_CAP: usize,
        const L: usize,
        const ROUNDS: usize,
    >(
        &self,
        bit_indices: [usize; ROUNDS],
        frozen_bits: [bool; ROUNDS],
        hard_bits: [u8; ROUNDS],
        magnitudes: [i64; ROUNDS],
    ) -> FixedSclPathBufferIntegerScheduleRun<L, N> {
        let plan =
            fixed_scl_integer_round_schedule_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
                bit_indices,
                hard_bits,
                magnitudes,
            );
        let schedule =
            try_fixed_scl_integer_round_schedule(bit_indices, frozen_bits, hard_bits, magnitudes);
        if !plan.domain_check.valid {
            return FixedSclPathBufferIntegerScheduleRun {
                domain_check: plan.domain_check,
                path_domain_check: plan.path_domain_check,
                work_counts: plan.work_counts,
                paths: FixedSclPathBuffer::<L, N>::new(),
                top: [FixedTopLEntry {
                    metric: i64::MAX,
                    index: usize::MAX,
                }; L],
            };
        }

        let run = self
            .try_expand_then_compact_public_rounds::<FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
                schedule.rounds,
            );
        FixedSclPathBufferIntegerScheduleRun {
            domain_check: plan.domain_check,
            path_domain_check: run.path_domain_check,
            work_counts: plan.work_counts,
            paths: run.paths,
            top: run.top,
        }
    }
}

impl<const CAP: usize, const N: usize> Default for FixedSclPathBuffer<CAP, N> {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SimulationConfig {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub trials: usize,
    pub seed: u64,
}

impl SimulationResult {
    pub fn bler(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.errors as f64 / self.trials as f64
        }
    }

    pub fn zero_error_upper_95(&self) -> Option<f64> {
        if self.errors == 0 && self.trials > 0 {
            Some(zero_error_upper_bound(self.trials, 0.05))
        } else {
            None
        }
    }
}

impl ImportanceSamplingResult {
    pub fn proposal_error_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.proposal_errors as f64 / self.trials as f64
        }
    }
}

pub fn zero_error_upper_bound(trials: usize, alpha: f64) -> f64 {
    assert!(trials > 0, "trials must be positive");
    assert!((0.0..1.0).contains(&alpha), "alpha must be in (0, 1)");
    1.0 - alpha.powf(1.0 / trials as f64)
}

pub fn baseline_reproduction_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [
        (128, 16, 0.0706),
        (128, 16, 0.0343),
        (256, 32, 0.0706),
        (256, 32, 0.0343),
        (512, 64, 0.0706),
        (512, 64, 0.0343),
    ]
    .into_iter()
    .enumerate()
    .map(|(i, (n, k, p))| SimulationConfig {
        n,
        k,
        p,
        trials,
        seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
    })
    .collect()
}

pub fn target_n2048_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [(2048, 256, 0.0706), (2048, 256, 0.0343)]
        .into_iter()
        .enumerate()
        .map(|(i, (n, k, p))| SimulationConfig {
            n,
            k,
            p,
            trials,
            seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
        })
        .collect()
}

pub fn high_noise_control_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [(2048, 256, 0.3), (2048, 256, 0.4), (2048, 256, 0.5)]
        .into_iter()
        .enumerate()
        .map(|(i, (n, k, p))| SimulationConfig {
            n,
            k,
            p,
            trials,
            seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
        })
        .collect()
}

pub fn fixed_i64_high_noise_control_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [(128, 16, 0.3), (128, 16, 0.4), (128, 16, 0.5)]
        .into_iter()
        .enumerate()
        .map(|(i, (n, k, p))| SimulationConfig {
            n,
            k,
            p,
            trials,
            seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
        })
        .collect()
}

pub fn fixed_i64_l8_validation_dispatch(cfg: &SimulationConfig) -> SimulationResult {
    match cfg.n {
        128 | 256 | 512 | 2048 => {
            simulate_bsc_scl_fixed_i64_l8_validation(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed)
        }
        other => panic!("fixed-i64 validation dispatch does not support N={other}"),
    }
}

pub fn fixed_schedule_top_l_compare_count(width: usize) -> usize {
    width.saturating_mul(width.saturating_sub(1)) / 2
}

pub fn fixed_schedule_top_l_selection_plan(
    width: usize,
    list_size: usize,
) -> FixedScheduleTopLSelectionPlan {
    let valid = list_size <= width;
    FixedScheduleTopLSelectionPlan {
        width,
        list_size,
        valid,
        failure_code: if valid {
            FIXED_TOP_L_SELECTION_DOMAIN_OK
        } else {
            FIXED_TOP_L_SELECTION_DOMAIN_WIDTH
        },
        compare_exchanges: if valid {
            fixed_schedule_top_l_compare_count(width)
        } else {
            0
        },
    }
}

pub fn fixed_scl_round_schedule_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
) -> FixedSclPublicRoundSchedulePlan {
    let mut bit_indices = [0usize; ROUNDS];
    for (index, round) in rounds.iter().enumerate() {
        bit_indices[index] = round.bit_index;
    }
    fixed_scl_public_round_schedule_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
        bit_indices,
    )
}

pub fn fixed_scl_round_schedule_plan_certificate<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
) -> FixedSclPublicRoundSchedulePlan {
    fixed_scl_round_schedule_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(rounds)
}

pub fn fixed_scl_round_schedule_plan_parity_check<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
    expected_public_plan: FixedSclPublicRoundSchedulePlan,
) -> FixedSclRoundSchedulePlanParityCheck {
    let round_schedule_plan =
        fixed_scl_round_schedule_plan_certificate::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
            rounds,
        );

    FixedSclRoundSchedulePlanParityCheck {
        matches: round_schedule_plan == expected_public_plan,
        round_schedule_plan,
        expected_public_plan,
    }
}

pub fn fixed_scl_round_schedule_shape_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
) -> FixedSclPublicRoundScheduleShapePlan {
    let mut bit_indices = [0usize; ROUNDS];
    for (index, round) in rounds.iter().enumerate() {
        bit_indices[index] = round.bit_index;
    }
    fixed_scl_public_round_schedule_shape_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
        bit_indices,
    )
}

pub fn fixed_scl_round_schedule_shape_plan_certificate<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
) -> FixedSclPublicRoundScheduleShapePlan {
    fixed_scl_round_schedule_shape_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(rounds)
}

pub fn fixed_scl_round_schedule_shape_parity_check<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    rounds: [FixedSclRound; ROUNDS],
    expected_shape_plan: FixedSclPublicRoundScheduleShapePlan,
) -> FixedSclRoundScheduleShapeParityCheck {
    let round_shape_plan = fixed_scl_round_schedule_shape_plan_certificate::<
        CAP,
        N,
        FIRST_CHILD_CAP,
        CHILD_CAP,
        L,
        ROUNDS,
    >(rounds);

    FixedSclRoundScheduleShapeParityCheck {
        matches: round_shape_plan == expected_shape_plan,
        round_shape_plan,
        expected_shape_plan,
    }
}

pub fn fixed_scl_public_round_work_counts(
    parent_capacity: usize,
    child_capacity: usize,
    list_size: usize,
    rounds: usize,
) -> FixedSclPublicRoundWorkCounts {
    fixed_scl_public_round_work_counts_with_capacities(
        parent_capacity,
        child_capacity,
        child_capacity,
        list_size,
        rounds,
    )
}

pub fn fixed_scl_public_round_work_counts_with_capacities(
    parent_capacity: usize,
    first_child_capacity: usize,
    repeated_child_capacity: usize,
    list_size: usize,
    rounds: usize,
) -> FixedSclPublicRoundWorkCounts {
    let first_rounds = usize::from(rounds > 0);
    let repeated_rounds = rounds.saturating_sub(1);
    FixedSclPublicRoundWorkCounts {
        parent_capacity,
        first_child_capacity,
        repeated_child_capacity,
        list_size,
        rounds,
        top_l_compare_exchanges: first_rounds
            .saturating_mul(fixed_schedule_top_l_compare_count(first_child_capacity))
            .saturating_add(
                repeated_rounds
                    .saturating_mul(fixed_schedule_top_l_compare_count(repeated_child_capacity)),
            ),
        child_slots_written: first_rounds
            .saturating_mul(parent_capacity)
            .saturating_mul(2)
            .saturating_add(repeated_rounds.saturating_mul(list_size.saturating_mul(2))),
        compacted_slots_written: rounds.saturating_mul(list_size),
    }
}

pub fn fixed_scl_public_round_work_shape_plan(
    parent_capacity: usize,
    first_child_capacity: usize,
    repeated_child_capacity: usize,
    list_size: usize,
    rounds: usize,
) -> FixedSclPublicRoundWorkShapePlan {
    let first_top_l_plan = fixed_schedule_top_l_selection_plan(first_child_capacity, list_size);
    let repeated_top_l_plan =
        fixed_schedule_top_l_selection_plan(repeated_child_capacity, list_size);
    let first_round_active = rounds > 0;
    let repeated_round_active = rounds > 1;
    let valid = (!first_round_active || first_top_l_plan.valid)
        && (!repeated_round_active || repeated_top_l_plan.valid);
    let work_rounds = if valid { rounds } else { 0 };

    FixedSclPublicRoundWorkShapePlan {
        parent_capacity,
        first_child_capacity,
        repeated_child_capacity,
        list_size,
        rounds,
        valid,
        first_top_l_plan,
        repeated_top_l_plan,
        work_counts: fixed_scl_public_round_work_counts_with_capacities(
            parent_capacity,
            first_child_capacity,
            repeated_child_capacity,
            list_size,
            work_rounds,
        ),
    }
}

pub fn fixed_scl_public_round_schedule_shape_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    bit_indices: [usize; ROUNDS],
) -> FixedSclPublicRoundScheduleShapePlan {
    let path_domain_check = fixed_scl_path_buffer_schedule_domain_check::<
        CAP,
        N,
        FIRST_CHILD_CAP,
        CHILD_CAP,
        L,
        ROUNDS,
    >(bit_indices);
    let active_rounds = if path_domain_check.valid { ROUNDS } else { 0 };
    let work_shape_plan =
        fixed_scl_public_round_work_shape_plan(CAP, FIRST_CHILD_CAP, CHILD_CAP, L, active_rounds);

    FixedSclPublicRoundScheduleShapePlan {
        valid: path_domain_check.valid && work_shape_plan.valid,
        path_domain_check,
        work_shape_plan,
    }
}

pub fn fixed_scl_public_round_run_shape_certificate<const L: usize, const N: usize>(
    run: &FixedSclPublicRoundScheduleRun<L, N>,
) -> FixedSclPublicRoundScheduleShapePlan {
    let counts = run.work_counts;
    let work_shape_plan = fixed_scl_public_round_work_shape_plan(
        counts.parent_capacity,
        counts.first_child_capacity,
        counts.repeated_child_capacity,
        counts.list_size,
        counts.rounds,
    );

    FixedSclPublicRoundScheduleShapePlan {
        valid: run.path_domain_check.valid && work_shape_plan.valid,
        path_domain_check: run.path_domain_check,
        work_shape_plan,
    }
}

pub fn fixed_scl_public_round_shape_parity_check<const L: usize, const N: usize>(
    run: &FixedSclPublicRoundScheduleRun<L, N>,
    expected_shape_plan: FixedSclPublicRoundScheduleShapePlan,
) -> FixedSclPublicRoundShapeParityCheck {
    let run_shape_certificate = fixed_scl_public_round_run_shape_certificate(run);

    FixedSclPublicRoundShapeParityCheck {
        matches: run_shape_certificate == expected_shape_plan,
        run_shape_certificate,
        expected_shape_plan,
    }
}

pub fn two_public_bits_run_shape_certificate<const L: usize, const N: usize>(
    run: &FixedSclPublicRoundScheduleRun<L, N>,
) -> FixedSclPublicRoundScheduleShapePlan {
    fixed_scl_public_round_run_shape_certificate(run)
}

pub fn two_public_bits_shape_parity_check<const L: usize, const N: usize>(
    run: &FixedSclPublicRoundScheduleRun<L, N>,
    expected_shape_plan: FixedSclPublicRoundScheduleShapePlan,
) -> FixedSclPublicRoundShapeParityCheck {
    fixed_scl_public_round_shape_parity_check(run, expected_shape_plan)
}

pub fn fixed_scl_one_bit_run_plan_certificate<
    const CHILD_CAP: usize,
    const L: usize,
    const N: usize,
>(
    run: &FixedSclOneBitExpansionRun<CHILD_CAP, L, N>,
) -> FixedSclPublicRoundSchedulePlan {
    FixedSclPublicRoundSchedulePlan {
        path_domain_check: run.path_domain_check,
        work_counts: run.work_counts,
    }
}

pub fn fixed_scl_one_bit_shape_parity_check<
    const CHILD_CAP: usize,
    const L: usize,
    const N: usize,
>(
    run: &FixedSclOneBitExpansionRun<CHILD_CAP, L, N>,
    expected_plan: FixedSclPublicRoundSchedulePlan,
) -> FixedSclOneBitShapeParityCheck {
    let run_plan_certificate = fixed_scl_one_bit_run_plan_certificate(run);

    FixedSclOneBitShapeParityCheck {
        matches: run_plan_certificate == expected_plan,
        run_plan_certificate,
        expected_plan,
    }
}

pub fn fixed_scl_public_round_schedule_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    bit_indices: [usize; ROUNDS],
) -> FixedSclPublicRoundSchedulePlan {
    let path_domain_check = fixed_scl_path_buffer_schedule_domain_check::<
        CAP,
        N,
        FIRST_CHILD_CAP,
        CHILD_CAP,
        L,
        ROUNDS,
    >(bit_indices);
    let rounds = if path_domain_check.valid { ROUNDS } else { 0 };
    FixedSclPublicRoundSchedulePlan {
        path_domain_check,
        work_counts: fixed_scl_public_round_work_counts_with_capacities(
            CAP,
            FIRST_CHILD_CAP,
            CHILD_CAP,
            L,
            rounds,
        ),
    }
}

pub fn fixed_scl_integer_round_schedule_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    bit_indices: [usize; ROUNDS],
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> FixedSclIntegerRoundSchedulePlan {
    let domain_check = fixed_scl_integer_schedule_domain_check(hard_bits, magnitudes);
    let public_plan =
        fixed_scl_public_round_schedule_plan::<CAP, N, FIRST_CHILD_CAP, CHILD_CAP, L, ROUNDS>(
            bit_indices,
        );
    let work_counts = if domain_check.valid {
        public_plan.work_counts
    } else {
        fixed_scl_public_round_work_counts_with_capacities(CAP, FIRST_CHILD_CAP, CHILD_CAP, L, 0)
    };

    FixedSclIntegerRoundSchedulePlan {
        domain_check,
        path_domain_check: public_plan.path_domain_check,
        work_counts,
    }
}

pub fn fixed_scl_integer_round_schedule_shape_plan<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    bit_indices: [usize; ROUNDS],
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> FixedSclIntegerRoundScheduleShapePlan {
    let domain_check = fixed_scl_integer_schedule_domain_check(hard_bits, magnitudes);
    let public_shape_plan = fixed_scl_public_round_schedule_shape_plan::<
        CAP,
        N,
        FIRST_CHILD_CAP,
        CHILD_CAP,
        L,
        ROUNDS,
    >(bit_indices);
    let work_shape_plan = if domain_check.valid {
        public_shape_plan.work_shape_plan
    } else {
        fixed_scl_public_round_work_shape_plan(CAP, FIRST_CHILD_CAP, CHILD_CAP, L, 0)
    };

    FixedSclIntegerRoundScheduleShapePlan {
        valid: domain_check.valid
            && public_shape_plan.path_domain_check.valid
            && work_shape_plan.valid,
        domain_check,
        path_domain_check: public_shape_plan.path_domain_check,
        work_shape_plan,
    }
}

pub fn fixed_scl_integer_round_run_plan_certificate<const L: usize, const N: usize>(
    run: &FixedSclPathBufferIntegerScheduleRun<L, N>,
) -> FixedSclIntegerRoundSchedulePlan {
    FixedSclIntegerRoundSchedulePlan {
        domain_check: run.domain_check,
        path_domain_check: run.path_domain_check,
        work_counts: run.work_counts,
    }
}

pub fn fixed_scl_integer_round_run_shape_certificate<const L: usize, const N: usize>(
    run: &FixedSclPathBufferIntegerScheduleRun<L, N>,
) -> FixedSclIntegerRoundScheduleShapePlan {
    let counts = run.work_counts;
    let work_shape_plan = fixed_scl_public_round_work_shape_plan(
        counts.parent_capacity,
        counts.first_child_capacity,
        counts.repeated_child_capacity,
        counts.list_size,
        counts.rounds,
    );

    FixedSclIntegerRoundScheduleShapePlan {
        valid: run.domain_check.valid && run.path_domain_check.valid && work_shape_plan.valid,
        domain_check: run.domain_check,
        path_domain_check: run.path_domain_check,
        work_shape_plan,
    }
}

pub fn fixed_scl_integer_shape_parity_check<const L: usize, const N: usize>(
    run: &FixedSclPathBufferIntegerScheduleRun<L, N>,
    expected_plan: FixedSclIntegerRoundSchedulePlan,
) -> FixedSclIntegerShapeParityCheck {
    let run_plan_certificate = fixed_scl_integer_round_run_plan_certificate(run);

    FixedSclIntegerShapeParityCheck {
        matches: run_plan_certificate == expected_plan,
        run_plan_certificate,
        expected_plan,
    }
}

pub fn fixed_scl_integer_schedule_shape_parity_check<const L: usize, const N: usize>(
    run: &FixedSclPathBufferIntegerScheduleRun<L, N>,
    expected_shape_plan: FixedSclIntegerRoundScheduleShapePlan,
) -> FixedSclIntegerScheduleShapeParityCheck {
    let run_shape_certificate = fixed_scl_integer_round_run_shape_certificate(run);

    FixedSclIntegerScheduleShapeParityCheck {
        matches: run_shape_certificate == expected_shape_plan,
        run_shape_certificate,
        expected_shape_plan,
    }
}

pub fn fixed_scl_integer_schedule_shape_failure_family(
    plan: FixedSclIntegerRoundScheduleShapePlan,
) -> u8 {
    let domain_invalid = u8::from(!plan.domain_check.valid);
    let path_invalid = u8::from(!plan.path_domain_check.valid);
    let work_invalid = u8::from(!plan.work_shape_plan.valid);
    let domain_valid = domain_invalid ^ 1;
    let path_valid = path_invalid ^ 1;
    let path_selected = path_invalid & domain_valid;
    let work_selected = work_invalid & domain_valid & path_valid;
    let domain_mask = 0u8.wrapping_sub(domain_invalid);
    let path_mask = 0u8.wrapping_sub(path_selected);
    let work_mask = 0u8.wrapping_sub(work_selected);
    let failure_after_work = select_u8(
        work_mask,
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_OK,
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE,
    );
    let failure_after_path = select_u8(
        path_mask,
        failure_after_work,
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN,
    );

    select_u8(
        domain_mask,
        failure_after_path,
        FIXED_SCL_INTEGER_SCHEDULE_SHAPE_FAILURE_FAMILY_INTEGER_DOMAIN,
    )
}

pub fn fixed_scl_public_round_schedule_shape_failure_family(
    plan: FixedSclPublicRoundScheduleShapePlan,
) -> u8 {
    if !plan.path_domain_check.valid {
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_PATH_DOMAIN
    } else if !plan.work_shape_plan.valid {
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_WORK_SHAPE
    } else {
        FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_FAMILY_OK
    }
}

pub fn fixed_scl_binary_child_write_domain_check<
    const SRC_CAP: usize,
    const CHILD_CAP: usize,
    const N: usize,
>(
    parent_slot: usize,
    dst_start: usize,
    bit_index: usize,
) -> FixedSclBinaryChildWriteDomainCheck {
    let parent_invalid = u8::from(parent_slot >= SRC_CAP);
    let dst_invalid = u8::from(dst_start >= CHILD_CAP || dst_start.saturating_add(1) >= CHILD_CAP);
    let bit_invalid = u8::from(bit_index >= N);
    let parent_valid = parent_invalid ^ 1;
    let dst_valid = dst_invalid ^ 1;
    let dst_selected = dst_invalid & parent_valid;
    let bit_selected = bit_invalid & parent_valid & dst_valid;
    let invalid = parent_invalid | dst_invalid | bit_invalid;
    let parent_mask = 0u8.wrapping_sub(parent_invalid);
    let dst_mask = 0u8.wrapping_sub(dst_selected);
    let bit_mask = 0u8.wrapping_sub(bit_selected);
    let valid_mask = 0usize.wrapping_sub(usize::from(invalid ^ 1));
    let failure_after_bit = select_u8(
        bit_mask,
        FIXED_SCL_CHILD_WRITE_DOMAIN_OK,
        FIXED_SCL_CHILD_WRITE_DOMAIN_BIT_INDEX,
    );
    let failure_after_dst = select_u8(
        dst_mask,
        failure_after_bit,
        FIXED_SCL_CHILD_WRITE_DOMAIN_DST_CAPACITY,
    );
    let failure_code = select_u8(
        parent_mask,
        failure_after_dst,
        FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT,
    );
    let child_slots_written = select_usize(valid_mask, 0, 2);

    FixedSclBinaryChildWriteDomainCheck {
        parent_capacity: SRC_CAP,
        child_capacity: CHILD_CAP,
        bit_width: N,
        parent_slot,
        dst_start,
        bit_index,
        child_slots_written,
        valid: invalid == 0,
        failure_code,
    }
}

pub fn fixed_scl_child_write_parity_check(
    run_domain_check: FixedSclBinaryChildWriteDomainCheck,
    expected_domain_check: FixedSclBinaryChildWriteDomainCheck,
) -> FixedSclChildWriteParityCheck {
    FixedSclChildWriteParityCheck {
        matches: run_domain_check == expected_domain_check,
        run_domain_check,
        expected_domain_check,
    }
}

pub fn fixed_scl_path_buffer_schedule_domain_check<
    const CAP: usize,
    const N: usize,
    const FIRST_CHILD_CAP: usize,
    const CHILD_CAP: usize,
    const L: usize,
    const ROUNDS: usize,
>(
    bit_indices: [usize; ROUNDS],
) -> FixedSclPathBufferScheduleDomainCheck {
    let empty_invalid = u8::from(ROUNDS == 0);
    let first_child_invalid = u8::from(CAP.saturating_mul(2) > FIRST_CHILD_CAP);
    let top_l_invalid = u8::from(L > FIRST_CHILD_CAP || (ROUNDS > 1 && L > CHILD_CAP));
    let repeated_child_invalid = u8::from(ROUNDS > 1 && L.saturating_mul(2) > CHILD_CAP);
    let empty_valid = empty_invalid ^ 1;
    let first_child_valid = first_child_invalid ^ 1;
    let top_l_valid = top_l_invalid ^ 1;
    let first_child_selected = first_child_invalid & empty_valid;
    let top_l_selected = top_l_invalid & empty_valid & first_child_valid;
    let repeated_child_selected =
        repeated_child_invalid & empty_valid & first_child_valid & top_l_valid;
    let shape_invalid =
        empty_invalid | first_child_invalid | top_l_invalid | repeated_child_invalid;
    let mut bit_invalid_seen = 0u8;
    let mut first_bit_invalid_round = FIXED_SCL_NO_INVALID_ROUND;

    for (round, bit_index) in bit_indices.iter().enumerate() {
        let bit_invalid = u8::from(*bit_index >= N);
        let first_bit_for_round = (bit_invalid_seen ^ 1) & bit_invalid;
        let first_bit_mask = 0usize.wrapping_sub(usize::from(first_bit_for_round));

        first_bit_invalid_round = select_usize(first_bit_mask, first_bit_invalid_round, round);
        bit_invalid_seen |= bit_invalid;
    }

    let bit_selected = bit_invalid_seen & (shape_invalid ^ 1);
    let empty_mask = 0u8.wrapping_sub(empty_invalid);
    let first_child_mask = 0u8.wrapping_sub(first_child_selected);
    let top_l_mask = 0u8.wrapping_sub(top_l_selected);
    let repeated_child_mask = 0u8.wrapping_sub(repeated_child_selected);
    let bit_mask = 0u8.wrapping_sub(bit_selected);
    let bit_round_mask = 0usize.wrapping_sub(usize::from(bit_selected));
    let failure_after_bit = select_u8(
        bit_mask,
        FIXED_SCL_PATH_DOMAIN_OK,
        FIXED_SCL_PATH_DOMAIN_BIT_INDEX,
    );
    let failure_after_repeated_child = select_u8(
        repeated_child_mask,
        failure_after_bit,
        FIXED_SCL_PATH_DOMAIN_REPEATED_CHILD_CAPACITY,
    );
    let failure_after_top_l = select_u8(
        top_l_mask,
        failure_after_repeated_child,
        FIXED_SCL_PATH_DOMAIN_TOP_L_WIDTH,
    );
    let failure_after_first_child = select_u8(
        first_child_mask,
        failure_after_top_l,
        FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY,
    );
    let failure_code = select_u8(
        empty_mask,
        failure_after_first_child,
        FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE,
    );
    let first_invalid_round = select_usize(
        bit_round_mask,
        FIXED_SCL_NO_INVALID_ROUND,
        first_bit_invalid_round,
    );
    let invalid = shape_invalid | bit_invalid_seen;

    FixedSclPathBufferScheduleDomainCheck {
        parent_capacity: CAP,
        first_child_capacity: FIRST_CHILD_CAP,
        repeated_child_capacity: CHILD_CAP,
        list_size: L,
        rounds: ROUNDS,
        bit_width: N,
        valid: invalid == 0,
        failure_code,
        first_invalid_round,
    }
}

pub fn fixed_scl_integer_schedule_domain_check<const ROUNDS: usize>(
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> FixedSclIntegerScheduleDomainCheck {
    let mut invalid_seen = 0u8;
    let mut failure_code = FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK;
    let mut first_invalid_round = FIXED_SCL_NO_INVALID_ROUND;

    for index in 0..ROUNDS {
        let hard_invalid = u8::from(hard_bits[index] > 1);
        let magnitude_invalid = u8::from(magnitudes[index] < 0);
        let hard_valid = hard_invalid ^ 1;
        let magnitude_selected = magnitude_invalid & hard_valid;
        let round_invalid = hard_invalid | magnitude_invalid;
        let first_for_round = (invalid_seen ^ 1) & round_invalid;
        let magnitude_mask = 0u8.wrapping_sub(magnitude_selected);
        let hard_mask = 0u8.wrapping_sub(hard_invalid);
        let first_mask = 0u8.wrapping_sub(first_for_round);
        let first_round_mask = 0usize.wrapping_sub(usize::from(first_for_round));
        let failure_after_magnitude = select_u8(
            magnitude_mask,
            FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
            FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
        );
        let round_failure_code = select_u8(
            hard_mask,
            failure_after_magnitude,
            FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
        );

        failure_code = select_u8(first_mask, failure_code, round_failure_code);
        first_invalid_round = select_usize(first_round_mask, first_invalid_round, index);
        invalid_seen |= round_invalid;
    }

    FixedSclIntegerScheduleDomainCheck {
        rounds: ROUNDS,
        valid: invalid_seen == 0,
        failure_code,
        first_invalid_round,
    }
}

pub fn fixed_scl_integer_metric_domain_check(
    hard_bit: u8,
    magnitude: i64,
) -> FixedSclIntegerMetricDomainCheck {
    let hard_invalid = u8::from(hard_bit > 1);
    let magnitude_invalid = u8::from(magnitude < 0);
    let hard_mask = 0u8.wrapping_sub(hard_invalid);
    let magnitude_selected = magnitude_invalid & (hard_invalid ^ 1);
    let magnitude_mask = 0u8.wrapping_sub(magnitude_selected);
    let failure_after_magnitude = select_u8(
        magnitude_mask,
        FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_OK,
        FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_MAGNITUDE,
    );
    let failure_code = select_u8(
        hard_mask,
        failure_after_magnitude,
        FIXED_SCL_INTEGER_SCHEDULE_DOMAIN_HARD_BIT,
    );
    let invalid = hard_invalid | magnitude_invalid;

    FixedSclIntegerMetricDomainCheck {
        valid: invalid == 0,
        failure_code,
    }
}

pub fn fixed_scl_integer_metric_deltas(
    frozen_bit: bool,
    hard_bit: u8,
    magnitude: i64,
) -> FixedSclMetricDeltas {
    assert!(hard_bit <= 1, "integer metric hard bit must be 0 or 1");
    assert!(
        magnitude >= 0,
        "integer metric magnitude must be non-negative"
    );

    let hard_bit_i64 = i64::from(hard_bit & 1);
    let hard_bit_mask = 0i64.wrapping_sub(hard_bit_i64);
    let frozen_i64 = i64::from(frozen_bit);
    let frozen_mask = 0i64.wrapping_sub(frozen_i64);

    let bit0_metric_delta = select_i64(hard_bit_mask, 0, magnitude);
    let unfrozen_bit1_delta = select_i64(hard_bit_mask, magnitude, 0);
    let bit1_metric_delta = select_i64(
        frozen_mask,
        unfrozen_bit1_delta,
        FIXED_SCL_FORBIDDEN_METRIC_DELTA,
    );

    FixedSclMetricDeltas {
        bit0_metric_delta,
        bit1_metric_delta,
    }
}

pub fn try_fixed_scl_integer_metric_deltas(
    frozen_bit: bool,
    hard_bit: u8,
    magnitude: i64,
) -> FixedSclIntegerMetricDeltaRun {
    let domain_check = fixed_scl_integer_metric_domain_check(hard_bit, magnitude);
    let invalid_i64 = i64::from(domain_check.valid) ^ 1;
    let invalid_mask = 0i64.wrapping_sub(invalid_i64);
    let magnitude_negative = i64::from(magnitude < 0);
    let magnitude_negative_mask = 0i64.wrapping_sub(magnitude_negative);
    let safe_magnitude = select_i64(magnitude_negative_mask, magnitude, 0);
    let hard_bit_i64 = i64::from(hard_bit & 1);
    let hard_bit_mask = 0i64.wrapping_sub(hard_bit_i64);
    let frozen_i64 = i64::from(frozen_bit);
    let frozen_mask = 0i64.wrapping_sub(frozen_i64);
    let bit0_metric_delta = select_i64(hard_bit_mask, 0, safe_magnitude);
    let unfrozen_bit1_delta = select_i64(hard_bit_mask, safe_magnitude, 0);
    let bit1_metric_delta = select_i64(
        frozen_mask,
        unfrozen_bit1_delta,
        FIXED_SCL_FORBIDDEN_METRIC_DELTA,
    );

    FixedSclIntegerMetricDeltaRun {
        domain_check,
        deltas: FixedSclMetricDeltas {
            bit0_metric_delta: select_i64(
                invalid_mask,
                bit0_metric_delta,
                FIXED_SCL_FORBIDDEN_METRIC_DELTA,
            ),
            bit1_metric_delta: select_i64(
                invalid_mask,
                bit1_metric_delta,
                FIXED_SCL_FORBIDDEN_METRIC_DELTA,
            ),
        },
    }
}

pub fn fixed_scl_integer_round_schedule<const ROUNDS: usize>(
    bit_indices: [usize; ROUNDS],
    frozen_bits: [bool; ROUNDS],
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> [FixedSclRound; ROUNDS] {
    let mut rounds = [FixedSclRound::new(0, 0, 0); ROUNDS];
    for index in 0..ROUNDS {
        let deltas = fixed_scl_integer_metric_deltas(
            frozen_bits[index],
            hard_bits[index],
            magnitudes[index],
        );
        rounds[index] = FixedSclRound::new(
            bit_indices[index],
            deltas.bit0_metric_delta,
            deltas.bit1_metric_delta,
        );
    }
    rounds
}

pub fn try_fixed_scl_integer_round_schedule<const ROUNDS: usize>(
    bit_indices: [usize; ROUNDS],
    frozen_bits: [bool; ROUNDS],
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> FixedSclIntegerRoundScheduleBuild<ROUNDS> {
    let domain_check = fixed_scl_integer_schedule_domain_check(hard_bits, magnitudes);
    let invalid_usize = usize::from(domain_check.valid) ^ 1;
    let invalid_i64 = i64::from(domain_check.valid) ^ 1;
    let invalid_mask_usize = 0usize.wrapping_sub(invalid_usize);
    let invalid_mask_i64 = 0i64.wrapping_sub(invalid_i64);
    let zero_round = FixedSclRound::new(0, 0, 0);
    let mut rounds = [zero_round; ROUNDS];

    for index in 0..ROUNDS {
        let delta_run = try_fixed_scl_integer_metric_deltas(
            frozen_bits[index],
            hard_bits[index],
            magnitudes[index],
        );
        let candidate_round = FixedSclRound::new(
            bit_indices[index],
            delta_run.deltas.bit0_metric_delta,
            delta_run.deltas.bit1_metric_delta,
        );
        rounds[index] = select_round(
            invalid_mask_usize,
            invalid_mask_i64,
            candidate_round,
            zero_round,
        );
    }

    FixedSclIntegerRoundScheduleBuild {
        domain_check,
        round_slots_written: select_usize(invalid_mask_usize, ROUNDS, 0),
        rounds,
    }
}

pub fn fixed_scl_integer_round_schedule_build_plan<const ROUNDS: usize>(
    hard_bits: [u8; ROUNDS],
    magnitudes: [i64; ROUNDS],
) -> FixedSclIntegerRoundScheduleBuildPlan {
    let domain_check = fixed_scl_integer_schedule_domain_check(hard_bits, magnitudes);
    let invalid_usize = usize::from(domain_check.valid) ^ 1;
    let invalid_mask_usize = 0usize.wrapping_sub(invalid_usize);

    FixedSclIntegerRoundScheduleBuildPlan {
        domain_check,
        round_slots_written: select_usize(invalid_mask_usize, ROUNDS, 0),
    }
}

pub fn fixed_scl_integer_round_build_certificate<const ROUNDS: usize>(
    build: &FixedSclIntegerRoundScheduleBuild<ROUNDS>,
) -> FixedSclIntegerRoundScheduleBuildPlan {
    FixedSclIntegerRoundScheduleBuildPlan {
        domain_check: build.domain_check,
        round_slots_written: build.round_slots_written,
    }
}

pub fn fixed_scl_integer_round_build_parity_check<const ROUNDS: usize>(
    build: &FixedSclIntegerRoundScheduleBuild<ROUNDS>,
    expected_plan: FixedSclIntegerRoundScheduleBuildPlan,
) -> FixedSclIntegerRoundScheduleBuildParityCheck {
    let run_build_certificate = fixed_scl_integer_round_build_certificate(build);

    FixedSclIntegerRoundScheduleBuildParityCheck {
        matches: run_build_certificate == expected_plan,
        run_build_certificate,
        expected_plan,
    }
}

pub fn fixed_schedule_top_l_i64<const WIDTH: usize, const L: usize>(
    metrics: [i64; WIDTH],
) -> [FixedTopLEntry; L] {
    assert!(L <= WIDTH, "top-L selector requires L <= WIDTH");
    let mut entries = [FixedTopLEntry {
        metric: i64::MAX,
        index: usize::MAX,
    }; WIDTH];
    for i in 0..WIDTH {
        entries[i] = FixedTopLEntry {
            metric: metrics[i],
            index: i,
        };
    }

    for i in 0..WIDTH {
        for j in (i + 1)..WIDTH {
            fixed_compare_exchange(&mut entries, i, j);
        }
    }

    let mut top = [FixedTopLEntry {
        metric: i64::MAX,
        index: usize::MAX,
    }; L];
    top[..L].copy_from_slice(&entries[..L]);
    top
}

fn fixed_compare_exchange(entries: &mut [FixedTopLEntry], left: usize, right: usize) {
    let a = entries[left];
    let b = entries[right];
    let take_b = entry_less_flag(b, a);
    let mask_usize = 0usize.wrapping_sub(take_b);
    let mask_i64 = 0i64.wrapping_sub(take_b as i64);

    entries[left] = FixedTopLEntry {
        metric: select_i64(mask_i64, a.metric, b.metric),
        index: select_usize(mask_usize, a.index, b.index),
    };
    entries[right] = FixedTopLEntry {
        metric: select_i64(mask_i64, b.metric, a.metric),
        index: select_usize(mask_usize, b.index, a.index),
    };
}

fn entry_less_flag(a: FixedTopLEntry, b: FixedTopLEntry) -> usize {
    let metric_lt = usize::from(a.metric < b.metric);
    let metric_eq = usize::from(a.metric == b.metric);
    let index_lt = usize::from(a.index < b.index);

    metric_lt | (metric_eq & index_lt)
}

fn select_i64(mask: i64, keep: i64, replace: i64) -> i64 {
    (keep & !mask) | (replace & mask)
}

fn select_usize(mask: usize, keep: usize, replace: usize) -> usize {
    (keep & !mask) | (replace & mask)
}

fn select_u8(mask: u8, keep: u8, replace: u8) -> u8 {
    (keep & !mask) | (replace & mask)
}

fn select_round(
    mask_usize: usize,
    mask_i64: i64,
    keep: FixedSclRound,
    replace: FixedSclRound,
) -> FixedSclRound {
    FixedSclRound {
        bit_index: select_usize(mask_usize, keep.bit_index, replace.bit_index),
        bit0_metric_delta: select_i64(mask_i64, keep.bit0_metric_delta, replace.bit0_metric_delta),
        bit1_metric_delta: select_i64(mask_i64, keep.bit1_metric_delta, replace.bit1_metric_delta),
    }
}

fn select_candidate<const N: usize>(
    mask_i64: i64,
    mask_u8: u8,
    keep: FixedSclCandidate<N>,
    replace: FixedSclCandidate<N>,
) -> FixedSclCandidate<N> {
    let mut bits = [0u8; N];
    for index in 0..N {
        bits[index] = select_u8(mask_u8, keep.bits[index], replace.bits[index]);
    }
    FixedSclCandidate {
        metric: select_i64(mask_i64, keep.metric, replace.metric),
        bits,
        active: select_u8(mask_u8, keep.active, replace.active),
    }
}

fn sanitize_candidate_active<const N: usize>(
    candidate: FixedSclCandidate<N>,
) -> FixedSclCandidate<N> {
    let active = candidate.active & 1;
    let active_i64_mask = 0i64.wrapping_sub(i64::from(active));
    let active_u8_mask = 0u8.wrapping_sub(active);
    FixedSclCandidate {
        metric: select_i64(active_i64_mask, i64::MAX, candidate.metric),
        bits: mask_bits(candidate.bits, active_u8_mask),
        active,
    }
}

fn mask_bits<const N: usize>(bits: [u8; N], mask: u8) -> [u8; N] {
    let mut masked = [0u8; N];
    for index in 0..N {
        masked[index] = bits[index] & mask;
    }
    masked
}

fn fixed_scl_metric_add(parent_metric: i64, metric_delta: i64) -> i64 {
    let parent_forbidden = (parent_metric == i64::MAX) as i64;
    let delta_forbidden = (metric_delta == FIXED_SCL_FORBIDDEN_METRIC_DELTA) as i64;
    let forbidden = parent_forbidden | delta_forbidden;
    let forbidden_mask = 0i64.wrapping_sub(forbidden);
    let sum = parent_metric.saturating_add(metric_delta);

    select_i64(forbidden_mask, sum, FIXED_SCL_FORBIDDEN_METRIC_DELTA)
}

pub fn scl_work_shape_audit_json() -> &'static str {
    concat!(
        "{\n",
        "  \"experiment\": \"codex-polar-scl-workshape-audit\",\n",
        "  \"ct_surface\": \"ct-003\",\n",
        "  \"component\": \"impl/polar_validation SCL decoder\",\n",
        "  \"status\": \"audit boundary only; current decoder is variable-shape reference code\",\n",
        "  \"current_verdict\": \"not_constant_time\",\n",
        "  \"production_constant_time_claim\": false,\n",
        "  \"audited_functions\": [\n",
        "    \"decode_scl\",\n",
        "    \"decode_scl_fixed_i64\",\n",
        "    \"decode_scl_fast\",\n",
        "    \"scl_decode_node\",\n",
        "    \"prune_paths\"\n",
        "  ],\n",
        "  \"active_decoder_entrypoints\": [\n",
        "    {\n",
        "      \"name\": \"decode_scl_fixed_i64\",\n",
        "      \"cli_decoder\": \"fixed-i64\",\n",
        "      \"status\": \"active_fixed_i64_reference_entrypoint_not_production_ct\",\n",
        "      \"metric_domain\": \"i64 path metrics with public validation scale\",\n",
        "      \"claim\": \"KAT/BLER-tested validation rail only; generated-code and timing/leakage audit pending before any production constant-time claim\"\n",
        "    }\n",
        "  ],\n",
        "  \"variable_shape_surfaces\": [\n",
        "    \"path metric sort in prune_paths\",\n",
        "    \"Vec growth and truncate in path pruning\",\n",
        "    \"branching on frozen_mask and candidate bit expansion\",\n",
        "    \"floating-point path metrics and total_cmp ordering\",\n",
        "    \"recursive SCL node composition with data-dependent path contents\"\n",
        "  ],\n",
        "  \"fixed_schedule_requirements\": [\n",
        "    \"fixed-list array layout for all paths\",\n",
        "    \"integer or masked metric updates\",\n",
        "    \"data-oblivious top-L selection network\",\n",
        "    \"no secret-dependent allocation, sorting, truncation, or branch pruning\",\n",
        "    \"generated-code and timing/leakage audit before any production claim\"\n",
        "  ],\n",
        "  \"metric_domain_assumptions\": [\n",
        "    \"negative metric deltas are diagnostic-only in source-level rail tests\",\n",
        "    \"future active integer SCL rail requires fixed-width non-negative penalties before decoder wiring\",\n",
        "    \"forbidden sentinel must remain terminal under parent-metric addition\"\n",
        "  ],\n",
        "  \"top_l_selection_domain_failure_codes\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public top-L selection shape\"},\n",
        "    {\"code\": 1, \"name\": \"width\", \"meaning\": \"list size must be no larger than selection width\"}\n",
        "  ],\n",
        "  \"public_path_domain_failure_codes\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public path-buffer schedule shape\"},\n",
        "    {\"code\": 1, \"name\": \"empty_schedule\", \"meaning\": \"round schedule must contain at least one public round\"},\n",
        "    {\"code\": 2, \"name\": \"first_child_capacity\", \"meaning\": \"first child buffer must hold two children per parent slot\"},\n",
        "    {\"code\": 3, \"name\": \"repeated_child_capacity\", \"meaning\": \"repeated child buffer must hold two children per compacted path\"},\n",
        "    {\"code\": 4, \"name\": \"top_l_width\", \"meaning\": \"list size must fit the parent and child selection widths\"},\n",
        "    {\"code\": 5, \"name\": \"bit_index\", \"meaning\": \"every public bit index must be inside the path bit width\"}\n",
        "  ],\n",
        "  \"public_child_write_failure_codes\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public fixed child-write domain\"},\n",
        "    {\"code\": 1, \"name\": \"parent_slot\", \"meaning\": \"parent slot must be inside the fixed parent buffer\"},\n",
        "    {\"code\": 2, \"name\": \"dst_capacity\", \"meaning\": \"destination child buffer must have room for both children\"},\n",
        "    {\"code\": 3, \"name\": \"bit_index\", \"meaning\": \"public bit index must be inside the path bit width\"}\n",
        "  ],\n",
        "  \"integer_schedule_domain_failure_codes\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public integer schedule inputs\"},\n",
        "    {\"code\": 1, \"name\": \"hard_bit\", \"meaning\": \"hard decisions must be public bits\"},\n",
        "    {\"code\": 2, \"name\": \"magnitude\", \"meaning\": \"integer metric magnitudes must be non-negative\"}\n",
        "  ],\n",
        "  \"integer_metric_domain_failure_codes\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public integer metric inputs\"},\n",
        "    {\"code\": 1, \"name\": \"hard_bit\", \"meaning\": \"hard decisions must be public bits\"},\n",
        "    {\"code\": 2, \"name\": \"magnitude\", \"meaning\": \"integer metric magnitudes must be non-negative\"}\n",
        "  ],\n",
        "  \"integer_schedule_shape_failure_families\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid integer schedule-shape preflight\"},\n",
        "    {\"code\": 1, \"name\": \"integer_domain\", \"meaning\": \"integer hard-bit or metric-magnitude domain failed first\"},\n",
        "    {\"code\": 2, \"name\": \"path_domain\", \"meaning\": \"public path-buffer schedule domain failed first\"},\n",
        "    {\"code\": 3, \"name\": \"work_shape\", \"meaning\": \"public top-L work-shape envelope failed after domain checks\"}\n",
        "  ],\n",
        "  \"public_round_schedule_shape_failure_families\": [\n",
        "    {\"code\": 0, \"name\": \"ok\", \"meaning\": \"valid public schedule-shape preflight\"},\n",
        "    {\"code\": 1, \"name\": \"path_domain\", \"meaning\": \"public path-buffer schedule domain failed first\"},\n",
        "    {\"code\": 2, \"name\": \"work_shape\", \"meaning\": \"public top-L work-shape envelope failed after path-domain checks\"}\n",
        "  ],\n",
        "  \"non_panicking_wrapper_failure_code_map\": [\n",
        "    {\"wrapper\": \"try_write_binary_children_from\", \"failure_family\": \"public_child_write_failure_codes\", \"status_field\": \"FixedSclBinaryChildWriteDomainCheck.failure_code\", \"work_count_field\": \"FixedSclBinaryChildWriteDomainCheck.child_slots_written\"},\n",
        "    {\"wrapper\": \"try_expand_then_compact_one_bit\", \"failure_family\": \"public_path_domain_failure_codes\", \"status_field\": \"FixedSclOneBitExpansionRun.path_domain_check.failure_code\", \"work_count_field\": \"FixedSclOneBitExpansionRun.work_counts\"},\n",
        "    {\"wrapper\": \"try_expand_then_compact_two_public_bits\", \"failure_family\": \"public_path_domain_failure_codes\", \"status_field\": \"FixedSclPublicRoundScheduleRun.path_domain_check.failure_code\", \"work_count_field\": \"FixedSclPublicRoundScheduleRun.work_counts\"},\n",
        "    {\"wrapper\": \"try_expand_then_compact_public_rounds\", \"failure_family\": \"public_path_domain_failure_codes\", \"status_field\": \"FixedSclPublicRoundScheduleRun.path_domain_check.failure_code\", \"work_count_field\": \"FixedSclPublicRoundScheduleRun.work_counts\"},\n",
        "    {\"wrapper\": \"try_fixed_scl_integer_metric_deltas\", \"failure_family\": \"integer_metric_domain_failure_codes\", \"status_field\": \"FixedSclIntegerMetricDeltaRun.domain_check.failure_code\", \"work_count_field\": \"none-single-round-delta\"},\n",
        "    {\"wrapper\": \"try_fixed_scl_integer_round_schedule\", \"failure_family\": \"integer_schedule_domain_failure_codes\", \"status_field\": \"FixedSclIntegerRoundScheduleBuild.domain_check.failure_code\", \"work_count_field\": \"FixedSclIntegerRoundScheduleBuild.round_slots_written\"},\n",
        "    {\"wrapper\": \"try_expand_then_compact_integer_round_schedule\", \"failure_family\": \"public_path_domain_failure_codes\", \"path_status_field\": \"FixedSclPathBufferIntegerScheduleRun.path_domain_check.failure_code\", \"integer_status_family\": \"integer_schedule_domain_failure_codes\", \"integer_status_field\": \"FixedSclPathBufferIntegerScheduleRun.domain_check.failure_code\", \"work_count_field\": \"FixedSclPathBufferIntegerScheduleRun.work_counts\"}\n",
        "  ],\n",
        "  \"prototype_building_blocks\": [\n",
        "    \"decode_scl_fixed_i64: active fixed-i64 validation entrypoint; not production constant-time; generated-code and timing audit pending\",\n",
        "    \"fixed_schedule_top_l_i64: source-level fixed schedule only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_schedule_top_l_selection_plan: execution-free top-L selection preflight for public width, list size, and compare-exchange count only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"FixedSclPathBuffer: fixed-capacity source-level slot buffer only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_binary_child_write_domain_check: public child-write domain validator for parent slot, destination capacity, and bit index before fixed-slot writes; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_child_write_parity_check: child-write run/preflight parity record that compares the non-panicking wrapper return check with an execution-free child-write preflight only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_write_binary_children_from: non-panicking child-write wrapper that skips fixed-slot writes on invalid public inputs; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"write_binary_children_from: integer child expansion into fixed slots only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"expand_then_compact_one_bit: one-bit expand then compact source-level prototype only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_expand_then_compact_one_bit: non-panicking one-bit expand then compact wrapper that returns public path-domain status; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_one_bit_run_plan_certificate: one-bit run/preflight plan certificate adapter for comparing source-level run status and work counts with execution-free one-bit preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_one_bit_shape_parity_check: one-bit run/preflight shape parity record that compares run-derived and execution-free one-bit certificates only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"expand_then_compact_two_public_bits: two-round public-bit loop source-level prototype only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_expand_then_compact_two_public_bits: non-panicking two-round public-bit helper that delegates to public schedule domain checks; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"two_public_bits_run_shape_certificate: two-public-bits run/preflight shape certificate adapter for comparing wrapper-specific source-level run status and work shape with execution-free public preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"two_public_bits_shape_parity_check: two-public-bits run/preflight shape parity record that reuses the public-round parity surface for the dedicated wrapper; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"FixedSclRound + expand_then_compact_public_rounds: public round schedule source-level prototype only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_expand_then_compact_public_rounds: non-panicking multi-round public schedule wrapper that returns public path-domain status; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_run_shape_certificate: public run-shape certificate adapter for comparing source-level run status and work counts with execution-free schedule-shape preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_shape_parity_check: public run/preflight shape parity record that compares run-derived and execution-free certificates only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_plan: execution-free FixedSclRound schedule preflight that extracts public bit indices and pairs path-domain status with public work counts only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_plan_certificate: FixedSclRound schedule/public preflight certificate adapter that extracts public bit-index shape only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_plan_parity_check: FixedSclRound schedule/public preflight parity record that compares round-derived public shape with explicit public bit-index preflight only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_shape_plan: execution-free FixedSclRound schedule-shape preflight that extracts public bit indices and pairs path-domain status with top-L work-shape envelopes only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_shape_plan_certificate: FixedSclRound schedule/public shape certificate adapter that extracts public bit-index shape and top-L envelopes only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_round_schedule_shape_parity_check: FixedSclRound schedule/public shape parity record that compares round-derived public top-L envelopes with explicit public bit-index shape preflight only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_schedule_plan: execution-free public schedule preflight that pairs path-domain status with public work counts only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_schedule_shape_plan: execution-free public schedule shape certificate that pairs path-domain status with first/repeated top-L preflights and public work counts only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_schedule_shape_failure_family: public schedule-shape failure-family classifier over public path/top-L envelope statuses only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_work_counts: public work-count audit for fixed SCL schedule parameters only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_work_counts_with_capacities: public work-count audit with separate first and repeated child capacities only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_public_round_work_shape_plan: execution-free public round work-shape plan that pairs first/repeated top-L preflights with public work counts only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_metric_domain_check: single-round integer metric domain validator for public hard-bit and non-negative magnitude inputs only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_metric_deltas: integer metric delta audit for hard-bit penalties and frozen branch forbidding only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_fixed_scl_integer_metric_deltas: non-panicking integer metric delta wrapper that returns terminal sentinels on invalid public metric inputs; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_schedule: public integer round schedule audit from hard-bit penalties into FixedSclRound arrays only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_schedule_domain_check: active integer schedule domain validator for hard-bit and non-negative magnitude inputs only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_schedule_build_plan: execution-free integer schedule-build preflight that pairs integer status with public round-slot write count only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_build_certificate: integer schedule-build run certificate adapter for comparing returned domain status and round-slot write count with execution-free build preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_build_parity_check: integer schedule-build run/preflight parity record that compares schedule-builder status and public round-slot write count only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_schedule_plan: execution-free integer schedule preflight that pairs integer status, path-domain status, and public work counts only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_schedule_shape_plan: execution-free integer schedule-shape preflight that pairs integer status, path-domain status, and public top-L work-shape envelopes only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_run_plan_certificate: integer run/preflight plan certificate adapter for comparing source-level run status and work counts with execution-free integer preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_round_run_shape_certificate: integer run/preflight shape certificate adapter for comparing source-level run status and top-L envelopes with execution-free integer shape preflight; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_shape_parity_check: integer run/preflight shape parity record that compares run-derived and execution-free integer certificates only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_schedule_shape_parity_check: integer schedule/run shape parity record that compares run-derived and execution-free integer top-L envelope certificates only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_integer_schedule_shape_failure_family: integer schedule-shape failure-family classifier over public integer/path/top-L envelope statuses only; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_fixed_scl_integer_round_schedule: non-panicking integer schedule builder that returns domain-check status before FixedSclRound arrays; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"fixed_scl_path_buffer_schedule_domain_check: public path-buffer shape validator for capacities and bit indices before expansion; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"try_expand_then_compact_integer_round_schedule: non-panicking path-buffer schedule wrapper that skips expansion on invalid integer inputs; not wired into decode_scl; generated-code and timing audit pending\",\n",
        "    \"expand_then_compact_integer_round_schedule: integer schedule source-level loop over fixed path buffers only; not wired into decode_scl; generated-code and timing audit pending\"\n",
        "  ],\n",
        "  \"public_work_count_examples\": [\n",
        "    {\n",
        "      \"label\": \"parent_capacity_2_child_capacity_4_list_size_2_rounds_3\",\n",
        "      \"parent_capacity\": 2,\n",
        "      \"child_capacity\": 4,\n",
        "      \"list_size\": 2,\n",
        "      \"rounds\": 3,\n",
        "      \"top_l_compare_exchanges\": 18,\n",
        "      \"child_slots_written\": 12,\n",
        "      \"compacted_slots_written\": 6,\n",
        "      \"source\": \"fixed_scl_public_round_work_counts(2, 4, 2, 3)\"\n",
        "    },\n",
        "    {\n",
        "      \"label\": \"parent_capacity_3_first_child_6_repeated_child_4_list_size_2_rounds_3\",\n",
        "      \"parent_capacity\": 3,\n",
        "      \"first_child_capacity\": 6,\n",
        "      \"repeated_child_capacity\": 4,\n",
        "      \"list_size\": 2,\n",
        "      \"rounds\": 3,\n",
        "      \"top_l_compare_exchanges\": 27,\n",
        "      \"child_slots_written\": 14,\n",
        "      \"compacted_slots_written\": 6,\n",
        "      \"source\": \"fixed_scl_public_round_work_counts_with_capacities(3, 6, 4, 2, 3)\"\n",
        "    },\n",
        "    {\n",
        "      \"label\": \"zero_rounds_no_expansion_work\",\n",
        "      \"parent_capacity\": 3,\n",
        "      \"first_child_capacity\": 6,\n",
        "      \"repeated_child_capacity\": 4,\n",
        "      \"list_size\": 2,\n",
        "      \"rounds\": 0,\n",
        "      \"top_l_compare_exchanges\": 0,\n",
        "      \"child_slots_written\": 0,\n",
        "      \"compacted_slots_written\": 0,\n",
        "      \"source\": \"fixed_scl_public_round_work_counts_with_capacities(3, 6, 4, 2, 0)\"\n",
        "    }\n",
        "  ],\n",
        "  \"required_action\": \"fixed-schedule integer decoder plan required before replacing ct-003\",\n",
        "  \"adjudication\": \"engineering audit artifact only; no production CT claim, no security claim, OPEN = LSN\"\n",
        "}\n",
    )
}

pub fn run_configs(configs: &[SimulationConfig]) -> Vec<SimulationResult> {
    configs
        .iter()
        .map(|cfg| simulate_bsc_sc(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed))
        .collect()
}

pub fn results_to_json(experiment: &str, results: &[SimulationResult]) -> String {
    results_to_json_with_decoder(experiment, "successive_cancellation_exact_llr", results)
}

pub fn results_to_json_with_decoder(
    experiment: &str,
    decoder: &str,
    results: &[SimulationResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str(&format!("  \"decoder\": \"{}\",\n", escape_json(decoder)));
    out.push_str("  \"frozen_set\": \"natural_order_bhattacharyya_z2i_bad_z2i1_good\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", result.n));
        out.push_str(&format!("      \"K\": {},\n", result.k));
        out.push_str(&format!("      \"p\": {:.10},\n", result.p));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"errors\": {},\n", result.errors));
        out.push_str(&format!("      \"bler\": {:.10},\n", result.bler()));
        if let Some(upper) = result.zero_error_upper_95() {
            out.push_str(&format!("      \"zero_error_upper_95\": {:.10},\n", upper));
        }
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn importance_results_to_json(
    experiment: &str,
    decoder: &str,
    results: &[ImportanceSamplingResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str(&format!("  \"decoder\": \"{}\",\n", escape_json(decoder)));
    out.push_str("  \"sampling\": \"tilted_bsc_proposal_reweighted_to_target_bsc\",\n");
    out.push_str("  \"frozen_set\": \"natural_order_bhattacharyya_z2i_bad_z2i1_good\",\n");
    out.push_str(
        "  \"adjudication\": \"P1b importance-sampling pilot; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", result.n));
        out.push_str(&format!("      \"K\": {},\n", result.k));
        out.push_str(&format!("      \"target_p\": {:.10},\n", result.target_p));
        out.push_str(&format!(
            "      \"proposal_p\": {:.10},\n",
            result.proposal_p
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!(
            "      \"proposal_errors\": {},\n",
            result.proposal_errors
        ));
        out.push_str(&format!(
            "      \"proposal_error_rate\": {:.10},\n",
            result.proposal_error_rate()
        ));
        out.push_str(&format!(
            "      \"weighted_bler_estimate\": {:.12e},\n",
            result.weighted_bler_estimate
        ));
        out.push_str(&format!(
            "      \"mean_likelihood_ratio\": {:.12e},\n",
            result.mean_likelihood_ratio
        ));
        out.push_str(&format!(
            "      \"effective_sample_size\": {:.6},\n",
            result.effective_sample_size
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn polar_rate_rows_to_json(
    experiment: &str,
    target_log2_half_sum_bound: f64,
    rows: &[PolarRateRow],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"bound_convention\": \"SC block-error bound uses 0.5 * sum selected Bhattacharyya Z_i; raw sum is also recorded\",\n");
    out.push_str(&format!(
        "  \"target_log2_half_sum_bound\": {:.6},\n",
        target_log2_half_sum_bound
    ));
    out.push_str("  \"adjudication\": \"engineering polar-rate sweep only; no closure, no break, OPEN = LSN\",\n");
    out.push_str("  \"rows\": [\n");
    for (i, row) in rows.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", row.n));
        out.push_str(&format!("      \"K\": {},\n", row.k));
        out.push_str(&format!("      \"p\": {:.10},\n", row.p));
        out.push_str(&format!("      \"rate\": {:.12},\n", row.rate));
        out.push_str(&format!(
            "      \"bhattacharyya_sum_bound\": {:.12e},\n",
            row.bhattacharyya_sum_bound
        ));
        out.push_str(&format!(
            "      \"half_sum_bound\": {:.12e},\n",
            row.half_sum_bound
        ));
        out.push_str(&format!(
            "      \"log2_bhattacharyya_sum_bound\": {:.6},\n",
            row.log2_bhattacharyya_sum_bound
        ));
        out.push_str(&format!(
            "      \"log2_half_sum_bound\": {:.6},\n",
            row.log2_half_sum_bound
        ));
        out.push_str(&format!(
            "      \"target_log2_half_sum_bound\": {:.6},\n",
            row.target_log2_half_sum_bound
        ));
        out.push_str(&format!(
            "      \"passes_half_sum_target\": {}\n",
            row.passes_half_sum_target
        ));
        out.push_str("    }");
        if i + 1 != rows.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

fn escape_json(value: &str) -> String {
    value
        .chars()
        .flat_map(|c| match c {
            '"' => "\\\"".chars().collect::<Vec<_>>(),
            '\\' => "\\\\".chars().collect::<Vec<_>>(),
            '\n' => "\\n".chars().collect::<Vec<_>>(),
            '\r' => "\\r".chars().collect::<Vec<_>>(),
            '\t' => "\\t".chars().collect::<Vec<_>>(),
            _ => vec![c],
        })
        .collect()
}

impl PolarCode {
    pub fn new(n: usize, k: usize, p: f64) -> Self {
        assert!(n.is_power_of_two(), "N must be a power of two");
        assert!(k <= n, "K must be <= N");
        assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

        let frozen = build_frozen_natural(n, k, p);
        let frozen_set = frozen.iter().copied().collect::<HashSet<_>>();
        let info_set = (0..n)
            .filter(|idx| !frozen_set.contains(idx))
            .collect::<Vec<_>>();
        let mut frozen_mask = vec![false; n];
        for &idx in &frozen {
            frozen_mask[idx] = true;
        }

        Self {
            n,
            k,
            p,
            frozen,
            info_set,
            frozen_mask,
        }
    }
}

pub fn build_frozen_natural(n: usize, k: usize, p: f64) -> Vec<usize> {
    assert!(n.is_power_of_two(), "N must be a power of two");
    assert!(k <= n, "K must be <= N");
    assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

    let z = bhattacharyya_reliabilities(n, p);
    let mut order = (0..n).collect::<Vec<_>>();
    order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));
    order[k..].to_vec()
}

pub fn bhattacharyya_reliabilities(n: usize, p: f64) -> Vec<f64> {
    assert!(n.is_power_of_two(), "N must be a power of two");
    assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

    let z0 = 2.0 * (p * (1.0 - p)).sqrt();
    let mut z = vec![z0];
    while z.len() < n {
        let mut next = vec![0.0; z.len() * 2];
        for (i, value) in z.iter().copied().enumerate() {
            next[2 * i] = 2.0 * value - value * value;
            next[2 * i + 1] = value * value;
        }
        z = next;
    }

    z
}

pub fn polar_rate_row(n: usize, k: usize, p: f64, target_log2_half_sum_bound: f64) -> PolarRateRow {
    assert!(k <= n, "K must be <= N");
    let z = bhattacharyya_reliabilities(n, p);
    let mut order = (0..n).collect::<Vec<_>>();
    order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));
    let bhattacharyya_sum_bound = order[..k].iter().map(|&idx| z[idx]).sum::<f64>();
    polar_rate_row_from_sum(n, k, p, target_log2_half_sum_bound, bhattacharyya_sum_bound)
}

pub fn sweep_polar_rate(
    n: usize,
    p_values: &[f64],
    k_start: usize,
    k_end: usize,
    k_step: usize,
    target_log2_half_sum_bound: f64,
) -> Vec<PolarRateRow> {
    assert!(k_step > 0, "K step must be positive");
    assert!(k_start <= k_end, "K start must be <= K end");
    assert!(k_end <= n, "K end must be <= N");

    let mut rows = Vec::new();
    for &p in p_values {
        let z = bhattacharyya_reliabilities(n, p);
        let mut order = (0..n).collect::<Vec<_>>();
        order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));

        let mut prefix = vec![0.0; n + 1];
        for (i, &idx) in order.iter().enumerate() {
            prefix[i + 1] = prefix[i] + z[idx];
        }

        let mut k = k_start;
        while k <= k_end {
            rows.push(polar_rate_row_from_sum(
                n,
                k,
                p,
                target_log2_half_sum_bound,
                prefix[k],
            ));
            match k.checked_add(k_step) {
                Some(next) => k = next,
                None => break,
            }
        }
    }
    rows
}

fn polar_rate_row_from_sum(
    n: usize,
    k: usize,
    p: f64,
    target_log2_half_sum_bound: f64,
    bhattacharyya_sum_bound: f64,
) -> PolarRateRow {
    let half_sum_bound = 0.5 * bhattacharyya_sum_bound;
    let log2_bhattacharyya_sum_bound = bhattacharyya_sum_bound.log2();
    let log2_half_sum_bound = half_sum_bound.log2();

    PolarRateRow {
        n,
        k,
        p,
        rate: k as f64 / n as f64,
        bhattacharyya_sum_bound,
        half_sum_bound,
        log2_bhattacharyya_sum_bound,
        log2_half_sum_bound,
        target_log2_half_sum_bound,
        passes_half_sum_target: log2_half_sum_bound <= target_log2_half_sum_bound,
    }
}

pub fn encode(code: &PolarCode, message: &[u8]) -> Vec<u8> {
    assert_eq!(message.len(), code.k, "message length must equal K");
    let mut u = vec![0u8; code.n];
    for (&idx, &bit) in code.info_set.iter().zip(message.iter()) {
        u[idx] = bit & 1;
    }
    polar_transform(&mut u);
    u
}

pub fn decode_successive_cancellation(code: &PolarCode, llr: &[f64]) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    let u_hat = sc_decode_node(llr, 0, &code.frozen_mask);
    code.info_set.iter().map(|&idx| u_hat[idx]).collect()
}

pub fn decode_scl(code: &PolarCode, llr: &[f64], list_size: usize) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    assert!(list_size > 0, "list size must be positive");
    let paths = scl_decode_node(llr, 0, &code.frozen_mask, list_size);
    let best = paths
        .first()
        .expect("SCL decoder must produce at least one path");
    code.info_set.iter().map(|&idx| best.bits[idx]).collect()
}

pub fn decode_scl_fast(code: &PolarCode, llr: &[f64], list_size: usize) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    assert!(list_size > 0, "list size must be positive");
    let mut paths = vec![SclPath {
        bits: vec![0; code.n],
        metric: 0.0,
    }];

    for phi in 0..code.n {
        let mut next_paths = Vec::with_capacity(paths.len() * 2);
        for path in &paths {
            let bit_llr = sc_bit_llr_minsum(llr, 0, phi, &path.bits);
            if code.frozen_mask[phi] {
                let mut bits = path.bits.clone();
                bits[phi] = 0;
                next_paths.push(SclPath {
                    bits,
                    metric: path.metric + bit_metric_minsum(bit_llr, 0),
                });
            } else {
                for bit in [0u8, 1u8] {
                    let mut bits = path.bits.clone();
                    bits[phi] = bit;
                    next_paths.push(SclPath {
                        bits,
                        metric: path.metric + bit_metric_minsum(bit_llr, bit),
                    });
                }
            }
        }
        prune_paths(&mut next_paths, list_size);
        paths = next_paths;
    }

    let best = paths.first().expect("fast SCL must keep at least one path");
    code.info_set.iter().map(|&idx| best.bits[idx]).collect()
}

pub fn decode_scl_fixed_i64<const N: usize, const L: usize, const CHILD_CAP: usize>(
    code: &PolarCode,
    llr: &[f64],
    metric_scale: f64,
) -> Vec<u8> {
    assert_eq!(code.n, N, "fixed SCL const N must match PolarCode N");
    assert_eq!(llr.len(), N, "LLR length must equal fixed SCL N");
    assert!(L > 0, "fixed SCL list size must be positive");
    assert!(
        CHILD_CAP >= L.saturating_mul(2),
        "fixed SCL child capacity must hold two children per path"
    );
    assert!(
        metric_scale.is_finite() && metric_scale > 0.0,
        "fixed SCL metric scale must be positive and finite"
    );

    let quantized_llr = quantize_llrs_i64::<N>(llr, metric_scale);
    let mut paths = FixedSclPathBuffer::<L, N>::new();
    paths.set_candidate(0, 0, [0; N]);
    let mut llr_scratch = [0i64; N];
    let mut partial_scratch = [0u8; N];

    for phi in 0..N {
        let mut children = FixedSclPathBuffer::<CHILD_CAP, N>::new();
        for parent_slot in 0..L {
            let bits = paths.bits(parent_slot);
            let bit_llr = sc_bit_llr_minsum_i64(
                &quantized_llr,
                0,
                phi,
                &bits,
                &mut llr_scratch,
                &mut partial_scratch,
            );
            let hard_bit = i64_negative_flag(bit_llr);
            let magnitude = llr_i64_metric_magnitude(bit_llr);
            let deltas =
                fixed_scl_integer_metric_deltas(code.frozen_mask[phi], hard_bit, magnitude);
            children.write_binary_children_from(
                &paths,
                parent_slot,
                parent_slot * 2,
                phi,
                deltas.bit0_metric_delta,
                deltas.bit1_metric_delta,
            );
        }
        let top = children.top_l_entries::<L>();
        paths = FixedSclPathBuffer::<L, N>::from_top_entries(&children, top);
    }

    let best_bits = paths.bits(0);
    code.info_set.iter().map(|&idx| best_bits[idx]).collect()
}

pub fn decode_scl_fixed_i64_l8_validation(code: &PolarCode, llr: &[f64]) -> Vec<u8> {
    match code.n {
        128 => decode_scl_fixed_i64::<128, 8, 16>(code, llr, FIXED_I64_VALIDATION_METRIC_SCALE),
        256 => decode_scl_fixed_i64::<256, 8, 16>(code, llr, FIXED_I64_VALIDATION_METRIC_SCALE),
        512 => decode_scl_fixed_i64::<512, 8, 16>(code, llr, FIXED_I64_VALIDATION_METRIC_SCALE),
        2048 => decode_scl_fixed_i64::<2048, 8, 16>(code, llr, FIXED_I64_VALIDATION_METRIC_SCALE),
        other => panic!("fixed-i64 L8 validation decode does not support N={other}"),
    }
}

fn i64_negative_flag(value: i64) -> u8 {
    ((value as u64) >> 63) as u8
}

fn llr_metric_magnitude_i64(llr: f64, metric_scale: f64) -> i64 {
    let cap = i64::MAX / 4;
    let scaled = (llr.abs() * metric_scale).round();
    let nonfinite = (!scaled.is_finite()) as i64;
    let too_large = (scaled >= cap as f64) as i64;
    let out_of_range = nonfinite | too_large;
    let range_mask = 0i64.wrapping_sub(out_of_range);
    let candidate = scaled as i64;

    select_i64(range_mask, candidate, cap)
}

fn quantize_llrs_i64<const N: usize>(llr: &[f64], metric_scale: f64) -> [i64; N] {
    assert_eq!(llr.len(), N, "fixed SCL LLR length must equal N");
    let mut quantized = [0i64; N];
    for (dst, &value) in quantized.iter_mut().zip(llr.iter()) {
        *dst = quantize_llr_i64(value, metric_scale);
    }
    quantized
}

fn quantize_llr_i64(llr: f64, metric_scale: f64) -> i64 {
    let magnitude = llr_metric_magnitude_i64(llr, metric_scale);
    let negative = (llr < 0.0) as i64;
    let sign_mask = 0i64.wrapping_sub(negative);

    select_i64(sign_mask, magnitude, magnitude.saturating_neg())
}

fn llr_i64_metric_magnitude(llr: i64) -> i64 {
    i64_abs_saturating(llr).min(i64::MAX / 4)
}

fn i64_abs_saturating(value: i64) -> i64 {
    value.saturating_abs()
}

pub fn simulate_bsc_sc(n: usize, k: usize, p: f64, trials: usize, seed: u64) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_successive_cancellation(&code, &llr);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl(&code, &llr, list_size);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fast(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl_fast(&code, &llr, list_size);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fixed_i64<const N: usize, const L: usize, const CHILD_CAP: usize>(
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    metric_scale: f64,
) -> SimulationResult {
    let code = PolarCode::new(N, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl_fixed_i64::<N, L, CHILD_CAP>(&code, &llr, metric_scale);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n: N,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fixed_i64_l8_validation(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl_fixed_i64_l8_validation(&code, &llr);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn compare_scl_fast_fixed_i64_decoded_bits<
    const N: usize,
    const L: usize,
    const CHILD_CAP: usize,
>(
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    metric_scale: f64,
) -> FixedI64DecoderAgreement {
    let code = PolarCode::new(N, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut decoded_mismatches = 0usize;
    let mut fast_errors = 0usize;
    let mut fixed_errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let fast_decoded = decode_scl_fast(&code, &llr, L);
        let fixed_decoded = decode_scl_fixed_i64::<N, L, CHILD_CAP>(&code, &llr, metric_scale);
        if fast_decoded != fixed_decoded {
            decoded_mismatches += 1;
        }
        if fast_decoded != message {
            fast_errors += 1;
        }
        if fixed_decoded != message {
            fixed_errors += 1;
        }
    }

    FixedI64DecoderAgreement {
        n: N,
        k,
        p,
        trials,
        decoded_mismatches,
        fast_errors,
        fixed_errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fast_importance(
    n: usize,
    k: usize,
    target_p: f64,
    proposal_p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> ImportanceSamplingResult {
    assert!(
        (0.0..0.5).contains(&target_p),
        "target_p must be in (0, 0.5)"
    );
    assert!(
        (0.0..0.5).contains(&proposal_p),
        "proposal_p must be in (0, 0.5)"
    );
    assert!(trials > 0, "trials must be positive");

    let code = PolarCode::new(n, k, target_p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - target_p) / target_p).ln();
    let llr1 = -llr0;
    let log_flip_weight = (target_p / proposal_p).ln();
    let log_clean_weight = ((1.0 - target_p) / (1.0 - proposal_p)).ln();
    let mut proposal_errors = 0usize;
    let mut weighted_error_sum = 0.0;
    let mut weight_sum = 0.0;
    let mut weight_square_sum = 0.0;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let mut flip_count = 0usize;
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < proposal_p;
                flip_count += usize::from(flipped);
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();

        let log_weight =
            flip_count as f64 * log_flip_weight + (n - flip_count) as f64 * log_clean_weight;
        let weight = log_weight.exp();
        weight_sum += weight;
        weight_square_sum += weight * weight;

        let decoded = decode_scl_fast(&code, &llr, list_size);
        if decoded != message {
            proposal_errors += 1;
            weighted_error_sum += weight;
        }
    }

    let effective_sample_size = if weight_square_sum == 0.0 {
        0.0
    } else {
        weight_sum * weight_sum / weight_square_sum
    };

    ImportanceSamplingResult {
        n,
        k,
        target_p,
        proposal_p,
        trials,
        proposal_errors,
        weighted_bler_estimate: weighted_error_sum / trials as f64,
        mean_likelihood_ratio: weight_sum / trials as f64,
        effective_sample_size,
        seed,
    }
}

fn polar_transform(bits: &mut [u8]) {
    let n = bits.len();
    let mut half = 1usize;
    while half < n {
        let step = half * 2;
        for block in (0..n).step_by(step) {
            for i in 0..half {
                bits[block + i] ^= bits[block + half + i];
            }
        }
        half = step;
    }
}

fn sc_decode_node(llr: &[f64], offset: usize, frozen_mask: &[bool]) -> Vec<u8> {
    if llr.len() == 1 {
        let bit = if frozen_mask[offset] || llr[0] >= 0.0 {
            0
        } else {
            1
        };
        return vec![bit];
    }

    let half = llr.len() / 2;
    let mut left_llr = vec![0.0; half];
    for i in 0..half {
        left_llr[i] = f_llr(llr[i], llr[half + i]);
    }
    let left = sc_decode_node(&left_llr, offset, frozen_mask);
    let mut left_partial = left.clone();
    polar_transform(&mut left_partial);

    let mut right_llr = vec![0.0; half];
    for i in 0..half {
        right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
    }
    let right = sc_decode_node(&right_llr, offset + half, frozen_mask);

    [left, right].concat()
}

#[derive(Clone, Debug)]
struct SclPath {
    bits: Vec<u8>,
    metric: f64,
}

fn scl_decode_node(
    llr: &[f64],
    offset: usize,
    frozen_mask: &[bool],
    list_size: usize,
) -> Vec<SclPath> {
    if llr.len() == 1 {
        if frozen_mask[offset] {
            return vec![SclPath {
                bits: vec![0],
                metric: bit_metric(llr[0], 0),
            }];
        }

        let mut paths = vec![
            SclPath {
                bits: vec![0],
                metric: bit_metric(llr[0], 0),
            },
            SclPath {
                bits: vec![1],
                metric: bit_metric(llr[0], 1),
            },
        ];
        prune_paths(&mut paths, list_size);
        return paths;
    }

    let half = llr.len() / 2;
    let mut left_llr = vec![0.0; half];
    for i in 0..half {
        left_llr[i] = f_llr(llr[i], llr[half + i]);
    }

    let left_paths = scl_decode_node(&left_llr, offset, frozen_mask, list_size);
    let mut combined = Vec::new();
    for left in left_paths {
        let mut left_partial = left.bits.clone();
        polar_transform(&mut left_partial);

        let mut right_llr = vec![0.0; half];
        for i in 0..half {
            right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
        }

        let right_paths = scl_decode_node(&right_llr, offset + half, frozen_mask, list_size);
        for right in right_paths {
            let mut bits = Vec::with_capacity(llr.len());
            bits.extend_from_slice(&left.bits);
            bits.extend_from_slice(&right.bits);
            combined.push(SclPath {
                bits,
                metric: left.metric + right.metric,
            });
        }
    }

    prune_paths(&mut combined, list_size);
    combined
}

fn prune_paths(paths: &mut Vec<SclPath>, list_size: usize) {
    paths.sort_by(|a, b| a.metric.total_cmp(&b.metric));
    paths.truncate(list_size);
}

fn bit_metric(llr: f64, bit: u8) -> f64 {
    let signed = if bit == 0 { llr } else { -llr };
    if signed >= 0.0 {
        (1.0 + (-signed).exp()).ln()
    } else {
        -signed + (1.0 + signed.exp()).ln()
    }
}

fn bit_metric_minsum(llr: f64, bit: u8) -> f64 {
    let agrees_with_hard_decision = (llr >= 0.0 && bit == 0) || (llr < 0.0 && bit == 1);
    if agrees_with_hard_decision {
        0.0
    } else {
        llr.abs()
    }
}

fn sc_bit_llr_minsum(llr: &[f64], offset: usize, phi: usize, decisions: &[u8]) -> f64 {
    if llr.len() == 1 {
        return llr[0];
    }

    let half = llr.len() / 2;
    if phi < offset + half {
        let mut left_llr = vec![0.0; half];
        for i in 0..half {
            left_llr[i] = f_llr_minsum(llr[i], llr[half + i]);
        }
        sc_bit_llr_minsum(&left_llr, offset, phi, decisions)
    } else {
        let mut left_partial = decisions[offset..offset + half].to_vec();
        polar_transform(&mut left_partial);

        let mut right_llr = vec![0.0; half];
        for i in 0..half {
            right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
        }
        sc_bit_llr_minsum(&right_llr, offset + half, phi, decisions)
    }
}

fn sc_bit_llr_minsum_i64(
    llr: &[i64],
    offset: usize,
    phi: usize,
    decisions: &[u8],
    llr_scratch: &mut [i64],
    partial_scratch: &mut [u8],
) -> i64 {
    if llr.len() == 1 {
        return llr[0];
    }

    let half = llr.len() / 2;
    if phi < offset + half {
        let (left_llr, rest_llr_scratch) = llr_scratch.split_at_mut(half);
        for i in 0..half {
            left_llr[i] = f_llr_minsum_i64(llr[i], llr[half + i]);
        }
        sc_bit_llr_minsum_i64(
            left_llr,
            offset,
            phi,
            decisions,
            rest_llr_scratch,
            partial_scratch,
        )
    } else {
        let (right_llr, rest_llr_scratch) = llr_scratch.split_at_mut(half);
        let (left_partial, rest_partial_scratch) = partial_scratch.split_at_mut(half);
        left_partial.copy_from_slice(&decisions[offset..offset + half]);
        polar_transform(left_partial);

        for i in 0..half {
            right_llr[i] = g_llr_i64(llr[i], llr[half + i], left_partial[i]);
        }
        sc_bit_llr_minsum_i64(
            right_llr,
            offset + half,
            phi,
            decisions,
            rest_llr_scratch,
            rest_partial_scratch,
        )
    }
}

fn f_llr(a: f64, b: f64) -> f64 {
    let sign = if (a < 0.0) ^ (b < 0.0) { -1.0 } else { 1.0 };
    let min_abs = a.abs().min(b.abs());
    let correction = (1.0 + (-(a + b).abs()).exp()).ln() - (1.0 + (-(a - b).abs()).exp()).ln();
    sign * min_abs + correction
}

fn f_llr_minsum(a: f64, b: f64) -> f64 {
    let sign = if (a < 0.0) ^ (b < 0.0) { -1.0 } else { 1.0 };
    sign * a.abs().min(b.abs())
}

fn f_llr_minsum_i64(a: i64, b: i64) -> i64 {
    let min_abs = i64_abs_saturating(a).min(i64_abs_saturating(b));
    let sign = i64_negative_flag(a) ^ i64_negative_flag(b);
    let sign_mask = 0i64.wrapping_sub(i64::from(sign));

    select_i64(sign_mask, min_abs, min_abs.saturating_neg())
}

fn g_llr(a: f64, b: f64, u: u8) -> f64 {
    if u == 0 {
        b + a
    } else {
        b - a
    }
}

fn g_llr_i64(a: i64, b: i64, u: u8) -> i64 {
    let add = b.saturating_add(a);
    let sub = b.saturating_sub(a);
    let bit = u & 1;
    let bit_mask = 0i64.wrapping_sub(i64::from(bit));

    select_i64(bit_mask, add, sub)
}

#[derive(Clone, Debug)]
struct Lcg64 {
    state: u64,
}

impl Lcg64 {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    fn next_u64(&mut self) -> u64 {
        self.state = self
            .state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.state
    }

    fn next_bool(&mut self) -> bool {
        (self.next_u64() >> 63) != 0
    }

    fn next_f64(&mut self) -> f64 {
        const SCALE: f64 = 1.0 / ((1u64 << 53) as f64);
        ((self.next_u64() >> 11) as f64) * SCALE
    }
}
