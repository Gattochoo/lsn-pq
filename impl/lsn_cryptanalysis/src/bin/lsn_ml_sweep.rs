use std::env;
use std::fs;

use lsn_cryptanalysis::{results_to_json, run_ml_trials};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rate: f64,
    trials: usize,
    seed: u64,
    output: String,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_ml_sweep --n-start 3 --n-end 4 --ratios 0.5,1.0,2.0 --p 0.25 --trials 20 --seed 3235823838 --output experiments/out.json"
        );
        std::process::exit(2);
    });

    let mut results = Vec::new();
    for n in args.n_start..=args.n_end {
        let base = 1usize << (2 * n);
        for &ratio in &args.ratios {
            let sample_count = ((base as f64) * ratio).round() as usize;
            eprintln!(
                "running n={n}, m={sample_count}, ratio={ratio:.3}, p={:.4}, trials={}",
                args.noise_rate, args.trials
            );
            results.push(run_ml_trials(
                n,
                sample_count,
                args.noise_rate,
                args.trials,
                args.seed ^ ((n as u64) << 32) ^ sample_count as u64,
            ));
        }
    }

    let json = results_to_json("codex-p2-rust-ml-bruteforce-smoke", &results);
    fs::write(&args.output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {}: {err}", args.output);
        std::process::exit(1);
    });
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n_start = 3;
    let mut n_end = 4;
    let mut ratios = vec![0.5, 1.0, 2.0];
    let mut noise_rate = 0.25;
    let mut trials = 20;
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
            "--ratios" => ratios = parse_ratios(value)?,
            "--p" => noise_rate = parse_value(key, value)?,
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
    if !(0.0..=0.5).contains(&noise_rate) {
        return Err("require p in [0, 0.5]".to_string());
    }
    if ratios.is_empty() || ratios.iter().any(|ratio| *ratio <= 0.0) {
        return Err("require positive ratios".to_string());
    }

    Ok(Args {
        n_start,
        n_end,
        ratios,
        noise_rate,
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

fn parse_ratios(value: &str) -> Result<Vec<f64>, String> {
    value
        .split(',')
        .map(|part| {
            part.parse()
                .map_err(|_| format!("invalid ratio in --ratios: {part}"))
        })
        .collect()
}
