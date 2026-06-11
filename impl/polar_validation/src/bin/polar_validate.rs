use std::{env, fs, path::PathBuf};

use polar_validation::{
    baseline_reproduction_configs, results_to_json_with_decoder, run_configs, simulate_bsc_scl,
};

fn main() {
    let mut trials = 200usize;
    let mut seed = 0xC0DE_C0DEu64;
    let mut output = PathBuf::from("experiments/123-codex-polar-rust-baseline.json");
    let mut decoder = String::from("sc");
    let mut list_size = 8usize;

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
            "--decoder" => {
                decoder = args.next().expect("--decoder requires sc or scl");
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

    let configs = baseline_reproduction_configs(trials, seed);
    let (results, decoder_label, experiment) = match decoder.as_str() {
        "sc" => (
            run_configs(&configs),
            String::from("successive_cancellation_exact_llr"),
            String::from("codex-p1-rust-sc-nle512-baseline"),
        ),
        "scl" => (
            configs
                .iter()
                .map(|cfg| simulate_bsc_scl(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed, list_size))
                .collect(),
            format!("scl_l{list_size}_exact_llr"),
            format!("codex-p1-rust-scl-l{list_size}-nle512-baseline"),
        ),
        other => panic!("unknown decoder {other}; expected sc or scl"),
    };
    for result in &results {
        eprintln!(
            "N={} K={} p={:.4} trials={} errors={} BLER={:.5}",
            result.n,
            result.k,
            result.p,
            result.trials,
            result.errors,
            result.bler()
        );
    }

    let json = results_to_json_with_decoder(&experiment, &decoder_label, &results);
    if let Some(parent) = output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&output, json).expect("failed to write JSON result");
    eprintln!("wrote {}", output.display());
}

fn print_help() {
    println!(
        "polar-validate [--trials N] [--seed U64] [--output PATH]\n\
         [--decoder sc|scl] [--list-size L]\n\
         Runs the Codex P1 short-length Rust SC polar baseline."
    );
}
