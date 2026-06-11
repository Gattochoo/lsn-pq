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

use lsn_ref::{
    ToyKemParams, toy_find_wrong_secret_control, toy_wrong_secret_control,
    toy_wrong_secret_control_to_json,
};

fn main() {
    let mut profile = String::from("n2");
    let mut output = None;
    let mut check = None;

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--profile" => {
                profile = args.next().expect("--profile requires n2 or n3-search");
            }
            "--output" => {
                output = Some(PathBuf::from(
                    args.next().expect("--output requires a path"),
                ));
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

    let (default_output, experiment, control) = match profile.as_str() {
        "n2" => {
            let params = ToyKemParams {
                n: 2,
                sample_count: 64,
                repetition: 3,
                polar_n: 16,
                polar_k: 8,
                public_noise_rate: 0.0,
                decoder_design_p: 0.0343,
            };
            (
                PathBuf::from("experiments/152-codex-lsn-ref-toy-kat.json"),
                "codex-lsn-ref-toy-kat",
                toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF),
            )
        }
        "n3-search" => {
            let params = ToyKemParams {
                n: 3,
                sample_count: 256,
                repetition: 3,
                polar_n: 32,
                polar_k: 16,
                public_noise_rate: 0.0,
                decoder_design_p: 0.0343,
            };
            let control = toy_find_wrong_secret_control(
                params, 0xA11CE, 0xA2000, 1024, 0x5EED, 0xC0DE, 0xBEEF,
            )
            .expect("failed to find n=3 wrong-secret fixture in seed window");
            (
                PathBuf::from("experiments/153-codex-lsn-ref-n3-kat-search.json"),
                "codex-lsn-ref-n3-kat-search",
                control,
            )
        }
        other => panic!("unknown --profile: {other}"),
    };
    let output = output.unwrap_or(default_output);
    let json = toy_wrong_secret_control_to_json(experiment, &control);

    if let Some(check_path) = check {
        let expected =
            fs::read_to_string(&check_path).expect("failed to read KAT fixture for checking");
        if expected != json {
            eprintln!(
                "KAT check failed: generated profile {profile} differs from {}",
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
    fs::write(&output, json).expect("failed to write KAT JSON");
    eprintln!("wrote {}", output.display());
}

fn print_help() {
    eprintln!(
        "lsn_toy_kat [--profile n2|n3-search] [--output PATH]\n\
         lsn_toy_kat [--profile n2|n3-search] --check PATH\n\
         Writes or verifies a deterministic toy LSN-KEM KAT vector with a wrong-secret negative control."
    );
}
