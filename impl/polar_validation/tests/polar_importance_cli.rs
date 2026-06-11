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

fn importance_bin() -> &'static str {
    env!("CARGO_BIN_EXE_polar_importance")
}

fn temp_fixture_path(name: &str) -> PathBuf {
    let mut path = std::env::temp_dir();
    path.push(format!(
        "polar_importance_{name}_{}.json",
        std::process::id()
    ));
    path
}

fn small_importance_args() -> [&'static str; 12] {
    [
        "--n",
        "128",
        "--k",
        "16",
        "--target-p",
        "0.4",
        "--proposal-values",
        "0.4",
        "--trials",
        "5",
        "--seed",
        "5397",
    ]
}

#[test]
fn cli_check_accepts_matching_importance_fixture() {
    let path = temp_fixture_path("matching");

    let generate_status = Command::new(importance_bin())
        .args(small_importance_args())
        .args(["--list-size", "8", "--output"])
        .arg(&path)
        .status()
        .expect("failed to run polar_importance generator");
    assert!(generate_status.success());

    let check_status = Command::new(importance_bin())
        .args(small_importance_args())
        .args(["--list-size", "8", "--check"])
        .arg(&path)
        .status()
        .expect("failed to run polar_importance checker");
    assert!(check_status.success());

    let _ = fs::remove_file(path);
}

#[test]
fn cli_check_rejects_mismatched_importance_fixture() {
    let path = temp_fixture_path("mismatch");
    fs::write(&path, "{ \"experiment\": \"wrong\" }\n").expect("failed to write bad fixture");

    let output = Command::new(importance_bin())
        .args(small_importance_args())
        .args(["--list-size", "8", "--check"])
        .arg(&path)
        .output()
        .expect("failed to run polar_importance checker");

    assert!(!output.status.success());
    assert!(
        String::from_utf8_lossy(&output.stderr).contains("importance check failed"),
        "stderr did not explain mismatch: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let _ = fs::remove_file(path);
}
