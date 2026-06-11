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

use lsn_ref::constant_time_inventory_json;

#[test]
fn ct_inventory_marks_current_reference_as_non_production() {
    let json = constant_time_inventory_json();

    assert!(json.contains("\"experiment\": \"codex-lsn-ref-ct-inventory\""));
    assert!(json.contains("\"verdict\": \"not_constant_time_reference\""));
    assert!(json.contains("\"production_constant_time_claim\": false"));
    assert!(json.contains("\"threat_model\""));
    assert!(
        json.contains("\"classification\": \"partial_fixed_layout_scaffold_not_production_ct\"")
    );
    assert!(json.contains("FixedLagrangian bitset scaffold"));
    assert!(json.contains("scanned mask lookup"));
    assert!(json.contains("polar SCL path pruning"));
    assert!(json.contains("explicit diagnostic_honest_only_points boundary"));
    assert!(json.contains("diagnostic selector depends on the wrong secret"));
}

#[test]
fn ct_inventory_cli_writes_and_checks_exact_json() {
    let bin = env::var("CARGO_BIN_EXE_lsn_ct_inventory")
        .expect("Cargo should expose the lsn_ct_inventory test binary path");
    let path = env::temp_dir().join(format!("lsn_ref_ct_inventory_{}.json", std::process::id()));

    let write = Command::new(&bin)
        .args(["--output", path.to_str().expect("temp path must be UTF-8")])
        .status()
        .expect("failed to run lsn_ct_inventory writer");
    assert!(write.success());

    let json = fs::read_to_string(&path).expect("failed to read generated CT inventory");
    assert!(json.contains("\"experiment\": \"codex-lsn-ref-ct-inventory\""));

    let check = Command::new(&bin)
        .args(["--check", path.to_str().expect("temp path must be UTF-8")])
        .status()
        .expect("failed to run lsn_ct_inventory checker");
    assert!(check.success());
}
