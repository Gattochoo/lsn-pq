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

    let mut best_index = 0;
    let mut best_score = i32::MIN;
    let mut runner_up_score = i32::MIN;

    for (index, row) in compact.rows.iter().enumerate() {
        let mut score = false_total;
        for &point in row {
            let point = point as usize;
            score += true_counts[point] - false_counts[point];
        }

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

pub fn lagrangian_count(n: usize) -> usize {
    (1..=n).map(|i| (1usize << i) + 1).product()
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
