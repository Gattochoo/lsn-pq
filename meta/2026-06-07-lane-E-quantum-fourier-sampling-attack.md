# Lane E (new direction) — death-mode ⑤ for LSN: the natural quantum Fourier-sampling attack also obeys the wall

> A genuinely new angle (the worst→avg line being saturated): the whole decoder program
> attacked LSN with **classical** decoders, but LSN is **quantum-native**, so the natural
> unexamined question is **death mode ⑤ (BQP-easy)** — does a *quantum*, structure-aware attack
> break it at poly samples? The self-duality (Lane C7, `F_Ω[1_L]=2^n·1_L`) makes one attack
> canonical: a quantum **symplectic-Fourier (Weil) sampling** — prepare a superposition over the
> positives, apply the Weil transform, measure — whose measurement distribution is
> `q(w)=|F_Ω[1_P](w)|²`. Tested n=4,5,6: it **reveals `L` at clean/dense** (calibration:
> concentration ratio `=2^n` exactly, recovery 100%) but its `L`-concentration **collapses to
> uniform at poly samples** (ratio → 1, recovery 0 at every `m/2^n<1`). The reason is structural:
> `q` is the symplectic-Fourier **power spectrum**, the **Fourier dual** of the XOR-autocorrelation
> `C(d)` (Lane C3) — so the quantum attack **inherits the channel-level closure**. **Death mode ⑤
> via this attack is CLOSED; a genuine quantum break needs a step beyond structure-aware Fourier
> sampling (the open post-quantum conjecture, NOT settled here).** Script:
> `lsn-experiments/24-quantum-fourier-sampling-attack.py`. Date: 2026-06-07.

---

## 한국어 요약

```text
새 각도(worst→avg 포화 후): LSN은 quantum-native인데 프로그램은 고전 디코더만 테스트 → death-mode
⑤(BQP-easy) 미점검. self-duality(C7)가 시사하는 자연스러운 양자 공격 = symplectic-Fourier(Weil)
sampling: 측정분포 q(w)=|F_Ω[1_P](w)|².
검증(n=4,5,6, p=0.10):
 - calibration: clean에서 conc-ratio = 정확히 2ⁿ(16/32/64), recovery 100% → 진짜로 L 드러냄(약한도구X).
 - sweep: dense conc-ratio 3.92–7.27(신호), SPARSE(m/2ⁿ<1)에서 ratio→~1(uniform)·recovery 0 전부.
구조적 이유: q(power spectrum)는 autocorrelation C(d)(C3)의 Fourier 쌍대 → channel-level 폐쇄 상속.
→ ★death-mode ⑤(이 자연 양자공격): CLOSED. 진짜 양자 break은 Fourier-sampling 너머(non-Clifford/
  period-finding)=열린 post-quantum 추측(미해결). 양자 break 아님·7th 아님·벽이 양자에도 성립.
```

## §1 The attack and the calibration

`F_Ω[1_L] = 2^n·1_L` (C7) ⇒ the symplectic-Fourier **power spectrum** of the membership
indicator concentrates on `L`. The quantum Fourier-sampling attack measures
`q(w)=|F_Ω[1_P](w)|²` (normalised). Calibration (clean `p=0`, full obs):

```text
  n   concentration ratio (= conc·2^n; uniform→1, clean→2^n)   recovery (top-|L| = L?)
  4              16.0  (= 2^4, exact)                            80/80
  5              32.0  (= 2^5, exact)                            60/60
  6              64.0  (= 2^6, exact)                            40/40   -> PASS
```

So the attack genuinely reveals `L` (ratio `=2^n` exactly, full recovery) — it is **not** a
weak tool; its poly-sample failure below is therefore meaningful.

## §2 The sweep (p=0.10): the quantum signal vanishes at poly samples

```text
  n=4: m=128(8x) ratio 3.92 | m=16(1x) 1.18 | SPARSE m=8 0.84, m=4 0.46   (recovery 0 throughout)
  n=5: m=512(16x) ratio 5.31| m=32(1x) 1.26 | SPARSE m=25 1.04, m=16 0.95, m=8 0.61
  n=6: m=2048(32x) ratio 7.27| m=64(1x) 1.16| SPARSE m=36 1.02, m=32 1.09, m=16 0.89
```

The `L`-concentration ratio is `>1` at dense observation (a quantum signal is present) but
**collapses to `~1` (uniform — no signal) at every poly-ward cell** `m/2^n<1`; exact recovery
is 0 at poly samples (and, like the classical Walsh family, fragile even dense at `p=0.1`).

## §3 Why — the Fourier-duality (the structural reason it can't beat the wall)

`q(w)=|F_Ω[1_P](w)|²` is the symplectic-Fourier **power spectrum**, and the XOR-autocorrelation
`C(d)=|{v∈P:v⊕d∈P}|` (the classical channel signal, Lane C3 / OFA-325-327) is its **Fourier
dual** (`C = WHT⁻¹[|WHT[·]|²]`). They are **one object in two bases**. So the quantum
measurement's `L`-concentration vanishes at poly samples for the *same* reason `C(d∈L)→0` does
(`E[true members]=m·2^{-n}→0`): the channel-level closure is basis-independent. The natural
quantum Fourier-sampling attack is therefore inside the **already-walled** Walsh/autocorrelation
family — it cannot beat the poly-sample wall.

## §4 Verdict (Sound Verifier)

**Death mode ⑤ (BQP-easy) via the natural quantum attack: CLOSED; LSN's wall holds for quantum
Fourier sampling too.** The canonical structure-aware quantum attack the self-duality suggests
(Weil/symplectic-Fourier sampling) reveals `L` at clean/dense (calibrated, ratio `=2^n`) but is
Fourier-dual to the autocorrelation, so it inherits the channel-level closure and **fails at
poly samples** (ratio → 1, recovery 0). This is genuinely new — the program's first explicit
quantum-attack assessment of LSN — and it shows the quantum-nativeness does **not** hand an
adversary a poly-sample Fourier-sampling break. **What it does NOT settle:** a genuine quantum
break requiring resources *beyond* structure-aware Fourier sampling (non-Clifford/magic, or a
period-finding-style speedup) — that is the open post-quantum-hardness conjecture (and the
membership channel here is exp-data anyway; the crypto channel is the poly *linear* one).
**No quantum break; no 7th; no security claim; OPEN = LSN.**

---

## References
- `lsn-experiments/24-quantum-fourier-sampling-attack.py` (this attack).
- Lane C7 (self-duality `F_Ω[1_L]=2^n 1_L`), Lane C3 / OFA-325-327 (autocorrelation channel-level closure; the Fourier dual).
- death mode ⑤ (BQP-easy) — the memory's quantum death mode, here applied to LSN for the first time.
