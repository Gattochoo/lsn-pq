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

use polar_validation::scl_work_shape_audit_json;

#[derive(Debug)]
struct Args {
    output: PathBuf,
    check: Option<PathBuf>,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        print_help();
        std::process::exit(2);
    });

    let json = scl_work_shape_audit_json();
    if let Some(check_path) = args.check {
        let expected = fs::read_to_string(&check_path).expect("failed to read SCL audit fixture");
        if expected != json {
            eprintln!(
                "SCL audit check failed: generated JSON differs from {}",
                check_path.display()
            );
            std::process::exit(1);
        }
        eprintln!("verified {}", check_path.display());
        return;
    }

    if let Some(parent) = args.output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&args.output, json).expect("failed to write SCL audit JSON");
    eprintln!("wrote {}", args.output.display());
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut output = PathBuf::from("experiments/polar-scl-workshape-audit.json");
    let mut check = None;

    let mut i = 0;
    while i < raw.len() {
        let key = &raw[i];
        if key == "--help" || key == "-h" {
            print_help();
            std::process::exit(0);
        }
        let value = raw
            .get(i + 1)
            .ok_or_else(|| format!("missing value after {key}"))?;
        match key.as_str() {
            "--output" => output = PathBuf::from(value),
            "--check" => check = Some(PathBuf::from(value)),
            other => return Err(format!("unknown argument {other}")),
        }
        i += 2;
    }

    Ok(Args { output, check })
}

fn print_help() {
    eprintln!(
        "polar-scl-audit [--output PATH] [--check PATH]\n\
         Writes or verifies the machine-readable SCL work-shape audit artifact."
    );
}
