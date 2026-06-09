# Lane C6 — spectral Ω-graph decoder (3rd structural family): the named-open route also obeys the wall

> Kimi's clique-drowning note left one honest caveat: a decoder using `Ω` *spectrally* (not
> as pair counts, not as greedy clique search) "is not ruled out by this analysis." Lane C6
> tests exactly that named-open route — a genuinely **third** decoder family. Result: it is a
> **strong** decoder (calibration passes decisively; at dense `p=0.10` it **grows with n** to
> **100% at n=7** — the strongest dense-regime signal the search has produced, above
> coset-gain's 13/16) — yet it **fails at every poly-ward cell** (`m/2^n<1` → 0 for all n),
> dying at `m=2^n`. So the strongest dense decoder still obeys the sample-complexity wall.
> **NOT REDUCES; the closure is not specific to the autocorrelation/clique channels.**
> Script: `lsn-experiments/21-spectral-omega-graph-decoder.py`. Date: 2026-06-06.

---

## 한국어 요약

```text
named-open 경로(symplectic-clique 문서 caveat #3: spectral on Ω-graph) 테스트 = 3번째 디코더 family.
디코더: P의 Ω-orthogonality 그래프에서 진짜 멤버=planted clique → centered adjacency 최상위
  고유벡터로 clique 복구 → 상위 정점들로 isotropic span 그리디 구성 → rank n·isotropic이면 수락.
calibration 가드(약한도구≠hardness): clean/저노이즈 복구 필수.
결과:
  - calibration PASS(강함): clean 100%; dense p=0.10에서 n 따라 성장 63→80→97→100%(n=7) =
    지금까지 dense 최강(coset-gain 13/16 상회). 약한 도구 아님.
  - sweep p=0.10: dense 복구하나 m=2^n부터 0, 모든 SPARSE(m/2^n<1) 셀 = 0 (n=4..7).
→ 가장 강한 dense 디코더조차 poly-sample 벽 준수. 3번째 독립 family도 벽 → 폐쇄가 autocorrelation/
  clique 채널 특정 아님. REDUCES 플래그 없음. 근본원인 동일(poly-sample서 진짜 clique<1 → spectral
  신호 부재). 7th 아님·보안주장 없음.
```

## §1 The decoder (3rd family) and calibration

`P` = positive vectors. Graph: edge `(v,w)` iff `Ω(v,w)=0`. True members of `L` are mutually
Ω-orthogonal (L isotropic) ⇒ a **planted clique**; false positives are random (`Ω=0` w.p. ½)
⇒ background `~ G(|P|,½)`. Recover spectrally: top eigenvector of the centered adjacency
`M = A − ½(J−I)` concentrates on the clique; rank vertices by it; greedily build an isotropic
F₂ span from the top-ranked; accept iff isotropic rank-`n`; exact = `span == L`.

```text
CALIBRATION (recovery counts):     p=0 full     p=.02 half   p=.05 half   p=.10 half
  n=4                               80/80        75/80        66/80        50/80
  n=5                               80/80        80/80        79/80        64/80
  n=6                               60/60        60/60        60/60        58/60
  n=7                               40/40        40/40        40/40        40/40   <- 100%
  => PASS (clean=100% all n; GROWS with n at dense p=0.10 -- a strong, genuine decoder,
     in fact the strongest dense-regime signal found, above coset-gain's 13/16).
```

The calibration guard matters (check #13): a decoder that failed clean recovery would make
its poly-sample failure meaningless. This one passes decisively, so its wall-obedience below
is informative, not a weak-tool artifact.

## §2 The sweep (p=0.10): strong at dense, zero at poly-ward

```text
  n   dense (half) recovery     m=2^n (ratio 1.0)    every SPARSE cell (m/2^n<1)
  4      51/80                       0/80                 0  (m=8,4)
  5      60/80                       0/80                 0  (m=25,16,8)
  6      58/60                       0/60                 0  (m=36,32,16)
  7      40/40                       0/40                 0  (m=64,49,32)
```

Despite being the strongest dense decoder, it **dies at `m=2^n`** and every sparser cell is
**0** — identical to the autocorrelation and clique families. Root cause is the same channel
fact (at `m/2^n<1` the expected true-member count `→0`, so there is no planted clique and the
spectral signal is absent), but the point is that a **distinct, strong** method confirms it.

## §3 Verdict (Sound Verifier)

**NOT REDUCES; a 3rd independent decoder family obeys the wall.** The spectral Ω-graph
decoder — the route explicitly flagged as "not ruled out" — is genuine and strong (passes
calibration; grows-with-n to 100% at dense `n=7`) yet fails at every poly-ward sample density
(`m/2^n<1` → 0, all n), dying at `m=2^n`. No SPARSE cell recovers, so **no ★REDUCES flag**.
This shows the poly-sample closure is **not specific to the autocorrelation or clique
channels** — three structurally-distinct decoder families (pair-count autocorrelation;
greedy clique; spectral) all hit the same sample-complexity wall, because the obstacle is the
channel (too few true members), not any one decoder. A REDUCES still requires a fundamentally
different *poly-sample* structural channel = the external `LSN ⊀ LPN` question. **No 7th; no
security claim; evidence, not proof.**

---

## References
- `lsn-experiments/21-spectral-omega-graph-decoder.py` (this experiment).
- Symplectic-clique / clique-drowning note (caveat #3, the named-open route); OFA-325/327
  channel-level closure; Task-5 + Lane C3 (sample-complexity / signal-vanishing).
