# Track F — sufficient-statistic reduction for lem:m2 rate question

**Date:** 2026-06-14. **Experiments:** 202, 203. **Commit prefix:** `track-F:`.

## What was proved / computed

**THEOREM (sufficient-statistic reduction).** At fixed $n$, let the rows of
$C \in \mathbb{F}_2^{m \times n}$ be classified by type
$\tau \in \mathbb{F}_2^n$.  Define

$$
T = \bigl((m_\tau)_{\tau \in \mathbb{F}_2^n},
        (s_\tau)_{\tau \in \mathbb{F}_2^n}\bigr),
$$

where $m_\tau$ counts rows of type $\tau$ and $s_\tau$ counts, among those
rows, how many have label bit $y_i=1$.  Then for both the reduction output
$P_{\rm out}$ and the matched-rate LPN target $P_{\rm lpn}$, the pair
$(C,y)$ depends only on $T$.

*Proof obligations satisfied in code:*
1. $\operatorname{rank}(C)$ and $y \in \operatorname{col}(C)$ are functions
   of $T$: membership holds iff there exists $w \in \mathbb{F}_2^n$ such that
   $s_\tau = m_\tau \cdot \langle w,\tau\rangle$ for every $\tau$ with
   $m_\tau>0$.
2. For a fixed secret $w$,
   $\operatorname{wt}(y+Cw)=\sum_\tau [\langle w,\tau\rangle=0]s_\tau
   +[\langle w,\tau\rangle=1](m_\tau-s_\tau)$, so $P_{\rm lpn}$ depends on
   $y$ only through $T$.
3. The mixture theorem of experiments 200/201 gives $P_{\rm out}$ through
   rank/membership only, hence through $T$.

Consequently

$$
\mathrm{SD}\bigl(P_{\rm out},P_{\rm lpn}\bigr)
= \frac12 \sum_T \bigl|P_{\rm out}(T)-P_{\rm lpn}(T)\bigr|.
$$

The implementation keeps every probability as an integer count over the common
denominator $q_{\rm den}\,N\,(2N)^m\,D^m$ with $N=2^n$ and
$p_{\rm eff}(n)=a/D$ in lowest terms.

## Files

* `experiments/202-KIMI-trackF-sufficient-statistic-reduction.py` — n=2 exact
  SD by enumerating $T$; cross-check against direct enumeration (experiments
  200/201) for $m \le 6$; decay fit.
* `experiments/203-KIMI-trackF-sufficient-statistic-n3.py` — general-$n$
  implementation; n=3 stretch values.
* `experiments/output/202-trackF-sufficient-statistic-n2.json`
* `experiments/output/203-trackF-sufficient-statistic-n3.json`

## Key exact values

### n=2, $p_{\rm eff}(2)=175/512$, $q_{\rm graph}(2)=29/64$

| $m$ | SD (exact) | SD (float) | $1-\mathrm{SD}$ |
|----:|-----------:|-----------:|----------------:|
| 2  | `36575/524288` | 0.069761 | 0.930239 |
| 3  | `695896635/4294967296` | 0.162026 | 0.837974 |
| 4  | `277825754675/1099511627776` | 0.252681 | 0.747319 |
| 5  | `11668368577886825/36028797018963968` | 0.323862 | 0.676138 |
| 6  | `27663233753869930405/73786976294838206464` | 0.374907 | 0.625093 |
| 7  | `62110524507069812281095/151115727451828646838272` | 0.411013 | 0.588987 |
| 8  | `16905825785074125865887285/38685626227668133590597632` | 0.437005 | 0.562995 |
| 12 | `2670376973898429557749111289348052212525/5444517870735015415413993718908291383296` | 0.490471 | 0.509529 |
| 16 | `776580527746517716721610547003155688886535620657255/1496577676626844588240573268701473812127674924007424` | 0.518904 | 0.481096 |
| 24 | `16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616` | 0.567854 | 0.432146 |
| 32 | `175842639268182236234225149971230384237897459955496283666363584364067225210764143038987088768788053693215/286687326998758938951352611912760867599570623646035140467198604923365359511060601008752319138765710819328` | 0.613360 | 0.386640 |
| 48 | `607477461132137352864009669432561278876547085540963876824000902259324180705585729760268074621527447131000809903636388269236874471512931193096020288141170484925/878694100496718043517683302282418331810487718418343092402491322775749527474899974671687634004666183037093927858109549828751614463963730408009475621262727315456` | 0.691341 | 0.308659 |

$m=64$ and $m=80$ are beyond the current exact enumeration wall: the state
space is $\binom{m+7}{7}$, which is $\approx 1.6\times 10^9$ at $m=64$ and
$\approx 5.8\times 10^9$ at $m=80$.

### 1-SD decay fit (n=2, $m \ge 8$)

* Exponential: $1-\mathrm{SD} \approx \exp(-0.4858 - 0.0145\,m)$.
* Power-law: $1-\mathrm{SD} \approx 1.139 \, m^{-0.321}$.

Both are finite-sample regressions, not proven asymptotics.

### n=3 stretch, $p_{\rm eff}(3)=3367/8192$, $q_{\rm graph}(3)=1241/4608$

| $m$ | SD (float) | $1-\mathrm{SD}$ |
|----:|-----------:|----------------:|
| 2  | 0.024842 | 0.975158 |
| 3  | 0.065029 | 0.934971 |
| 4  | 0.125596 | 0.874404 |
| 6  | 0.216626 | 0.783374 |
| 8  | 0.255124 | 0.744876 |
| 10 | 0.269815 | 0.730185 |
| 12 | 0.276540 | 0.723460 |

The n=3 values are also exact and cross-checked against direct enumeration for
$m \le 4$.

## Claim labels

* `sufficient_statistic_reduction` — **THEOREM** (proved; verified against
  direct enumeration for small $m$).
* `n2_exact_sd_m_le_48` — **EVIDENCE** (exact finite computation).
* `n3_exact_sd` — **EVIDENCE** (exact finite computation).
* `decay_fit` — **EVIDENCE** (finite-sample regression).
* `lem_m2_status` — **OPEN**.

## PRE-REGISTER interpretation guards

* **Axis:** all conclusions are on the $m$-axis at fixed $n$; no fixed-small-$m$
  hardness claim is made.
* **Comparison distribution:** $P_{\rm lpn}$ is $LPN_{p_{\rm eff}(n)}$, the
  matched-rate target, not $LPN_{1/4}$.
* **Practical meaning:** the SD numbers measure distance between two explicit
  distributions; they do not by themselves imply a practical attack.

## Standing guards

* **L1 exact arithmetic:** all arithmetic uses `fractions.Fraction` (and the
  equivalent integer-count formulation with a common power-of-2 denominator).
  JSON stores fractions as strings.
* **L2 J-twist care:** the row-type inner product is the standard
  $\mathbb{F}_2$ pairing; no symplectic dual is involved here.
* **L3 query-class hygiene:** any SQ statement names its query class
  explicitly; the unrestricted Feldman theorem is not invoked.

## Status

Committed as `track-F:` (one track-only commit). Not pushed.
