use std::env;
use std::fs;

use lsn_cryptanalysis::{isd_results_to_json, run_isd_budget_trials};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rates: Vec<f64>,
    trials: usize,
    attempt_budgets: Vec<usize>,
    seed: u64,
    output: String,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_isd_sweep --n-start 3 --n-end 5 --ratios 4.0 --p-values 0.0,0.25 --trials 10 --attempt-values 2000,10000 --seed 3235823838 --output experiments/out.json"
        );
        std::process::exit(2);
    });

    let mut results = Vec::new();
    for n in args.n_start..=args.n_end {
        let base = 1usize << (2 * n);
        for &ratio in &args.ratios {
            let sample_count = ((base as f64) * ratio).round() as usize;
            for &noise_rate in &args.noise_rates {
                eprintln!(
                    "running isd n={n}, m={sample_count}, ratio={ratio:.3}, p={noise_rate:.4}, trials={}, attempt_budgets={:?}",
                    args.trials, args.attempt_budgets
                );
                results.extend(run_isd_budget_trials(
                    n,
                    sample_count,
                    noise_rate,
                    args.trials,
                    &args.attempt_budgets,
                    args.seed ^ ((n as u64) << 40) ^ sample_count as u64 ^ noise_rate.to_bits(),
                ));
            }
        }
    }

    let json = isd_results_to_json("codex-p2-positive-basis-isd-screen", &results);
    fs::write(&args.output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {}: {err}", args.output);
        std::process::exit(1);
    });
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n_start = 3;
    let mut n_end = 5;
    let mut ratios = vec![4.0];
    let mut noise_rates = vec![0.0, 0.25];
    let mut trials = 10;
    let mut attempt_budgets = vec![2000];
    let mut seed = 3_235_823_838u64;
    let mut output = None;

    let mut i = 0;
    while i < raw.len() {
        let key = &raw[i];
        let value = raw
            .get(i + 1)
            .ok_or_else(|| format!("missing value after {key}"))?;
        match key.as_str() {
            "--n-start" => n_start = parse_value(key, value)?,
            "--n-end" => n_end = parse_value(key, value)?,
            "--ratios" => ratios = parse_list(value, "--ratios")?,
            "--p-values" => noise_rates = parse_list(value, "--p-values")?,
            "--trials" => trials = parse_value(key, value)?,
            "--max-attempts" => attempt_budgets = vec![parse_value(key, value)?],
            "--attempt-values" => attempt_budgets = parse_usize_list(value, "--attempt-values")?,
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
    if attempt_budgets.is_empty() || attempt_budgets.contains(&0) {
        return Err("require positive attempt budgets".to_string());
    }

    Ok(Args {
        n_start,
        n_end,
        ratios,
        noise_rates,
        trials,
        attempt_budgets,
        seed,
        output: output.ok_or_else(|| "missing --output".to_string())?,
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

fn parse_usize_list(value: &str, key: &str) -> Result<Vec<usize>, String> {
    value
        .split(',')
        .map(|part| {
            part.parse()
                .map_err(|_| format!("invalid value in {key}: {part}"))
        })
        .collect()
}
