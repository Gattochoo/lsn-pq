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

use std::{fs, path::PathBuf, process::Command};

fn kat_bin() -> &'static str {
    env!("CARGO_BIN_EXE_lsn_toy_kat")
}

fn temp_fixture_path(name: &str) -> PathBuf {
    let mut path = std::env::temp_dir();
    path.push(format!("lsn_ref_{name}_{}.json", std::process::id()));
    path
}

#[test]
fn cli_check_accepts_matching_n3_fixture() {
    let path = temp_fixture_path("matching_n3");

    let generate_status = Command::new(kat_bin())
        .args(["--profile", "n3-search", "--output"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_toy_kat generator");
    assert!(generate_status.success());

    let check_status = Command::new(kat_bin())
        .args(["--profile", "n3-search", "--check"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_toy_kat checker");
    assert!(check_status.success());

    let _ = fs::remove_file(path);
}

#[test]
fn cli_generates_noisy_n2_fixture_with_negative_control() {
    let path = temp_fixture_path("noisy_n2");

    let generate_status = Command::new(kat_bin())
        .args(["--profile", "n2-noisy", "--output"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_toy_kat generator");
    assert!(generate_status.success());

    let json = fs::read_to_string(&path).expect("failed to read generated noisy fixture");
    assert!(json.contains("\"public_noise_rate\": 0.2500000000"));
    assert!(json.contains("\"roundtrip_ok\": true"));
    assert!(json.contains("\"wrong_secret_roundtrip_ok\": false"));

    let check_status = Command::new(kat_bin())
        .args(["--profile", "n2-noisy", "--check"])
        .arg(&path)
        .status()
        .expect("failed to run lsn_toy_kat checker");
    assert!(check_status.success());

    let _ = fs::remove_file(path);
}

#[test]
fn cli_check_rejects_mismatched_fixture_negative_control() {
    let path = temp_fixture_path("mismatched_n3");
    fs::write(&path, "{ \"experiment\": \"wrong fixture\" }\n")
        .expect("failed to write mismatched fixture");

    let output = Command::new(kat_bin())
        .args(["--profile", "n3-search", "--check"])
        .arg(&path)
        .output()
        .expect("failed to run lsn_toy_kat checker");

    assert!(!output.status.success());
    assert!(
        String::from_utf8_lossy(&output.stderr).contains("KAT check failed"),
        "stderr did not explain mismatch: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let _ = fs::remove_file(path);
}
