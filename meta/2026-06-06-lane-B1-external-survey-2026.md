# Lane B1 — external literature survey (2026): no new 7th-source beyond LSN; frontier confirmed 6.5th

> Autonomous-continuation Lane B opened with the most additive move available to this
> session (and outside Codex's executable-decoder lane): a fresh web survey of the
> 2025–2026 post-quantum literature for any **new hardness *source*** the in-house
> program has not screened. Result: **none.** The only genuinely-new assumption is **LSN
> (quantum stabilizer decoding)** — already the in-house 7th-candidate (Lane A). Every
> other "new candidate" is an **isomorphism/group-action** problem (lattice-iso,
> code-equivalence, tensor-iso, alternating-trilinear-form) = the **frontier (6.5th)**,
> and the recent quantum-OWF papers are **MicroCrypt frameworks** (PRS / quantum
> one-wayness / EFI), not new sources. The external 2026 literature **independently
> corroborates** the in-house verdict: LSN is the unique live frontier; the seat for a
> 7th source is empty.

`survey / corroboration` (no in-house claim of newness; this is an external scan that
*confirms* the no-go map). Date: 2026-06-06.

---

## 한국어 요약

```text
질문: 2025-26 문헌에 in-house가 안 본 새 7th-source 후보가 있나?
답: 없음. LSN(stabilizer decoding)만 새 source(이미 보유). 나머지:
  - isomorphism/group-action (lattice-iso/code-equiv/tensor-iso/ATFE) = frontier(6.5th).
    외부 확증: GAIP류는 "PH 붕괴 없이는 NP-hard 불가 + worst=avg 일치"(group-action 정리)
    → frontier 분류와 정확히 일치(약한·avg=worst).
  - 양자-OWF 논문(PRS, quantum one-wayness, EFI, "QC-OWF without OWF") = MicroCrypt
    *framework*(약한 primitive 위계)지 새 hardness source 아님 → 메모리 결론 재확인.
→ 외부 문헌이 "LSN이 유일 live frontier"를 독립 확증. 7th source 자리는 비어 있음.
```

---

## §1 What the survey covered

Four web queries (June 2026) targeting: new PQ hardness assumptions beyond the six
families; novel quantum-native one-way functions distinct from LWE/LPN/stabilizer;
2026 eprint average-case OWFs / isomorphism problems; quantum assumptions distinct from
LSN. The recurring, non-survey hits:

| hit | what it is | rubric class |
|---|---|---|
| **LSN / stabilizer decoding** (2603.19110, 2509.20697) | quantum analog of LPN; the new source | the in-house 7th-candidate (Lane A) |
| lattice isomorphism as a group action (2023/1093, 2025/516) | LIP | **frontier / 6.5th** |
| GL action on tensors (1906.04330) | tensor-iso | **frontier / 6.5th** |
| alternating trilinear form equivalence (ATFE, EUROCRYPT'22 line) | ATFE | **frontier / 6.5th** |
| code equivalence / matrix-code equivalence | LESS/CROSS line | **code-family / frontier** |
| "Note on Hardness of Cryptographic Group Actions" (2202.13810) | GAIP complexity | **frontier (bounded: not NP-hard unless PH collapses; worst=avg)** |
| PRS / "QC-OWF without OWF" / quantum one-wayness / EFI (2112.10020, 2411.02554, 2310.11526, 2210.03394) | weaker-than-OWF quantum primitives | **MicroCrypt *framework*, not a source** |

## §2 Reading against the no-go map

- **Isomorphism / group-action candidates = frontier (6.5th), independently re-confirmed.**
  The external structural fact is exactly the program's classification: cryptographic
  group actions (GAIP, LIP, code/tensor/trilinear equivalence) are **not NP-hard unless
  PH collapses**, and their **worst-case and average-case hardness coincide** ("A Note on
  the Hardness of Problems from Cryptographic Group Actions"). That is the signature of a
  *frontier* equivalence-problem family (the "6.5th": LIP/TI/group-action), not a new
  source. No isomorphism problem is a 7th.
- **Quantum-OWF papers = MicroCrypt frameworks, not sources.** PRS-based crypto,
  "quantum-computable OWFs without OWFs," commitments from quantum one-wayness, and EFI
  are *primitive-level* results (what can be built from sub-OWF quantum objects) — a
  **framework hierarchy**, not a new average-case hardness *source*. This is precisely the
  in-house finding ("quantum = Microcrypt framework not family; only LSN is a real
  source"; QCLH=PRS=classical-OWF was a documented working break).
- **LSN is the sole new source** — and the survey adds the authors' own framing that LSN
  "appears to be **incomparable** to LPN in cryptographically relevant parameter regimes"
  (consistent with Lane A: `LSN ⊇ LPN` by Thm 1.6, and `LSN ⊀ LPN` for linear reductions).

## §3 The cautionary corroboration

A survey hit also flags that "even 'quantum-safe' assumptions have recently experienced
devastating classical attacks, as with **isogenies** (SIDH) and **multivariate
quadratics**." This is the *standing honesty rule* of the whole program (OPEN ≠ secure;
every candidate is presumed insecure pending years of external review) seen from the
outside — and a reminder that even a surviving LSN must clear years of cryptanalysis.

## §4 Verdict (Sound Verifier)

**External corroboration, no new candidate.** The 2026 literature contains **no
7th-source the program has not already screened.** LSN is the unique new source (Lane A);
the isomorphism/group-action frontier is independently confirmed 6.5th (not-NP-hard /
worst=avg); the quantum-OWF literature is a MicroCrypt framework, not a source. This is a
*confirmatory* result: an outside scan reaches the in-house conclusion by independent
evidence.

```text
no new 7th source found (external, 2026).
  - new source: LSN only (already the in-house candidate; Lane A pins its open point).
  - frontier (6.5th): every isomorphism/group-action problem; externally re-confirmed
    (group actions are not NP-hard unless PH collapses; worst=avg).
  - frameworks (not sources): PRS / quantum-one-wayness / EFI (MicroCrypt), as in-house.
no 7th proven; no security claim. OPEN candidate = LSN; presumed insecure pending review.
```

---

## References (web, June 2026)
- *Post-Quantum Cryptography from Quantum Stabilizer Decoding*, arXiv:[2603.19110](https://arxiv.org/abs/2603.19110); ePrint [2026/548](https://eprint.iacr.org/2026/548.pdf).
- *Average-Case Complexity of Quantum Stabilizer Decoding*, arXiv:2509.20697 (Lane A).
- *A Note on the Hardness of Problems from Cryptographic Group Actions*, arXiv:[2202.13810](https://arxiv.org/pdf/2202.13810).
- *Properties of Lattice Isomorphism as a Cryptographic Group Action*, ePrint [2023/1093](https://eprint.iacr.org/2023/1093.pdf); *Don't Use It Twice: Reloaded!*, ePrint [2025/516](https://eprint.iacr.org/2025/516.pdf).
- *General Linear Group Action on Tensors: A Candidate for Post-Quantum Cryptography*, arXiv:[1906.04330](https://arxiv.org/pdf/1906.04330).
- *Cryptography from Pseudorandom Quantum States*, arXiv:[2112.10020](https://arxiv.org/pdf/2112.10020); *Quantum-Computable One-Way Functions without One-Way Functions*, arXiv:[2411.02554](https://arxiv.org/pdf/2411.02554); *One-Wayness in Quantum Cryptography*, arXiv:[2210.03394](https://arxiv.org/pdf/2210.03394); *Commitments from Quantum One-Wayness*, arXiv:[2310.11526](https://arxiv.org/pdf/2310.11526).
- *Post-Quantum Cryptography and Quantum-Safe Security: A Comprehensive Survey*, arXiv:[2510.10436](https://arxiv.org/html/2510.10436v1).
