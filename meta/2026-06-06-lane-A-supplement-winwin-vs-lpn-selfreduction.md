# Lane A supplement — the win-win barrier situated in the (limited) state of LPN self-reducibility

> Lane A pinned the single open point (`non-linear sympLPN → LPN`) and noted the authors'
> **win-win barrier**: such a reduction "could also improve the random self-reductions
> achievable for LPN." This short supplement asks how *strong* that barrier is, by checking
> the known state of LPN self-reducibility (focused literature dig, June 2026). Finding: LPN's
> self-reductions are **limited** — search↔decision holds, but **poly-sample random
> self-reduction / sample amplification does not** — so a non-linear `sympLPN→LPN` reduction
> really would have to **transcend a known limit of LPN theory**. The win-win barrier is
> therefore *meaningful*, not rhetorical. **Evidence, not proof; secondary sources; status
> unchanged (OPEN).** Date: 2026-06-06.

---

## 한국어 요약

```text
win-win 장벽: 비선형 sympLPN→LPN reduction이 존재하면 LPN의 random self-reduction을 개선하는 셈.
이게 강한가? = LPN self-reducibility의 현 상태에 달림.
문헌(2차 출처): LPN은 search↔decision self-reduction은 있으나, poly-sample에서의 random
  self-reduction/sample amplification은 자유롭지 않음("high-noise amplification은 sub-exp
  cryptanalysis엔 쓰이나 poly-sample efficient hardness reduction엔 부적용"). 
→ 비선형 reduction은 알려진 LPN self-reduction 한계를 넘어야 함 → win-win 장벽 *의미 있음*.
+ 2026 후속(QIP'26 등)에 non-linear 질문 해결 연구 없음 → open point 외부적으로도 여전히 열림.
판정 불변: OPEN. 증거지 증명 아님; 2차 출처.
```

## §1 The question

The win-win barrier (Lane A §4) is only as strong as the gap between "what a non-linear
`sympLPN→LPN` reduction would need" and "what LPN self-reduction theory already gives for
free." If LPN had powerful poly-sample random self-reductions, the barrier would be weak (the
reduction could piggy-back on them); if LPN's self-reductions are limited, the barrier is real.

## §2 What LPN self-reducibility actually provides (focused dig, June 2026)

- **Search ↔ decision:** a standard LPN self-reduction exists (decision-LPN ≡ search-LPN).
- **Sample / hardness amplification is limited at poly samples:** the literature is explicit
  that *"high-noise sample amplification has been used to cryptanalyze LPN in sub-exponential
  time, but this technique does not seem to be applicable in the context of efficient (PPT)
  hardness reduction, especially when the number of samples is at most polynomial."* I.e. the
  amplification tricks live in the **sub-exponential** regime, **not** the poly-time/
  poly-sample regime where a crypto reduction must operate.
- There is a bounded↔unbounded-samples connection (small-error few-sample hard ⇒ larger-error
  unbounded-sample hard), but it does **not** hand you a free poly-sample random
  self-reduction of the kind a `sympLPN→LPN` collapse would require.

So LPN's self-reductions are **narrow** (search↔decision; some parameter trade-offs) and do
**not** include a general poly-sample random self-reduction. A non-linear `sympLPN→LPN`
reduction, per the authors, would *improve* exactly this — hence it would have to **go beyond
the known limits of LPN self-reducibility**. That is a genuine obstacle, not a slogan.

## §3 No 2026 resolution of the non-linear question

The focused scan surfaced only the two source papers (2603.19110, 2509.20697) and adjacent
items (a QIP'26 showcase from Vaikuntanathan's group; an ITCS'26 "Decoding Balanced Linear
Codes with Preprocessing" — decoding-with-preprocessing, not the reduction question). **No
work resolving `non-linear sympLPN → LPN`** appeared. The open point is, externally too, still
open — consistent with Lane A and the capstone.

## §4 Verdict (Sound Verifier)

**The win-win barrier is meaningful (status unchanged: OPEN).** A non-linear `sympLPN→LPN`
reduction would have to exceed the known (limited) state of LPN self-reducibility — so the
barrier is a real obstacle backed by an independent hard problem, not mere rhetoric. This
*strengthens the evidence* around the single open point without settling it. **Evidence, not
proof; secondary sources (verify against primary LPN-self-reduction literature before
citing); no 7th; no security claim.**

---

## References (web, June 2026; secondary)
- LPN self-reduction / amplification: *Cryptography from LPN*; *On Learning Parities with
  Dependent Noise* (arXiv:2404.11325); *On the Hardness of Sparsely Learning Parity with
  Noise*; *Low-Noise LPN sample amplification* (IET 2016).
- Sources: 2603.19110 §2.4 (win-win remark), 2509.20697 (sympLPN as the LPN↔stabilizer bridge).
- In-house: Lane A (`2026-06-06-lane-A-lsn-lpn-reduction-scope.md`).
