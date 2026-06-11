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

use std::{env, fs, process::Command};

use lsn_ref::{
    ToyKemParams, ToyPublicPreflightScanConfig, toy_public_wrong_secret_preflight_scan,
    toy_public_wrong_secret_preflight_scan_to_json,
};

#[test]
fn public_preflight_scan_finds_small_random_sample_negative_control() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };
    let report = toy_public_wrong_secret_preflight_scan(ToyPublicPreflightScanConfig {
        params,
        honest_secret_seed: 0xA11CE,
        sample_seed_start: 0x5EED,
        sample_seed_trials: 1,
        wrong_secret_seed_start: 0xA11CF,
        wrong_secret_seed_trials: 1,
        noise_seed: 0xC0DE,
        encaps_seed: 0xBEEF,
    });

    assert!(report.found_fixture);
    assert_eq!(report.attempts, 1);
    assert_eq!(report.found_sample_seed, Some(0x5EED));
    assert_eq!(report.found_wrong_secret_seed, Some(0xA11CF));

    let json = toy_public_wrong_secret_preflight_scan_to_json(
        "codex-lsn-ref-public-preflight-smoke",
        "n2-public-smoke",
        &report,
    );
    assert!(json.contains("\"selection_mode\": \"random-public-samples\""));
    assert!(json.contains("\"found_fixture\": true"));
    assert!(json.contains("\"diagnostic_only\": false"));
}

#[test]
fn public_preflight_cli_writes_and_checks_paper_r7_report() {
    let bin = env::var("CARGO_BIN_EXE_lsn_public_preflight")
        .expect("Cargo should expose the lsn_public_preflight test binary path");
    let path = env::temp_dir().join(format!(
        "lsn_ref_public_preflight_{}.json",
        std::process::id()
    ));

    let write = Command::new(&bin)
        .args(["--profile", "n2-paper-r7-public-preflight", "--output"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_public_preflight writer");
    assert!(write.success());

    let json = fs::read_to_string(&path).expect("failed to read generated preflight report");
    assert!(json.contains("\"profile\": \"n2-paper-r7-public-preflight\""));
    assert!(json.contains("\"selection_mode\": \"random-public-samples\""));
    assert!(json.contains("\"diagnostic_only\": false"));
    assert!(json.contains("\"polar_N\": 2048"));

    let check = Command::new(&bin)
        .args(["--profile", "n2-paper-r7-public-preflight", "--check"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_public_preflight checker");
    assert!(check.success());
}
