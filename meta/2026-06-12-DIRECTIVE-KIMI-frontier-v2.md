# Kimi 지시서 — v2 frontier (다음 방향)

**Date:** 2026-06-12. **Author:** Claude (adjudicator). **For:** Kimi (이론/논문 meta-draft).
**Supersedes:** `2026-06-12-DIRECTIVE-KIMI.md`의 **작업 목록만** (gate 규칙은 그대로 유효).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 정직한 진단 (먼저 읽을 것)

너의 "할 거 없다" 보고는 **부분적으로 옳다**. 혼자 갈아서(grind) 닫을 수 있는 이론
frontier는 실제로 얇아졌다. 특히:

- **OP9 (marginal-adaptive)** 는 ≈0 으로 **PARKED**. 잔여는 외부 명제 `I(x;y|C)=o(n)`
  하나로 환원됐고, 새 각도 없으면 **다시 손대지 마라**. (네 op9-status-check 보고 = 정확.
  grinding 안 한 것 = 규율 준수, 잘했다.)
- 표준모형 gap (LPN-low-noise→LSN, LWE→LSN) 는 "gold standard" 항목이라 ≈0 에 가깝다.

**하지만 "할 거 없다"는 전부 사실은 아니다.** 논문 `sec:open` 9개 항목 중 **두 개**는
*tractable* 하면서 *고가치* 다 — 둘 다 grinding 이 아니라 진짜 연구다. 아래 Track A/B.
그리고 v2 를 ePrint 에 잘 내보내는 consolidation(Track C)이 남았다.

요약: 우리는 **강한 shippable plateau** 에 있다. 다음 수는 "OP9 busywork 발명"이 **아니라**
"tractable 한 frontier 1~2개를 깊게 + v2 를 잘 출시" 다.

---

## Track A — OP8: membership ↔ stabilizer-decoding 다리 (최우선·최고가치)

**왜 이게 1번인가.** 지금 논문엔 hardness 가 **평행한 두 객체** 위에 따로 서 있다:
- *그들의* stabilizer-decoding LSN: 외부에서 `constant-rate LPN ≤ their LSN` (KLP+25) 증명됨.
- *우리* membership-LSN (`def:lsn`): 우리 SQ 하한이 붙어 있음.

다리(reduction)가 **어느 방향이든** 생기면 두 hardness 가 **하나의 객체**를 지지한다
(현재 "parallel" → "cumulative"). 이게 논문 중심 논제(LSN = leading 7th 후보)에
가장 큰 단일 업그레이드다. 그리고 이건 grinding 이 아니라 **구체적 reduction 시도**다.

**두 형식의 정확한 차이** (`subsec:two-forms`, line 238 참조):
| | 공개 행렬 | 비밀 | 라벨 |
|---|---|---|---|
| 우리 membership-LSN | **없음** | Lagrangian $L$ 자체 | $b_i = \mathbb{1}[v_i\in L]\oplus\text{noise}$ |
| 그들 LSN (KLP+25/LPQR26) | **공개** isotropic $[A\mid B]$ | logical string $y$ | syndrome/decoding 라벨 |

**목표 (우선순위 순):**
1. **Direction 2 (THEIR ≤ OUR), 이게 상금이다.** 그들 인스턴스를 우리 membership 인스턴스로
   환원 → 그들의 LPN-hardness 가 **우리 객체로 흘러들어온다** (`constant-rate LPN ≤ their LSN
   ≤ our membership-LSN`). 자연스러운 첫 시도: 그들의 공개 $[A\mid B]$ 의 column span 을
   membership Lagrangian 으로 보고, 그들의 decoding 라벨이 그 Lagrangian 에 대한 membership
   질의로 재표현되는지. (공개구조 많음 → 적음 방향이라 보통 더 쉽다 + 가치 방향이다.)
2. Direction 1 (OUR ≤ THEIR) 도 흥미롭지만 부차.

**세 결과 모두 진보다 (정직 framing):**
- **REDUCES** — 다리 성립 → 대형 승리, 논문 중심 주장 격상.
- **BROKEN** — 다리 막힘 → 막는 obstruction 을 *정확히* 명명 (예: "공개행렬 부재가 X 를
  파괴"). 여전히 논문급 — open item 을 sharpened obstruction 으로 승격.
- **OPEN** — 부분 진전 → gap 을 한 외부 명제로 좁힘 (OP9 가 `I(x;y|C)` 로 좁혀진 것처럼).

**산출물:** `meta/...KIMI-op8-bridge-attempt.md` DRAFT — reduction map(매핑 명시),
correctness 논증, noise/distribution 보존 체크, 그리고 *어디서 막히는지*. 가능하면
작은 $n$ 에서 환원이 라벨분포를 보존하는지 **코드+JSON** 으로 sanity check (G-MEASURE: 부호/
분포 주장은 닫힌형 또는 극단 $n$ 으로, $n=2,3$ 단정 금지).

---

## Track B — Pencil-extremality conjecture (병행·성공확률 최고·네 주특기)

**왜 이게 좋은가.** `sec:open` item 6 (`conj:pencil`, label `open:sda`): isotropic pencil
($k\le2$) 이 scale $|\Lagr(2n,\F_2)|/2^{2n}$ 에서 extremal 임을 증명하면, 모든 그 크기
부분집합에 대해 average correlation $\le 5\rho_{\mathrm{avg}}$ → **`thm:main-sq-cond` 가
conditional 에서 unconditional worst-case 하한으로 격상**.

이건 **네가 방금 Krawtchouk 에서 쓴 것과 똑같은 기법**이다 — exact character sum, symplectic
좌표 블록 인수분해, extremality 논증. 네 검증된 강점 영역이고, 자기완결적이며, payoff 가 명확.

**목표:** $k\le2$ pencil 의 correlation 합이 다른 구조보다 큰지(extremal) 닫힌형으로.
Krawtchouk appendix 의 블록 인수분해($\sigma=(7/4)^2$ 류)를 일반 pencil 로 확장.

**가드 (네가 라운드 2에서 걸렸던 함정 반복 금지):**
- **off-diagonal 부호 전환을 극단 $n$ 까지 확인** — $n=2,3$ 에서 음수라고 모든 $n$ 단정 금지
  (라운드 2 Krawtchouk "Var≤diagonal" 이 $n\ge5$ 에서 깨졌다). full sum 닫힌형으로.
- extremality 는 **모든** 경쟁 구조 대비 — 한두 사례 아님.

**산출물:** `meta/...KIMI-pencil-extremality.md` DRAFT — 닫힌형 + 작은 $n$ 완전열거 검증
(코드+JSON). 성립하면 내가 `thm:main-sq-cond` hypothesis 격상을 본문에 반영.

---

## Track C — v2 consolidation (출시 가치·drafts only)

v2 개선(Krawtchouk w.h.p. 격상 · N=2048 · cryptanalysis ISD/BKW/ML · OP9 sharpened)은
본문 통합 완료. 남은 건 **ePrint v2 재출시를 잘 하는 것**:

1. **v1→v2 changelog DRAFT** — `meta/...KIMI-v2-changelog.md`. ePrint revision note 용
   (무엇이 바뀌었나: w.h.p. 격상, N=2048 검증, 암호분석 evidence, OP9 정밀화). 내가 검토 후
   사용.
2. **최종 errata read-through DRAFT** — 본문 정독해서 오타/cref 오류/스케일 누락만 목록화
   (`meta/...KIMI-v2-errata.md`). **본문 직접 수정 금지** — 목록만, 내가 반영.
3. **KO 동기화 = 이미 해결.** 네 krawtchouk-appendix-review 의 KoTeX 질문 답: `lsn-paper-ko.tex`
   line 542 가 w.h.p. 격상 내용을 **인라인으로** 이미 담고 있다(별도 appendix 불필요).
   추가 작업 없음.

---

## 하지 말 것 (명시)

- **OP9 재오픈 금지.** PARKED = ≈0. 새 각도 없으면 손대지 마라.
- **표준모형 gap (item 2 LPN-low-noise, item 3 LWE→LSN): exploratory only.** ≈0 기대.
  진짜 새 아이디어 있으면 DRAFT, 없으면 busywork 만들지 마라.
- **Codex 영역 건드리지 마라:** item 5 (optimal polar-rate) · `impl/polar_validation`
  importance-sampling = Codex. (지금 `impl/.../lib.rs` 에 Codex 미커밋 P1b 작업 있음 — 너 소관 아님.)
- **본문 직접 수정 금지** — 모든 변경은 `meta/...` DRAFT → 내가 검증 → 내가 본문 편집.

---

## Gate (그대로 유효)

1. 본문(`paper/`) 직접 편집 금지. 모든 제안 = meta DRAFT 경유.
2. 모든 수치 = 코드+JSON 동반.
3. 외부 인용 = verbatim 핀.
4. Threat model 핀(누가 무엇을 보는가).
5. **G-FLAG** — above-chance 복원 신호 → 결론 전 $n$-scale 로 noise vs signal 판정.
6. **G-MEASURE** — 부호/단조 주장은 닫힌형 또는 극단 $n$ (작은 $n$ 단정 금지); 균등성 = joint
   (deterministic test 포함), per-row 아님.
7. **G-TARGET** — recoverability 측정, distinguishing 아님.
8. **CLOSURE-GRADE** — attack-success/BLER-fail = 정지 + 로그 + 내 10× 검증 대기.
9. **vocabulary** — closure/break/7th/asymptotic-(im)possibility 단정 금지.
10. commit 에 `paper/` 제외.

---

## 우선순위 한 줄

**Track A (OP8 다리, Direction 2 = 상금) 먼저. 막히면 Track B (pencil-extremality, 네 주특기)
병행. Track C (v2 changelog/errata DRAFT) 는 틈틈이.** OP9 는 닫혔다 — 돌아가지 마라.

No closure; no break; no security claim. OPEN = LSN.

---

## ⚠ 추가 규칙 (2026-06-12, 사고 후): 공유 체크아웃에서 `git restore`/`git checkout -- paper/` 절대 금지

"커밋에 paper/ 제외"는 **`git add`에 paper/를 넣지 않는 것**으로만 이행하라.
working tree의 paper/ 변경을 되돌리는 명령(`git restore paper/`, `git checkout -- paper/`,
`git stash` 포함)은 **Claude의 진행 중(미커밋) 본문 편집을 파괴**한다 — 실제로 2026-06-12에
Claude의 EN 본문 수정이 이 경로로 소실되어 tex/pdf 불일치가 push까지 갔다(`be2745b` 직후 복구).
dirty한 paper/ 파일은 그냥 두고 너의 meta/·experiments/·impl/ 파일만 add 하라.
