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

//! Experimental LSN reference-implementation scaffolding.
//!
//! This crate is intentionally not a production constant-time implementation yet.

use lsn_cryptanalysis::{Lagrangian, XorShift64, random_lagrangian};
use polar_validation::{PolarCode, decode_scl_fast, encode};

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ToyKemParams {
    pub n: usize,
    pub sample_count: usize,
    pub repetition: usize,
    pub polar_n: usize,
    pub polar_k: usize,
    pub public_noise_rate: f64,
    pub decoder_design_p: f64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ToyKatVector {
    pub params: ToyKemParams,
    pub secret_seed: u64,
    pub sample_seed: u64,
    pub noise_seed: u64,
    pub encaps_seed: u64,
    pub secret_lagrangian_points: Vec<u32>,
    pub public_points: Vec<u32>,
    pub public_labels: Vec<u8>,
    pub selected_indices: Vec<usize>,
    pub message_bits: Vec<u8>,
    pub public_majority_bits: Vec<u8>,
    pub clean_majority_bits: Vec<u8>,
    pub ciphertext_syndrome_bits: Vec<u8>,
    pub decoded_message_bits: Vec<u8>,
    pub encapsulated_key_hex: String,
    pub decapsulated_key_hex: String,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ToyWrongSecretControl {
    pub honest: ToyKatVector,
    pub wrong_secret_seed: u64,
    pub wrong_secret_lagrangian_points: Vec<u32>,
    pub wrong_secret_clean_majority_bits: Vec<u8>,
    pub wrong_secret_decoded_message_bits: Vec<u8>,
    pub wrong_secret_decapsulated_key_hex: String,
    pub wrong_secret_roundtrip_ok: bool,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ToyPublicPreflightScanConfig {
    pub params: ToyKemParams,
    pub honest_secret_seed: u64,
    pub sample_seed_start: u64,
    pub sample_seed_trials: usize,
    pub wrong_secret_seed_start: u64,
    pub wrong_secret_seed_trials: usize,
    pub noise_seed: u64,
    pub encaps_seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ToyPublicPreflightScanReport {
    pub config: ToyPublicPreflightScanConfig,
    pub attempts: usize,
    pub found_fixture: bool,
    pub found_sample_seed: Option<u64>,
    pub found_wrong_secret_seed: Option<u64>,
}

pub const LSN_REF_MAX_FIXED_LAGRANGIAN_N: usize = 8;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FixedLagrangianError {
    NTooLarge {
        n: usize,
        max_n: usize,
    },
    PointOutOfRange {
        n: usize,
        point: u32,
        universe: usize,
    },
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FixedLagrangian {
    n: usize,
    universe: usize,
    words: Vec<u64>,
}

impl FixedLagrangian {
    pub fn from_lagrangian(n: usize, lagrangian: &Lagrangian) -> Self {
        let points = lagrangian.iter().copied().collect::<Vec<_>>();
        Self::from_points(n, &points)
    }

    pub fn from_points(n: usize, points: &[u32]) -> Self {
        Self::try_from_points(n, points).expect("invalid fixed Lagrangian layout")
    }

    pub fn try_from_points(n: usize, points: &[u32]) -> Result<Self, FixedLagrangianError> {
        if n > LSN_REF_MAX_FIXED_LAGRANGIAN_N {
            return Err(FixedLagrangianError::NTooLarge {
                n,
                max_n: LSN_REF_MAX_FIXED_LAGRANGIAN_N,
            });
        }

        let total_dim = 2 * n;
        let universe = 1usize << total_dim;
        let mut words = vec![0u64; universe.div_ceil(64)];
        for &point in points {
            let index = point as usize;
            if index >= universe {
                return Err(FixedLagrangianError::PointOutOfRange { n, point, universe });
            }
            words[index >> 6] |= 1u64 << (index & 63);
        }

        Ok(Self { n, universe, words })
    }

    pub fn n(&self) -> usize {
        self.n
    }

    pub fn universe(&self) -> usize {
        self.universe
    }

    pub fn word_count(&self) -> usize {
        self.words.len()
    }

    pub fn contains_mask(&self, point: u32) -> u64 {
        let index = point as usize;
        if index >= self.universe {
            return 0;
        }

        let bit = (self.words[index >> 6] >> (index & 63)) & 1;
        0u64.wrapping_sub(bit)
    }

    pub fn contains_mask_scanned(&self, point: u32) -> u64 {
        let index = point as usize;
        let target_word_index = index >> 6;
        let bit_index = index & 63;
        let in_range_mask = 0u64.wrapping_sub((index < self.universe) as u64);
        let mut selected_word = 0u64;

        for (word_index, &word) in self.words.iter().enumerate() {
            let word_mask = 0u64.wrapping_sub((word_index == target_word_index) as u64);
            selected_word |= word & word_mask;
        }

        let bit = (selected_word >> bit_index) & 1;
        0u64.wrapping_sub(bit) & in_range_mask
    }

    pub fn contains_u8(&self, point: u32) -> u8 {
        (self.contains_mask(point) & 1) as u8
    }

    pub fn contains_u8_scanned(&self, point: u32) -> u8 {
        (self.contains_mask_scanned(point) & 1) as u8
    }
}

pub fn diagnostic_honest_only_points(
    honest_points: &[u32],
    wrong_secret: &FixedLagrangian,
) -> Vec<u32> {
    honest_points
        .iter()
        .copied()
        .filter(|&point| wrong_secret.contains_u8_scanned(point) == 0)
        .collect()
}

pub fn toy_kat_vector(
    params: ToyKemParams,
    secret_seed: u64,
    sample_seed: u64,
    noise_seed: u64,
    encaps_seed: u64,
) -> ToyKatVector {
    validate_params(params);

    let mut secret_rng = XorShift64::new(secret_seed);
    let secret = random_lagrangian(params.n, 16 * params.n.max(1), &mut secret_rng);
    let fixed_secret = FixedLagrangian::from_lagrangian(params.n, &secret);
    let secret_lagrangian_points = secret.iter().copied().collect::<Vec<_>>();

    let (public_points, public_labels) = public_samples(params, &secret, sample_seed, noise_seed);
    let selected_indices = selected_indices(
        params.sample_count,
        params.polar_n * params.repetition,
        encaps_seed,
    );

    let message_bits = bits_from_seed(params.polar_k, encaps_seed ^ 0xA5A5_5A5A_D3C1_B2E0);
    let code = PolarCode::new(params.polar_n, params.polar_k, params.decoder_design_p);
    let codeword = encode(&code, &message_bits);

    let public_majority_bits =
        block_majorities(&selected_indices, &public_labels, params.repetition);
    let clean_membership_labels = public_points
        .iter()
        .map(|&point| fixed_secret.contains_u8_scanned(point))
        .collect::<Vec<_>>();
    let clean_majority_bits = block_majorities(
        &selected_indices,
        &clean_membership_labels,
        params.repetition,
    );

    let ciphertext_syndrome_bits = xor_bits(&public_majority_bits, &codeword);
    let received_codeword = xor_bits(&ciphertext_syndrome_bits, &clean_majority_bits);
    let decoded_message_bits = decode_codeword_bits(&code, &received_codeword);

    let encapsulated_key_hex = toy_key_hex(encaps_seed, &message_bits, &ciphertext_syndrome_bits);
    let decapsulated_key_hex = toy_key_hex(
        encaps_seed,
        &decoded_message_bits,
        &ciphertext_syndrome_bits,
    );

    ToyKatVector {
        params,
        secret_seed,
        sample_seed,
        noise_seed,
        encaps_seed,
        secret_lagrangian_points,
        public_points,
        public_labels,
        selected_indices,
        message_bits,
        public_majority_bits,
        clean_majority_bits,
        ciphertext_syndrome_bits,
        decoded_message_bits,
        encapsulated_key_hex,
        decapsulated_key_hex,
    }
}

pub fn toy_wrong_secret_control(
    params: ToyKemParams,
    honest_secret_seed: u64,
    wrong_secret_seed: u64,
    sample_seed: u64,
    noise_seed: u64,
    encaps_seed: u64,
) -> ToyWrongSecretControl {
    let honest = toy_kat_vector(
        params,
        honest_secret_seed,
        sample_seed,
        noise_seed,
        encaps_seed,
    );
    let mut wrong_secret_rng = XorShift64::new(wrong_secret_seed);
    let wrong_secret = random_lagrangian(params.n, 16 * params.n.max(1), &mut wrong_secret_rng);
    let fixed_wrong_secret = FixedLagrangian::from_lagrangian(params.n, &wrong_secret);
    let wrong_secret_lagrangian_points = wrong_secret.iter().copied().collect::<Vec<_>>();
    let wrong_secret_labels = honest
        .public_points
        .iter()
        .map(|&point| fixed_wrong_secret.contains_u8_scanned(point))
        .collect::<Vec<_>>();
    let wrong_secret_clean_majority_bits = block_majorities(
        &honest.selected_indices,
        &wrong_secret_labels,
        params.repetition,
    );
    let wrong_secret_received_codeword = xor_bits(
        &honest.ciphertext_syndrome_bits,
        &wrong_secret_clean_majority_bits,
    );
    let code = PolarCode::new(params.polar_n, params.polar_k, params.decoder_design_p);
    let wrong_secret_decoded_message_bits =
        decode_codeword_bits(&code, &wrong_secret_received_codeword);
    let wrong_secret_decapsulated_key_hex = toy_key_hex(
        encaps_seed,
        &wrong_secret_decoded_message_bits,
        &honest.ciphertext_syndrome_bits,
    );
    let wrong_secret_roundtrip_ok =
        honest.encapsulated_key_hex == wrong_secret_decapsulated_key_hex;

    ToyWrongSecretControl {
        honest,
        wrong_secret_seed,
        wrong_secret_lagrangian_points,
        wrong_secret_clean_majority_bits,
        wrong_secret_decoded_message_bits,
        wrong_secret_decapsulated_key_hex,
        wrong_secret_roundtrip_ok,
    }
}

pub fn toy_divergent_wrong_secret_control(
    params: ToyKemParams,
    honest_secret_seed: u64,
    wrong_secret_seed: u64,
    noise_seed: u64,
    encaps_seed: u64,
) -> Option<ToyWrongSecretControl> {
    validate_params(params);

    let mut honest_secret_rng = XorShift64::new(honest_secret_seed);
    let honest_secret = random_lagrangian(params.n, 16 * params.n.max(1), &mut honest_secret_rng);
    let mut wrong_secret_rng = XorShift64::new(wrong_secret_seed);
    let wrong_secret = random_lagrangian(params.n, 16 * params.n.max(1), &mut wrong_secret_rng);
    let fixed_wrong_secret = FixedLagrangian::from_lagrangian(params.n, &wrong_secret);
    let honest_secret_points = honest_secret.iter().copied().collect::<Vec<_>>();
    let honest_only_points =
        diagnostic_honest_only_points(&honest_secret_points, &fixed_wrong_secret);
    if honest_only_points.is_empty() {
        return None;
    }

    let selected_count = params.polar_n * params.repetition;
    let mut noise_rng = XorShift64::new(noise_seed);
    let mut public_points = Vec::with_capacity(selected_count);
    let mut public_labels = Vec::with_capacity(selected_count);
    for i in 0..selected_count {
        let point = honest_only_points[i % honest_only_points.len()];
        let noisy = noise_rng.next_f64() < params.public_noise_rate;
        public_points.push(point);
        public_labels.push(u8::from(!noisy));
    }
    let selected_indices = (0..selected_count).collect::<Vec<_>>();

    let honest = toy_kat_from_parts(
        params,
        honest_secret_seed,
        0,
        noise_seed,
        encaps_seed,
        honest_secret_points,
        public_points,
        public_labels,
        selected_indices,
        &honest_secret,
    );

    let wrong_secret_lagrangian_points = wrong_secret.iter().copied().collect::<Vec<_>>();
    let wrong_secret_labels = honest
        .public_points
        .iter()
        .map(|&point| fixed_wrong_secret.contains_u8_scanned(point))
        .collect::<Vec<_>>();
    let wrong_secret_clean_majority_bits = block_majorities(
        &honest.selected_indices,
        &wrong_secret_labels,
        params.repetition,
    );
    let wrong_secret_received_codeword = xor_bits(
        &honest.ciphertext_syndrome_bits,
        &wrong_secret_clean_majority_bits,
    );
    let code = PolarCode::new(params.polar_n, params.polar_k, params.decoder_design_p);
    let wrong_secret_decoded_message_bits =
        decode_codeword_bits(&code, &wrong_secret_received_codeword);
    let wrong_secret_decapsulated_key_hex = toy_key_hex(
        encaps_seed,
        &wrong_secret_decoded_message_bits,
        &honest.ciphertext_syndrome_bits,
    );
    let wrong_secret_roundtrip_ok =
        honest.encapsulated_key_hex == wrong_secret_decapsulated_key_hex;
    let honest_roundtrip_ok = honest.encapsulated_key_hex == honest.decapsulated_key_hex;
    if !honest_roundtrip_ok || wrong_secret_roundtrip_ok {
        return None;
    }

    Some(ToyWrongSecretControl {
        honest,
        wrong_secret_seed,
        wrong_secret_lagrangian_points,
        wrong_secret_clean_majority_bits,
        wrong_secret_decoded_message_bits,
        wrong_secret_decapsulated_key_hex,
        wrong_secret_roundtrip_ok,
    })
}

pub fn toy_find_wrong_secret_control(
    params: ToyKemParams,
    honest_secret_seed: u64,
    wrong_secret_seed_start: u64,
    wrong_secret_seed_trials: usize,
    sample_seed: u64,
    noise_seed: u64,
    encaps_seed: u64,
) -> Option<ToyWrongSecretControl> {
    for offset in 0..wrong_secret_seed_trials {
        let wrong_secret_seed = wrong_secret_seed_start.wrapping_add(offset as u64);
        let control = toy_wrong_secret_control(
            params,
            honest_secret_seed,
            wrong_secret_seed,
            sample_seed,
            noise_seed,
            encaps_seed,
        );
        let honest_roundtrip_ok =
            control.honest.encapsulated_key_hex == control.honest.decapsulated_key_hex;
        if honest_roundtrip_ok && !control.wrong_secret_roundtrip_ok {
            return Some(control);
        }
    }
    None
}

pub fn toy_public_wrong_secret_preflight_scan(
    config: ToyPublicPreflightScanConfig,
) -> ToyPublicPreflightScanReport {
    validate_params(config.params);
    assert!(
        config.sample_seed_trials > 0,
        "sample_seed_trials must be positive"
    );
    assert!(
        config.wrong_secret_seed_trials > 0,
        "wrong_secret_seed_trials must be positive"
    );

    let mut attempts = 0usize;
    for sample_offset in 0..config.sample_seed_trials {
        let sample_seed = config.sample_seed_start.wrapping_add(sample_offset as u64);
        for wrong_offset in 0..config.wrong_secret_seed_trials {
            let wrong_secret_seed = config
                .wrong_secret_seed_start
                .wrapping_add(wrong_offset as u64);
            attempts += 1;
            let control = toy_wrong_secret_control(
                config.params,
                config.honest_secret_seed,
                wrong_secret_seed,
                sample_seed,
                config.noise_seed,
                config.encaps_seed,
            );
            let honest_roundtrip_ok =
                control.honest.encapsulated_key_hex == control.honest.decapsulated_key_hex;
            if honest_roundtrip_ok && !control.wrong_secret_roundtrip_ok {
                return ToyPublicPreflightScanReport {
                    config,
                    attempts,
                    found_fixture: true,
                    found_sample_seed: Some(sample_seed),
                    found_wrong_secret_seed: Some(wrong_secret_seed),
                };
            }
        }
    }

    ToyPublicPreflightScanReport {
        config,
        attempts,
        found_fixture: false,
        found_sample_seed: None,
        found_wrong_secret_seed: None,
    }
}

fn toy_kat_from_parts(
    params: ToyKemParams,
    secret_seed: u64,
    sample_seed: u64,
    noise_seed: u64,
    encaps_seed: u64,
    secret_lagrangian_points: Vec<u32>,
    public_points: Vec<u32>,
    public_labels: Vec<u8>,
    selected_indices: Vec<usize>,
    secret: &Lagrangian,
) -> ToyKatVector {
    let message_bits = bits_from_seed(params.polar_k, encaps_seed ^ 0xA5A5_5A5A_D3C1_B2E0);
    let code = PolarCode::new(params.polar_n, params.polar_k, params.decoder_design_p);
    let codeword = encode(&code, &message_bits);
    let public_majority_bits =
        block_majorities(&selected_indices, &public_labels, params.repetition);
    let fixed_secret = FixedLagrangian::from_lagrangian(params.n, secret);
    let clean_membership_labels = public_points
        .iter()
        .map(|&point| fixed_secret.contains_u8_scanned(point))
        .collect::<Vec<_>>();
    let clean_majority_bits = block_majorities(
        &selected_indices,
        &clean_membership_labels,
        params.repetition,
    );

    let ciphertext_syndrome_bits = xor_bits(&public_majority_bits, &codeword);
    let received_codeword = xor_bits(&ciphertext_syndrome_bits, &clean_majority_bits);
    let decoded_message_bits = decode_codeword_bits(&code, &received_codeword);
    let encapsulated_key_hex = toy_key_hex(encaps_seed, &message_bits, &ciphertext_syndrome_bits);
    let decapsulated_key_hex = toy_key_hex(
        encaps_seed,
        &decoded_message_bits,
        &ciphertext_syndrome_bits,
    );

    ToyKatVector {
        params,
        secret_seed,
        sample_seed,
        noise_seed,
        encaps_seed,
        secret_lagrangian_points,
        public_points,
        public_labels,
        selected_indices,
        message_bits,
        public_majority_bits,
        clean_majority_bits,
        ciphertext_syndrome_bits,
        decoded_message_bits,
        encapsulated_key_hex,
        decapsulated_key_hex,
    }
}

pub fn toy_kat_to_json(experiment: &str, kat: &ToyKatVector) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"status\": \"toy reference KAT scaffold; not production constant-time; no security claim\",\n");
    out.push_str("  \"params\": {\n");
    out.push_str(&format!("    \"n\": {},\n", kat.params.n));
    out.push_str(&format!(
        "    \"sample_count\": {},\n",
        kat.params.sample_count
    ));
    out.push_str(&format!("    \"repetition\": {},\n", kat.params.repetition));
    out.push_str(&format!("    \"polar_N\": {},\n", kat.params.polar_n));
    out.push_str(&format!("    \"polar_K\": {},\n", kat.params.polar_k));
    out.push_str(&format!(
        "    \"public_noise_rate\": {:.10},\n",
        kat.params.public_noise_rate
    ));
    out.push_str(&format!(
        "    \"decoder_design_p\": {:.10}\n",
        kat.params.decoder_design_p
    ));
    out.push_str("  },\n");
    out.push_str("  \"seeds\": {\n");
    out.push_str(&format!("    \"secret_seed\": {},\n", kat.secret_seed));
    out.push_str(&format!("    \"sample_seed\": {},\n", kat.sample_seed));
    out.push_str(&format!("    \"noise_seed\": {},\n", kat.noise_seed));
    out.push_str(&format!("    \"encaps_seed\": {}\n", kat.encaps_seed));
    out.push_str("  },\n");
    out.push_str(&format!(
        "  \"secret_lagrangian_points\": {},\n",
        u32_array_json(&kat.secret_lagrangian_points)
    ));
    out.push_str(&format!(
        "  \"public_points\": {},\n",
        u32_array_json(&kat.public_points)
    ));
    out.push_str(&format!(
        "  \"public_labels\": {},\n",
        u8_array_json(&kat.public_labels)
    ));
    out.push_str(&format!(
        "  \"selected_indices\": {},\n",
        usize_array_json(&kat.selected_indices)
    ));
    out.push_str(&format!(
        "  \"message_bits\": {},\n",
        u8_array_json(&kat.message_bits)
    ));
    out.push_str(&format!(
        "  \"public_majority_bits\": {},\n",
        u8_array_json(&kat.public_majority_bits)
    ));
    out.push_str(&format!(
        "  \"clean_majority_bits\": {},\n",
        u8_array_json(&kat.clean_majority_bits)
    ));
    out.push_str(&format!(
        "  \"ciphertext_syndrome_bits\": {},\n",
        u8_array_json(&kat.ciphertext_syndrome_bits)
    ));
    out.push_str(&format!(
        "  \"decoded_message_bits\": {},\n",
        u8_array_json(&kat.decoded_message_bits)
    ));
    out.push_str(&format!(
        "  \"encapsulated_key_hex\": \"{}\",\n",
        kat.encapsulated_key_hex
    ));
    out.push_str(&format!(
        "  \"decapsulated_key_hex\": \"{}\",\n",
        kat.decapsulated_key_hex
    ));
    out.push_str(&format!(
        "  \"roundtrip_ok\": {}\n",
        kat.encapsulated_key_hex == kat.decapsulated_key_hex
    ));
    out.push_str("}\n");
    out
}

pub fn toy_wrong_secret_control_to_json(
    experiment: &str,
    control: &ToyWrongSecretControl,
) -> String {
    toy_wrong_secret_control_to_json_inner(experiment, control, None)
}

pub fn toy_wrong_secret_control_to_json_with_diagnostics(
    experiment: &str,
    control: &ToyWrongSecretControl,
    selection_mode: &str,
    diagnostic_note: &str,
) -> String {
    toy_wrong_secret_control_to_json_inner(
        experiment,
        control,
        Some(ToyWrongSecretJsonMetadata::Diagnostic {
            selection_mode,
            diagnostic_note,
        }),
    )
}

pub fn toy_wrong_secret_control_to_json_with_public_selection(
    experiment: &str,
    control: &ToyWrongSecretControl,
    selection_mode: &str,
) -> String {
    toy_wrong_secret_control_to_json_inner(
        experiment,
        control,
        Some(ToyWrongSecretJsonMetadata::PublicSelection { selection_mode }),
    )
}

pub fn constant_time_inventory_json() -> &'static str {
    concat!(
        "{\n",
        "  \"experiment\": \"codex-lsn-ref-ct-inventory\",\n",
        "  \"status\": \"constant-time discipline inventory only; current code is toy/reference scaffolding; no security claim\",\n",
        "  \"verdict\": \"not_constant_time_reference\",\n",
        "  \"production_constant_time_claim\": false,\n",
        "  \"threat_model\": \"local timing/cache observer of encapsulation or decapsulation; public parameters and public samples are visible; Lagrangian membership, selected secret state, decoder paths, message bits, and noise bits are secret until explicitly serialized for KAT diagnostics\",\n",
        "  \"scope\": [\n",
        "    \"impl/lsn_ref toy LSN-KEM KAT rail\",\n",
        "    \"impl/polar_validation SC/SCL decoder used by the toy KAT rail\"\n",
        "  ],\n",
        "  \"inventory\": [\n",
        "    {\n",
        "      \"id\": \"ct-001\",\n",
        "      \"surface\": \"Lagrangian membership representation\",\n",
        "      \"classification\": \"partial_fixed_layout_scaffold_not_production_ct\",\n",
        "      \"issue\": \"FixedLagrangian bitset scaffold now uses scanned mask lookup for toy membership label generation and an explicit bounded reference layout via LSN_REF_MAX_FIXED_LAGRANGIAN_N, but secret construction, diagnostic selectors, and leakage audit remain non-production\",\n",
        "      \"required_action\": \"replace remaining set-style construction and diagnostic membership, replace the bounded reference layout with a reviewed production-sized layout, check generated code for data-oblivious access, and run an independent timing/leakage audit before any production claim\"\n",
        "    },\n",
        "    {\n",
        "      \"id\": \"ct-002\",\n",
        "      \"surface\": \"public-sample selection and toy divergent diagnostic selector\",\n",
        "      \"classification\": \"diagnostic_only_not_public_distribution\",\n",
        "      \"issue\": \"diagnostic selector depends on the wrong secret, is intentionally outside the public LSN distribution, and is isolated behind an explicit diagnostic_honest_only_points boundary\",\n",
        "      \"required_action\": \"keep divergent diagnostics out of production APIs and use random-public-samples profiles for public-distribution KAT plumbing\"\n",
        "    },\n",
        "    {\n",
        "      \"id\": \"ct-003\",\n",
        "      \"surface\": \"polar SCL decoder\",\n",
        "      \"classification\": \"not_constant_time\",\n",
        "      \"issue\": \"polar SCL path pruning uses data-dependent metrics, sorting, branching, heap-like vector growth, and floating-point operations\",\n",
        "      \"required_action\": \"replace with fixed-list, fixed-schedule, integer or masked metric updates and data-oblivious selection\"\n",
        "    },\n",
        "    {\n",
        "      \"id\": \"ct-004\",\n",
        "      \"surface\": \"toy RNG and key derivation\",\n",
        "      \"classification\": \"toy_only_not_cryptographic\",\n",
        "      \"issue\": \"XorShift/LCG randomness and toy hash lanes are deterministic test scaffolding, not production cryptographic primitives\",\n",
        "      \"required_action\": \"replace with an approved DRBG/KDF and define serialization, domain separation, and failure handling\"\n",
        "    },\n",
        "    {\n",
        "      \"id\": \"ct-005\",\n",
        "      \"surface\": \"KAT JSON serialization\",\n",
        "      \"classification\": \"test_artifact_only\",\n",
        "      \"issue\": \"KATs intentionally serialize secrets, public samples, labels, selected indices, and wrong-secret controls\",\n",
        "      \"required_action\": \"keep KAT serialization outside production APIs and gate it behind explicit test-only tooling\"\n",
        "    }\n",
        "  ],\n",
        "  \"next_required_work\": [\n",
        "    \"fixed-layout Lagrangian representation\",\n",
        "    \"constant-time membership and symplectic operations\",\n",
        "    \"data-oblivious polar decoder schedule\",\n",
        "    \"public-distribution KAT selection rule\",\n",
        "    \"independent timing/leakage audit after implementation\"\n",
        "  ]\n",
        "}\n",
    )
}

pub fn toy_public_wrong_secret_preflight_scan_to_json(
    experiment: &str,
    profile: &str,
    report: &ToyPublicPreflightScanReport,
) -> String {
    let verdict = if report.found_fixture {
        "found_public_random_sample_negative_control"
    } else {
        "no_public_random_sample_negative_control_in_bounded_scan"
    };
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str(&format!("  \"profile\": \"{}\",\n", escape_json(profile)));
    out.push_str("  \"status\": \"bounded public-selection preflight scan; not production constant-time; no security claim\",\n");
    out.push_str(&format!("  \"verdict\": \"{}\",\n", verdict));
    out.push_str("  \"selection_mode\": \"random-public-samples\",\n");
    out.push_str("  \"diagnostic_only\": false,\n");
    out.push_str(&format!("  \"found_fixture\": {},\n", report.found_fixture));
    out.push_str(&format!("  \"attempts\": {},\n", report.attempts));
    out.push_str("  \"params\": {\n");
    out.push_str(&format!("    \"n\": {},\n", report.config.params.n));
    out.push_str(&format!(
        "    \"sample_count\": {},\n",
        report.config.params.sample_count
    ));
    out.push_str(&format!(
        "    \"repetition\": {},\n",
        report.config.params.repetition
    ));
    out.push_str(&format!(
        "    \"polar_N\": {},\n",
        report.config.params.polar_n
    ));
    out.push_str(&format!(
        "    \"polar_K\": {},\n",
        report.config.params.polar_k
    ));
    out.push_str(&format!(
        "    \"public_noise_rate\": {:.10},\n",
        report.config.params.public_noise_rate
    ));
    out.push_str(&format!(
        "    \"decoder_design_p\": {:.10}\n",
        report.config.params.decoder_design_p
    ));
    out.push_str("  },\n");
    out.push_str("  \"seeds\": {\n");
    out.push_str(&format!(
        "    \"honest_secret_seed\": {},\n",
        report.config.honest_secret_seed
    ));
    out.push_str(&format!(
        "    \"sample_seed_start\": {},\n",
        report.config.sample_seed_start
    ));
    out.push_str(&format!(
        "    \"sample_seed_trials\": {},\n",
        report.config.sample_seed_trials
    ));
    out.push_str(&format!(
        "    \"wrong_secret_seed_start\": {},\n",
        report.config.wrong_secret_seed_start
    ));
    out.push_str(&format!(
        "    \"wrong_secret_seed_trials\": {},\n",
        report.config.wrong_secret_seed_trials
    ));
    out.push_str(&format!(
        "    \"noise_seed\": {},\n",
        report.config.noise_seed
    ));
    out.push_str(&format!(
        "    \"encaps_seed\": {}\n",
        report.config.encaps_seed
    ));
    out.push_str("  },\n");
    out.push_str(&format!(
        "  \"found_sample_seed\": {},\n",
        u64_option_json(report.found_sample_seed)
    ));
    out.push_str(&format!(
        "  \"found_wrong_secret_seed\": {}\n",
        u64_option_json(report.found_wrong_secret_seed)
    ));
    out.push_str("}\n");
    out
}

enum ToyWrongSecretJsonMetadata<'a> {
    PublicSelection {
        selection_mode: &'a str,
    },
    Diagnostic {
        selection_mode: &'a str,
        diagnostic_note: &'a str,
    },
}

fn toy_wrong_secret_control_to_json_inner(
    experiment: &str,
    control: &ToyWrongSecretControl,
    metadata: Option<ToyWrongSecretJsonMetadata<'_>>,
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"status\": \"toy reference KAT scaffold; not production constant-time; no security claim\",\n");
    out.push_str("  \"negative_control\": \"same public key and ciphertext, decapsulated with a wrong Lagrangian secret\",\n");
    if let Some(metadata) = metadata {
        match metadata {
            ToyWrongSecretJsonMetadata::PublicSelection { selection_mode } => {
                out.push_str(&format!(
                    "  \"selection_mode\": \"{}\",\n",
                    escape_json(selection_mode)
                ));
                out.push_str("  \"diagnostic_only\": false,\n");
            }
            ToyWrongSecretJsonMetadata::Diagnostic {
                selection_mode,
                diagnostic_note,
            } => {
                out.push_str(&format!(
                    "  \"selection_mode\": \"{}\",\n",
                    escape_json(selection_mode)
                ));
                out.push_str("  \"diagnostic_only\": true,\n");
                out.push_str(&format!(
                    "  \"diagnostic_note\": \"{}\",\n",
                    escape_json(diagnostic_note)
                ));
            }
        }
    }
    out.push_str(&format!(
        "  \"roundtrip_ok\": {},\n",
        control.honest.encapsulated_key_hex == control.honest.decapsulated_key_hex
    ));
    out.push_str(&format!(
        "  \"wrong_secret_roundtrip_ok\": {},\n",
        control.wrong_secret_roundtrip_ok
    ));
    out.push_str("  \"params\": {\n");
    out.push_str(&format!("    \"n\": {},\n", control.honest.params.n));
    out.push_str(&format!(
        "    \"sample_count\": {},\n",
        control.honest.params.sample_count
    ));
    out.push_str(&format!(
        "    \"repetition\": {},\n",
        control.honest.params.repetition
    ));
    out.push_str(&format!(
        "    \"polar_N\": {},\n",
        control.honest.params.polar_n
    ));
    out.push_str(&format!(
        "    \"polar_K\": {},\n",
        control.honest.params.polar_k
    ));
    out.push_str(&format!(
        "    \"public_noise_rate\": {:.10},\n",
        control.honest.params.public_noise_rate
    ));
    out.push_str(&format!(
        "    \"decoder_design_p\": {:.10}\n",
        control.honest.params.decoder_design_p
    ));
    out.push_str("  },\n");
    out.push_str("  \"seeds\": {\n");
    out.push_str(&format!(
        "    \"honest_secret_seed\": {},\n",
        control.honest.secret_seed
    ));
    out.push_str(&format!(
        "    \"wrong_secret_seed\": {},\n",
        control.wrong_secret_seed
    ));
    out.push_str(&format!(
        "    \"sample_seed\": {},\n",
        control.honest.sample_seed
    ));
    out.push_str(&format!(
        "    \"noise_seed\": {},\n",
        control.honest.noise_seed
    ));
    out.push_str(&format!(
        "    \"encaps_seed\": {}\n",
        control.honest.encaps_seed
    ));
    out.push_str("  },\n");
    out.push_str(&format!(
        "  \"honest_secret_lagrangian_points\": {},\n",
        u32_array_json(&control.honest.secret_lagrangian_points)
    ));
    out.push_str(&format!(
        "  \"wrong_secret_lagrangian_points\": {},\n",
        u32_array_json(&control.wrong_secret_lagrangian_points)
    ));
    out.push_str(&format!(
        "  \"public_points\": {},\n",
        u32_array_json(&control.honest.public_points)
    ));
    out.push_str(&format!(
        "  \"public_labels\": {},\n",
        u8_array_json(&control.honest.public_labels)
    ));
    out.push_str(&format!(
        "  \"selected_indices\": {},\n",
        usize_array_json(&control.honest.selected_indices)
    ));
    out.push_str(&format!(
        "  \"message_bits\": {},\n",
        u8_array_json(&control.honest.message_bits)
    ));
    out.push_str(&format!(
        "  \"ciphertext_syndrome_bits\": {},\n",
        u8_array_json(&control.honest.ciphertext_syndrome_bits)
    ));
    out.push_str(&format!(
        "  \"decoded_message_bits\": {},\n",
        u8_array_json(&control.honest.decoded_message_bits)
    ));
    out.push_str(&format!(
        "  \"wrong_secret_decoded_message_bits\": {},\n",
        u8_array_json(&control.wrong_secret_decoded_message_bits)
    ));
    out.push_str(&format!(
        "  \"encapsulated_key_hex\": \"{}\",\n",
        control.honest.encapsulated_key_hex
    ));
    out.push_str(&format!(
        "  \"decapsulated_key_hex\": \"{}\",\n",
        control.honest.decapsulated_key_hex
    ));
    out.push_str(&format!(
        "  \"wrong_secret_decapsulated_key_hex\": \"{}\"\n",
        control.wrong_secret_decapsulated_key_hex
    ));
    out.push_str("}\n");
    out
}

fn validate_params(params: ToyKemParams) {
    assert!(params.n > 0, "n must be positive");
    assert!(
        2 * params.n <= 32,
        "toy bitmask model supports dimension at most 32"
    );
    assert!(params.sample_count > 0, "sample_count must be positive");
    assert!(params.repetition > 0, "repetition must be positive");
    assert!(params.repetition % 2 == 1, "repetition must be odd");
    assert!(
        params.polar_n.is_power_of_two(),
        "polar_N must be a power of two"
    );
    assert!(
        params.polar_k <= params.polar_n,
        "polar_K must be <= polar_N"
    );
    assert!(
        params.polar_n * params.repetition <= params.sample_count,
        "sample_count must cover polar_N * repetition"
    );
    assert!(
        (0.0..=0.5).contains(&params.public_noise_rate),
        "public_noise_rate must be in [0, 0.5]"
    );
    assert!(
        (0.0..0.5).contains(&params.decoder_design_p),
        "decoder_design_p must be in (0, 0.5)"
    );
}

fn public_samples(
    params: ToyKemParams,
    secret: &Lagrangian,
    sample_seed: u64,
    noise_seed: u64,
) -> (Vec<u32>, Vec<u8>) {
    let total_dim = 2 * params.n;
    let universe = 1usize << total_dim;
    let mut sample_rng = XorShift64::new(sample_seed);
    let mut noise_rng = XorShift64::new(noise_seed);
    let fixed_secret = FixedLagrangian::from_lagrangian(params.n, secret);
    let mut points = Vec::with_capacity(params.sample_count);
    let mut labels = Vec::with_capacity(params.sample_count);

    for _ in 0..params.sample_count {
        let point = sample_rng.next_index(universe) as u32;
        let noisy = noise_rng.next_f64() < params.public_noise_rate;
        points.push(point);
        labels.push(fixed_secret.contains_u8_scanned(point) ^ u8::from(noisy));
    }

    (points, labels)
}

fn selected_indices(sample_count: usize, selected_count: usize, seed: u64) -> Vec<usize> {
    assert!(selected_count <= sample_count);
    let mut rng = XorShift64::new(seed ^ 0xC17C_0DEC_F00D_1234);
    let mut indices = (0..sample_count).collect::<Vec<_>>();
    for i in 0..selected_count {
        let j = i + rng.next_index(sample_count - i);
        indices.swap(i, j);
    }
    indices.truncate(selected_count);
    indices
}

fn bits_from_seed(len: usize, seed: u64) -> Vec<u8> {
    let mut rng = XorShift64::new(seed);
    (0..len).map(|_| u8::from(rng.next_bool())).collect()
}

fn block_majorities(selected_indices: &[usize], labels: &[u8], repetition: usize) -> Vec<u8> {
    selected_indices
        .chunks_exact(repetition)
        .map(|chunk| {
            let ones = chunk.iter().filter(|&&idx| labels[idx] == 1).count();
            u8::from(ones * 2 > repetition)
        })
        .collect()
}

fn xor_bits(left: &[u8], right: &[u8]) -> Vec<u8> {
    assert_eq!(
        left.len(),
        right.len(),
        "bit vectors must have equal length"
    );
    left.iter()
        .zip(right.iter())
        .map(|(&a, &b)| (a ^ b) & 1)
        .collect()
}

fn decode_codeword_bits(code: &PolarCode, bits: &[u8]) -> Vec<u8> {
    let llr0 = ((1.0 - code.p) / code.p).ln();
    let llr = bits
        .iter()
        .map(|&bit| if bit == 0 { llr0 } else { -llr0 })
        .collect::<Vec<_>>();
    decode_scl_fast(code, &llr, 8)
}

fn toy_key_hex(encaps_seed: u64, message_bits: &[u8], syndrome_bits: &[u8]) -> String {
    let mut lanes = [
        0x243F_6A88_85A3_08D3u64 ^ encaps_seed,
        0x1319_8A2E_0370_7344u64,
        0xA409_3822_299F_31D0u64,
        0x082E_FA98_EC4E_6C89u64,
    ];
    absorb_u64(&mut lanes, encaps_seed);
    absorb_bits(&mut lanes, message_bits);
    absorb_bits(&mut lanes, syndrome_bits);

    let mut out = String::with_capacity(64);
    for lane in lanes {
        out.push_str(&format!("{:016x}", finalize_lane(lane)));
    }
    out
}

fn absorb_bits(lanes: &mut [u64; 4], bits: &[u8]) {
    absorb_u64(lanes, bits.len() as u64);
    for (i, &bit) in bits.iter().enumerate() {
        let word = ((i as u64) << 1) ^ u64::from(bit & 1);
        absorb_u64(lanes, word);
    }
}

fn absorb_u64(lanes: &mut [u64; 4], word: u64) {
    for (i, lane) in lanes.iter_mut().enumerate() {
        *lane ^= word.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15));
        *lane = finalize_lane(*lane);
    }
}

fn finalize_lane(mut x: u64) -> u64 {
    x ^= x >> 30;
    x = x.wrapping_mul(0xBF58_476D_1CE4_E5B9);
    x ^= x >> 27;
    x = x.wrapping_mul(0x94D0_49BB_1331_11EB);
    x ^ (x >> 31)
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

fn u8_array_json(values: &[u8]) -> String {
    let body = values
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(", ");
    format!("[{}]", body)
}

fn u32_array_json(values: &[u32]) -> String {
    let body = values
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(", ");
    format!("[{}]", body)
}

fn usize_array_json(values: &[usize]) -> String {
    let body = values
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(", ");
    format!("[{}]", body)
}

fn u64_option_json(value: Option<u64>) -> String {
    value.map_or_else(|| String::from("null"), |value| value.to_string())
}
