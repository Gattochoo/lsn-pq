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

pub fn run_ml_trials(
    n: usize,
    sample_count: usize,
    noise_rate: f64,
    trials: usize,
    seed: u64,
) -> MlTrialResult {
    let lagrangians = enumerate_lagrangians(n);
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
        let guess = brute_force_ml_decode(&samples, &lagrangians);
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
