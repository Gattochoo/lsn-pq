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
    ToyKemParams, toy_divergent_wrong_secret_control, toy_find_wrong_secret_control,
    toy_kat_vector, toy_wrong_secret_control, toy_wrong_secret_control_to_json,
};

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
