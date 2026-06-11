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
    let mut describe = false;

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
            "--describe" => {
                describe = true;
            }
            "--help" | "-h" => {
                print_help();
                return;
            }
            other => panic!("unknown argument: {other}"),
        }
    }

    let spec = profile_spec(&profile);

    if describe {
        print!("{}", profile_description_json(&profile, &spec));
        return;
    }

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
        "lsn_public_preflight [--profile n2-paper-r7-public-preflight|n2-paper-r7-public-preflight-wrong16] [--output PATH]\n\
         lsn_public_preflight [--profile n2-paper-r7-public-preflight|n2-paper-r7-public-preflight-wrong16] --check PATH\n\
         lsn_public_preflight [--profile n2-paper-r7-public-preflight|n2-paper-r7-public-preflight-wrong16] --describe\n\
         Writes or verifies a bounded public-selection KAT preflight report."
    );
}

fn profile_spec(profile: &str) -> ProfileSpec {
    let mut spec = ProfileSpec {
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
    };

    match profile {
        "n2-paper-r7-public-preflight" => spec,
        "n2-paper-r7-public-preflight-wrong16" => {
            spec.default_output = PathBuf::from(
                "experiments/184-codex-lsn-ref-n2-paper-r7-public-preflight-wrong16.json",
            );
            spec.experiment = "codex-lsn-ref-n2-paper-r7-public-preflight-wrong16";
            spec.config.wrong_secret_seed_trials = 16;
            spec
        }
        other => panic!("unknown --profile: {other}"),
    }
}

fn profile_description_json(profile: &str, spec: &ProfileSpec) -> String {
    format!(
        "{{\n  \"profile\": \"{}\",\n  \"experiment\": \"{}\",\n  \"default_output\": \"{}\",\n  \"status\": \"profile description only; does not run the preflight scan\",\n  \"selection_mode\": \"random-public-samples\",\n  \"diagnostic_only\": false,\n  \"params\": {{\n    \"n\": {},\n    \"sample_count\": {},\n    \"repetition\": {},\n    \"polar_N\": {},\n    \"polar_K\": {},\n    \"public_noise_rate\": {:.10},\n    \"decoder_design_p\": {:.10}\n  }},\n  \"seeds\": {{\n    \"honest_secret_seed\": {},\n    \"sample_seed_start\": {},\n    \"sample_seed_trials\": {},\n    \"wrong_secret_seed_start\": {},\n    \"wrong_secret_seed_trials\": {},\n    \"noise_seed\": {},\n    \"encaps_seed\": {}\n  }}\n}}\n",
        profile,
        spec.experiment,
        spec.default_output.display(),
        spec.config.params.n,
        spec.config.params.sample_count,
        spec.config.params.repetition,
        spec.config.params.polar_n,
        spec.config.params.polar_k,
        spec.config.params.public_noise_rate,
        spec.config.params.decoder_design_p,
        spec.config.honest_secret_seed,
        spec.config.sample_seed_start,
        spec.config.sample_seed_trials,
        spec.config.wrong_secret_seed_start,
        spec.config.wrong_secret_seed_trials,
        spec.config.noise_seed,
        spec.config.encaps_seed,
    )
}
