use lsn_cryptanalysis::{
    CompactLagrangians, LsnSample, XorShift64, brute_force_ml_decode, compact_ml_decode,
    enumerate_lagrangians, positive_basis_isd_decode, results_to_json, run_isd_trials,
    run_ml_trials, run_span_trials, sample_lsn, span_of_positives_decode, span_results_to_json,
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
