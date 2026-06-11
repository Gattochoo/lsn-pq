# KLP+25 (arXiv:2509.20697) Definition Pins — OP8 bridge 기초자료

**Actor:** Claude (adjudicator). **Date:** 2026-06-12.
**Source:** arXiv:2509.20697 "Hardness of decoding random quantum stabilizer codes"
(Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan), HTML 버전 fetch.
**매체 주의:** arXiv HTML을 fetch 도구(소형모델 매개)로 추출 — 서론(§1)은 인용 확보,
**본문(§3 이후)은 페이지 절단으로 미확보**. 아래 인용은 서론/기술개요의 verbatim 추출이며,
**formal 정리 번호·정확한 변형은 논문 인용 전 PDF 재확인 필수** (§4 참조).
2026-06-08 TRIARC 정독 기록(`...lsn-7th-family-status-report.md`)과 교차 일치 확인됨.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. 핀된 정의 (서론 verbatim)

### 1.1 다표본 변형 LSN^m — §1.2.1

> "In the first, we define LSN^m(k,n,p) by providing m noisy codewords. Each "sample" has
> a fresh error **E** and fresh code **C**, but has the *same* secret logical state x ∈ Z₂^k."

확정 사실: **표본마다 code(공개 행렬)와 error가 새로 뽑히고, 비밀 y(k-bit)만 고정.**
base `LSN` (위첨자 없음) = 표본 1개. stateLSN^m(Haar-random 논리상태 변형)도 존재.

### 1.2 고전(symplectic) 표현 — §1.2.2

> "Let A_i ∈ Z₂^{2n×n} be a random matrix whose columns are all orthogonal in the
> symplectic inner product. Let B_i ∈ Z₂^{2n×k} be a random matrix with the same property,
> such that all columns of A_i and B_i are collectively linearly independent. Let
> r_i ∈ Z₂^n be a random string, and e_i ∈ Z₂^{2n} be the symplectic representation of
> a Pauli drawn from the depolarizing distribution."
>
> "The search task is, given m samples of ([A_i|B_i], [A_i|B_i]·[r_i; y]+e_i), to find y"

확정 사실:
- 표본 = **noisy codeword** (잡음 낀 점) — 멤버십 라벨 아님. Kimi 가설모델 기각 재확인.
- A_i: n열 쌍별 심플렉틱 직교 ⇒ colspan(A_i) = **라그랑지안(공개)**.
- B_i: k열 서로 등방 + A와 합쳐 선형독립. **⇒ [A|B] 전체는 등방일 수 없다**
  (n+k 독립열 > 최대 등방차원 n). — 우리 논문이 "public isotropic matrix [A|B]"라고
  쓴 것은 **불가능한 서술**이었음 → 본 커밋에서 수정 (EN line 238·1171, KO 동기화).

### 1.3 LPN → LSN 하드니스 — Thm 1.6 (informal) + 기술개요

> Thm 1.6 (informal): "Fix any k≥1 and p∈(0,1) which is not necessarily a constant.
> There exists a reduction from LPN(⌊np/6⌋, 2n, p/6) to LSN(k,n,p)."

기술개요의 변형 관련 인용:
> "Unfortunately, we are able to prove a decision-to-search reduction in the case of
> multiple samples. More precisely, we can reduce Decision LSN^{2m}(k,n,p) to
> Search LSN^m(k,n,p)."
> "we must prove a new reduction directly to Decision LSN²"
> "a reduction from Decision LPN to Search LSN^{poly(n)}"

## 2. ⚠ 미해소 잔여 (PDF 재확인 항목 — 본문 인용 금지)

**그들의 LPN-하드니스가 정확히 어느 변형에 떨어지는가:**
- 인용 조합 (i): "Decision LPN → Search LSN^{poly(n)}" ⇒ 다표본 search.
- 인용 조합 (ii): "Decision LPN → Decision LSN²" + "Decision LSN^{2m} ≤ Search LSN^m"을
  m=1로 합성하면 **Decision LSN² ≤ Search LSN¹ ⇒ 단일표본 search에도 하드니스**가
  떨어질 *수도* 있다.
- (i)·(ii)가 양립하는지, informal Thm 1.6의 formal counterpart(정리 번호·정확한 statement)가
  무엇인지는 **HTML 절단으로 미확인**. → 논문 본문에 변형-귀속을 쓰기 전에 PDF에서
  formal 정리(아마 §6 "Average-Case Hardness...")를 직접 확인할 것.
- **이 잔여가 OP8 obstruction 분기의 사활이다**: 단일표본 search에 하드니스가 떨어지면
  정보예산 벽(=OP9 lem:m2 통일) 쪽이 하드니스-운반 변형을 직접 겨냥하고, poly-표본에만
  떨어지면 frame-alignment 벽이 작전구역이다.

## 3. 본문 정밀도 수정 (이 커밋, 내 소관 편집)

| 위치 | 전 | 후 |
|---|---|---|
| EN line 238 (two-forms) | "public isotropic matrix [A\|B]" | A-블록 라그랑지안·B-블록 등방·연접은 등방 불가 명시 + noisy-codeword 표본 형태 + LSN^m fresh-matrix 사실 추가 |
| EN line 1171 (OP8) | "(public isotropic matrix, …)" | "(public stabilizer matrix [A\|B] with a Lagrangian A-block, noisy-codeword samples, …)" |
| KO 199·597 | 동일 오류 | EN과 동기화 |

추가·수정된 내용은 전부 §1의 핀에서 직접 따름(불확실 사항 §2는 본문 미반영).

## 4. Kimi OP8 재작성에 주는 의미 (지시 갱신)

판정문(`2026-06-12-CLAUDE-adjudication-op8-pencil-changelog.md`) §1.3 구조 유지하되:
1. 정의는 본 문서 §1을 기초로 (가설 ⚠ 불필요 — 핀 완료).
2. 변형별 obstruction 분리 유지(단일표본 = 정보예산/lem:m2 통일 · 다표본 = frame-alignment).
3. **§2의 미해소 잔여(하드니스 귀속 변형)는 열린 채로 명시** — "어느 변형이 하드니스를
   운반하는가"를 전제하지 말 것. 두 경우 모두를 다루는 조건부 서술이 정직한 형태.
4. "BROKEN 가능성 높음" 같은 가능성 단정 금지(게이트 9).

No closure; no break; no security claim. OPEN = LSN.
