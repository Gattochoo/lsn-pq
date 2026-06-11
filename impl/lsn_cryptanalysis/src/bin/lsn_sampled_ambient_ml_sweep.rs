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
    run_sampled_candidate_ambient_ml_trials, sampled_candidate_ml_results_to_json,
};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rates: Vec<f64>,
    trials: usize,
    seed: u64,
    output: String,
    progress: bool,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_sampled_ambient_ml_sweep --n-start 6 --n-end 8 --ratios 0.03125,0.0625,0.125 --p-values 0.25,0.5 --trials 8 --seed 3235823841 [--progress] --output experiments/out.json"
        );
        std::process::exit(2);
    });

    let mut results = Vec::new();
    for n in args.n_start..=args.n_end {
        eprintln!(
            "running ambient-ml n={n}, candidate_count={}, ratios={:?}, p_values={:?}, trials={}",
            1usize << (2 * n),
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
                    let cell = run_sampled_candidate_ambient_ml_trials(
                        n,
                        &[ratio],
                        &[noise_rate],
                        args.trials,
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
            results.extend(run_sampled_candidate_ambient_ml_trials(
                n,
                &args.ratios,
                &args.noise_rates,
                args.trials,
                n_seed,
            ));
        }
    }

    let json = sampled_candidate_ml_results_to_json(
        "codex-p2-sampled-ambient-size-candidate-ml",
        &results,
    );
    fs::write(&args.output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {}: {err}", args.output);
        std::process::exit(1);
    });
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

    let mut i = 0;
    while i < raw.len() {
        let key = &raw[i];
        if key == "--progress" {
            progress = true;
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

    Ok(Args {
        n_start,
        n_end,
        ratios,
        noise_rates,
        trials,
        seed,
        output: output.ok_or_else(|| "missing --output".to_string())?,
        progress,
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
    }
}
