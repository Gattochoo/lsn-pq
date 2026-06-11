use std::env;
use std::fs;

use lsn_cryptanalysis::{bucket_certificate_results_to_json, run_bucket_certificate_trials};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rates: Vec<f64>,
    trials: usize,
    bucket_extra: usize,
    seed: u64,
    output: String,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_bucket_certificate_sweep --n-start 4 --n-end 8 --ratios 64.0 --p-values 0.0,0.25,0.5 --trials 5 --bucket-extra 2 --seed 3235823838 --output experiments/out.json"
        );
        std::process::exit(2);
    });

    let mut results = Vec::new();
    for n in args.n_start..=args.n_end {
        let base = 1usize << (2 * n);
        let bucket_bits = n + args.bucket_extra;
        for &ratio in &args.ratios {
            let sample_count = ((base as f64) * ratio).round() as usize;
            for &noise_rate in &args.noise_rates {
                eprintln!(
                    "running bucket-cert n={n}, m={sample_count}, ratio={ratio:.3}, p={noise_rate:.4}, trials={}, bucket_bits={bucket_bits}",
                    args.trials
                );
                results.push(run_bucket_certificate_trials(
                    n,
                    sample_count,
                    noise_rate,
                    args.trials,
                    bucket_bits,
                    args.seed
                        ^ ((n as u64) << 40)
                        ^ ((bucket_bits as u64) << 24)
                        ^ sample_count as u64
                        ^ noise_rate.to_bits(),
                ));
            }
        }
    }

    let json =
        bucket_certificate_results_to_json("codex-p2-bucket-rate-certificate-screen", &results);
    fs::write(&args.output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {}: {err}", args.output);
        std::process::exit(1);
    });
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n_start = 4;
    let mut n_end = 8;
    let mut ratios = vec![64.0];
    let mut noise_rates = vec![0.0, 0.25, 0.5];
    let mut trials = 5;
    let mut bucket_extra = 2;
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
            "--bucket-extra" => bucket_extra = parse_value(key, value)?,
            "--seed" => seed = parse_value(key, value)?,
            "--output" => output = Some(value.clone()),
            other => return Err(format!("unknown argument {other}")),
        }
        i += 2;
    }

    if n_start == 0 || n_end < n_start {
        return Err("require 1 <= n-start <= n-end".to_string());
    }
    if n_end + bucket_extra > 2 * n_end {
        return Err("require bucket-extra <= n-end".to_string());
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
        bucket_extra,
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
