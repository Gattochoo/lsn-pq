use std::env;
use std::fs;

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
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_sampled_ambient_ml_sweep --n-start 6 --n-end 8 --ratios 0.03125,0.0625,0.125 --p-values 0.25,0.5 --trials 8 --seed 3235823841 --output experiments/out.json"
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
        results.extend(run_sampled_candidate_ambient_ml_trials(
            n,
            &args.ratios,
            &args.noise_rates,
            args.trials,
            args.seed ^ ((n as u64) << 40),
        ));
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
