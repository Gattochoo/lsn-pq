use std::{env, fs, path::PathBuf};

use polar_validation::{importance_results_to_json, simulate_bsc_scl_fast_importance};

#[derive(Debug)]
struct Args {
    n: usize,
    k: usize,
    target_p: f64,
    proposal_values: Vec<f64>,
    trials: usize,
    seed: u64,
    list_size: usize,
    output: PathBuf,
    check: Option<PathBuf>,
}

fn main() {
    let args = parse_args(env::args().skip(1).collect()).unwrap_or_else(|err| {
        eprintln!("{err}");
        print_help();
        std::process::exit(2);
    });

    let mut results = Vec::new();
    for (i, &proposal_p) in args.proposal_values.iter().enumerate() {
        let seed = args
            .seed
            .wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15));
        let result = simulate_bsc_scl_fast_importance(
            args.n,
            args.k,
            args.target_p,
            proposal_p,
            args.trials,
            seed,
            args.list_size,
        );
        eprintln!(
            "N={} K={} target_p={:.4} proposal_p={:.4} trials={} proposal_errors={} weighted_bler={:.4e} mean_lr={:.4e} ess={:.2}",
            result.n,
            result.k,
            result.target_p,
            result.proposal_p,
            result.trials,
            result.proposal_errors,
            result.weighted_bler_estimate,
            result.mean_likelihood_ratio,
            result.effective_sample_size
        );
        results.push(result);
    }

    let json = importance_results_to_json(
        "codex-p1b-polar-scl-fast-importance-pilot",
        &format!("scl_l{}_minsum_pathmetric", args.list_size),
        &results,
    );
    if let Some(check_path) = args.check {
        let expected = fs::read_to_string(&check_path).expect("failed to read importance fixture");
        if expected != json {
            eprintln!(
                "importance check failed: generated JSON differs from {}",
                check_path.display()
            );
            std::process::exit(1);
        }
        eprintln!("verified {}", check_path.display());
        return;
    }

    if let Some(parent) = args.output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&args.output, json).expect("failed to write JSON result");
    eprintln!("wrote {}", args.output.display());
}

fn parse_args(raw: Vec<String>) -> Result<Args, String> {
    let mut n = 2048usize;
    let mut k = 256usize;
    let mut target_p = 0.0706;
    let mut proposal_values = vec![0.0706, 0.08, 0.10, 0.12];
    let mut trials = 200usize;
    let mut seed = 0x5151_2026u64;
    let mut list_size = 8usize;
    let mut output = PathBuf::from("experiments/polar-importance.json");
    let mut check = None;

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
            "--k" => k = parse_value(key, value)?,
            "--target-p" => target_p = parse_value(key, value)?,
            "--proposal-values" => proposal_values = parse_list(value, key)?,
            "--trials" => trials = parse_value(key, value)?,
            "--seed" => seed = parse_value(key, value)?,
            "--list-size" => list_size = parse_value(key, value)?,
            "--output" => output = PathBuf::from(value),
            "--check" => check = Some(PathBuf::from(value)),
            other => return Err(format!("unknown argument {other}")),
        }
        i += 2;
    }

    if proposal_values.is_empty() {
        return Err("require at least one proposal value".to_string());
    }

    Ok(Args {
        n,
        k,
        target_p,
        proposal_values,
        trials,
        seed,
        list_size,
        output,
        check,
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
        "polar-importance [--n N] [--k K] [--target-p P] [--proposal-values Q1,Q2]\n\
         [--trials T] [--seed U64] [--list-size L] [--output PATH]\n\
         [--check PATH]\n\
         Runs or verifies a tilted-BSC importance-sampling pilot for the fast SCL decoder."
    );
}
