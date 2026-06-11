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

use std::env;
use std::fs;
use std::time::Instant;

use lsn_cryptanalysis::{
    run_sampled_candidate_ambient_ml_trials, run_sampled_candidate_ambient_ml_trials_streaming,
    run_sampled_candidate_ambient_ml_trials_streaming_with_cap,
    run_sampled_candidate_ambient_ml_trials_with_cap, sampled_candidate_ml_results_to_json,
};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rates: Vec<f64>,
    trials: usize,
    seed: u64,
    output: Option<String>,
    progress: bool,
    dry_run: bool,
    candidate_cap: Option<usize>,
    streaming: bool,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_sampled_ambient_ml_sweep --n-start 6 --n-end 8 --ratios 0.03125,0.0625,0.125 --p-values 0.25,0.5 --trials 8 --seed 3235823841 [--progress] [--dry-run] --output experiments/out.json"
        );
        std::process::exit(2);
    });

    if args.dry_run {
        print_dry_run(&args);
        return;
    }

    let mut results = Vec::new();
    for n in args.n_start..=args.n_end {
        eprintln!(
            "running ambient-ml n={n}, candidate_count={}, ratios={:?}, p_values={:?}, trials={}",
            candidate_count_for_n(n, args.candidate_cap),
            args.ratios,
            args.noise_rates,
            args.trials
        );
        let n_seed = args.seed ^ ((n as u64) << 40);
        if args.progress {
            for &ratio in &args.ratios {
                let sample_count = ((1usize << (2 * n)) as f64 * ratio).round() as usize;
                for &noise_rate in &args.noise_rates {
                    eprintln!(
                        "  cell start n={n} ratio={ratio} samples={sample_count} p={noise_rate} trials={}",
                        args.trials
                    );
                    let start = Instant::now();
                    let cell = run_cell(
                        n,
                        &[ratio],
                        &[noise_rate],
                        args.trials,
                        args.candidate_cap,
                        args.streaming,
                        n_seed,
                    );
                    let elapsed = start.elapsed();
                    if let Some(result) = cell.first() {
                        eprintln!(
                            "  cell done n={n} ratio={ratio} p={noise_rate} successes={}/{} margin={:.3} elapsed_ms={}",
                            result.successes,
                            result.trials,
                            result.avg_secret_margin,
                            elapsed.as_millis()
                        );
                    }
                    results.extend(cell);
                }
            }
        } else {
            results.extend(run_cell(
                n,
                &args.ratios,
                &args.noise_rates,
                args.trials,
                args.candidate_cap,
                args.streaming,
                n_seed,
            ));
        }
    }

    let experiment = match (args.candidate_cap.is_some(), args.streaming) {
        (false, false) => "codex-p2-sampled-ambient-size-candidate-ml",
        (true, false) => "codex-p2-capped-ambient-size-candidate-ml",
        (false, true) => "codex-p2-streaming-ambient-size-candidate-ml",
        (true, true) => "codex-p2-capped-streaming-ambient-size-candidate-ml",
    };
    let json = sampled_candidate_ml_results_to_json(experiment, &results);
    let output = args
        .output
        .as_ref()
        .expect("non-dry-run parse must require output");
    fs::write(output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {output}: {err}");
        std::process::exit(1);
    });
}

fn run_cell(
    n: usize,
    ratios: &[f64],
    noise_rates: &[f64],
    trials: usize,
    candidate_cap: Option<usize>,
    streaming: bool,
    seed: u64,
) -> Vec<lsn_cryptanalysis::SampledCandidateMlTrialResult> {
    match (candidate_cap, streaming) {
        (Some(cap), false) => run_sampled_candidate_ambient_ml_trials_with_cap(
            n,
            ratios,
            noise_rates,
            trials,
            cap,
            seed,
        ),
        (None, false) => {
            run_sampled_candidate_ambient_ml_trials(n, ratios, noise_rates, trials, seed)
        }
        (Some(cap), true) => run_sampled_candidate_ambient_ml_trials_streaming_with_cap(
            n,
            ratios,
            noise_rates,
            trials,
            cap,
            seed,
        ),
        (None, true) => {
            run_sampled_candidate_ambient_ml_trials_streaming(n, ratios, noise_rates, trials, seed)
        }
    }
}

fn print_dry_run(args: &Args) {
    for line in dry_run_lines(args) {
        eprintln!("{line}");
    }
}

fn dry_run_lines(args: &Args) -> Vec<String> {
    let mut lines = Vec::new();
    for n in args.n_start..=args.n_end {
        let ambient_candidate_count = pow2(2 * n);
        let candidate_count = candidate_count_for_n_u128(n, args.candidate_cap);
        let lagrangian_points = pow2(n);
        let row_storage_points = if args.streaming {
            lagrangian_points
        } else {
            candidate_count.saturating_mul(lagrangian_points)
        };
        lines.push(format!(
            "dry-run ambient-ml n={n} streaming={} ambient_candidate_count={ambient_candidate_count} candidate_count={candidate_count} lagrangian_points={lagrangian_points} row_storage_points={row_storage_points}",
            args.streaming
        ));
        for &ratio in &args.ratios {
            let sample_count = ((ambient_candidate_count as f64) * ratio).round() as u128;
            for &noise_rate in &args.noise_rates {
                let score_pairs = candidate_count
                    .saturating_mul(sample_count)
                    .saturating_mul(args.trials as u128);
                let profile_updates = sample_count.saturating_mul(args.trials as u128);
                let candidate_point_visits = candidate_count
                    .saturating_mul(lagrangian_points)
                    .saturating_mul(args.trials as u128);
                lines.push(format!(
                    "  cell n={n} ratio={ratio} samples={sample_count} p={noise_rate} trials={} score_pairs={score_pairs} profile_updates={profile_updates} candidate_point_visits={candidate_point_visits}",
                    args.trials
                ));
            }
        }
    }
    lines
}

fn pow2(exp: usize) -> u128 {
    1u128
        .checked_shl(exp as u32)
        .unwrap_or_else(|| panic!("2^{exp} does not fit in u128"))
}

fn candidate_count_for_n(n: usize, cap: Option<usize>) -> usize {
    let ambient = 1usize << (2 * n);
    cap.unwrap_or(ambient).min(ambient)
}

fn candidate_count_for_n_u128(n: usize, cap: Option<usize>) -> u128 {
    let ambient = pow2(2 * n);
    cap.map(|cap| (cap as u128).min(ambient)).unwrap_or(ambient)
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n_start = 6;
    let mut n_end = 8;
    let mut ratios = vec![0.03125, 0.0625, 0.125, 0.25];
    let mut noise_rates = vec![0.25, 0.5];
    let mut trials = 8;
    let mut seed = 3_235_823_841u64;
    let mut output = None;
    let mut progress = false;
    let mut dry_run = false;
    let mut candidate_cap = None;
    let mut streaming = false;

    let mut i = 0;
    while i < raw.len() {
        let key = &raw[i];
        if key == "--progress" {
            progress = true;
            i += 1;
            continue;
        }
        if key == "--dry-run" {
            dry_run = true;
            i += 1;
            continue;
        }
        if key == "--streaming" {
            streaming = true;
            i += 1;
            continue;
        }
        let value = raw
            .get(i + 1)
            .ok_or_else(|| format!("missing value after {key}"))?;
        match key.as_str() {
            "--n-start" => n_start = parse_value(key, value)?,
            "--n-end" => n_end = parse_value(key, value)?,
            "--ratios" => ratios = parse_list(value, "--ratios")?,
            "--p-values" => noise_rates = parse_list(value, "--p-values")?,
            "--trials" => trials = parse_value(key, value)?,
            "--seed" => seed = parse_value(key, value)?,
            "--candidate-cap" => candidate_cap = Some(parse_value(key, value)?),
            "--output" => output = Some(value.clone()),
            other => return Err(format!("unknown argument {other}")),
        }
        i += 2;
    }

    if n_start == 0 || n_end < n_start {
        return Err("require 1 <= n-start <= n-end".to_string());
    }
    if ratios.is_empty() || ratios.iter().any(|ratio| *ratio <= 0.0) {
        return Err("require positive ratios".to_string());
    }
    if noise_rates.is_empty() || noise_rates.iter().any(|p| !(0.0..=0.5).contains(p)) {
        return Err("require p-values in [0, 0.5]".to_string());
    }
    if output.is_none() && !dry_run {
        return Err("missing --output".to_string());
    }
    if matches!(candidate_cap, Some(cap) if cap < 2) {
        return Err("require candidate-cap >= 2".to_string());
    }

    Ok(Args {
        n_start,
        n_end,
        ratios,
        noise_rates,
        trials,
        seed,
        output,
        progress,
        dry_run,
        candidate_cap,
        streaming,
    })
}

fn parse_value<T>(key: &str, value: &str) -> Result<T, String>
where
    T: std::str::FromStr,
{
    value
        .parse()
        .map_err(|_| format!("invalid value for {key}: {value}"))
}

fn parse_list(value: &str, key: &str) -> Result<Vec<f64>, String> {
    value
        .split(',')
        .map(|part| {
            part.parse()
                .map_err(|_| format!("invalid value in {key}: {part}"))
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn owned(args: &[&str]) -> Vec<String> {
        args.iter().map(|arg| arg.to_string()).collect()
    }

    #[test]
    fn parse_args_defaults_progress_off() {
        let args = parse_args(owned(&[
            "--n-start",
            "10",
            "--n-end",
            "10",
            "--ratios",
            "0.03125",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "8",
            "--seed",
            "3235823857",
            "--output",
            "/tmp/out.json",
        ]))
        .unwrap();

        assert!(!args.progress);
        assert!(!args.dry_run);
    }

    #[test]
    fn parse_args_accepts_value_free_progress_flag() {
        let args = parse_args(owned(&[
            "--n-start",
            "10",
            "--n-end",
            "10",
            "--ratios",
            "0.03125",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "8",
            "--seed",
            "3235823857",
            "--progress",
            "--output",
            "/tmp/out.json",
        ]))
        .unwrap();

        assert!(args.progress);
        assert!(!args.dry_run);
    }

    #[test]
    fn parse_args_accepts_dry_run_without_output() {
        let args = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.015625",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "1",
            "--seed",
            "3235823859",
            "--dry-run",
        ]))
        .unwrap();

        assert!(args.dry_run);
        assert!(args.output.is_none());
    }

    #[test]
    fn parse_args_accepts_candidate_cap() {
        let args = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.015625",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "1",
            "--seed",
            "3235823859",
            "--candidate-cap",
            "4096",
            "--output",
            "/tmp/out.json",
        ]))
        .unwrap();

        assert_eq!(args.candidate_cap, Some(4096));
    }

    #[test]
    fn parse_args_accepts_streaming_mode() {
        let args = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.015625",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "1",
            "--seed",
            "3235823859",
            "--streaming",
            "--output",
            "/tmp/out.json",
        ]))
        .unwrap();

        assert!(args.streaming);
    }

    #[test]
    fn dry_run_lines_distinguish_streaming_row_storage_from_capped_storage() {
        let streaming = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.000244140625",
            "--p-values",
            "0.25",
            "--trials",
            "1",
            "--seed",
            "3235823863",
            "--streaming",
            "--dry-run",
        ]))
        .unwrap();
        let capped = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.000244140625",
            "--p-values",
            "0.25",
            "--trials",
            "1",
            "--seed",
            "3235823863",
            "--candidate-cap",
            "4096",
            "--dry-run",
        ]))
        .unwrap();

        let streaming_lines = dry_run_lines(&streaming);
        let capped_lines = dry_run_lines(&capped);

        assert!(streaming_lines[0].contains("streaming=true"));
        assert!(streaming_lines[0].contains("candidate_count=4194304"));
        assert!(streaming_lines[0].contains("row_storage_points=2048"));
        assert!(streaming_lines[1].contains("score_pairs=4294967296"));
        assert!(streaming_lines[1].contains("profile_updates=1024"));
        assert!(streaming_lines[1].contains("candidate_point_visits=8589934592"));

        assert!(capped_lines[0].contains("streaming=false"));
        assert!(capped_lines[0].contains("candidate_count=4096"));
        assert!(capped_lines[0].contains("row_storage_points=8388608"));
        assert!(capped_lines[1].contains("score_pairs=4194304"));
        assert!(capped_lines[1].contains("profile_updates=1024"));
        assert!(capped_lines[1].contains("candidate_point_visits=8388608"));
    }

    #[test]
    fn parse_args_requires_output_without_dry_run() {
        let err = parse_args(owned(&[
            "--n-start",
            "11",
            "--n-end",
            "11",
            "--ratios",
            "0.015625",
            "--p-values",
            "0.25,0.5",
            "--trials",
            "1",
            "--seed",
            "3235823859",
        ]))
        .unwrap_err();

        assert_eq!(err, "missing --output");
    }
}
