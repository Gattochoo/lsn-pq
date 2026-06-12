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

use polar_validation::{
    baseline_reproduction_configs, high_noise_control_configs, results_to_json_with_decoder,
    simulate_bsc_sc, simulate_bsc_scl, simulate_bsc_scl_fast, simulate_bsc_scl_fixed_i64,
    target_n2048_configs, SimulationConfig, SimulationResult,
};

const FIXED_I64_METRIC_SCALE: f64 = 1024.0;

fn main() {
    let mut trials = 200usize;
    let mut seed = 0xC0DE_C0DEu64;
    let mut output = PathBuf::from("experiments/123-codex-polar-rust-baseline.json");
    let mut decoder = String::from("sc");
    let mut list_size = 8usize;
    let mut suite = String::from("baseline");
    let mut check: Option<PathBuf> = None;

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--trials" => {
                trials = args
                    .next()
                    .expect("--trials requires a value")
                    .parse()
                    .expect("--trials must be a positive integer");
            }
            "--seed" => {
                seed = args
                    .next()
                    .expect("--seed requires a value")
                    .parse()
                    .expect("--seed must be an integer");
            }
            "--output" => {
                output = PathBuf::from(args.next().expect("--output requires a path"));
            }
            "--check" => {
                check = Some(PathBuf::from(args.next().expect("--check requires a path")));
            }
            "--decoder" => {
                decoder = args.next().expect("--decoder requires sc or scl");
            }
            "--suite" => {
                suite = args.next().expect("--suite requires baseline or n2048");
            }
            "--list-size" => {
                list_size = args
                    .next()
                    .expect("--list-size requires a value")
                    .parse()
                    .expect("--list-size must be a positive integer");
            }
            "--help" | "-h" => {
                print_help();
                return;
            }
            other => panic!("unknown argument: {other}"),
        }
    }

    let configs = match suite.as_str() {
        "baseline" => baseline_reproduction_configs(trials, seed),
        "n2048" => target_n2048_configs(trials, seed),
        "high-noise" => high_noise_control_configs(trials, seed),
        other => panic!("unknown suite {other}; expected baseline, n2048, or high-noise"),
    };
    let (results, decoder_label, experiment) = match decoder.as_str() {
        "sc" => (
            run_and_report(&configs, |cfg| {
                simulate_bsc_sc(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed)
            }),
            String::from("successive_cancellation_exact_llr"),
            format!("codex-p1-rust-sc-{suite}"),
        ),
        "scl" => (
            run_and_report(&configs, |cfg| {
                simulate_bsc_scl(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed, list_size)
            }),
            format!("scl_l{list_size}_exact_llr"),
            format!("codex-p1-rust-scl-l{list_size}-{suite}"),
        ),
        "scl-fast" => (
            run_and_report(&configs, |cfg| {
                simulate_bsc_scl_fast(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed, list_size)
            }),
            format!("scl_l{list_size}_minsum_pathmetric"),
            format!("codex-p1-rust-scl-fast-l{list_size}-{suite}"),
        ),
        "fixed-i64" => (
            run_and_report(&configs, |cfg| {
                simulate_bsc_scl_fixed_i64_dispatch(cfg, list_size)
            }),
            format!("scl_l{list_size}_fixed_i64_metric_scale_1024"),
            format!("codex-p1-rust-scl-fixed-i64-l{list_size}-{suite}"),
        ),
        other => panic!("unknown decoder {other}; expected sc, scl, scl-fast, or fixed-i64"),
    };

    let json = results_to_json_with_decoder(&experiment, &decoder_label, &results);
    if let Some(check_path) = check {
        let expected = fs::read_to_string(&check_path).expect("failed to read polar fixture");
        if expected != json {
            eprintln!(
                "polar validate check failed: generated JSON differs from {}",
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
    fs::write(&output, json).expect("failed to write JSON result");
    eprintln!("wrote {}", output.display());
}

fn run_and_report<F>(configs: &[SimulationConfig], mut run: F) -> Vec<SimulationResult>
where
    F: FnMut(&SimulationConfig) -> SimulationResult,
{
    let mut results = Vec::with_capacity(configs.len());
    for cfg in configs {
        let result = run(cfg);
        eprintln!(
            "N={} K={} p={:.4} trials={} errors={} BLER={:.5}",
            result.n,
            result.k,
            result.p,
            result.trials,
            result.errors,
            result.bler()
        );
        results.push(result);
    }
    results
}

fn simulate_bsc_scl_fixed_i64_dispatch(
    cfg: &SimulationConfig,
    list_size: usize,
) -> SimulationResult {
    assert_eq!(
        list_size, 8,
        "fixed-i64 polar-validate currently supports --list-size 8 only"
    );

    match cfg.n {
        128 => simulate_bsc_scl_fixed_i64::<128, 8, 16>(
            cfg.k,
            cfg.p,
            cfg.trials,
            cfg.seed,
            FIXED_I64_METRIC_SCALE,
        ),
        256 => simulate_bsc_scl_fixed_i64::<256, 8, 16>(
            cfg.k,
            cfg.p,
            cfg.trials,
            cfg.seed,
            FIXED_I64_METRIC_SCALE,
        ),
        512 => simulate_bsc_scl_fixed_i64::<512, 8, 16>(
            cfg.k,
            cfg.p,
            cfg.trials,
            cfg.seed,
            FIXED_I64_METRIC_SCALE,
        ),
        2048 => simulate_bsc_scl_fixed_i64::<2048, 8, 16>(
            cfg.k,
            cfg.p,
            cfg.trials,
            cfg.seed,
            FIXED_I64_METRIC_SCALE,
        ),
        other => panic!("fixed-i64 polar-validate does not support N={other}"),
    }
}

fn print_help() {
    println!(
        "polar-validate [--trials N] [--seed U64] [--output PATH]\n\
         [--suite baseline|n2048|high-noise]\n\
         [--decoder sc|scl|scl-fast|fixed-i64] [--list-size L]\n\
         [--check PATH]\n\
         Runs a Codex P1 Rust polar validation suite."
    );
}
