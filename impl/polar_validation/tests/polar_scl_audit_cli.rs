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

#[test]
fn polar_scl_audit_cli_writes_and_checks_exact_json() {
    let bin = env::var("CARGO_BIN_EXE_polar_scl_audit")
        .expect("Cargo should expose the polar_scl_audit test binary path");
    let path = env::temp_dir().join(format!("polar_scl_audit_{}.json", std::process::id()));

    let write = Command::new(&bin)
        .args(["--output", path.to_str().expect("temp path must be UTF-8")])
        .status()
        .expect("failed to run polar_scl_audit writer");
    assert!(write.success());

    let json = fs::read_to_string(&path).expect("failed to read generated SCL audit");
    assert!(json.contains("\"experiment\": \"codex-polar-scl-workshape-audit\""));
    assert!(json.contains("\"current_verdict\": \"not_constant_time\""));

    let check = Command::new(&bin)
        .args(["--check", path.to_str().expect("temp path must be UTF-8")])
        .status()
        .expect("failed to run polar_scl_audit checker");
    assert!(check.success());
}
