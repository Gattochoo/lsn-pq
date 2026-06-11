use std::env;
use std::fs;

use lsn_cryptanalysis::{sampled_candidate_ml_model, sampled_candidate_ml_model_to_json};

#[derive(Debug)]
struct Args {
    n_start: usize,
    n_end: usize,
    ratios: Vec<f64>,
    noise_rates: Vec<f64>,
    candidate_counts: Vec<usize>,
    output: String,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        eprintln!(
            "usage: lsn_sampled_ml_model --n-start 8 --n-end 10 --ratios 0.0625,0.125,0.25 --p-values 0.25,0.5 --candidate-values 512,2048,8192,32768 --output experiments/out.json"
        );
        std::process::exit(2);
    });

    let rows = sampled_candidate_ml_model(
        args.n_start,
        args.n_end,
        &args.ratios,
        &args.noise_rates,
        &args.candidate_counts,
    );
    let json = sampled_candidate_ml_model_to_json("codex-p2-sampled-candidate-ml-model", &rows);
    fs::write(&args.output, json).unwrap_or_else(|err| {
        eprintln!("failed to write {}: {err}", args.output);
        std::process::exit(1);
    });
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n_start = 8;
    let mut n_end = 10;
    let mut ratios = vec![0.0625, 0.125, 0.25];
    let mut noise_rates = vec![0.25, 0.5];
    let mut candidate_counts = vec![512, 2048, 8192, 32768];
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
            "--ratios" => ratios = parse_f64_list(value, "--ratios")?,
            "--p-values" => noise_rates = parse_f64_list(value, "--p-values")?,
            "--candidate-values" => {
                candidate_counts = parse_usize_list(value, "--candidate-values")?
            }
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
    if candidate_counts.is_empty() || candidate_counts.iter().any(|&count| count < 2) {
        return Err("require candidate counts >= 2".to_string());
    }

    Ok(Args {
        n_start,
        n_end,
        ratios,
        noise_rates,
        candidate_counts,
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

fn parse_f64_list(value: &str, key: &str) -> Result<Vec<f64>, String> {
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
