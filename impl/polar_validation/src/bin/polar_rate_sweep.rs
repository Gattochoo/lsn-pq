use std::{env, fs, path::PathBuf};

use polar_validation::{polar_rate_rows_to_json, sweep_polar_rate};

#[derive(Debug)]
struct Args {
    n: usize,
    p_values: Vec<f64>,
    k_start: usize,
    k_end: usize,
    k_step: usize,
    target_log2: f64,
    output: PathBuf,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        print_help();
        std::process::exit(2);
    });

    let rows = sweep_polar_rate(
        args.n,
        &args.p_values,
        args.k_start,
        args.k_end,
        args.k_step,
        args.target_log2,
    );

    for &p in &args.p_values {
        let best = rows
            .iter()
            .filter(|row| row.p == p && row.passes_half_sum_target)
            .max_by_key(|row| row.k);
        match best {
            Some(row) => eprintln!(
                "p={:.10} max_passing_K={} rate={:.6} log2_half_sum={:.3}",
                row.p, row.k, row.rate, row.log2_half_sum_bound
            ),
            None => eprintln!("p={p:.10} max_passing_K=none"),
        }
    }

    let json = polar_rate_rows_to_json("codex-p1b-polar-rate-sweep-n2048", args.target_log2, &rows);
    if let Some(parent) = args.output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&args.output, json).expect("failed to write JSON result");
    eprintln!("wrote {}", args.output.display());
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n = 2048usize;
    let mut p_values = vec![0.0706, 0.0343];
    let mut k_start = 1usize;
    let mut k_end = 512usize;
    let mut k_step = 1usize;
    let mut target_log2 = -128.0;
    let mut output = PathBuf::from("experiments/polar-rate-sweep.json");

    let mut i = 0;
    while i < raw.len() {
        let key = &raw[i];
        if key == "--help" || key == "-h" {
            print_help();
            std::process::exit(0);
        }
        let value = raw
            .get(i + 1)
            .ok_or_else(|| format!("missing value after {key}"))?;
        match key.as_str() {
            "--n" => n = parse_value(key, value)?,
            "--p-values" => p_values = parse_list(value, key)?,
            "--k-start" => k_start = parse_value(key, value)?,
            "--k-end" => k_end = parse_value(key, value)?,
            "--k-step" => k_step = parse_value(key, value)?,
            "--target-log2" => target_log2 = parse_value(key, value)?,
            "--output" => output = PathBuf::from(value),
            other => return Err(format!("unknown argument {other}")),
        }
        i += 2;
    }

    if p_values.is_empty() {
        return Err("require at least one p value".to_string());
    }
    if k_step == 0 {
        return Err("K step must be positive".to_string());
    }
    if k_start > k_end {
        return Err("K start must be <= K end".to_string());
    }
    if k_end > n {
        return Err("K end must be <= N".to_string());
    }

    Ok(Args {
        n,
        p_values,
        k_start,
        k_end,
        k_step,
        target_log2,
        output,
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

fn print_help() {
    eprintln!(
        "polar-rate-sweep [--n N] [--p-values P1,P2] [--k-start K0]\n\
         [--k-end K1] [--k-step STEP] [--target-log2 LOG2] [--output PATH]\n\
         Sweeps the conservative half-sum Bhattacharyya SC block-error bound."
    );
}
