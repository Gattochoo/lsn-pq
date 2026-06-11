use polar_validation::{
    baseline_reproduction_configs, build_frozen_natural, decode_scl, decode_scl_fast,
    decode_successive_cancellation, encode, high_noise_control_configs, results_to_json,
    results_to_json_with_decoder, simulate_bsc_sc, simulate_bsc_scl, simulate_bsc_scl_fast,
    target_n2048_configs, PolarCode,
};

#[test]
fn natural_order_frozen_set_matches_small_reference() {
    let frozen = build_frozen_natural(8, 4, 0.0706);
    assert_eq!(frozen, vec![4, 2, 1, 0]);
}

#[test]
fn noiseless_successive_cancellation_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(8, 4, 0.0706);
    let msg = vec![1, 0, 1, 1];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_successive_cancellation(&code, &llr);
    assert_eq!(decoded, msg);
}

#[test]
fn noiseless_scl_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(16, 8, 0.0706);
    let msg = vec![1, 0, 1, 1, 0, 0, 1, 0];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_scl(&code, &llr, 8);
    assert_eq!(decoded, msg);
}

#[test]
fn noiseless_fast_scl_roundtrip_recovers_info_bits() {
    let code = PolarCode::new(16, 8, 0.0706);
    let msg = vec![1, 0, 1, 1, 0, 0, 1, 0];
    let x = encode(&code, &msg);
    let llr = x
        .iter()
        .map(|&bit| if bit == 0 { 12.0 } else { -12.0 })
        .collect::<Vec<_>>();

    let decoded = decode_scl_fast(&code, &llr, 8);
    assert_eq!(decoded, msg);
}

#[test]
fn short_bsc_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_sc(128, 16, 0.0343, 25, 0x5eed);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn short_bsc_scl_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_scl(128, 16, 0.0706, 25, 0x51c1, 8);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn short_bsc_fast_scl_smoke_reproduces_zero_bler_with_fixed_seed() {
    let result = simulate_bsc_scl_fast(128, 16, 0.0706, 25, 0xF451C1, 8);
    assert_eq!(result.errors, 0);
    assert_eq!(result.trials, 25);
}

#[test]
fn baseline_reproduction_configs_cover_paper_short_lengths() {
    let configs = baseline_reproduction_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(
        triples,
        vec![
            (128, 16, 0.0706),
            (128, 16, 0.0343),
            (256, 32, 0.0706),
            (256, 32, 0.0343),
            (512, 64, 0.0706),
            (512, 64, 0.0343),
        ]
    );
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn target_n2048_configs_cover_paper_design_points() {
    let configs = target_n2048_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(triples, vec![(2048, 256, 0.0706), (2048, 256, 0.0343)]);
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn high_noise_control_configs_cover_failure_points() {
    let configs = high_noise_control_configs(200, 0xC0DEC0DE);
    let triples = configs
        .iter()
        .map(|cfg| (cfg.n, cfg.k, cfg.p))
        .collect::<Vec<_>>();
    assert_eq!(
        triples,
        vec![(2048, 256, 0.3), (2048, 256, 0.4), (2048, 256, 0.5),]
    );
    assert!(configs.iter().all(|cfg| cfg.trials == 200));
}

#[test]
fn high_noise_fast_scl_smoke_fails_when_channel_is_random() {
    let result = simulate_bsc_scl_fast(128, 16, 0.5, 25, 0xBAD5EED, 8);
    assert_eq!(result.trials, 25);
    assert!(
        result.errors >= 20,
        "expected high-noise BLER near 1, got {result:?}"
    );
}

#[test]
fn result_json_records_bler_and_seed() {
    let result = simulate_bsc_sc(128, 16, 0.0343, 5, 12345);
    let json = results_to_json("codex-p1-smoke", &[result]);
    assert!(json.contains("\"experiment\": \"codex-p1-smoke\""));
    assert!(json.contains("\"seed\": 12345"));
    assert!(json.contains("\"bler\": 0"));
}

#[test]
fn result_json_can_label_scl_decoder() {
    let result = simulate_bsc_scl(128, 16, 0.0706, 5, 67890, 8);
    let json = results_to_json_with_decoder("codex-p1-scl-smoke", "scl_l8_exact_llr", &[result]);
    assert!(json.contains("\"decoder\": \"scl_l8_exact_llr\""));
}
