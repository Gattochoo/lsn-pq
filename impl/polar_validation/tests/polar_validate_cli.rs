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

fn validate_bin() -> &'static str {
    env!("CARGO_BIN_EXE_polar-validate")
}

fn temp_fixture_path(name: &str) -> PathBuf {
    let mut path = std::env::temp_dir();
    path.push(format!("polar_validate_{name}_{}.json", std::process::id()));
    path
}

#[test]
fn cli_writes_fixed_i64_baseline_fixture() {
    let path = temp_fixture_path("fixed_i64");

    let output = Command::new(validate_bin())
        .args([
            "--decoder",
            "fixed-i64",
            "--suite",
            "baseline",
            "--trials",
            "1",
            "--seed",
            "5397",
            "--output",
        ])
        .arg(&path)
        .output()
        .expect("failed to run polar-validate fixed-i64 generator");

    assert!(
        output.status.success(),
        "fixed-i64 generator failed: stdout={} stderr={}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );

    let json = fs::read_to_string(&path).expect("failed to read fixed-i64 fixture");
    assert!(json.contains("\"experiment\": \"codex-p1-rust-scl-fixed-i64-l8-baseline\""));
    assert!(json.contains("\"decoder\": \"scl_l8_fixed_i64_metric_scale_1024\""));
    assert!(json.contains("\"N\": 128"));
    assert!(json.contains("\"N\": 512"));

    let _ = fs::remove_file(path);
}
