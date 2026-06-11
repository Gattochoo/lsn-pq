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
    ToyKemParams, ToyPublicPreflightScanConfig, toy_public_wrong_secret_preflight_scan,
    toy_public_wrong_secret_preflight_scan_to_json,
};

const HONEST_SECRET_SEED: u64 = 0xA11CE;
const SAMPLE_SEED: u64 = 0x5EED;
const NOISE_SEED: u64 = 0xC0DE;
const ENCAPS_SEED: u64 = 0xBEEF;

struct ProfileSpec {
    default_output: PathBuf,
    experiment: &'static str,
    config: ToyPublicPreflightScanConfig,
}

fn main() {
    let mut profile = String::from("n2-paper-r7-public-preflight");
    let mut output = None;
    let mut check = None;

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--profile" => {
                profile = args
                    .next()
                    .expect("--profile requires n2-paper-r7-public-preflight");
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

    let spec = match profile.as_str() {
        "n2-paper-r7-public-preflight" => ProfileSpec {
            default_output: PathBuf::from(
                "experiments/183-codex-lsn-ref-n2-paper-r7-public-preflight.json",
            ),
            experiment: "codex-lsn-ref-n2-paper-r7-public-preflight",
            config: ToyPublicPreflightScanConfig {
                params: ToyKemParams {
                    n: 2,
                    sample_count: 2048 * 7,
                    repetition: 7,
                    polar_n: 2048,
                    polar_k: 256,
                    public_noise_rate: 0.25,
                    decoder_design_p: 0.0706,
                },
                honest_secret_seed: HONEST_SECRET_SEED,
                sample_seed_start: SAMPLE_SEED,
                sample_seed_trials: 1,
                wrong_secret_seed_start: 0xA11CF,
                wrong_secret_seed_trials: 1,
                noise_seed: NOISE_SEED,
                encaps_seed: ENCAPS_SEED,
            },
        },
        other => panic!("unknown --profile: {other}"),
    };

    let report = toy_public_wrong_secret_preflight_scan(spec.config);
    let json = toy_public_wrong_secret_preflight_scan_to_json(spec.experiment, &profile, &report);

    if let Some(check_path) = check {
        let expected =
            fs::read_to_string(&check_path).expect("failed to read preflight report for checking");
        if expected != json {
            eprintln!(
                "preflight check failed: generated profile {profile} differs from {}",
                check_path.display()
            );
            std::process::exit(1);
        }
        eprintln!("verified {}", check_path.display());
        return;
    }

    let output = output.unwrap_or_else(|| spec.default_output.clone());
    if let Some(parent) = output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&output, json).expect("failed to write preflight JSON");
    eprintln!("wrote {}", output.display());
}

fn print_help() {
    eprintln!(
        "lsn_public_preflight [--profile n2-paper-r7-public-preflight] [--output PATH]\n\
         lsn_public_preflight [--profile n2-paper-r7-public-preflight] --check PATH\n\
         Writes or verifies a bounded public-selection KAT preflight report."
    );
}
