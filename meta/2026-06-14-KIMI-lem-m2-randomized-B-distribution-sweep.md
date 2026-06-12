# lem:m2 randomized adaptive $B$ — distribution sweep

**Date:** 2026-06-14

## Model

- $n=2$, ambient dimension $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$.
- $B$ is drawn per $A$ from one of the candidate distributions.
- Output $(C,y) = (BA, B(Ax+e))$.

## Results

### $m=3$

| Distribution | SD |
|--------------|---:|
| Uniform (all $B$) | 3225/32768 |
| Uniform full-rank | 1567/10240 |
| Bernoulli($1/4$) rows | 61842683/167772160 |
| Bernoulli($1/3$) rows | 149444543/680244480 |
| Bernoulli($1/2$) rows | 3225/32768 |
| Best $p^*$ | 1/2 -> 3225/32768 |

### $m=4$

| Distribution | SD |
|--------------|---:|
| Uniform (all $B$) | 5903/32768 |
| Uniform full-rank | 91717/430080 |
| Uniform rank-3 | 151841/737280 |
| Bernoulli($1/4$) rows | 3671446401/8589934592 |
| Bernoulli($1/3$) rows | 54459235553/195910410240 |
| Bernoulli($1/2$) rows | 5903/32768 |
| Best $p^*$ | 1/2 -> 5903/32768 |

## Interpretation

- For both $m=3$ and $m=4$, the uniform (all $B$) distribution — equivalently Bernoulli($1/2$) rows — achieves the smallest SD among all tested distributions.
- Uniform full-rank $B$ is larger than uniform all-$B$ for both $m=3$ and $m=4$, so rank conditioning does **not** help.
- Bernoulli($p$) with $p \neq 1/2$ is larger than uniform, so biasing row sparsity does **not** help.
- Thus for $n=2$ the correlated noise $e'=Be$ is already effectively i.i.d. under uniform $B$, and the next step is scaling to $n=3$.

## Limitations

- Only $n=2$.
- Only $m=3,4$.
- Distributions are independent per $A$.
