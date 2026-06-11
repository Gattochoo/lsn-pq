// Copyright 2026 Kwanghoo Choo
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use std::collections::{BTreeSet, HashSet, VecDeque};

pub type Lagrangian = BTreeSet<u32>;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LsnSample {
    pub point: u32,
    pub label: bool,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct MlGuess {
    pub best_index: usize,
    pub best_score: usize,
    pub runner_up_score: usize,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SpanAttackResult {
    pub n: usize,
    pub total_dim: usize,
    pub positive_count: usize,
    pub span_rank: usize,
    pub recovered_index: Option<usize>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct IsdAttackResult {
    pub n: usize,
    pub total_dim: usize,
    pub positive_count: usize,
    pub attempts_used: usize,
    pub valid_candidates: usize,
    pub best_score: usize,
    pub recovered_index: Option<usize>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CompactLagrangians {
    pub n: usize,
    pub total_dim: usize,
    pub universe: usize,
    rows: Vec<Vec<u32>>,
}

impl CompactLagrangians {
    pub fn from_lagrangians(n: usize, lagrangians: &[Lagrangian]) -> Self {
        let total_dim = 2 * n;
        let universe = 1usize << total_dim;
        let rows = lagrangians
            .iter()
            .map(|lagrangian| lagrangian.iter().copied().collect::<Vec<_>>())
            .collect();
        Self {
            n,
            total_dim,
            universe,
            rows,
        }
    }

    pub fn len(&self) -> usize {
        self.rows.len()
    }

    pub fn is_empty(&self) -> bool {
        self.rows.is_empty()
    }
}

#[derive(Clone, Copy, Debug)]
pub struct MlTrialResult {
    pub n: usize,
    pub lagrangians: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub successes: usize,
    pub seed: u64,
}

impl MlTrialResult {
    pub fn success_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.successes as f64 / self.trials as f64
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct SampledCandidateMlTrialResult {
    pub n: usize,
    pub total_dim: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub candidate_count: usize,
    pub successes: usize,
    pub avg_secret_score: f64,
    pub avg_best_false_score: f64,
    pub avg_secret_margin: f64,
    pub seed: u64,
}

impl SampledCandidateMlTrialResult {
    pub fn success_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.successes as f64 / self.trials as f64
        }
    }
}

pub fn wilson_score_interval(successes: usize, trials: usize, z: f64) -> (f64, f64) {
    if trials == 0 {
        return (0.0, 0.0);
    }

    let n = trials as f64;
    let p_hat = successes as f64 / n;
    let z2 = z * z;
    let denominator = 1.0 + z2 / n;
    let center = (p_hat + z2 / (2.0 * n)) / denominator;
    let half_width = z * ((p_hat * (1.0 - p_hat) + z2 / (4.0 * n)) / n).sqrt() / denominator;

    (
        (center - half_width).max(0.0),
        (center + half_width).min(1.0),
    )
}

#[derive(Clone, Copy, Debug)]
pub struct SampledCandidateFalseMaxTrialResult {
    pub n: usize,
    pub total_dim: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub candidate_count: usize,
    pub avg_secret_score: f64,
    pub avg_best_false_score: f64,
    pub avg_secret_margin_to_false_max: f64,
    pub seed: u64,
}

#[derive(Clone, Copy, Debug)]
pub struct SampledCandidateMlModelRow {
    pub n: usize,
    pub total_dim: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub candidate_count: usize,
    pub disagreement_rate: f64,
    pub mean_pair_margin: f64,
    pub sigma_pair_margin: f64,
    pub extreme_value_penalty: f64,
    pub predicted_secret_margin: f64,
}

#[derive(Clone, Copy, Debug)]
pub struct SpanTrialResult {
    pub n: usize,
    pub lagrangians: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub successes: usize,
    pub rank_n_count: usize,
    pub overfull_rank_count: usize,
    pub full_rank_count: usize,
    pub avg_positive_count: f64,
    pub avg_span_rank: f64,
    pub seed: u64,
}

impl SpanTrialResult {
    pub fn success_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.successes as f64 / self.trials as f64
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct IsdTrialResult {
    pub n: usize,
    pub lagrangians: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub max_attempts: usize,
    pub successes: usize,
    pub avg_positive_count: f64,
    pub avg_attempts_used: f64,
    pub avg_valid_candidates: f64,
    pub avg_best_score: f64,
    pub seed: u64,
}

impl IsdTrialResult {
    pub fn success_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.successes as f64 / self.trials as f64
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct BkwBucketTrialResult {
    pub n: usize,
    pub total_dim: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub bucket_bits: usize,
    pub pair_limit_per_bucket: usize,
    pub avg_pairs: f64,
    pub avg_label_xor_rate: f64,
    pub avg_matched_random_xor_rate: f64,
    pub avg_label_xor_excess: f64,
    pub delta_in_secret_floor: f64,
    pub avg_delta_in_secret_when_label_equal: f64,
    pub avg_delta_in_secret_when_label_unequal: f64,
    pub seed: u64,
}

#[derive(Clone, Copy, Debug)]
pub struct BucketCertificateTrialResult {
    pub n: usize,
    pub total_dim: usize,
    pub sample_count: usize,
    pub noise_rate: f64,
    pub trials: usize,
    pub bucket_bits: usize,
    pub bucket_count: usize,
    pub avg_observed_bucket_count: f64,
    pub avg_bucket_sample_count: f64,
    pub avg_global_label_rate: f64,
    pub avg_bucket_rate_variance: f64,
    pub avg_matched_random_variance: f64,
    pub avg_excess_bucket_rate_variance: f64,
    pub avg_projected_secret_bucket_count: f64,
    pub avg_projected_secret_bucket_fraction: f64,
    pub seed: u64,
}

#[derive(Clone, Copy, Debug)]
pub struct BkwNoiseModelRow {
    pub initial_noise_rate: f64,
    pub rounds: usize,
    pub xor_width: usize,
    pub effective_noise_rate: f64,
    pub bias: f64,
    pub signal_retention: f64,
}

#[derive(Clone, Copy, Debug)]
pub struct XorShift64 {
    state: u64,
}

impl XorShift64 {
    pub fn new(seed: u64) -> Self {
        let state = if seed == 0 {
            0x9E37_79B9_7F4A_7C15
        } else {
            seed
        };
        Self { state }
    }

    pub fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }

    pub fn next_bool(&mut self) -> bool {
        (self.next_u64() & 1) == 1
    }

    pub fn next_f64(&mut self) -> f64 {
        let bits = self.next_u64() >> 11;
        (bits as f64) * (1.0 / ((1u64 << 53) as f64))
    }

    pub fn next_index(&mut self, upper: usize) -> usize {
        assert!(upper > 0, "upper must be positive");
        (self.next_u64() as usize) % upper
    }
}

pub fn symplectic_form(x: u32, y: u32, n: usize) -> bool {
    let mut acc = 0u32;
    for i in 0..n {
        let x_e = (x >> (2 * i)) & 1;
        let x_f = (x >> (2 * i + 1)) & 1;
        let y_e = (y >> (2 * i)) & 1;
        let y_f = (y >> (2 * i + 1)) & 1;
        acc ^= (x_e & y_f) ^ (x_f & y_e);
    }
    acc == 1
}

pub fn transvection(v: u32, x: u32, n: usize) -> u32 {
    if symplectic_form(x, v, n) { x ^ v } else { x }
}

pub fn enumerate_lagrangians(n: usize) -> Vec<Lagrangian> {
    assert!(n > 0, "n must be positive");
    assert!(2 * n <= 32, "bitmask model supports dimension at most 32");

    let l0 = standard_lagrangian(n);
    let generators = transvection_generators(n);
    let mut orbit = HashSet::new();
    let mut queue = VecDeque::new();

    orbit.insert(l0.clone());
    queue.push_back(l0);

    while let Some(lagrangian) = queue.pop_front() {
        for &generator in &generators {
            let image = apply_transvection(&lagrangian, generator, n);
            if orbit.insert(image.clone()) {
                queue.push_back(image);
            }
        }
    }

    let mut out: Vec<_> = orbit.into_iter().collect();
    out.sort_by_key(|lagr| lagr.iter().copied().collect::<Vec<_>>());
    out
}

pub fn random_lagrangian(n: usize, walk_steps: usize, rng: &mut XorShift64) -> Lagrangian {
    assert!(n > 0, "n must be positive");
    assert!(2 * n <= 32, "bitmask model supports dimension at most 32");

    let basis = random_lagrangian_basis(n, walk_steps, rng);
    span_from_basis(&basis)
}

pub fn sample_lsn(
    secret: &Lagrangian,
    sample_count: usize,
    noise_rate: f64,
    total_dim: usize,
    rng: &mut XorShift64,
) -> Vec<LsnSample> {
    assert!(
        (0.0..=0.5).contains(&noise_rate),
        "noise rate must be in [0, 0.5]"
    );
    assert!(
        total_dim <= 32,
        "bitmask model supports dimension at most 32"
    );

    let universe = 1usize << total_dim;
    let mut samples = Vec::with_capacity(sample_count);
    for _ in 0..sample_count {
        let point = rng.next_index(universe) as u32;
        let noise = rng.next_f64() < noise_rate;
        samples.push(LsnSample {
            point,
            label: secret.contains(&point) ^ noise,
        });
    }
    samples
}

pub fn bkw_bucket_observable(
    n: usize,
    samples: &[LsnSample],
    secret: &Lagrangian,
    bucket_bits: usize,
    pair_limit_per_bucket: usize,
) -> BkwBucketTrialResult {
    let total_dim = 2 * n;
    assert!(
        bucket_bits <= total_dim,
        "bucket bits exceed ambient dimension"
    );
    assert!(
        pair_limit_per_bucket > 0,
        "pair limit per bucket must be positive"
    );

    let bucket_count = 1usize << bucket_bits;
    let bucket_mask = (bucket_count - 1) as u32;
    let mut buckets = vec![Vec::<LsnSample>::new(); bucket_count];
    let mut positive_count = 0usize;

    for sample in samples {
        assert!(
            (sample.point as usize) < (1usize << total_dim),
            "sample point outside ambient universe"
        );
        if sample.label {
            positive_count += 1;
        }
        buckets[(sample.point & bucket_mask) as usize].push(*sample);
    }

    let mut pairs = 0usize;
    let mut label_xor_count = 0usize;
    let mut equal_count = 0usize;
    let mut unequal_count = 0usize;
    let mut delta_in_secret_equal = 0usize;
    let mut delta_in_secret_unequal = 0usize;

    for bucket in buckets {
        let mut bucket_pairs = 0usize;
        'outer: for i in 0..bucket.len() {
            for j in (i + 1)..bucket.len() {
                let a = bucket[i];
                let b = bucket[j];
                let label_xor = a.label ^ b.label;
                let delta = a.point ^ b.point;
                let delta_in_secret = secret.contains(&delta);

                pairs += 1;
                bucket_pairs += 1;
                if label_xor {
                    label_xor_count += 1;
                    unequal_count += 1;
                    if delta_in_secret {
                        delta_in_secret_unequal += 1;
                    }
                } else {
                    equal_count += 1;
                    if delta_in_secret {
                        delta_in_secret_equal += 1;
                    }
                }

                if bucket_pairs >= pair_limit_per_bucket {
                    break 'outer;
                }
            }
        }
    }

    let q = if samples.is_empty() {
        0.0
    } else {
        positive_count as f64 / samples.len() as f64
    };
    let matched_random_xor_rate = 2.0 * q * (1.0 - q);
    let label_xor_rate = rate(label_xor_count, pairs);

    BkwBucketTrialResult {
        n,
        total_dim,
        sample_count: samples.len(),
        noise_rate: 0.0,
        trials: 1,
        bucket_bits,
        pair_limit_per_bucket,
        avg_pairs: pairs as f64,
        avg_label_xor_rate: label_xor_rate,
        avg_matched_random_xor_rate: matched_random_xor_rate,
        avg_label_xor_excess: label_xor_rate - matched_random_xor_rate,
        delta_in_secret_floor: 2f64.powi(-(n as i32)),
        avg_delta_in_secret_when_label_equal: rate(delta_in_secret_equal, equal_count),
        avg_delta_in_secret_when_label_unequal: rate(delta_in_secret_unequal, unequal_count),
        seed: 0,
    }
}

pub fn bucket_rate_certificate(
    n: usize,
    samples: &[LsnSample],
    secret: &Lagrangian,
    bucket_bits: usize,
) -> BucketCertificateTrialResult {
    let total_dim = 2 * n;
    assert!(
        bucket_bits <= total_dim,
        "bucket bits exceed ambient dimension"
    );
    assert!(
        bucket_bits <= 24,
        "bucket certificate screen caps in-memory buckets at 2^24"
    );

    let bucket_count = 1usize << bucket_bits;
    let bucket_mask = (bucket_count - 1) as u32;
    let mut counts = vec![0usize; bucket_count];
    let mut positives = vec![0usize; bucket_count];
    let mut positive_total = 0usize;

    for sample in samples {
        assert!(
            (sample.point as usize) < (1usize << total_dim),
            "sample point outside ambient universe"
        );
        let bucket = (sample.point & bucket_mask) as usize;
        counts[bucket] += 1;
        if sample.label {
            positives[bucket] += 1;
            positive_total += 1;
        }
    }

    let global_label_rate = rate(positive_total, samples.len());
    let mut observed_bucket_count = 0usize;
    let mut bucket_rate_variance_sum = 0.0;
    let mut matched_random_variance_sum = 0.0;

    for (&count, &positive_count) in counts.iter().zip(positives.iter()) {
        if count == 0 {
            continue;
        }
        observed_bucket_count += 1;
        let bucket_rate = positive_count as f64 / count as f64;
        let deviation = bucket_rate - global_label_rate;
        bucket_rate_variance_sum += deviation * deviation;
        matched_random_variance_sum += global_label_rate * (1.0 - global_label_rate) / count as f64;
    }

    let observed_denom = observed_bucket_count.max(1) as f64;
    let bucket_rate_variance = bucket_rate_variance_sum / observed_denom;
    let matched_random_variance = matched_random_variance_sum / observed_denom;
    let projected_secret_bucket_count = secret
        .iter()
        .map(|point| (point & bucket_mask) as usize)
        .collect::<HashSet<_>>()
        .len();

    BucketCertificateTrialResult {
        n,
        total_dim,
        sample_count: samples.len(),
        noise_rate: 0.0,
        trials: 1,
        bucket_bits,
        bucket_count,
        avg_observed_bucket_count: observed_bucket_count as f64,
        avg_bucket_sample_count: if observed_bucket_count == 0 {
            0.0
        } else {
            samples.len() as f64 / observed_bucket_count as f64
        },
        avg_global_label_rate: global_label_rate,
        avg_bucket_rate_variance: bucket_rate_variance,
        avg_matched_random_variance: matched_random_variance,
        avg_excess_bucket_rate_variance: bucket_rate_variance - matched_random_variance,
        avg_projected_secret_bucket_count: projected_secret_bucket_count as f64,
        avg_projected_secret_bucket_fraction: projected_secret_bucket_count as f64
            / bucket_count as f64,
        seed: 0,
    }
}

pub fn run_bucket_certificate_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    bucket_bits: usize,
    seed: u64,
) -> BucketCertificateTrialResult {
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut observed_bucket_count_sum = 0.0;
    let mut bucket_sample_count_sum = 0.0;
    let mut global_label_rate_sum = 0.0;
    let mut bucket_rate_variance_sum = 0.0;
    let mut matched_random_variance_sum = 0.0;
    let mut excess_bucket_rate_variance_sum = 0.0;
    let mut projected_secret_bucket_count_sum = 0.0;
    let mut projected_secret_bucket_fraction_sum = 0.0;

    for _ in 0..trials {
        let secret = random_lagrangian(n, 8 * total_dim.max(1), &mut rng);
        let samples = sample_lsn(&secret, sample_count, noise_rate, total_dim, &mut rng);
        let result = bucket_rate_certificate(n, &samples, &secret, bucket_bits);

        observed_bucket_count_sum += result.avg_observed_bucket_count;
        bucket_sample_count_sum += result.avg_bucket_sample_count;
        global_label_rate_sum += result.avg_global_label_rate;
        bucket_rate_variance_sum += result.avg_bucket_rate_variance;
        matched_random_variance_sum += result.avg_matched_random_variance;
        excess_bucket_rate_variance_sum += result.avg_excess_bucket_rate_variance;
        projected_secret_bucket_count_sum += result.avg_projected_secret_bucket_count;
        projected_secret_bucket_fraction_sum += result.avg_projected_secret_bucket_fraction;
    }

    let denom = trials.max(1) as f64;
    BucketCertificateTrialResult {
        n,
        total_dim,
        sample_count,
        noise_rate,
        trials,
        bucket_bits,
        bucket_count: 1usize << bucket_bits,
        avg_observed_bucket_count: observed_bucket_count_sum / denom,
        avg_bucket_sample_count: bucket_sample_count_sum / denom,
        avg_global_label_rate: global_label_rate_sum / denom,
        avg_bucket_rate_variance: bucket_rate_variance_sum / denom,
        avg_matched_random_variance: matched_random_variance_sum / denom,
        avg_excess_bucket_rate_variance: excess_bucket_rate_variance_sum / denom,
        avg_projected_secret_bucket_count: projected_secret_bucket_count_sum / denom,
        avg_projected_secret_bucket_fraction: projected_secret_bucket_fraction_sum / denom,
        seed,
    }
}

pub fn bkw_xor_noise_rate(noise_rate: f64) -> f64 {
    assert!(
        (0.0..=0.5).contains(&noise_rate),
        "noise rate must be in [0, 0.5]"
    );
    2.0 * noise_rate * (1.0 - noise_rate)
}

pub fn bkw_noise_after_rounds(initial_noise_rate: f64, rounds: usize) -> f64 {
    let mut noise_rate = initial_noise_rate;
    for _ in 0..rounds {
        noise_rate = bkw_xor_noise_rate(noise_rate);
    }
    noise_rate
}

pub fn bkw_noise_model(initial_noise_rates: &[f64], max_rounds: usize) -> Vec<BkwNoiseModelRow> {
    let mut rows = Vec::new();
    for &initial_noise_rate in initial_noise_rates {
        assert!(
            (0.0..=0.5).contains(&initial_noise_rate),
            "noise rate must be in [0, 0.5]"
        );
        for rounds in 0..=max_rounds {
            let effective_noise_rate = bkw_noise_after_rounds(initial_noise_rate, rounds);
            let bias = 1.0 - 2.0 * effective_noise_rate;
            rows.push(BkwNoiseModelRow {
                initial_noise_rate,
                rounds,
                xor_width: 1usize << rounds,
                effective_noise_rate,
                bias,
                signal_retention: bias.abs(),
            });
        }
    }
    rows
}

pub fn run_bkw_bucket_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    bucket_bits: usize,
    pair_limit_per_bucket: usize,
    seed: u64,
) -> BkwBucketTrialResult {
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut pair_sum = 0.0;
    let mut label_xor_rate_sum = 0.0;
    let mut matched_random_xor_rate_sum = 0.0;
    let mut label_xor_excess_sum = 0.0;
    let mut delta_equal_sum = 0.0;
    let mut delta_unequal_sum = 0.0;

    for _ in 0..trials {
        let secret = random_lagrangian(n, 8 * total_dim.max(1), &mut rng);
        let samples = sample_lsn(&secret, sample_count, noise_rate, total_dim, &mut rng);
        let result =
            bkw_bucket_observable(n, &samples, &secret, bucket_bits, pair_limit_per_bucket);
        pair_sum += result.avg_pairs;
        label_xor_rate_sum += result.avg_label_xor_rate;
        matched_random_xor_rate_sum += result.avg_matched_random_xor_rate;
        label_xor_excess_sum += result.avg_label_xor_excess;
        delta_equal_sum += result.avg_delta_in_secret_when_label_equal;
        delta_unequal_sum += result.avg_delta_in_secret_when_label_unequal;
    }

    let denom = trials.max(1) as f64;
    BkwBucketTrialResult {
        n,
        total_dim,
        sample_count,
        noise_rate,
        trials,
        bucket_bits,
        pair_limit_per_bucket,
        avg_pairs: pair_sum / denom,
        avg_label_xor_rate: label_xor_rate_sum / denom,
        avg_matched_random_xor_rate: matched_random_xor_rate_sum / denom,
        avg_label_xor_excess: label_xor_excess_sum / denom,
        delta_in_secret_floor: 2f64.powi(-(n as i32)),
        avg_delta_in_secret_when_label_equal: delta_equal_sum / denom,
        avg_delta_in_secret_when_label_unequal: delta_unequal_sum / denom,
        seed,
    }
}

pub fn brute_force_ml_decode(samples: &[LsnSample], lagrangians: &[Lagrangian]) -> MlGuess {
    assert!(!lagrangians.is_empty(), "candidate set must be nonempty");

    let mut best_index = 0;
    let mut best_score = 0;
    let mut runner_up_score = 0;

    for (index, lagrangian) in lagrangians.iter().enumerate() {
        let score = samples
            .iter()
            .filter(|sample| lagrangian.contains(&sample.point) == sample.label)
            .count();

        if score > best_score {
            runner_up_score = best_score;
            best_score = score;
            best_index = index;
        } else if score > runner_up_score {
            runner_up_score = score;
        }
    }

    MlGuess {
        best_index,
        best_score,
        runner_up_score,
    }
}

pub fn compact_ml_decode(samples: &[LsnSample], compact: &CompactLagrangians) -> MlGuess {
    assert!(!compact.is_empty(), "candidate set must be nonempty");

    let mut best_index = 0;
    let mut best_score = i32::MIN;
    let mut runner_up_score = i32::MIN;

    for (index, score) in compact_ml_scores(samples, compact).into_iter().enumerate() {
        if score > best_score {
            runner_up_score = best_score;
            best_score = score;
            best_index = index;
        } else if score > runner_up_score {
            runner_up_score = score;
        }
    }

    MlGuess {
        best_index,
        best_score: best_score as usize,
        runner_up_score: runner_up_score.max(0) as usize,
    }
}

pub fn run_sampled_candidate_ml_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    candidate_count: usize,
    seed: u64,
) -> SampledCandidateMlTrialResult {
    assert!(
        candidate_count >= 2,
        "candidate_count must include at least secret plus one decoy"
    );
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut successes = 0usize;
    let mut secret_score_sum = 0i64;
    let mut best_false_score_sum = 0i64;
    let mut secret_margin_sum = 0i64;

    for _ in 0..trials {
        let secret = random_lagrangian(n, 8 * total_dim.max(1), &mut rng);
        let samples = sample_lsn(&secret, sample_count, noise_rate, total_dim, &mut rng);
        let mut candidates = Vec::with_capacity(candidate_count);
        candidates.push(secret);
        for _ in 1..candidate_count {
            candidates.push(random_lagrangian(n, 8 * total_dim.max(1), &mut rng));
        }

        let compact = CompactLagrangians::from_lagrangians(n, &candidates);
        let scores = compact_ml_scores(&samples, &compact);
        let secret_score = scores[0];
        let mut best_index = 0usize;
        let mut best_score = i32::MIN;
        let mut best_false_score = i32::MIN;
        for (index, &score) in scores.iter().enumerate() {
            if score > best_score {
                best_score = score;
                best_index = index;
            }
            if index != 0 && score > best_false_score {
                best_false_score = score;
            }
        }

        if best_index == 0 {
            successes += 1;
        }
        secret_score_sum += secret_score as i64;
        best_false_score_sum += best_false_score as i64;
        secret_margin_sum += (secret_score - best_false_score) as i64;
    }

    let denom = trials.max(1) as f64;
    SampledCandidateMlTrialResult {
        n,
        total_dim,
        sample_count,
        noise_rate,
        trials,
        candidate_count,
        successes,
        avg_secret_score: secret_score_sum as f64 / denom,
        avg_best_false_score: best_false_score_sum as f64 / denom,
        avg_secret_margin: secret_margin_sum as f64 / denom,
        seed,
    }
}

pub fn run_sampled_candidate_ml_budget_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    candidate_counts: &[usize],
    seed: u64,
) -> Vec<SampledCandidateMlTrialResult> {
    assert!(
        !candidate_counts.is_empty(),
        "candidate count list must be nonempty"
    );
    assert!(
        candidate_counts.iter().all(|&count| count >= 2),
        "candidate counts must include at least secret plus one decoy"
    );

    let total_dim = 2 * n;
    let universe = 1usize << total_dim;
    let max_candidate_count = *candidate_counts.iter().max().unwrap();
    let mut rng = XorShift64::new(seed);
    let mut successes = vec![0usize; candidate_counts.len()];
    let mut secret_score_sums = vec![0i64; candidate_counts.len()];
    let mut best_false_score_sums = vec![0i64; candidate_counts.len()];
    let mut secret_margin_sums = vec![0i64; candidate_counts.len()];

    for _ in 0..trials {
        let secret_basis = random_lagrangian_basis(n, 8 * total_dim.max(1), &mut rng);
        let secret_points = points_from_basis(&secret_basis);
        let secret = secret_points.iter().copied().collect::<Lagrangian>();
        let samples = sample_lsn(&secret, sample_count, noise_rate, total_dim, &mut rng);

        let mut rows = Vec::with_capacity(max_candidate_count);
        rows.push(secret_points);
        for _ in 1..max_candidate_count {
            let basis = random_lagrangian_basis(n, 8 * total_dim.max(1), &mut rng);
            rows.push(points_from_basis(&basis));
        }
        let compact = CompactLagrangians {
            n,
            total_dim,
            universe,
            rows,
        };
        let scores = compact_ml_scores(&samples, &compact);
        let secret_score = scores[0];

        for (index, &candidate_count) in candidate_counts.iter().enumerate() {
            let mut best_index = 0usize;
            let mut best_score = i32::MIN;
            let mut best_false_score = i32::MIN;

            for (candidate_index, &score) in scores[..candidate_count].iter().enumerate() {
                if score > best_score {
                    best_score = score;
                    best_index = candidate_index;
                }
                if candidate_index != 0 && score > best_false_score {
                    best_false_score = score;
                }
            }

            if best_index == 0 {
                successes[index] += 1;
            }
            secret_score_sums[index] += secret_score as i64;
            best_false_score_sums[index] += best_false_score as i64;
            secret_margin_sums[index] += (secret_score - best_false_score) as i64;
        }
    }

    let denom = trials.max(1) as f64;
    candidate_counts
        .iter()
        .enumerate()
        .map(|(index, &candidate_count)| SampledCandidateMlTrialResult {
            n,
            total_dim,
            sample_count,
            noise_rate,
            trials,
            candidate_count,
            successes: successes[index],
            avg_secret_score: secret_score_sums[index] as f64 / denom,
            avg_best_false_score: best_false_score_sums[index] as f64 / denom,
            avg_secret_margin: secret_margin_sums[index] as f64 / denom,
            seed: seed ^ candidate_count as u64,
        })
        .collect()
}

pub fn run_sampled_candidate_ambient_ml_trials(
    n: usize,
    sample_ratios: &[f64],
    noise_rates: &[f64],
    trials: usize,
    seed: u64,
) -> Vec<SampledCandidateMlTrialResult> {
    run_sampled_candidate_ambient_ml_trials_with_optional_cap(
        n,
        sample_ratios,
        noise_rates,
        trials,
        None,
        seed,
    )
}

pub fn run_sampled_candidate_ambient_ml_trials_with_cap(
    n: usize,
    sample_ratios: &[f64],
    noise_rates: &[f64],
    trials: usize,
    candidate_cap: usize,
    seed: u64,
) -> Vec<SampledCandidateMlTrialResult> {
    run_sampled_candidate_ambient_ml_trials_with_optional_cap(
        n,
        sample_ratios,
        noise_rates,
        trials,
        Some(candidate_cap),
        seed,
    )
}

fn run_sampled_candidate_ambient_ml_trials_with_optional_cap(
    n: usize,
    sample_ratios: &[f64],
    noise_rates: &[f64],
    trials: usize,
    candidate_cap: Option<usize>,
    seed: u64,
) -> Vec<SampledCandidateMlTrialResult> {
    assert!(n > 0, "n must be positive");
    assert!(
        sample_ratios.iter().all(|ratio| *ratio > 0.0),
        "sample ratios must be positive"
    );
    assert!(
        noise_rates.iter().all(|p| (0.0..=0.5).contains(p)),
        "noise rates must be in [0, 0.5]"
    );

    let base = 1usize << (2 * n);
    let candidate_count = candidate_cap.unwrap_or(base).min(base);
    assert!(
        candidate_count >= 2,
        "candidate cap must leave at least secret plus one decoy"
    );
    let mut results = Vec::new();
    for &ratio in sample_ratios {
        let sample_count = ((base as f64) * ratio).round() as usize;
        for &noise_rate in noise_rates {
            results.extend(run_sampled_candidate_ml_budget_trials(
                n,
                sample_count,
                noise_rate,
                trials,
                &[candidate_count],
                seed ^ ((n as u64) << 44) ^ sample_count as u64 ^ noise_rate.to_bits(),
            ));
        }
    }
    results
}

pub fn run_sampled_candidate_false_max_budget_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    candidate_counts: &[usize],
    seed: u64,
) -> Vec<SampledCandidateFalseMaxTrialResult> {
    assert!(
        !candidate_counts.is_empty(),
        "candidate count list must be nonempty"
    );
    assert!(
        candidate_counts.iter().all(|&count| count >= 1),
        "candidate counts must include at least one decoy"
    );

    let total_dim = 2 * n;
    let universe = 1usize << total_dim;
    let max_candidate_count = *candidate_counts.iter().max().unwrap();
    let mut rng = XorShift64::new(seed);
    let mut secret_score_sums = vec![0i64; candidate_counts.len()];
    let mut best_false_score_sums = vec![0i64; candidate_counts.len()];
    let mut secret_margin_sums = vec![0i64; candidate_counts.len()];

    for _ in 0..trials {
        let secret_basis = random_lagrangian_basis(n, 8 * total_dim.max(1), &mut rng);
        let secret_points = points_from_basis(&secret_basis);
        let secret = secret_points.iter().copied().collect::<Lagrangian>();
        let samples = sample_lsn(&secret, sample_count, noise_rate, total_dim, &mut rng);

        let mut rows = Vec::with_capacity(max_candidate_count + 1);
        rows.push(secret_points);
        for _ in 0..max_candidate_count {
            let basis = random_lagrangian_basis(n, 8 * total_dim.max(1), &mut rng);
            rows.push(points_from_basis(&basis));
        }

        let compact = CompactLagrangians {
            n,
            total_dim,
            universe,
            rows,
        };
        let scores = compact_ml_scores(&samples, &compact);
        let secret_score = scores[0];

        for (index, &candidate_count) in candidate_counts.iter().enumerate() {
            let best_false_score = scores[1..=candidate_count]
                .iter()
                .copied()
                .max()
                .expect("candidate_count >= 1");

            secret_score_sums[index] += secret_score as i64;
            best_false_score_sums[index] += best_false_score as i64;
            secret_margin_sums[index] += (secret_score - best_false_score) as i64;
        }
    }

    let denom = trials.max(1) as f64;
    candidate_counts
        .iter()
        .enumerate()
        .map(
            |(index, &candidate_count)| SampledCandidateFalseMaxTrialResult {
                n,
                total_dim,
                sample_count,
                noise_rate,
                trials,
                candidate_count,
                avg_secret_score: secret_score_sums[index] as f64 / denom,
                avg_best_false_score: best_false_score_sums[index] as f64 / denom,
                avg_secret_margin_to_false_max: secret_margin_sums[index] as f64 / denom,
                seed: seed ^ candidate_count as u64,
            },
        )
        .collect()
}

pub fn span_of_positives_decode(
    n: usize,
    samples: &[LsnSample],
    lagrangians: &[Lagrangian],
) -> SpanAttackResult {
    let total_dim = 2 * n;
    let positives = samples
        .iter()
        .filter(|sample| sample.label)
        .map(|sample| sample.point)
        .collect::<Vec<_>>();
    let basis = gf2_basis(&positives, total_dim);
    let span_rank = basis.len();

    let recovered_index = if span_rank == n {
        let positive_span = span_from_basis(&basis);
        lagrangians
            .iter()
            .position(|lagrangian| *lagrangian == positive_span)
    } else {
        None
    };

    SpanAttackResult {
        n,
        total_dim,
        positive_count: positives.len(),
        span_rank,
        recovered_index,
    }
}

pub fn run_span_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    seed: u64,
) -> SpanTrialResult {
    let lagrangians = enumerate_lagrangians(n);
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut successes = 0;
    let mut rank_n_count = 0;
    let mut overfull_rank_count = 0;
    let mut full_rank_count = 0;
    let mut positive_count_sum = 0usize;
    let mut span_rank_sum = 0usize;

    for _ in 0..trials {
        let secret_index = rng.next_index(lagrangians.len());
        let samples = sample_lsn(
            &lagrangians[secret_index],
            sample_count,
            noise_rate,
            total_dim,
            &mut rng,
        );
        let result = span_of_positives_decode(n, &samples, &lagrangians);
        if result.recovered_index == Some(secret_index) {
            successes += 1;
        }
        if result.span_rank == n {
            rank_n_count += 1;
        }
        if result.span_rank > n {
            overfull_rank_count += 1;
        }
        if result.span_rank == total_dim {
            full_rank_count += 1;
        }
        positive_count_sum += result.positive_count;
        span_rank_sum += result.span_rank;
    }

    let denom = trials.max(1) as f64;
    SpanTrialResult {
        n,
        lagrangians: lagrangians.len(),
        sample_count,
        noise_rate,
        trials,
        successes,
        rank_n_count,
        overfull_rank_count,
        full_rank_count,
        avg_positive_count: positive_count_sum as f64 / denom,
        avg_span_rank: span_rank_sum as f64 / denom,
        seed,
    }
}

pub fn positive_basis_isd_decode(
    n: usize,
    samples: &[LsnSample],
    lagrangians: &[Lagrangian],
    max_attempts: usize,
    rng: &mut XorShift64,
) -> IsdAttackResult {
    let total_dim = 2 * n;
    let positives = samples
        .iter()
        .filter(|sample| sample.label)
        .map(|sample| sample.point)
        .collect::<Vec<_>>();

    let mut attempts_used = 0;
    let mut valid_candidates = 0;
    let mut best_score = 0;
    let mut recovered_index = None;

    let all_positive_basis = gf2_basis(&positives, total_dim);
    if all_positive_basis.len() == n && is_isotropic_basis(&all_positive_basis, n) {
        attempts_used += 1;
        if let Some(index) = candidate_index_from_basis(&all_positive_basis, lagrangians) {
            valid_candidates += 1;
            best_score = score_lagrangian(&lagrangians[index], samples);
            recovered_index = Some(index);
        }
    }

    if positives.len() >= n {
        for _ in 0..max_attempts {
            attempts_used += 1;
            let subset = sample_positive_subset(&positives, n, rng);
            let basis = gf2_basis(&subset, total_dim);
            if basis.len() != n || !is_isotropic_basis(&basis, n) {
                continue;
            }
            if let Some(index) = candidate_index_from_basis(&basis, lagrangians) {
                valid_candidates += 1;
                let score = score_lagrangian(&lagrangians[index], samples);
                if score > best_score {
                    best_score = score;
                    recovered_index = Some(index);
                }
            }
        }
    }

    IsdAttackResult {
        n,
        total_dim,
        positive_count: positives.len(),
        attempts_used,
        valid_candidates,
        best_score,
        recovered_index,
    }
}

pub fn run_isd_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    max_attempts: usize,
    seed: u64,
) -> IsdTrialResult {
    let lagrangians = enumerate_lagrangians(n);
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut successes = 0;
    let mut positive_count_sum = 0usize;
    let mut attempts_used_sum = 0usize;
    let mut valid_candidates_sum = 0usize;
    let mut best_score_sum = 0usize;

    for _ in 0..trials {
        let secret_index = rng.next_index(lagrangians.len());
        let samples = sample_lsn(
            &lagrangians[secret_index],
            sample_count,
            noise_rate,
            total_dim,
            &mut rng,
        );
        let result = positive_basis_isd_decode(n, &samples, &lagrangians, max_attempts, &mut rng);
        if result.recovered_index == Some(secret_index) {
            successes += 1;
        }
        positive_count_sum += result.positive_count;
        attempts_used_sum += result.attempts_used;
        valid_candidates_sum += result.valid_candidates;
        best_score_sum += result.best_score;
    }

    let denom = trials.max(1) as f64;
    IsdTrialResult {
        n,
        lagrangians: lagrangians.len(),
        sample_count,
        noise_rate,
        trials,
        max_attempts,
        successes,
        avg_positive_count: positive_count_sum as f64 / denom,
        avg_attempts_used: attempts_used_sum as f64 / denom,
        avg_valid_candidates: valid_candidates_sum as f64 / denom,
        avg_best_score: best_score_sum as f64 / denom,
        seed,
    }
}

pub fn run_isd_budget_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    attempt_budgets: &[usize],
    seed: u64,
) -> Vec<IsdTrialResult> {
    assert!(
        !attempt_budgets.is_empty(),
        "attempt budget list must be nonempty"
    );
    let lagrangians = enumerate_lagrangians(n);
    let total_dim = 2 * n;
    let mut instance_rng = XorShift64::new(seed);
    let mut successes = vec![0usize; attempt_budgets.len()];
    let mut positive_count_sums = vec![0usize; attempt_budgets.len()];
    let mut attempts_used_sums = vec![0usize; attempt_budgets.len()];
    let mut valid_candidate_sums = vec![0usize; attempt_budgets.len()];
    let mut best_score_sums = vec![0usize; attempt_budgets.len()];

    for trial_index in 0..trials {
        let secret_index = instance_rng.next_index(lagrangians.len());
        let samples = sample_lsn(
            &lagrangians[secret_index],
            sample_count,
            noise_rate,
            total_dim,
            &mut instance_rng,
        );

        for (budget_index, &max_attempts) in attempt_budgets.iter().enumerate() {
            let mut attack_rng =
                XorShift64::new(seed ^ ((trial_index as u64) << 32) ^ ((max_attempts as u64) << 1));
            let result =
                positive_basis_isd_decode(n, &samples, &lagrangians, max_attempts, &mut attack_rng);
            if result.recovered_index == Some(secret_index) {
                successes[budget_index] += 1;
            }
            positive_count_sums[budget_index] += result.positive_count;
            attempts_used_sums[budget_index] += result.attempts_used;
            valid_candidate_sums[budget_index] += result.valid_candidates;
            best_score_sums[budget_index] += result.best_score;
        }
    }

    let denom = trials.max(1) as f64;
    attempt_budgets
        .iter()
        .enumerate()
        .map(|(budget_index, &max_attempts)| IsdTrialResult {
            n,
            lagrangians: lagrangians.len(),
            sample_count,
            noise_rate,
            trials,
            max_attempts,
            successes: successes[budget_index],
            avg_positive_count: positive_count_sums[budget_index] as f64 / denom,
            avg_attempts_used: attempts_used_sums[budget_index] as f64 / denom,
            avg_valid_candidates: valid_candidate_sums[budget_index] as f64 / denom,
            avg_best_score: best_score_sums[budget_index] as f64 / denom,
            seed: seed ^ max_attempts as u64,
        })
        .collect()
}

pub fn sampled_candidate_ml_model_row(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    candidate_count: usize,
) -> SampledCandidateMlModelRow {
    assert!(n > 0, "n must be positive");
    assert!(
        (0.0..=0.5).contains(&noise_rate),
        "noise rate must be in [0, 0.5]"
    );
    assert!(
        candidate_count >= 2,
        "candidate_count must include at least one decoy"
    );

    let total_dim = 2 * n;
    let q = 2f64.powi(-(n as i32));
    let disagreement_rate = 2.0 * q * (1.0 - q);
    let bias = 1.0 - 2.0 * noise_rate;
    let mean_per_sample = bias * disagreement_rate;
    let variance_per_sample = (disagreement_rate - mean_per_sample * mean_per_sample).max(0.0);
    let mean_pair_margin = sample_count as f64 * mean_per_sample;
    let sigma_pair_margin = (sample_count as f64 * variance_per_sample).sqrt();
    let decoy_count = (candidate_count - 1) as f64;
    let extreme_value_penalty = if decoy_count <= 1.0 {
        0.0
    } else {
        sigma_pair_margin * (2.0 * decoy_count.ln()).sqrt()
    };

    SampledCandidateMlModelRow {
        n,
        total_dim,
        sample_count,
        noise_rate,
        candidate_count,
        disagreement_rate,
        mean_pair_margin,
        sigma_pair_margin,
        extreme_value_penalty,
        predicted_secret_margin: mean_pair_margin - extreme_value_penalty,
    }
}

pub fn sampled_candidate_ml_model(
    n_start: usize,
    n_end: usize,
    ratios: &[f64],
    noise_rates: &[f64],
    candidate_counts: &[usize],
) -> Vec<SampledCandidateMlModelRow> {
    assert!(
        n_start > 0 && n_end >= n_start,
        "require 1 <= n_start <= n_end"
    );
    assert!(
        ratios.iter().all(|ratio| *ratio > 0.0),
        "ratios must be positive"
    );
    let mut rows = Vec::new();
    for n in n_start..=n_end {
        let base = 1usize << (2 * n);
        for &ratio in ratios {
            let sample_count = ((base as f64) * ratio).round() as usize;
            for &noise_rate in noise_rates {
                for &candidate_count in candidate_counts {
                    rows.push(sampled_candidate_ml_model_row(
                        n,
                        sample_count,
                        noise_rate,
                        candidate_count,
                    ));
                }
            }
        }
    }
    rows
}

pub fn run_ml_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    seed: u64,
) -> MlTrialResult {
    let lagrangians = enumerate_lagrangians(n);
    let compact = CompactLagrangians::from_lagrangians(n, &lagrangians);
    let total_dim = 2 * n;
    let mut rng = XorShift64::new(seed);
    let mut successes = 0;

    for _ in 0..trials {
        let secret_index = rng.next_index(lagrangians.len());
        let samples = sample_lsn(
            &lagrangians[secret_index],
            sample_count,
            noise_rate,
            total_dim,
            &mut rng,
        );
        let guess = compact_ml_decode(&samples, &compact);
        if guess.best_index == secret_index {
            successes += 1;
        }
    }

    MlTrialResult {
        n,
        lagrangians: lagrangians.len(),
        sample_count,
        noise_rate,
        trials,
        successes,
        seed,
    }
}

pub fn results_to_json(experiment: &str, results: &[MlTrialResult]) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"brute_force_ml_over_lagrangians\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels\",\n",
    );
    out.push_str("  \"adjudication\": \"P2 empirical cryptanalysis harness; evidence, not proof; OPEN = LSN\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"lagrangians\": {},\n", result.lagrangians));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"successes\": {},\n", result.successes));
        out.push_str(&format!(
            "      \"success_rate\": {:.10},\n",
            result.success_rate()
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn sampled_candidate_ml_results_to_json(
    experiment: &str,
    results: &[SampledCandidateMlTrialResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"sampled_candidate_ml_planted_secret\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels; experiment plants the secret among random Lagrangian decoys to measure ML score separation without full orbit enumeration\",\n",
    );
    out.push_str("  \"adjudication\": \"P2 sampled-candidate ML screen; evidence, not proof; OPEN = LSN\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"total_dim\": {},\n", result.total_dim));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!(
            "      \"candidate_count\": {},\n",
            result.candidate_count
        ));
        out.push_str(&format!("      \"successes\": {},\n", result.successes));
        out.push_str(&format!(
            "      \"success_rate\": {:.10},\n",
            result.success_rate()
        ));
        out.push_str(&format!(
            "      \"avg_secret_score\": {:.6},\n",
            result.avg_secret_score
        ));
        out.push_str(&format!(
            "      \"avg_best_false_score\": {:.6},\n",
            result.avg_best_false_score
        ));
        out.push_str(&format!(
            "      \"avg_secret_margin\": {:.6},\n",
            result.avg_secret_margin
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn sampled_candidate_false_max_results_to_json(
    experiment: &str,
    results: &[SampledCandidateFalseMaxTrialResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"control\": \"sampled_candidate_false_max_unplanted\",\n");
    out.push_str("  \"threat_model\": \"attacker candidate set is all random decoy Lagrangians; the secret is scored only as an external reference and is not a candidate\",\n");
    out.push_str(
        "  \"adjudication\": \"P2 false-max calibration; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"total_dim\": {},\n", result.total_dim));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!(
            "      \"candidate_count\": {},\n",
            result.candidate_count
        ));
        out.push_str(&format!(
            "      \"avg_secret_score\": {:.6},\n",
            result.avg_secret_score
        ));
        out.push_str(&format!(
            "      \"avg_best_false_score\": {:.6},\n",
            result.avg_best_false_score
        ));
        out.push_str(&format!(
            "      \"avg_secret_margin_to_false_max\": {:.6},\n",
            result.avg_secret_margin_to_false_max
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn sampled_candidate_ml_model_to_json(
    experiment: &str,
    rows: &[SampledCandidateMlModelRow],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"model\": \"sampled_candidate_ml_extreme_value_proxy\",\n");
    out.push_str(
        "  \"assumption\": \"independent random decoy Lagrangian disagreement proxy; false-max penalty sigma*sqrt(2 ln(candidate_count-1))\",\n",
    );
    out.push_str("  \"adjudication\": \"P2 planted-candidate ML interpretation model; evidence, not proof; OPEN = LSN\",\n");
    out.push_str("  \"results\": [\n");
    for (i, row) in rows.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", row.n));
        out.push_str(&format!("      \"total_dim\": {},\n", row.total_dim));
        out.push_str(&format!("      \"sample_count\": {},\n", row.sample_count));
        out.push_str(&format!("      \"noise_rate\": {:.10},\n", row.noise_rate));
        out.push_str(&format!(
            "      \"candidate_count\": {},\n",
            row.candidate_count
        ));
        out.push_str(&format!(
            "      \"disagreement_rate\": {:.12},\n",
            row.disagreement_rate
        ));
        out.push_str(&format!(
            "      \"mean_pair_margin\": {:.6},\n",
            row.mean_pair_margin
        ));
        out.push_str(&format!(
            "      \"sigma_pair_margin\": {:.6},\n",
            row.sigma_pair_margin
        ));
        out.push_str(&format!(
            "      \"extreme_value_penalty\": {:.6},\n",
            row.extreme_value_penalty
        ));
        out.push_str(&format!(
            "      \"predicted_secret_margin\": {:.6}\n",
            row.predicted_secret_margin
        ));
        out.push_str("    }");
        if i + 1 != rows.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn span_results_to_json(experiment: &str, results: &[SpanTrialResult]) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"span_of_positives\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels\",\n",
    );
    out.push_str("  \"adjudication\": \"P2 negative control; low-noise sanity plus constant-rate failure; evidence, not proof; OPEN = LSN\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"lagrangians\": {},\n", result.lagrangians));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"successes\": {},\n", result.successes));
        out.push_str(&format!(
            "      \"success_rate\": {:.10},\n",
            result.success_rate()
        ));
        out.push_str(&format!(
            "      \"rank_n_count\": {},\n",
            result.rank_n_count
        ));
        out.push_str(&format!(
            "      \"overfull_rank_count\": {},\n",
            result.overfull_rank_count
        ));
        out.push_str(&format!(
            "      \"full_rank_count\": {},\n",
            result.full_rank_count
        ));
        out.push_str(&format!(
            "      \"avg_positive_count\": {:.6},\n",
            result.avg_positive_count
        ));
        out.push_str(&format!(
            "      \"avg_span_rank\": {:.6},\n",
            result.avg_span_rank
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn isd_results_to_json(experiment: &str, results: &[IsdTrialResult]) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"positive_basis_isd\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels\",\n",
    );
    out.push_str("  \"adjudication\": \"P2 negative control; low-noise sanity plus constant-rate capped-attempt screen; evidence, not proof; OPEN = LSN\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"lagrangians\": {},\n", result.lagrangians));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!(
            "      \"max_attempts\": {},\n",
            result.max_attempts
        ));
        out.push_str(&format!("      \"successes\": {},\n", result.successes));
        out.push_str(&format!(
            "      \"success_rate\": {:.10},\n",
            result.success_rate()
        ));
        out.push_str(&format!(
            "      \"avg_positive_count\": {:.6},\n",
            result.avg_positive_count
        ));
        out.push_str(&format!(
            "      \"avg_attempts_used\": {:.6},\n",
            result.avg_attempts_used
        ));
        out.push_str(&format!(
            "      \"avg_valid_candidates\": {:.6},\n",
            result.avg_valid_candidates
        ));
        out.push_str(&format!(
            "      \"avg_best_score\": {:.6},\n",
            result.avg_best_score
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn bkw_results_to_json(experiment: &str, results: &[BkwBucketTrialResult]) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"bkw_bucket_pair_observable\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels; secret only used for diagnostic enrichment\",\n",
    );
    out.push_str(
        "  \"adjudication\": \"P2 BKW adaptation screen; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"total_dim\": {},\n", result.total_dim));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"bucket_bits\": {},\n", result.bucket_bits));
        out.push_str(&format!(
            "      \"pair_limit_per_bucket\": {},\n",
            result.pair_limit_per_bucket
        ));
        out.push_str(&format!("      \"avg_pairs\": {:.6},\n", result.avg_pairs));
        out.push_str(&format!(
            "      \"avg_label_xor_rate\": {:.10},\n",
            result.avg_label_xor_rate
        ));
        out.push_str(&format!(
            "      \"avg_matched_random_xor_rate\": {:.10},\n",
            result.avg_matched_random_xor_rate
        ));
        out.push_str(&format!(
            "      \"avg_label_xor_excess\": {:.10},\n",
            result.avg_label_xor_excess
        ));
        out.push_str(&format!(
            "      \"delta_in_secret_floor\": {:.10},\n",
            result.delta_in_secret_floor
        ));
        out.push_str(&format!(
            "      \"avg_delta_in_secret_when_label_equal\": {:.10},\n",
            result.avg_delta_in_secret_when_label_equal
        ));
        out.push_str(&format!(
            "      \"avg_delta_in_secret_when_label_unequal\": {:.10},\n",
            result.avg_delta_in_secret_when_label_unequal
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn bucket_certificate_results_to_json(
    experiment: &str,
    results: &[BucketCertificateTrialResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"attack\": \"bucket_positive_rate_certificate\",\n");
    out.push_str(
        "  \"threat_model\": \"attacker observes public points and noisy membership labels; secret only used for diagnostic projection-size reporting\",\n",
    );
    out.push_str(
        "  \"adjudication\": \"P2 non-xor certificate screen; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"n\": {},\n", result.n));
        out.push_str(&format!("      \"total_dim\": {},\n", result.total_dim));
        out.push_str(&format!(
            "      \"sample_count\": {},\n",
            result.sample_count
        ));
        out.push_str(&format!(
            "      \"noise_rate\": {:.10},\n",
            result.noise_rate
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"bucket_bits\": {},\n", result.bucket_bits));
        out.push_str(&format!(
            "      \"bucket_count\": {},\n",
            result.bucket_count
        ));
        out.push_str(&format!(
            "      \"avg_observed_bucket_count\": {:.6},\n",
            result.avg_observed_bucket_count
        ));
        out.push_str(&format!(
            "      \"avg_bucket_sample_count\": {:.6},\n",
            result.avg_bucket_sample_count
        ));
        out.push_str(&format!(
            "      \"avg_global_label_rate\": {:.10},\n",
            result.avg_global_label_rate
        ));
        out.push_str(&format!(
            "      \"avg_bucket_rate_variance\": {:.12},\n",
            result.avg_bucket_rate_variance
        ));
        out.push_str(&format!(
            "      \"avg_matched_random_variance\": {:.12},\n",
            result.avg_matched_random_variance
        ));
        out.push_str(&format!(
            "      \"avg_excess_bucket_rate_variance\": {:.12},\n",
            result.avg_excess_bucket_rate_variance
        ));
        out.push_str(&format!(
            "      \"avg_projected_secret_bucket_count\": {:.6},\n",
            result.avg_projected_secret_bucket_count
        ));
        out.push_str(&format!(
            "      \"avg_projected_secret_bucket_fraction\": {:.10},\n",
            result.avg_projected_secret_bucket_fraction
        ));
        out.push_str(&format!("      \"seed\": {}\n", result.seed));
        out.push_str("    }");
        if i + 1 != results.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn bkw_noise_model_to_json(experiment: &str, rows: &[BkwNoiseModelRow]) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"model\": \"bkw_label_xor_noise_growth\",\n");
    out.push_str("  \"recurrence\": \"p_{r+1}=2*p_r*(1-p_r); bias_{r+1}=bias_r^2\",\n");
    out.push_str(
        "  \"adjudication\": \"P2 BKW cost/noise model; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, row) in rows.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!(
            "      \"initial_noise_rate\": {:.10},\n",
            row.initial_noise_rate
        ));
        out.push_str(&format!("      \"rounds\": {},\n", row.rounds));
        out.push_str(&format!("      \"xor_width\": {},\n", row.xor_width));
        out.push_str(&format!(
            "      \"effective_noise_rate\": {:.10},\n",
            row.effective_noise_rate
        ));
        out.push_str(&format!("      \"bias\": {:.10},\n", row.bias));
        out.push_str(&format!(
            "      \"signal_retention\": {:.10}\n",
            row.signal_retention
        ));
        out.push_str("    }");
        if i + 1 != rows.len() {
            out.push(',');
        }
        out.push('\n');
    }
    out.push_str("  ]\n");
    out.push_str("}\n");
    out
}

pub fn lagrangian_count(n: usize) -> usize {
    (1..=n).map(|i| (1usize << i) + 1).product()
}

fn rate(numerator: usize, denominator: usize) -> f64 {
    if denominator == 0 {
        0.0
    } else {
        numerator as f64 / denominator as f64
    }
}

fn compact_ml_scores(samples: &[LsnSample], compact: &CompactLagrangians) -> Vec<i32> {
    let mut true_counts = vec![0i32; compact.universe];
    let mut false_counts = vec![0i32; compact.universe];
    let mut false_total = 0i32;

    for sample in samples {
        let point = sample.point as usize;
        assert!(
            point < compact.universe,
            "sample point outside compact universe"
        );
        if sample.label {
            true_counts[point] += 1;
        } else {
            false_counts[point] += 1;
            false_total += 1;
        }
    }

    compact
        .rows
        .iter()
        .map(|row| {
            let mut score = false_total;
            for &point in row {
                let point = point as usize;
                score += true_counts[point] - false_counts[point];
            }
            score
        })
        .collect()
}

fn escape_json(input: &str) -> String {
    input
        .chars()
        .flat_map(|c| match c {
            '"' => "\\\"".chars().collect::<Vec<_>>(),
            '\\' => "\\\\".chars().collect::<Vec<_>>(),
            '\n' => "\\n".chars().collect::<Vec<_>>(),
            '\r' => "\\r".chars().collect::<Vec<_>>(),
            '\t' => "\\t".chars().collect::<Vec<_>>(),
            _ => vec![c],
        })
        .collect()
}

fn standard_lagrangian(n: usize) -> Lagrangian {
    let mut out = BTreeSet::new();
    for coeffs in 0..(1usize << n) {
        let mut point = 0u32;
        for i in 0..n {
            if ((coeffs >> i) & 1) == 1 {
                point ^= 1u32 << (2 * i);
            }
        }
        out.insert(point);
    }
    out
}

fn random_lagrangian_basis(n: usize, walk_steps: usize, rng: &mut XorShift64) -> Vec<u32> {
    let mut basis = (0..n).map(|i| 1u32 << (2 * i)).collect::<Vec<_>>();
    let universe = 1usize << (2 * n);
    for _ in 0..walk_steps {
        let v = rng.next_index(universe) as u32;
        for basis_vec in &mut basis {
            *basis_vec = transvection(v, *basis_vec, n);
        }
    }
    basis
}

fn transvection_generators(n: usize) -> Vec<u32> {
    let mut generators = Vec::new();

    for i in 0..n {
        generators.push(1u32 << (2 * i));
        generators.push(1u32 << (2 * i + 1));
    }

    for i in 0..n {
        for j in (i + 1)..n {
            generators.push((1u32 << (2 * i)) | (1u32 << (2 * j)));
            generators.push((1u32 << (2 * i + 1)) | (1u32 << (2 * j + 1)));
        }
    }

    for i in 0..n {
        for j in 0..n {
            generators.push((1u32 << (2 * i)) | (1u32 << (2 * j + 1)));
        }
    }

    generators.sort_unstable();
    generators.dedup();
    generators
}

fn apply_transvection(lagrangian: &Lagrangian, v: u32, n: usize) -> Lagrangian {
    lagrangian
        .iter()
        .map(|&point| transvection(v, point, n))
        .collect()
}

fn is_isotropic_basis(basis: &[u32], n: usize) -> bool {
    basis
        .iter()
        .enumerate()
        .all(|(i, &a)| basis[i..].iter().all(|&b| !symplectic_form(a, b, n)))
}

fn candidate_index_from_basis(basis: &[u32], lagrangians: &[Lagrangian]) -> Option<usize> {
    let span = span_from_basis(basis);
    lagrangians
        .iter()
        .position(|lagrangian| *lagrangian == span)
}

fn score_lagrangian(lagrangian: &Lagrangian, samples: &[LsnSample]) -> usize {
    samples
        .iter()
        .filter(|sample| lagrangian.contains(&sample.point) == sample.label)
        .count()
}

fn sample_positive_subset(positives: &[u32], subset_len: usize, rng: &mut XorShift64) -> Vec<u32> {
    let mut chosen = Vec::with_capacity(subset_len);
    let mut used = HashSet::new();

    while chosen.len() < subset_len {
        let index = rng.next_index(positives.len());
        if used.insert(index) {
            chosen.push(positives[index]);
        }
    }

    chosen
}

fn gf2_basis(rows: &[u32], total_dim: usize) -> Vec<u32> {
    assert!(
        total_dim <= 32,
        "bitmask model supports dimension at most 32"
    );
    let mut basis_by_pivot = vec![0u32; total_dim];

    for &row in rows {
        let mut v = row;
        for col in (0..total_dim).rev() {
            if ((v >> col) & 1) == 0 {
                continue;
            }
            if basis_by_pivot[col] == 0 {
                basis_by_pivot[col] = v;
                break;
            }
            v ^= basis_by_pivot[col];
        }
    }

    basis_by_pivot.into_iter().filter(|&row| row != 0).collect()
}

fn span_from_basis(basis: &[u32]) -> Lagrangian {
    let mut out = BTreeSet::new();
    for coeffs in 0..(1usize << basis.len()) {
        let mut point = 0u32;
        for (i, &basis_vec) in basis.iter().enumerate() {
            if ((coeffs >> i) & 1) == 1 {
                point ^= basis_vec;
            }
        }
        out.insert(point);
    }
    out
}

fn points_from_basis(basis: &[u32]) -> Vec<u32> {
    let mut out = Vec::with_capacity(1usize << basis.len());
    for coeffs in 0..(1usize << basis.len()) {
        let mut point = 0u32;
        for (i, &basis_vec) in basis.iter().enumerate() {
            if ((coeffs >> i) & 1) == 1 {
                point ^= basis_vec;
            }
        }
        out.push(point);
    }
    out
}
