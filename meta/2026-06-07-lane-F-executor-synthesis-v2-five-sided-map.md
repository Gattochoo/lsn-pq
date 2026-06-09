# Lane F — executor synthesis v2: the five-sided map of LSN (supersedes the addendum's index)

> The original capstone addendum (`39be9e32`) indexed the executor lanes through D/C3. The run
> has since added five lanes and a live collaboration, so the executor-side synthesis is updated
> here: **LSN has now been probed from FIVE independent sides — reduction, decoders, average-case
> constructions, worst→avg, and quantum attack — and all five obey the wall at crypto complexity.**
> The entire 7th question reduces to **three precisely-named open propositions, all ≈0 in-house /
> external.** This is the current executor map; the adjudicator's `…CAPSTONE-7th-hardness-final-
> report.md` remains the FINAL verdict. Sound Verifier throughout; no 7th; no security claim.
> Date: 2026-06-07.

---

## 한국어 요약

```text
LSN을 다섯 독립 측면에서 공략 → 전부 crypto 복잡도에서 벽:
 1 reduction : LSN⊀LPN은 linear만 증명(A+suppl) · LSN⊇LPN(C2 degeneracy/C4 completion engine,
               코드검증) · end-to-end는 decision-distinguisher 존재증명, in-house 계산 불가(C5).
 2 decoders  : 고전 3 family(bucket-rank Task5 / signal-vanish C3 / spectral C6) + Codex →
               channel-level 폐쇄(poly-sample서 신호 소멸).
 3 avg-case  : framework-exhaustion(B1 서베이 새 source 없음 / B2 신선 후보 5개 fold).
 4 worst→avg : SATURATED — subspace decoupling은 SvN-irreducibility(adjudicator)로 닫힘, 국한
               (C7) + 스케일링(C8↔Codex OFA-342 수렴). fresh-noise encoding만 OPEN.
 5 quantum   : death-mode ⑤ — 자연 symplectic-Fourier sampling 공격은 autocorrelation의 Fourier
   attack      쌍대라 walled(Lane E). beyond-Fourier(non-Clifford/period-finding)만 OPEN.
세 열린 명제(전부 ≈0 외부/research-discovery): (i)외부 LSN⊀LPN any-reduction (ii)worst→avg
 fresh-noise encoding (iii)beyond-Fourier 양자 break. 7th 증명 없음·OPEN=LSN·보안 주장 없음.
```

## §1 The five-sided map (each side → the wall)

```text
 SIDE              key result                                         lanes / scripts        status
 ───────────────────────────────────────────────────────────────────────────────────────────────
 1 reduction       LSN⊀LPN proven LINEAR-only (info-theoretic; win-   A, A-suppl, C(17),     WALL
                   win-guarded); LSN⊇LPN (degeneracy + completion     C2(18), C4(20), C5     (open: any-
                   engine, code-verified); end-to-end = decision-     reduction)
                   distinguisher proof, not in-house-computable
 2 decoders        3 classical families all wall at poly-sample,      Task5(16), C3(19),     WALL
                   channel-level closure (signal → 0)                 C6(21) + Codex
 3 avg-case        no new 2026 source; 5 fresh candidates all fold    B1, B2                 WALL
                   into known frameworks (G1∧¬④ = new framework ≈0)
 4 worst→avg       subspace code/noise decoupling CLOSED by Sp-       C7(22), C8(23) +       WALL
                   irreducibility (= SvN rigidity); localized +       SEED + adjudicator     (open: fresh-
                   scaled (K(n)=2,3,6). instance-rand free=trivial.   (SvN)                  noise encoding)
 5 quantum attack  natural symplectic-Fourier (Weil) sampling is      E(24)                  WALL
                   Fourier-dual to autocorrelation → walled;          (death mode ⑤)         (open: beyond-
                   reveals L clean (ratio=2^n) but →uniform at poly                          Fourier)
```

Five methodologies sharing little machinery — proof-scope analysis, structural decoders,
construction screening, representation-theory (Weil/SvN), and quantum Fourier sampling — all
land on the same wall at (constant rate ∧ poly samples). The convergence is now five-fold.

## §2 The three open propositions (all ≈0 in-house / external)

```text
 (i)   external `LSN ⊀ LPN` for NON-LINEAR/adaptive reductions
       (linear ruled out; win-win-guarded: a reduction would improve LPN self-reductions).
 (ii)  worst→avg via a FRESH-NOISE encoding of worst-case stabilizer decoding into avg sympLPN
       (the subspace/symmetry route is closed by SvN-irreducibility; this one is untouched).
 (iii) a quantum break BEYOND structure-aware Fourier sampling (non-Clifford / period-finding;
       the relevant Heisenberg-Weyl structure is non-abelian-HSP, no obvious Shor foothold).
```

All three are research-discovery / community-scale. None is an in-house gap; each is the precise
external frontier of one side. (i) is the in-house program's designated single open point; (ii)
and (iii) emerged from this run's worst→avg and quantum lanes.

## §3 Verdict (Sound Verifier)

**No 7th found or proven; LSN is the unique survivor, now walled from five independent sides;
the question reduces to three precisely-named external propositions.** This updates the
executor-side record (the addendum `39be9e32` covered sides 1–3 partially through D/C3; sides
4–5 and the open propositions (ii),(iii) are added here). The adjudicator's FINAL capstone
stands as the program's verdict; this is its current executor-side map. **No security claim;
OPEN = LSN, presumed insecure pending external review.**

```text
in-house: CONCLUDED (adjudicator FINAL). executor map: 5 sides walled, 3 open propositions.
7th ⟺ resolving any of: LSN∖LPN non-linear (i) | worst→avg fresh-noise (ii) | beyond-Fourier quantum (iii).
```

---

## References (executor lanes, on `shared/hardness-7th-exchange`)
- Reduction: A (`…lane-A-lsn-lpn-reduction-scope`), A-suppl, C (`17`), C2 (`18`), C4 (`20`), C5.
- Decoders: Task5 (`16`), C3 (`19`), C6 (`21`).
- Avg-case: B1, B2.
- Worst→avg: C7 (`22`), C8 (`23`); SEED (parallel) + adjudicator SvN (`…lane-adjudicator-svn-…`).
- Quantum: E (`24`).
- Synthesis: D (three-sided), addendum (`39be9e32`), this v2. Adjudicator FINAL: `…CAPSTONE-7th-hardness-final-report.md`.
