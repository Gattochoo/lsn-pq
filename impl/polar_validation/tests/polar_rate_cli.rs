use std::{fs, path::PathBuf, process::Command};

fn rate_bin() -> &'static str {
    env!("CARGO_BIN_EXE_polar_rate_sweep")
}

fn temp_fixture_path(name: &str) -> PathBuf {
    let mut path = std::env::temp_dir();
    path.push(format!("polar_rate_{name}_{}.json", std::process::id()));
    path
}

fn small_rate_args() -> [&'static str; 12] {
    [
        "--n",
        "128",
        "--p-values",
        "0.0343",
        "--k-start",
        "8",
        "--k-end",
        "16",
        "--k-step",
        "4",
        "--target-log2",
        "-40",
    ]
}

#[test]
fn cli_check_accepts_matching_rate_fixture() {
    let path = temp_fixture_path("matching");

    let generate_status = Command::new(rate_bin())
        .args(small_rate_args())
        .args(["--output"])
        .arg(&path)
        .status()
        .expect("failed to run polar_rate_sweep generator");
    assert!(generate_status.success());

    let check_status = Command::new(rate_bin())
        .args(small_rate_args())
        .args(["--check"])
        .arg(&path)
        .status()
        .expect("failed to run polar_rate_sweep checker");
    assert!(check_status.success());

    let _ = fs::remove_file(path);
}

#[test]
fn cli_check_rejects_mismatched_rate_fixture() {
    let path = temp_fixture_path("mismatch");
    fs::write(&path, "{ \"experiment\": \"wrong\" }\n").expect("failed to write bad fixture");

    let output = Command::new(rate_bin())
        .args(small_rate_args())
        .args(["--check"])
        .arg(&path)
        .output()
        .expect("failed to run polar_rate_sweep checker");

    assert!(!output.status.success());
    assert!(
        String::from_utf8_lossy(&output.stderr).contains("rate check failed"),
        "stderr did not explain mismatch: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let _ = fs::remove_file(path);
}
