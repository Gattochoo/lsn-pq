use std::collections::HashSet;

#[derive(Clone, Debug)]
pub struct PolarCode {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub frozen: Vec<usize>,
    pub info_set: Vec<usize>,
    frozen_mask: Vec<bool>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct SimulationResult {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub trials: usize,
    pub errors: usize,
    pub seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ImportanceSamplingResult {
    pub n: usize,
    pub k: usize,
    pub target_p: f64,
    pub proposal_p: f64,
    pub trials: usize,
    pub proposal_errors: usize,
    pub weighted_bler_estimate: f64,
    pub mean_likelihood_ratio: f64,
    pub effective_sample_size: f64,
    pub seed: u64,
}

#[derive(Clone, Debug, PartialEq)]
pub struct PolarRateRow {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub rate: f64,
    pub bhattacharyya_sum_bound: f64,
    pub half_sum_bound: f64,
    pub log2_bhattacharyya_sum_bound: f64,
    pub log2_half_sum_bound: f64,
    pub target_log2_half_sum_bound: f64,
    pub passes_half_sum_target: bool,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SimulationConfig {
    pub n: usize,
    pub k: usize,
    pub p: f64,
    pub trials: usize,
    pub seed: u64,
}

impl SimulationResult {
    pub fn bler(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.errors as f64 / self.trials as f64
        }
    }

    pub fn zero_error_upper_95(&self) -> Option<f64> {
        if self.errors == 0 && self.trials > 0 {
            Some(zero_error_upper_bound(self.trials, 0.05))
        } else {
            None
        }
    }
}

impl ImportanceSamplingResult {
    pub fn proposal_error_rate(&self) -> f64 {
        if self.trials == 0 {
            0.0
        } else {
            self.proposal_errors as f64 / self.trials as f64
        }
    }
}

pub fn zero_error_upper_bound(trials: usize, alpha: f64) -> f64 {
    assert!(trials > 0, "trials must be positive");
    assert!((0.0..1.0).contains(&alpha), "alpha must be in (0, 1)");
    1.0 - alpha.powf(1.0 / trials as f64)
}

pub fn baseline_reproduction_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [
        (128, 16, 0.0706),
        (128, 16, 0.0343),
        (256, 32, 0.0706),
        (256, 32, 0.0343),
        (512, 64, 0.0706),
        (512, 64, 0.0343),
    ]
    .into_iter()
    .enumerate()
    .map(|(i, (n, k, p))| SimulationConfig {
        n,
        k,
        p,
        trials,
        seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
    })
    .collect()
}

pub fn target_n2048_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [(2048, 256, 0.0706), (2048, 256, 0.0343)]
        .into_iter()
        .enumerate()
        .map(|(i, (n, k, p))| SimulationConfig {
            n,
            k,
            p,
            trials,
            seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
        })
        .collect()
}

pub fn high_noise_control_configs(trials: usize, seed: u64) -> Vec<SimulationConfig> {
    [(2048, 256, 0.3), (2048, 256, 0.4), (2048, 256, 0.5)]
        .into_iter()
        .enumerate()
        .map(|(i, (n, k, p))| SimulationConfig {
            n,
            k,
            p,
            trials,
            seed: seed.wrapping_add((i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)),
        })
        .collect()
}

pub fn run_configs(configs: &[SimulationConfig]) -> Vec<SimulationResult> {
    configs
        .iter()
        .map(|cfg| simulate_bsc_sc(cfg.n, cfg.k, cfg.p, cfg.trials, cfg.seed))
        .collect()
}

pub fn results_to_json(experiment: &str, results: &[SimulationResult]) -> String {
    results_to_json_with_decoder(experiment, "successive_cancellation_exact_llr", results)
}

pub fn results_to_json_with_decoder(
    experiment: &str,
    decoder: &str,
    results: &[SimulationResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str(&format!("  \"decoder\": \"{}\",\n", escape_json(decoder)));
    out.push_str("  \"frozen_set\": \"natural_order_bhattacharyya_z2i_bad_z2i1_good\",\n");
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", result.n));
        out.push_str(&format!("      \"K\": {},\n", result.k));
        out.push_str(&format!("      \"p\": {:.10},\n", result.p));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!("      \"errors\": {},\n", result.errors));
        out.push_str(&format!("      \"bler\": {:.10},\n", result.bler()));
        if let Some(upper) = result.zero_error_upper_95() {
            out.push_str(&format!("      \"zero_error_upper_95\": {:.10},\n", upper));
        }
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

pub fn importance_results_to_json(
    experiment: &str,
    decoder: &str,
    results: &[ImportanceSamplingResult],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str(&format!("  \"decoder\": \"{}\",\n", escape_json(decoder)));
    out.push_str("  \"sampling\": \"tilted_bsc_proposal_reweighted_to_target_bsc\",\n");
    out.push_str("  \"frozen_set\": \"natural_order_bhattacharyya_z2i_bad_z2i1_good\",\n");
    out.push_str(
        "  \"adjudication\": \"P1b importance-sampling pilot; evidence, not proof; OPEN = LSN\",\n",
    );
    out.push_str("  \"results\": [\n");
    for (i, result) in results.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", result.n));
        out.push_str(&format!("      \"K\": {},\n", result.k));
        out.push_str(&format!("      \"target_p\": {:.10},\n", result.target_p));
        out.push_str(&format!(
            "      \"proposal_p\": {:.10},\n",
            result.proposal_p
        ));
        out.push_str(&format!("      \"trials\": {},\n", result.trials));
        out.push_str(&format!(
            "      \"proposal_errors\": {},\n",
            result.proposal_errors
        ));
        out.push_str(&format!(
            "      \"proposal_error_rate\": {:.10},\n",
            result.proposal_error_rate()
        ));
        out.push_str(&format!(
            "      \"weighted_bler_estimate\": {:.12e},\n",
            result.weighted_bler_estimate
        ));
        out.push_str(&format!(
            "      \"mean_likelihood_ratio\": {:.12e},\n",
            result.mean_likelihood_ratio
        ));
        out.push_str(&format!(
            "      \"effective_sample_size\": {:.6},\n",
            result.effective_sample_size
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

pub fn polar_rate_rows_to_json(
    experiment: &str,
    target_log2_half_sum_bound: f64,
    rows: &[PolarRateRow],
) -> String {
    let mut out = String::new();
    out.push_str("{\n");
    out.push_str(&format!(
        "  \"experiment\": \"{}\",\n",
        escape_json(experiment)
    ));
    out.push_str("  \"bound_convention\": \"SC block-error bound uses 0.5 * sum selected Bhattacharyya Z_i; raw sum is also recorded\",\n");
    out.push_str(&format!(
        "  \"target_log2_half_sum_bound\": {:.6},\n",
        target_log2_half_sum_bound
    ));
    out.push_str("  \"adjudication\": \"engineering polar-rate sweep only; no closure, no break, OPEN = LSN\",\n");
    out.push_str("  \"rows\": [\n");
    for (i, row) in rows.iter().enumerate() {
        out.push_str("    {\n");
        out.push_str(&format!("      \"N\": {},\n", row.n));
        out.push_str(&format!("      \"K\": {},\n", row.k));
        out.push_str(&format!("      \"p\": {:.10},\n", row.p));
        out.push_str(&format!("      \"rate\": {:.12},\n", row.rate));
        out.push_str(&format!(
            "      \"bhattacharyya_sum_bound\": {:.12e},\n",
            row.bhattacharyya_sum_bound
        ));
        out.push_str(&format!(
            "      \"half_sum_bound\": {:.12e},\n",
            row.half_sum_bound
        ));
        out.push_str(&format!(
            "      \"log2_bhattacharyya_sum_bound\": {:.6},\n",
            row.log2_bhattacharyya_sum_bound
        ));
        out.push_str(&format!(
            "      \"log2_half_sum_bound\": {:.6},\n",
            row.log2_half_sum_bound
        ));
        out.push_str(&format!(
            "      \"target_log2_half_sum_bound\": {:.6},\n",
            row.target_log2_half_sum_bound
        ));
        out.push_str(&format!(
            "      \"passes_half_sum_target\": {}\n",
            row.passes_half_sum_target
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

fn escape_json(value: &str) -> String {
    value
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

impl PolarCode {
    pub fn new(n: usize, k: usize, p: f64) -> Self {
        assert!(n.is_power_of_two(), "N must be a power of two");
        assert!(k <= n, "K must be <= N");
        assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

        let frozen = build_frozen_natural(n, k, p);
        let frozen_set = frozen.iter().copied().collect::<HashSet<_>>();
        let info_set = (0..n)
            .filter(|idx| !frozen_set.contains(idx))
            .collect::<Vec<_>>();
        let mut frozen_mask = vec![false; n];
        for &idx in &frozen {
            frozen_mask[idx] = true;
        }

        Self {
            n,
            k,
            p,
            frozen,
            info_set,
            frozen_mask,
        }
    }
}

pub fn build_frozen_natural(n: usize, k: usize, p: f64) -> Vec<usize> {
    assert!(n.is_power_of_two(), "N must be a power of two");
    assert!(k <= n, "K must be <= N");
    assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

    let z = bhattacharyya_reliabilities(n, p);
    let mut order = (0..n).collect::<Vec<_>>();
    order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));
    order[k..].to_vec()
}

pub fn bhattacharyya_reliabilities(n: usize, p: f64) -> Vec<f64> {
    assert!(n.is_power_of_two(), "N must be a power of two");
    assert!((0.0..=0.5).contains(&p), "p must be in [0, 0.5]");

    let z0 = 2.0 * (p * (1.0 - p)).sqrt();
    let mut z = vec![z0];
    while z.len() < n {
        let mut next = vec![0.0; z.len() * 2];
        for (i, value) in z.iter().copied().enumerate() {
            next[2 * i] = 2.0 * value - value * value;
            next[2 * i + 1] = value * value;
        }
        z = next;
    }

    z
}

pub fn polar_rate_row(n: usize, k: usize, p: f64, target_log2_half_sum_bound: f64) -> PolarRateRow {
    assert!(k <= n, "K must be <= N");
    let z = bhattacharyya_reliabilities(n, p);
    let mut order = (0..n).collect::<Vec<_>>();
    order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));
    let bhattacharyya_sum_bound = order[..k].iter().map(|&idx| z[idx]).sum::<f64>();
    polar_rate_row_from_sum(n, k, p, target_log2_half_sum_bound, bhattacharyya_sum_bound)
}

pub fn sweep_polar_rate(
    n: usize,
    p_values: &[f64],
    k_start: usize,
    k_end: usize,
    k_step: usize,
    target_log2_half_sum_bound: f64,
) -> Vec<PolarRateRow> {
    assert!(k_step > 0, "K step must be positive");
    assert!(k_start <= k_end, "K start must be <= K end");
    assert!(k_end <= n, "K end must be <= N");

    let mut rows = Vec::new();
    for &p in p_values {
        let z = bhattacharyya_reliabilities(n, p);
        let mut order = (0..n).collect::<Vec<_>>();
        order.sort_by(|&a, &b| z[a].total_cmp(&z[b]).then_with(|| a.cmp(&b)));

        let mut prefix = vec![0.0; n + 1];
        for (i, &idx) in order.iter().enumerate() {
            prefix[i + 1] = prefix[i] + z[idx];
        }

        let mut k = k_start;
        while k <= k_end {
            rows.push(polar_rate_row_from_sum(
                n,
                k,
                p,
                target_log2_half_sum_bound,
                prefix[k],
            ));
            match k.checked_add(k_step) {
                Some(next) => k = next,
                None => break,
            }
        }
    }
    rows
}

fn polar_rate_row_from_sum(
    n: usize,
    k: usize,
    p: f64,
    target_log2_half_sum_bound: f64,
    bhattacharyya_sum_bound: f64,
) -> PolarRateRow {
    let half_sum_bound = 0.5 * bhattacharyya_sum_bound;
    let log2_bhattacharyya_sum_bound = bhattacharyya_sum_bound.log2();
    let log2_half_sum_bound = half_sum_bound.log2();

    PolarRateRow {
        n,
        k,
        p,
        rate: k as f64 / n as f64,
        bhattacharyya_sum_bound,
        half_sum_bound,
        log2_bhattacharyya_sum_bound,
        log2_half_sum_bound,
        target_log2_half_sum_bound,
        passes_half_sum_target: log2_half_sum_bound <= target_log2_half_sum_bound,
    }
}

pub fn encode(code: &PolarCode, message: &[u8]) -> Vec<u8> {
    assert_eq!(message.len(), code.k, "message length must equal K");
    let mut u = vec![0u8; code.n];
    for (&idx, &bit) in code.info_set.iter().zip(message.iter()) {
        u[idx] = bit & 1;
    }
    polar_transform(&mut u);
    u
}

pub fn decode_successive_cancellation(code: &PolarCode, llr: &[f64]) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    let u_hat = sc_decode_node(llr, 0, &code.frozen_mask);
    code.info_set.iter().map(|&idx| u_hat[idx]).collect()
}

pub fn decode_scl(code: &PolarCode, llr: &[f64], list_size: usize) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    assert!(list_size > 0, "list size must be positive");
    let paths = scl_decode_node(llr, 0, &code.frozen_mask, list_size);
    let best = paths
        .first()
        .expect("SCL decoder must produce at least one path");
    code.info_set.iter().map(|&idx| best.bits[idx]).collect()
}

pub fn decode_scl_fast(code: &PolarCode, llr: &[f64], list_size: usize) -> Vec<u8> {
    assert_eq!(llr.len(), code.n, "LLR length must equal N");
    assert!(list_size > 0, "list size must be positive");
    let mut paths = vec![SclPath {
        bits: vec![0; code.n],
        metric: 0.0,
    }];

    for phi in 0..code.n {
        let mut next_paths = Vec::with_capacity(paths.len() * 2);
        for path in &paths {
            let bit_llr = sc_bit_llr_minsum(llr, 0, phi, &path.bits);
            if code.frozen_mask[phi] {
                let mut bits = path.bits.clone();
                bits[phi] = 0;
                next_paths.push(SclPath {
                    bits,
                    metric: path.metric + bit_metric_minsum(bit_llr, 0),
                });
            } else {
                for bit in [0u8, 1u8] {
                    let mut bits = path.bits.clone();
                    bits[phi] = bit;
                    next_paths.push(SclPath {
                        bits,
                        metric: path.metric + bit_metric_minsum(bit_llr, bit),
                    });
                }
            }
        }
        prune_paths(&mut next_paths, list_size);
        paths = next_paths;
    }

    let best = paths.first().expect("fast SCL must keep at least one path");
    code.info_set.iter().map(|&idx| best.bits[idx]).collect()
}

pub fn simulate_bsc_sc(n: usize, k: usize, p: f64, trials: usize, seed: u64) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_successive_cancellation(&code, &llr);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl(&code, &llr, list_size);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fast(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> SimulationResult {
    let code = PolarCode::new(n, k, p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - p) / p).ln();
    let llr1 = -llr0;
    let mut errors = 0usize;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < p;
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();
        let decoded = decode_scl_fast(&code, &llr, list_size);
        if decoded != message {
            errors += 1;
        }
    }

    SimulationResult {
        n,
        k,
        p,
        trials,
        errors,
        seed,
    }
}

pub fn simulate_bsc_scl_fast_importance(
    n: usize,
    k: usize,
    target_p: f64,
    proposal_p: f64,
    trials: usize,
    seed: u64,
    list_size: usize,
) -> ImportanceSamplingResult {
    assert!(
        (0.0..0.5).contains(&target_p),
        "target_p must be in (0, 0.5)"
    );
    assert!(
        (0.0..0.5).contains(&proposal_p),
        "proposal_p must be in (0, 0.5)"
    );
    assert!(trials > 0, "trials must be positive");

    let code = PolarCode::new(n, k, target_p);
    let mut rng = Lcg64::new(seed);
    let llr0 = ((1.0 - target_p) / target_p).ln();
    let llr1 = -llr0;
    let log_flip_weight = (target_p / proposal_p).ln();
    let log_clean_weight = ((1.0 - target_p) / (1.0 - proposal_p)).ln();
    let mut proposal_errors = 0usize;
    let mut weighted_error_sum = 0.0;
    let mut weight_sum = 0.0;
    let mut weight_square_sum = 0.0;

    for _ in 0..trials {
        let message = (0..k)
            .map(|_| if rng.next_bool() { 1 } else { 0 })
            .collect::<Vec<_>>();
        let x = encode(&code, &message);
        let mut flip_count = 0usize;
        let llr = x
            .iter()
            .map(|&bit| {
                let flipped = rng.next_f64() < proposal_p;
                flip_count += usize::from(flipped);
                let y = bit ^ u8::from(flipped);
                if y == 0 {
                    llr0
                } else {
                    llr1
                }
            })
            .collect::<Vec<_>>();

        let log_weight =
            flip_count as f64 * log_flip_weight + (n - flip_count) as f64 * log_clean_weight;
        let weight = log_weight.exp();
        weight_sum += weight;
        weight_square_sum += weight * weight;

        let decoded = decode_scl_fast(&code, &llr, list_size);
        if decoded != message {
            proposal_errors += 1;
            weighted_error_sum += weight;
        }
    }

    let effective_sample_size = if weight_square_sum == 0.0 {
        0.0
    } else {
        weight_sum * weight_sum / weight_square_sum
    };

    ImportanceSamplingResult {
        n,
        k,
        target_p,
        proposal_p,
        trials,
        proposal_errors,
        weighted_bler_estimate: weighted_error_sum / trials as f64,
        mean_likelihood_ratio: weight_sum / trials as f64,
        effective_sample_size,
        seed,
    }
}

fn polar_transform(bits: &mut [u8]) {
    let n = bits.len();
    let mut half = 1usize;
    while half < n {
        let step = half * 2;
        for block in (0..n).step_by(step) {
            for i in 0..half {
                bits[block + i] ^= bits[block + half + i];
            }
        }
        half = step;
    }
}

fn sc_decode_node(llr: &[f64], offset: usize, frozen_mask: &[bool]) -> Vec<u8> {
    if llr.len() == 1 {
        let bit = if frozen_mask[offset] || llr[0] >= 0.0 {
            0
        } else {
            1
        };
        return vec![bit];
    }

    let half = llr.len() / 2;
    let mut left_llr = vec![0.0; half];
    for i in 0..half {
        left_llr[i] = f_llr(llr[i], llr[half + i]);
    }
    let left = sc_decode_node(&left_llr, offset, frozen_mask);
    let mut left_partial = left.clone();
    polar_transform(&mut left_partial);

    let mut right_llr = vec![0.0; half];
    for i in 0..half {
        right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
    }
    let right = sc_decode_node(&right_llr, offset + half, frozen_mask);

    [left, right].concat()
}

#[derive(Clone, Debug)]
struct SclPath {
    bits: Vec<u8>,
    metric: f64,
}

fn scl_decode_node(
    llr: &[f64],
    offset: usize,
    frozen_mask: &[bool],
    list_size: usize,
) -> Vec<SclPath> {
    if llr.len() == 1 {
        if frozen_mask[offset] {
            return vec![SclPath {
                bits: vec![0],
                metric: bit_metric(llr[0], 0),
            }];
        }

        let mut paths = vec![
            SclPath {
                bits: vec![0],
                metric: bit_metric(llr[0], 0),
            },
            SclPath {
                bits: vec![1],
                metric: bit_metric(llr[0], 1),
            },
        ];
        prune_paths(&mut paths, list_size);
        return paths;
    }

    let half = llr.len() / 2;
    let mut left_llr = vec![0.0; half];
    for i in 0..half {
        left_llr[i] = f_llr(llr[i], llr[half + i]);
    }

    let left_paths = scl_decode_node(&left_llr, offset, frozen_mask, list_size);
    let mut combined = Vec::new();
    for left in left_paths {
        let mut left_partial = left.bits.clone();
        polar_transform(&mut left_partial);

        let mut right_llr = vec![0.0; half];
        for i in 0..half {
            right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
        }

        let right_paths = scl_decode_node(&right_llr, offset + half, frozen_mask, list_size);
        for right in right_paths {
            let mut bits = Vec::with_capacity(llr.len());
            bits.extend_from_slice(&left.bits);
            bits.extend_from_slice(&right.bits);
            combined.push(SclPath {
                bits,
                metric: left.metric + right.metric,
            });
        }
    }

    prune_paths(&mut combined, list_size);
    combined
}

fn prune_paths(paths: &mut Vec<SclPath>, list_size: usize) {
    paths.sort_by(|a, b| a.metric.total_cmp(&b.metric));
    paths.truncate(list_size);
}

fn bit_metric(llr: f64, bit: u8) -> f64 {
    let signed = if bit == 0 { llr } else { -llr };
    if signed >= 0.0 {
        (1.0 + (-signed).exp()).ln()
    } else {
        -signed + (1.0 + signed.exp()).ln()
    }
}

fn bit_metric_minsum(llr: f64, bit: u8) -> f64 {
    let agrees_with_hard_decision = (llr >= 0.0 && bit == 0) || (llr < 0.0 && bit == 1);
    if agrees_with_hard_decision {
        0.0
    } else {
        llr.abs()
    }
}

fn sc_bit_llr_minsum(llr: &[f64], offset: usize, phi: usize, decisions: &[u8]) -> f64 {
    if llr.len() == 1 {
        return llr[0];
    }

    let half = llr.len() / 2;
    if phi < offset + half {
        let mut left_llr = vec![0.0; half];
        for i in 0..half {
            left_llr[i] = f_llr_minsum(llr[i], llr[half + i]);
        }
        sc_bit_llr_minsum(&left_llr, offset, phi, decisions)
    } else {
        let mut left_partial = decisions[offset..offset + half].to_vec();
        polar_transform(&mut left_partial);

        let mut right_llr = vec![0.0; half];
        for i in 0..half {
            right_llr[i] = g_llr(llr[i], llr[half + i], left_partial[i]);
        }
        sc_bit_llr_minsum(&right_llr, offset + half, phi, decisions)
    }
}

fn f_llr(a: f64, b: f64) -> f64 {
    let sign = if (a < 0.0) ^ (b < 0.0) { -1.0 } else { 1.0 };
    let min_abs = a.abs().min(b.abs());
    let correction = (1.0 + (-(a + b).abs()).exp()).ln() - (1.0 + (-(a - b).abs()).exp()).ln();
    sign * min_abs + correction
}

fn f_llr_minsum(a: f64, b: f64) -> f64 {
    let sign = if (a < 0.0) ^ (b < 0.0) { -1.0 } else { 1.0 };
    sign * a.abs().min(b.abs())
}

fn g_llr(a: f64, b: f64, u: u8) -> f64 {
    if u == 0 {
        b + a
    } else {
        b - a
    }
}

#[derive(Clone, Debug)]
struct Lcg64 {
    state: u64,
}

impl Lcg64 {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    fn next_u64(&mut self) -> u64 {
        self.state = self
            .state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.state
    }

    fn next_bool(&mut self) -> bool {
        (self.next_u64() >> 63) != 0
    }

    fn next_f64(&mut self) -> f64 {
        const SCALE: f64 = 1.0 / ((1u64 << 53) as f64);
        ((self.next_u64() >> 11) as f64) * SCALE
    }
}
