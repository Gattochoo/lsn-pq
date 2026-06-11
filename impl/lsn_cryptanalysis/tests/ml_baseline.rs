use lsn_cryptanalysis::{
    CompactLagrangians, LsnSample, XorShift64, bkw_noise_after_rounds, bkw_xor_noise_rate,
    brute_force_ml_decode, bucket_rate_certificate, compact_ml_decode, enumerate_lagrangians,
    positive_basis_isd_decode, random_lagrangian, results_to_json, run_bkw_bucket_trials,
    run_isd_budget_trials, run_isd_trials, run_ml_trials, run_sampled_candidate_ambient_ml_trials,
    run_sampled_candidate_false_max_budget_trials, run_sampled_candidate_ml_budget_trials,
    run_sampled_candidate_ml_trials, run_span_trials, sample_lsn, sampled_candidate_ml_model_row,
    span_of_positives_decode, span_results_to_json, symplectic_form, wilson_score_interval,
};

#[test]
fn transvection_orbit_matches_small_lagrangian_counts() {
    let n2 = enumerate_lagrangians(2);
    let n3 = enumerate_lagrangians(3);

    assert_eq!(n2.len(), 15);
    assert_eq!(n3.len(), 135);
    assert!(n2.iter().all(|lagr| lagr.len() == 4));
    assert!(n3.iter().all(|lagr| lagr.len() == 8));
}

#[test]
fn ml_decoder_recovers_noiseless_secret_at_small_n() {
    let lagrangians = enumerate_lagrangians(3);
    let secret_idx = 17;
    let secret = &lagrangians[secret_idx];
    let mut samples = Vec::new();

    for a in 0..64 {
        samples.push(LsnSample {
            point: a,
            label: secret.contains(&a),
        });
    }

    let guess = brute_force_ml_decode(&samples, &lagrangians);
    assert_eq!(guess.best_index, secret_idx);
    assert_eq!(guess.best_score, 64);
}

#[test]
fn random_labels_do_not_look_like_clean_lsn() {
    let lagrangians = enumerate_lagrangians(3);
    let mut rng = XorShift64::new(0xC0DEC0DE);
    let mut samples = Vec::new();

    for point in 0..64 {
        samples.push(LsnSample {
            point,
            label: rng.next_bool(),
        });
    }

    let guess = brute_force_ml_decode(&samples, &lagrangians);
    assert!(guess.best_score < 56);
}

#[test]
fn noisy_sampler_is_seed_reproducible() {
    let lagrangians = enumerate_lagrangians(3);
    let secret = &lagrangians[23];
    let mut rng_a = XorShift64::new(12345);
    let mut rng_b = XorShift64::new(12345);

    let a = sample_lsn(secret, 32, 0.25, 6, &mut rng_a);
    let b = sample_lsn(secret, 32, 0.25, 6, &mut rng_b);

    assert_eq!(a, b);
}

#[test]
fn ml_trial_runner_recovers_noiseless_lsn() {
    let result = run_ml_trials(3, 64, 0.0, 4, 0xA11CE);

    assert_eq!(result.successes, 4);
    assert_eq!(result.trials, 4);
    assert_eq!(result.sample_count, 64);
}

#[test]
fn result_json_records_threat_model_and_success_rate() {
    let result = run_ml_trials(3, 64, 0.0, 2, 0xB0B);
    let json = results_to_json("codex-p2-ml-smoke", &[result]);

    assert!(json.contains("\"experiment\": \"codex-p2-ml-smoke\""));
    assert!(json.contains(
        "\"threat_model\": \"attacker observes public points and noisy membership labels\""
    ));
    assert!(json.contains("\"success_rate\": 1.0000000000"));
}

#[test]
fn compact_ml_decoder_matches_reference_scorer() {
    let lagrangians = enumerate_lagrangians(4);
    let compact = CompactLagrangians::from_lagrangians(4, &lagrangians);
    let mut rng = XorShift64::new(0xDEC0DED);
    let samples = sample_lsn(&lagrangians[91], 96, 0.25, 8, &mut rng);

    let reference = brute_force_ml_decode(&samples, &lagrangians);
    let packed = compact_ml_decode(&samples, &compact);

    assert_eq!(packed, reference);
}

#[test]
fn span_of_positives_recovers_noiseless_full_observation() {
    let lagrangians = enumerate_lagrangians(3);
    let secret_idx = 41;
    let secret = &lagrangians[secret_idx];
    let samples = (0..64)
        .map(|point| LsnSample {
            point,
            label: secret.contains(&point),
        })
        .collect::<Vec<_>>();

    let result = span_of_positives_decode(3, &samples, &lagrangians);

    assert_eq!(result.positive_count, 8);
    assert_eq!(result.span_rank, 3);
    assert_eq!(result.recovered_index, Some(secret_idx));
}

#[test]
fn span_of_positives_rejects_full_space_positive_set() {
    let lagrangians = enumerate_lagrangians(3);
    let samples = (0..64)
        .map(|point| LsnSample { point, label: true })
        .collect::<Vec<_>>();

    let result = span_of_positives_decode(3, &samples, &lagrangians);

    assert_eq!(result.positive_count, 64);
    assert_eq!(result.span_rank, 6);
    assert_eq!(result.recovered_index, None);
}

#[test]
fn span_trial_runner_recovers_noiseless_instances() {
    let result = run_span_trials(3, 512, 0.0, 3, 0x5A5A);

    assert_eq!(result.trials, 3);
    assert_eq!(result.successes, 3);
    assert_eq!(result.rank_n_count, 3);
    assert_eq!(result.overfull_rank_count, 0);
}

#[test]
fn span_result_json_records_overfull_failure_stats() {
    let result = run_span_trials(3, 512, 0.25, 2, 0xBAD5EED);
    let json = span_results_to_json("codex-p2-span-smoke", &[result]);

    assert!(json.contains("\"attack\": \"span_of_positives\""));
    assert!(json.contains("\"avg_positive_count\""));
    assert!(json.contains("\"overfull_rank_count\""));
}

#[test]
fn positive_basis_isd_recovers_noiseless_secret() {
    let lagrangians = enumerate_lagrangians(3);
    let secret_idx = 19;
    let secret = &lagrangians[secret_idx];
    let samples = (0..64)
        .map(|point| LsnSample {
            point,
            label: secret.contains(&point),
        })
        .collect::<Vec<_>>();
    let mut rng = XorShift64::new(0x15D);

    let result = positive_basis_isd_decode(3, &samples, &lagrangians, 200, &mut rng);

    assert_eq!(result.recovered_index, Some(secret_idx));
    assert!(result.valid_candidates >= 1);
}

#[test]
fn positive_basis_isd_trial_runner_has_noiseless_sanity() {
    let result = run_isd_trials(3, 256, 0.0, 5, 500, 0x15D15D);

    assert_eq!(result.trials, 5);
    assert_eq!(result.successes, 5);
    assert!(result.avg_valid_candidates >= 1.0);
}

#[test]
fn isd_budget_runner_preserves_attempt_budgets() {
    let results = run_isd_budget_trials(3, 256, 0.0, 2, &[10, 20], 0xBADC0DE);

    assert_eq!(results.len(), 2);
    assert_eq!(results[0].max_attempts, 10);
    assert_eq!(results[1].max_attempts, 20);
    assert_eq!(results[0].successes, 2);
    assert_eq!(results[1].successes, 2);
    assert_eq!(results[0].avg_positive_count, results[1].avg_positive_count);
}

#[test]
fn random_lagrangian_walk_preserves_isotropic_subspace() {
    let mut rng = XorShift64::new(0x5A17);
    let lagrangian = random_lagrangian(6, 64, &mut rng);
    let points = lagrangian.iter().copied().collect::<Vec<_>>();

    assert_eq!(points.len(), 64);
    for (i, &a) in points.iter().enumerate() {
        for &b in &points[i..] {
            assert!(!symplectic_form(a, b, 6));
        }
    }
}

#[test]
fn bkw_bucket_runner_has_noiseless_positive_control() {
    let results = run_bkw_bucket_trials(4, 512, 0.0, 2, 4, 16, 0xB00B1E);

    assert_eq!(results.trials, 2);
    assert!(results.avg_pairs > 0.0);
    assert!(results.avg_delta_in_secret_when_label_equal > results.delta_in_secret_floor);
}

#[test]
fn bkw_xor_noise_recurrence_squares_bias() {
    assert_eq!(bkw_xor_noise_rate(0.0), 0.0);
    assert_eq!(bkw_xor_noise_rate(0.5), 0.5);

    assert!((bkw_xor_noise_rate(0.25) - 0.375).abs() < 1e-12);
    assert!((bkw_noise_after_rounds(0.25, 2) - 0.46875).abs() < 1e-12);
    assert!((bkw_noise_after_rounds(0.25, 3) - 0.498046875).abs() < 1e-12);
}

#[test]
fn bucket_rate_certificate_detects_clean_projection_variance() {
    let mut rng = XorShift64::new(0xCE471F);
    let secret = random_lagrangian(4, 64, &mut rng);
    let samples = sample_lsn(&secret, 4096, 0.0, 8, &mut rng);

    let result = bucket_rate_certificate(4, &samples, &secret, 6);

    assert_eq!(result.bucket_bits, 6);
    assert!(result.avg_projected_secret_bucket_count <= 16.0);
    assert!(result.avg_excess_bucket_rate_variance > 0.001);
}

#[test]
fn sampled_candidate_ml_recovers_noiseless_planted_candidate() {
    let result = run_sampled_candidate_ml_trials(4, 2048, 0.0, 3, 32, 0x5A6DCAFE);

    assert_eq!(result.trials, 3);
    assert_eq!(result.candidate_count, 32);
    assert_eq!(result.successes, 3);
    assert!(result.avg_secret_margin > 0.0);
}

#[test]
fn sampled_candidate_budget_runner_preserves_candidate_counts() {
    let results = run_sampled_candidate_ml_budget_trials(4, 2048, 0.0, 2, &[16, 64], 0xCAFE_DA7E);

    assert_eq!(results.len(), 2);
    assert_eq!(results[0].candidate_count, 16);
    assert_eq!(results[1].candidate_count, 64);
    assert_eq!(results[0].successes, 2);
    assert_eq!(results[1].successes, 2);
    assert!(results[0].avg_secret_score >= results[1].avg_secret_score - 1e-9);
}

#[test]
fn sampled_candidate_extreme_value_model_has_noise_control() {
    let structured = sampled_candidate_ml_model_row(10, 65_536, 0.25, 32_768);
    let random = sampled_candidate_ml_model_row(10, 65_536, 0.5, 32_768);
    let larger_cloud = sampled_candidate_ml_model_row(10, 65_536, 0.25, 131_072);

    assert!(structured.predicted_secret_margin > 0.0);
    assert!(random.predicted_secret_margin < 0.0);
    assert!(larger_cloud.predicted_secret_margin < structured.predicted_secret_margin);
}

#[test]
fn sampled_candidate_false_max_runner_excludes_secret_candidate() {
    let results =
        run_sampled_candidate_false_max_budget_trials(4, 2048, 0.0, 2, &[16, 64], 0xFACE_FEED);

    assert_eq!(results.len(), 2);
    assert_eq!(results[0].candidate_count, 16);
    assert_eq!(results[1].candidate_count, 64);
    assert!(results[0].avg_secret_margin_to_false_max > 0.0);
    assert!(results[1].avg_secret_margin_to_false_max > 0.0);
    assert!(results[1].avg_best_false_score >= results[0].avg_best_false_score);
}

#[test]
fn sampled_candidate_ambient_runner_uses_universe_sized_cloud() {
    let results = run_sampled_candidate_ambient_ml_trials(4, &[0.5], &[0.0], 2, 0xA0B1_C2D3_E4F5);

    assert_eq!(results.len(), 1);
    assert_eq!(results[0].n, 4);
    assert_eq!(results[0].sample_count, 128);
    assert_eq!(results[0].candidate_count, 256);
    assert_eq!(results[0].successes, 2);
    assert!(results[0].avg_secret_margin > 0.0);
}

#[test]
fn wilson_score_interval_keeps_boundary_rates_honest() {
    let (half_low, half_high) = wilson_score_interval(10, 20, 1.96);
    let (perfect_low, perfect_high) = wilson_score_interval(20, 20, 1.96);
    let (empty_low, empty_high) = wilson_score_interval(0, 0, 1.96);

    assert!((half_low - 0.299).abs() < 0.001);
    assert!((half_high - 0.701).abs() < 0.001);
    assert!((perfect_low - 0.839).abs() < 0.001);
    assert!((perfect_high - 1.0).abs() < 1e-12);
    assert_eq!((empty_low, empty_high), (0.0, 0.0));
}
