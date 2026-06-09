# Lane C3 — independent cross-check of the channel-level signal-vanishing (Lane D Side-1)

> Lane D Side-1 leans on the adjudicator's **channel-level closure** of the autocorrelation
> family (OFA-325/327): at poly-ward density the raw signal any such decoder reads vanishes.
> Task 5 measured the *downstream* symptom (exact recovery → 0); Lane C3 measures the
> *upstream signal* directly, from an **independent implementation**. Result: the
> **L-specific excess autocorrelation** `mean C(d∈L) − mean C(d∉L)` collapses from tens
> (dense) to **<1% of the dense value (≈0.01–0.04% for n=6,7) once `m/2^n < 1`**, and the
> absolute `C(d∈L) → ~0`. The signal itself is gone — independent of any decoder.
> **Channel-level closure confirmed; NOT REDUCES; evidence, not proof.** Script:
> `lsn-experiments/19-autocorr-signal-vanish-crosscheck.py`.

`working code (independent cross-check; includes a self-corrected metric)`. Date: 2026-06-06.

---

## 한국어 요약

```text
질문: autocorrelation 디코더가 읽는 raw 신호가 poly-ward에서 정말 사라지나? (디코더 무관)
지표(정직 수정): 올바른 양 = EXCESS = mean C(d∈L) − mean C(d∉L) (L 고유 lift).
  (처음엔 signal/background RATIO를 봤으나 둘 다 →0이라 0/0 noise → 부적절. 검증이 잡음.)
결과(p=0.10, 독립 구현):
  dense(half) excess = 2.35/5.36/10.84/20.59 (n=4..7, n 따라 성장) = 100% 기준.
  m=2^n: 이미 1.47%→0.04%로 급감.
  SPARSE(m/2^n<1): excess = dense의 0.00–0.88% (n=6,7은 0.01–0.04%) = 수천 배 붕괴 ≈0.
  + 절대 C(d∈L)도 →~0 (positive-pair가 거의 없음).
→ poly-ward에선 autocorrelation에 읽을 L-구조가 사실상 없음 → 현재·미래 모든 autocorr
  디코더 불가. 채널-레벨 폐쇄(OFA-325/327) 독립 확증, Task5 recovery→0의 메커니즘. 증거.
```

---

## §1 Method and the honest metric correction

For `n=4..7`, `p=0.10`, sweeping `m`, I compute (independent of Task 5's decoder) the mean
XOR-autocorrelation `C(d)=|{v∈P: v⊕d∈P}|` over `d∈L\{0}` (**signal**) vs over `d∉L`
(**background**).

**Self-correction (verification caught an over-claim):** I first reported the *ratio*
`signal/background`, predicting `→1` at sparse `m`. The data refuted that framing: at sparse
`m` both signal and background collapse to `~0`, so the ratio is a noisy `0/0` (it wandered
2–4, not 1). The **decoder-relevant** quantity is the **L-specific EXCESS**
`= mean C(d∈L) − mean C(d∉L)` (the autocorrelation lift attributable to `L`). That is the
metric reported below; the ratio is not meaningful near zero counts.

## §2 Data (excess collapses to ≈0 at poly-ward density)

```text
 EXCESS = mean C(d∈L) − mean C(d∉L);  %dense = excess / (half-obs excess)
  n   half-obs excess   m=2^n      m/2^n<1 (SPARSE) excesses (% of dense)
  4        2.35 (100%)   1.47%     0.88%, 0.04%
  5        5.36 (100%)   0.54%     0.25%, 0.22%, ~0%
  6       10.84 (100%)   0.05%     0.01%, 0.04%, 0.01%
  7       20.59 (100%)   0.04%     0.01%, 0.02%, 0.00%
 (absolute signal C(d∈L): tens at half-obs  ->  ~0.001–0.02 at sparse)
```

Two facts, both pointing the same way:
1. the **L-specific excess** collapses to **<1% of dense** as soon as `m/2^n < 1` (to
   **~0.01–0.04%** for the crypto-scale `n=6,7`) — orders of magnitude down;
2. the **absolute** `C(d∈L) → ~0` — almost no positive-pairs `(v, v⊕d∈P)` survive, because
   `E[#true members observed] = m/2^n → 0`.

So at poly-ward density the autocorrelation carries essentially **no `L`-structure** for any
decoder to read. The signal floor is concentrated in the dense regime (even `m=2^n` is
already `≤1.5%` of dense and shrinking with `n`), consistent with Task 5's exponential `m*`.

## §3 Verdict (Sound Verifier)

**Channel-level signal-vanishing CONFIRMED (independently).** The L-specific autocorrelation
excess and the absolute signal both collapse to `≈0` at `m/2^n < 1`. This independently
reproduces the adjudicator's channel-level closure (OFA-325/327) and supplies the *upstream
mechanism* behind Task 5's `recovery → 0`: not a weak decoder, but **no signal to read** — so
**no autocorrelation decoder, present or future, can recover at poly-sample**. A REDUCES
would require a fundamentally different (non-autocorrelation) poly-sample structural channel
— the external `LSN ⊀ LPN` question. **NOT REDUCES; evidence, not proof; no security claim.**

---

## References
- `lsn-experiments/19-autocorr-signal-vanish-crosscheck.py` (this cross-check).
- OFA-325/327 channel-level closure (adjudicator); Task 5 (`16-task5-sample-density-sweep.py`).
- Lane D (`2026-06-06-lane-D-synthesis-three-sided-convergence.md`) — Side-1 this supports.
