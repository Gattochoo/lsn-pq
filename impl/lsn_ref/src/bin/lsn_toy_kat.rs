use std::{env, fs, path::PathBuf};

use lsn_ref::{ToyKemParams, toy_wrong_secret_control, toy_wrong_secret_control_to_json};

fn main() {
    let mut output = PathBuf::from("experiments/152-codex-lsn-ref-toy-kat.json");

    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--output" => {
                output = PathBuf::from(args.next().expect("--output requires a path"));
            }
            "--help" | "-h" => {
                print_help();
                return;
            }
            other => panic!("unknown argument: {other}"),
        }
    }

    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };
    let control = toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF);
    let json = toy_wrong_secret_control_to_json("codex-lsn-ref-toy-kat", &control);

    if let Some(parent) = output.parent() {
        fs::create_dir_all(parent).expect("failed to create output directory");
    }
    fs::write(&output, json).expect("failed to write KAT JSON");
    eprintln!("wrote {}", output.display());
}

fn print_help() {
    eprintln!(
        "lsn_toy_kat [--output PATH]\n\
         Writes a deterministic toy LSN-KEM KAT vector with a wrong-secret negative control."
    );
}
