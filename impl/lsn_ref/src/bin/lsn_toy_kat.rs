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
    ToyKemParams, toy_divergent_wrong_secret_control, toy_find_wrong_secret_control,
    toy_wrong_secret_control_to_json,
};

const HONEST_SECRET_SEED: u64 = 0xA11CE;
const SAMPLE_SEED: u64 = 0x5EED;
const NOISE_SEED: u64 = 0xC0DE;
const ENCAPS_SEED: u64 = 0xBEEF;

struct ProfileSpec {
    default_output: PathBuf,
    experiment: &'static str,
    params: ToyKemParams,
    wrong_secret_seed_start: u64,
    wrong_secret_seed_trials: usize,
    preflight_only_reason: Option<&'static str>,
    selection_mode: SelectionMode,
}

#[derive(Clone, Copy)]
enum SelectionMode {
    RandomPublicSamples,
    DivergentWrongSecretDiagnostic,
}

impl SelectionMode {
    fn as_str(self) -> &'static str {
        match self {
            SelectionMode::RandomPublicSamples => "random-public-samples",
            SelectionMode::DivergentWrongSecretDiagnostic => "divergent-wrong-secret-diagnostic",
        }
    }
}

fn main() {
    let mut profile = String::from("n2");
    let mut output = None;
    let mut check = None;
    let mut describe = false;

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--profile" => {
                profile = args
                    .next()
                    .expect("--profile requires n2, n2-noisy, n2-paper-r7, or n3-search");
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

    let spec = match profile.as_str() {
        "n2" => ProfileSpec {
            default_output: PathBuf::from("experiments/152-codex-lsn-ref-toy-kat.json"),
            experiment: "codex-lsn-ref-toy-kat",
            params: ToyKemParams {
                n: 2,
                sample_count: 64,
                repetition: 3,
                polar_n: 16,
                polar_k: 8,
                public_noise_rate: 0.0,
                decoder_design_p: 0.0343,
            },
            wrong_secret_seed_start: 0xA11CF,
            wrong_secret_seed_trials: 1,
            preflight_only_reason: None,
            selection_mode: SelectionMode::RandomPublicSamples,
        },
        "n2-noisy" => ProfileSpec {
            default_output: PathBuf::from("experiments/180-codex-lsn-ref-n2-noisy-kat.json"),
            experiment: "codex-lsn-ref-n2-noisy-kat",
            params: ToyKemParams {
                n: 2,
                sample_count: 512,
                repetition: 9,
                polar_n: 32,
                polar_k: 8,
                public_noise_rate: 0.25,
                decoder_design_p: 0.0343,
            },
            wrong_secret_seed_start: 0xA2000,
            wrong_secret_seed_trials: 4096,
            preflight_only_reason: None,
            selection_mode: SelectionMode::RandomPublicSamples,
        },
        "n2-paper-r7" => ProfileSpec {
            default_output: PathBuf::from("experiments/181-codex-lsn-ref-n2-paper-r7-kat.json"),
            experiment: "codex-lsn-ref-n2-paper-r7-kat",
            params: ToyKemParams {
                n: 2,
                sample_count: 2048 * 7,
                repetition: 7,
                polar_n: 2048,
                polar_k: 256,
                public_noise_rate: 0.25,
                decoder_design_p: 0.0706,
            },
            wrong_secret_seed_start: 0xA11CF,
            wrong_secret_seed_trials: 1,
            preflight_only_reason: Some(
                "small-n toy majority gate did not yield a wrong-secret negative-control fixture",
            ),
            selection_mode: SelectionMode::RandomPublicSamples,
        },
        "n2-paper-r7-divergent" => ProfileSpec {
            default_output: PathBuf::from(
                "experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json",
            ),
            experiment: "codex-lsn-ref-n2-paper-r7-divergent-kat",
            params: ToyKemParams {
                n: 2,
                sample_count: 2048 * 7,
                repetition: 7,
                polar_n: 2048,
                polar_k: 256,
                public_noise_rate: 0.25,
                decoder_design_p: 0.0706,
            },
            wrong_secret_seed_start: 0xA11CF,
            wrong_secret_seed_trials: 1,
            preflight_only_reason: None,
            selection_mode: SelectionMode::DivergentWrongSecretDiagnostic,
        },
        "n3-search" => ProfileSpec {
            default_output: PathBuf::from("experiments/153-codex-lsn-ref-n3-kat-search.json"),
            experiment: "codex-lsn-ref-n3-kat-search",
            params: ToyKemParams {
                n: 3,
                sample_count: 256,
                repetition: 3,
                polar_n: 32,
                polar_k: 16,
                public_noise_rate: 0.0,
                decoder_design_p: 0.0343,
            },
            wrong_secret_seed_start: 0xA2000,
            wrong_secret_seed_trials: 1024,
            preflight_only_reason: None,
            selection_mode: SelectionMode::RandomPublicSamples,
        },
        other => panic!("unknown --profile: {other}"),
    };

    if describe {
        print!("{}", profile_description_json(&profile, &spec));
        return;
    }

    if let Some(reason) = spec.preflight_only_reason {
        eprintln!("profile {profile} is preflight-only: {reason}");
        std::process::exit(2);
    }

    let output = output.unwrap_or_else(|| spec.default_output.clone());
    let control = match spec.selection_mode {
        SelectionMode::RandomPublicSamples => toy_find_wrong_secret_control(
            spec.params,
            HONEST_SECRET_SEED,
            spec.wrong_secret_seed_start,
            spec.wrong_secret_seed_trials,
            SAMPLE_SEED,
            NOISE_SEED,
            ENCAPS_SEED,
        )
        .expect("failed to find wrong-secret fixture in seed window"),
        SelectionMode::DivergentWrongSecretDiagnostic => toy_divergent_wrong_secret_control(
            spec.params,
            HONEST_SECRET_SEED,
            spec.wrong_secret_seed_start,
            NOISE_SEED,
            ENCAPS_SEED,
        )
        .expect("failed to build divergent wrong-secret diagnostic fixture"),
    };
    let json = toy_wrong_secret_control_to_json(spec.experiment, &control);

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
        "lsn_toy_kat [--profile n2|n2-noisy|n2-paper-r7|n2-paper-r7-divergent|n3-search] [--output PATH]\n\
         lsn_toy_kat [--profile n2|n2-noisy|n2-paper-r7|n2-paper-r7-divergent|n3-search] --check PATH\n\
         lsn_toy_kat [--profile n2|n2-noisy|n2-paper-r7|n2-paper-r7-divergent|n3-search] --describe\n\
         Writes or verifies a deterministic toy LSN-KEM KAT vector with a wrong-secret negative control."
    );
}

fn profile_description_json(profile: &str, spec: &ProfileSpec) -> String {
    format!(
        "{{\n  \"profile\": \"{}\",\n  \"experiment\": \"{}\",\n  \"default_output\": \"{}\",\n  \"status\": \"profile description only; does not generate a KAT fixture\",\n  \"preflight_only\": {},\n  \"preflight_only_reason\": \"{}\",\n  \"selection_mode\": \"{}\",\n  \"params\": {{\n    \"n\": {},\n    \"sample_count\": {},\n    \"repetition\": {},\n    \"polar_N\": {},\n    \"polar_K\": {},\n    \"public_noise_rate\": {:.10},\n    \"decoder_design_p\": {:.10}\n  }},\n  \"seeds\": {{\n    \"honest_secret_seed\": {},\n    \"wrong_secret_seed_start\": {},\n    \"wrong_secret_seed_trials\": {},\n    \"sample_seed\": {},\n    \"noise_seed\": {},\n    \"encaps_seed\": {}\n  }}\n}}\n",
        profile,
        spec.experiment,
        spec.default_output.display(),
        spec.preflight_only_reason.is_some(),
        spec.preflight_only_reason.unwrap_or(""),
        spec.selection_mode.as_str(),
        spec.params.n,
        spec.params.sample_count,
        spec.params.repetition,
        spec.params.polar_n,
        spec.params.polar_k,
        spec.params.public_noise_rate,
        spec.params.decoder_design_p,
        HONEST_SECRET_SEED,
        spec.wrong_secret_seed_start,
        spec.wrong_secret_seed_trials,
        SAMPLE_SEED,
        NOISE_SEED,
        ENCAPS_SEED
    )
}
