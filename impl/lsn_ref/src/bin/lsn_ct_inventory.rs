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

use std::{env, fs, path::PathBuf};

use lsn_ref::constant_time_inventory_json;

fn main() {
    let mut output = PathBuf::from("experiments/182-codex-lsn-ref-ct-inventory.json");
    let mut check = None;

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--output" => {
                output = PathBuf::from(args.next().expect("--output requires a path"));
            }
            "--check" => {
                check = Some(PathBuf::from(args.next().expect("--check requires a path")));
            }
            "--help" | "-h" => {
                print_help();
                return;
            }
            other => panic!("unknown argument: {other}"),
        }
    }

    let json = constant_time_inventory_json();

    if let Some(check_path) = check {
        let expected =
            fs::read_to_string(&check_path).expect("failed to read CT inventory for checking");
        if expected != json {
            eprintln!(
                "CT inventory check failed: generated JSON differs from {}",
                check_path.display()
            );
            std::process::exit(1);
        }
        eprintln!("verified {}", check_path.display());
        return;
    }

    if let Some(parent) = output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&output, json).expect("failed to write CT inventory JSON");
    eprintln!("wrote {}", output.display());
}

fn print_help() {
    eprintln!(
        "lsn_ct_inventory [--output PATH]\n\
         lsn_ct_inventory --check PATH\n\
         Writes or verifies the machine-readable constant-time discipline inventory."
    );
}
