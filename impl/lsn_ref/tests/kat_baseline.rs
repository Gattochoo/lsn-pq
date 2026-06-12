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

use lsn_ref::{
    DiagnosticHonestOnlyMask, FixedLagrangian, FixedLagrangianError,
    LSN_REF_FIXED_LAGRANGIAN_WORDS, LSN_REF_MAX_FIXED_LAGRANGIAN_N, ToyKemParams,
    diagnostic_honest_only_point_masks, diagnostic_honest_only_points,
    toy_divergent_wrong_secret_control, toy_find_wrong_secret_control, toy_kat_vector,
    toy_wrong_secret_control, toy_wrong_secret_control_to_json,
    toy_wrong_secret_control_to_json_with_diagnostics,
};

#[test]
fn fixed_lagrangian_membership_matches_point_set_for_public_points() {
    let points = [0, 6, 9, 15];
    let fixed = FixedLagrangian::from_points(2, &points);

    assert_eq!(fixed.n(), 2);
    assert_eq!(fixed.universe(), 16);
    assert_eq!(fixed.word_count(), 1);

    for point in 0..16 {
        let expected = points.contains(&point);
        assert_eq!(fixed.contains_u8(point), u8::from(expected));
        assert_eq!(
            fixed.contains_mask(point),
            if expected { u64::MAX } else { 0 }
        );
    }

    assert_eq!(fixed.contains_mask(16), 0);
    assert_eq!(fixed.contains_u8(16), 0);
}

#[test]
fn fixed_lagrangian_mask_membership_handles_word_boundaries() {
    let points = [
        0, 1, 2, 3, 63, 64, 65, 66, 127, 128, 129, 130, 191, 192, 193, 255,
    ];
    let fixed = FixedLagrangian::from_points(4, &points);

    assert_eq!(fixed.universe(), 256);
    assert_eq!(fixed.word_count(), 4);

    for point in 0..256 {
        let expected = points.contains(&point);
        assert_eq!(
            fixed.contains_mask(point),
            if expected { u64::MAX } else { 0 }
        );
        assert_eq!(fixed.contains_u8(point), u8::from(expected));
    }

    assert_eq!(fixed.contains_mask(256), 0);
    assert_eq!(fixed.contains_u8(256), 0);
}

#[test]
fn fixed_lagrangian_membership_labels_use_mask_path() {
    let fixed = FixedLagrangian::from_points(2, &[0, 6, 9, 15]);
    let query_points = [0, 1, 6, 8, 9, 15, 16];

    assert_eq!(
        fixed.membership_labels(&query_points),
        vec![1, 0, 1, 0, 1, 1, 0]
    );
}

#[test]
fn fixed_lagrangian_membership_labels_into_fills_existing_buffer() {
    let fixed = FixedLagrangian::from_points(2, &[0, 6, 9, 15]);
    let query_points = [15, 14, 9, 6, 0];
    let mut labels = [9u8; 5];

    fixed.membership_labels_into(&query_points, &mut labels);

    assert_eq!(labels, [1, 0, 1, 1, 1]);
}

#[test]
fn fixed_lagrangian_uses_fixed_max_word_storage() {
    assert_eq!(LSN_REF_FIXED_LAGRANGIAN_WORDS, 1024);

    let n2 = FixedLagrangian::from_points(2, &[0, 6, 9, 15]);
    let n4 = FixedLagrangian::from_points(
        4,
        &[
            0, 1, 2, 3, 63, 64, 65, 66, 127, 128, 129, 130, 191, 192, 193, 255,
        ],
    );

    assert_eq!(n2.word_count(), 1);
    assert_eq!(n4.word_count(), 4);
    assert_eq!(n2.storage_word_count(), LSN_REF_FIXED_LAGRANGIAN_WORDS);
    assert_eq!(n4.storage_word_count(), LSN_REF_FIXED_LAGRANGIAN_WORDS);
}

#[test]
fn fixed_lagrangian_source_avoids_secret_dependent_word_indexing() {
    let source = include_str!("../src/lib.rs");

    assert!(!source.contains("self.words[index >> 6]"));
    assert!(!source.contains("words[index >> 6]"));
    assert!(!source.contains(
        "if index >= universe {\n                return Err(FixedLagrangianError::PointOutOfRange"
    ));
    assert!(source.contains("words: [u64; LSN_REF_FIXED_LAGRANGIAN_WORDS]"));
    assert!(!source.contains("contains_mask_scanned"));
    assert!(!source.contains("contains_u8_scanned"));
    assert!(source.contains("PointCountMismatch"));
}

#[test]
fn toy_public_sample_source_takes_fixed_lagrangian_boundary() {
    let source = include_str!("../src/lib.rs");

    assert!(source.contains(
        "fn public_samples(\n    params: ToyKemParams,\n    fixed_secret: &FixedLagrangian,"
    ));
    assert!(
        !source.contains("fn public_samples(\n    params: ToyKemParams,\n    secret: &Lagrangian,")
    );
}

#[test]
fn toy_kat_parts_source_takes_fixed_lagrangian_boundary() {
    let source = include_str!("../src/lib.rs");

    assert!(source.contains("    fixed_secret: &FixedLagrangian,\n) -> ToyKatVector {"));
    assert!(!source.contains("    secret: &Lagrangian,\n) -> ToyKatVector {"));
}

#[test]
fn fixed_lagrangian_try_from_points_rejects_out_of_layout_inputs() {
    assert_eq!(LSN_REF_MAX_FIXED_LAGRANGIAN_N, 8);
    assert_eq!(
        FixedLagrangian::try_from_points(LSN_REF_MAX_FIXED_LAGRANGIAN_N + 1, &[]),
        Err(FixedLagrangianError::NTooLarge {
            n: LSN_REF_MAX_FIXED_LAGRANGIAN_N + 1,
            max_n: LSN_REF_MAX_FIXED_LAGRANGIAN_N,
        })
    );
    assert_eq!(
        FixedLagrangian::try_from_points(2, &[0, 6, 9]),
        Err(FixedLagrangianError::PointCountMismatch {
            n: 2,
            expected: 4,
            actual: 3,
        })
    );
    assert_eq!(
        FixedLagrangian::try_from_points(2, &[0, 6, 9, 16]),
        Err(FixedLagrangianError::PointOutOfRange {
            n: 2,
            point: 16,
            universe: 16,
        })
    );
    assert!(FixedLagrangian::try_from_points(2, &[0, 6, 9, 15]).is_ok());
}

#[test]
fn diagnostic_honest_only_points_uses_fixed_wrong_secret_boundary() {
    let honest_points = [0, 6, 9, 15];
    let wrong_secret = FixedLagrangian::from_points(2, &[0, 2, 12, 14]);

    let honest_only = diagnostic_honest_only_points(&honest_points, &wrong_secret);

    assert_eq!(honest_only, vec![6, 9, 15]);
}

#[test]
fn diagnostic_honest_only_point_masks_keep_fixed_shape_boundary() {
    let honest_points = [0, 6, 9, 15];
    let wrong_secret = FixedLagrangian::from_points(2, &[0, 2, 12, 14]);

    let masks = diagnostic_honest_only_point_masks(&honest_points, &wrong_secret);

    assert_eq!(
        masks,
        vec![
            DiagnosticHonestOnlyMask {
                point: 0,
                include_mask: 0
            },
            DiagnosticHonestOnlyMask {
                point: 6,
                include_mask: u64::MAX
            },
            DiagnosticHonestOnlyMask {
                point: 9,
                include_mask: u64::MAX
            },
            DiagnosticHonestOnlyMask {
                point: 15,
                include_mask: u64::MAX
            },
        ]
    );
}

#[test]
fn toy_kat_vector_roundtrips_with_zero_noise() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let kat = toy_kat_vector(params, 0xA11CE, 0x5EED, 0xC0DE, 0xBEEF);

    assert_eq!(kat.encapsulated_key_hex, kat.decapsulated_key_hex);
    assert_eq!(kat.ciphertext_syndrome_bits.len(), params.polar_n);
    assert_eq!(kat.message_bits.len(), params.polar_k);
}

#[test]
fn toy_kat_vector_detects_wrong_secret_negative_control() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let control = toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF);

    assert_eq!(
        control.honest.encapsulated_key_hex,
        control.honest.decapsulated_key_hex
    );
    assert_ne!(
        control.honest.encapsulated_key_hex,
        control.wrong_secret_decapsulated_key_hex
    );
    assert!(!control.wrong_secret_roundtrip_ok);
}

#[test]
fn toy_wrong_secret_control_json_records_both_outcomes() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };
    let control = toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF);
    let json = toy_wrong_secret_control_to_json("codex-lsn-ref-toy-kat", &control);

    assert!(json.contains("\"roundtrip_ok\": true"));
    assert!(json.contains("\"wrong_secret_roundtrip_ok\": false"));
    assert!(json.contains("\"status\": \"toy reference KAT scaffold"));
}

#[test]
fn toy_find_wrong_secret_control_finds_n3_fixture() {
    let params = ToyKemParams {
        n: 3,
        sample_count: 256,
        repetition: 3,
        polar_n: 32,
        polar_k: 16,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let control =
        toy_find_wrong_secret_control(params, 0xA11CE, 0xA2000, 1024, 0x5EED, 0xC0DE, 0xBEEF)
            .expect("expected an n=3 wrong-secret fixture in the bounded seed window");

    assert_eq!(control.honest.params.n, 3);
    assert_eq!(
        control.honest.encapsulated_key_hex,
        control.honest.decapsulated_key_hex
    );
    assert!(!control.wrong_secret_roundtrip_ok);
}

#[test]
fn divergent_wrong_secret_control_forces_clean_majority_separation() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 48,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let control = toy_divergent_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0xC0DE, 0xBEEF)
        .expect("expected an honest-only divergent toy fixture");

    assert_eq!(
        control.honest.selected_indices.len(),
        params.polar_n * params.repetition
    );
    assert!(
        control
            .honest
            .clean_majority_bits
            .iter()
            .all(|&bit| bit == 1)
    );
    assert!(
        control
            .wrong_secret_clean_majority_bits
            .iter()
            .all(|&bit| bit == 0)
    );
    assert_eq!(
        control.honest.encapsulated_key_hex,
        control.honest.decapsulated_key_hex
    );
    assert_ne!(
        control.honest.encapsulated_key_hex,
        control.wrong_secret_decapsulated_key_hex
    );
    assert!(!control.wrong_secret_roundtrip_ok);
}

#[test]
fn divergent_wrong_secret_control_json_self_labels_as_diagnostic() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 48,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let control = toy_divergent_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0xC0DE, 0xBEEF)
        .expect("expected an honest-only divergent toy fixture");
    let json = toy_wrong_secret_control_to_json_with_diagnostics(
        "codex-lsn-ref-n2-paper-r7-divergent-kat",
        &control,
        "divergent-wrong-secret-diagnostic",
        "diagnostic selector uses honest-only points; not a public-distribution KAT",
    );

    assert!(json.contains("\"selection_mode\": \"divergent-wrong-secret-diagnostic\""));
    assert!(json.contains("\"diagnostic_only\": true"));
    assert!(json.contains(
        "\"diagnostic_note\": \"diagnostic selector uses honest-only points; not a public-distribution KAT\""
    ));
    assert!(json.contains("\"roundtrip_ok\": true"));
    assert!(json.contains("\"wrong_secret_roundtrip_ok\": false"));
}
