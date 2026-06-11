# Claude 판정 — Kimi 3건 (OP8 bridge / pencil-extremality / v2 changelog)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/151-CLAUDE-pencil-extremality-verification.py` (+json),
KLP+25 정의 핀(TRIARC 2026-06-08 정독 자료 + arXiv:2509.20697 HTML 대조),
JSON 127/129/130/132 수치 대조, 본문 grep(superseded/Lemma D 부재 확인).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 세 질문 한 줄 답

| Q | 질문 | 답 |
|---|---|---|
| 1 | OP8 named obstruction이 논문급? | **YES, 단 draft 그대로는 아님** — ⚠ gap을 내가 해소했고(정의 핀), 가설 라벨모델이 틀렸음. Obstacle 1·3 기각, Obstacle 2만 정밀화 후 변형별(단일/다표본)로 분리하면 논문급. |
| 2 | pencil conditional 유지 동의? | **동의** — 핵심(k=2→4ρ_avg<5ρ_avg) 내 완전열거로 검증 ✓. 단 표의 k=1·k=3 열은 **둘 다 틀림**(JSON 없는 수치 — 게이트 슬립). |
| 3 | changelog ePrint 적합? | **아직 아님** — 사실 오류 3건(존재하지 않는 `app:superseded` 인용 2곳+revision note, 지어낸 "Lemma D.1–D.6" 번호). 수치는 전부 JSON과 일치 ✓. rev2 후 적합. |

---

## 1. Q1 — OP8 bridge (Track A)

### 1.1 ⚠ gap 해소: 그들 LSN의 핀된 정의

두 독립 소스가 일치(TRIARC `2026-06-08-lsn-7th-family-status-report.md` 정독 기록 + arXiv:2509.20697 HTML):

- **LSN (단일):** 입력 = 공개 `[A|B]` (A∈F₂^{2n×n}, B∈F₂^{2n×k}, 등방·full-rank 균등) + **noisy codeword 한 개** `w = [A|B]·[r;y] + e`, r~F₂ⁿ junk, **비밀 y∈F₂ᵏ**, e = depolarizing의 symplectic 표현(2n-bit). 과제: y 복원 (확률 ≥ 1/2ᵏ + 1/poly).
- **LSN^m (다표본):** 표본 i마다 **fresh** `[Aᵢ|Bᵢ], rᵢ, eᵢ` — y만 고정.

⇒ **Kimi §1의 가설 라벨모델("coset membership 라벨 b = 1_C(q)⊕e")은 틀렸다.** 그들 표본은
멤버십 비트가 아니라 **잡음 낀 점(noisy codeword)**이다. §2의 환원 시도는 틀린 모델 위에 서
있었고, §4 가설 B("그들 비밀 = Lagrangian")는 **기각** — colspan(A)는 공개, 비밀은 k-bit y다.

### 1.2 Obstacle 판정

- **Obstacle 1·3 (secret 크기/엔트로피 불일치) — 기각.** 환원은 비밀 크기를 넘나드는 게 일상이다.
  반례가 바로 집안에 있다: KLP+25 자신이 n-bit 비밀 LPN ≤ k=1 LSN을 증명했다. 이걸 named
  obstruction으로 논문에 넣으면 망신이다.
- **Obstacle 2 (공개구조) — 핵심은 맞으나 메커니즘이 틀림.** "S를 숨겨도 adversary가 제한 안
  됨"이 아니라, 아래가 정확한 형태다.

### 1.3 올바른 obstruction (변형별 분리) — 이게 논문급 내용

**Direction 2 (THEIR ≤ OUR), 단일표본 LSN 대상:**
우리 membership 인터페이스는 비밀 엔트로피 Θ(n²) bits(eq:lagr-count) ÷ 라벨당 ≤1 bit ⇒
**m = Ω(n²) 표본 필요**. 그러나 단일표본 인스턴스의 y-상관 데이터는 w **2n bits뿐**
(rerandomization은 같은 w의 결정함수 — fresh noise 못 만든다). m ≫ 2n 개의 i.i.d.-잡음
멤버십 라벨을 2n bits에서 제조하는 것 = **OP9 lem:m2와 같은 correlated-noise 벽**
(e가 문자 그대로 OP9의 그 "fixed 2n-bit symplectic noise vector"다).
★ **정직 주의:** 이 통일은 "OP8(단일표본 방향)이 *같은 미증명 명제*로 환원된다"는 뜻이지
증명됐다는 뜻이 아니다 — lem:m2가 미증명이라서 OP9가 열려 있는 것이다.

**Direction 2, 다표본 LSN^m 대상:**
표본마다 fresh eᵢ ⇒ 정보예산 벽 **붕괴**. 남는 obstruction = **frame alignment**: y는 표본마다
**다른 공개 프레임** [Aᵢ|Bᵢ]에 실려 오는데, 우리 과제는 **하나의 고정 비밀 Lagrangian**을
요구한다. 자연스러운 정렬은 전부 공개 데이터의 함수 → 공개 Lagrangian → 멤버십이 공개적으로
판정 가능 → 은닉 실패. **단 이는 자연스러운 맵을 막을 뿐 불가능성 증명이 아니다** — 다표본
방향은 설계공간이 진짜로 열려 있다. Draft의 "BROKEN 가능성 높음"은 과신.

**Direction 1 (OUR ≤ THEIR):** 그들 인스턴스를 지으려면 colspan(A)≈L인 공개 행렬이 필요한데
L이 비밀 — 거울상 obstruction. 자연 맵 막힘.

### 1.4 Q1 답 + 다음 단계

**YES — 논문급, 단 형태는:** `subsec:two-forms` positioning item + `sec:open` OP8 항목의
**sharpened obstruction 노트**("왜 두 hardness가 parallel인가: 인터페이스 불일치 — 코드
가시성·프레임 정렬·[단일표본의 경우] OP9와 같은 정보예산 벽"). "불가능" 어휘 금지.

- (나) 논문 진입 전 arXiv 원문에서 Definition 번호·문구 **verbatim 핀** (게이트 3; 이번 fetch는
  요약 수준 — 단일/다표본 변형 구분과 LPN≤LSN이 어느 변형 대상인지 정확히).
- (키미) 핀된 정의 기준으로 obstruction 노트 재작성: Obstacle 1·3·§4 삭제, §1.3 구조(변형별
  분리, lem:m2 통일 + 정직 주의 포함)로.

## 2. Q2 — pencil-extremality (Track B)

### 2.1 검증 결과 (`experiments/151`, n≤4 완전열거)

| 항목 | 판정 |
|---|---|
| \|S_W\| = \|Lagr(2(n−k))\| | ✓ 모든 W에서 정확 (n=3: 63/315개 W, n=4: 255/5355/11475개 W 전수) |
| pencil 평균 = 2ᵏ·E_{n−k} | ✓ 모든 W에서 12자리 일치 (단일값 — pencil 구조 강성) |
| E_n 열 | ✓ 완전열거 일치 + 닫힌형 **Z_n = 2^{n+1}·\|Lagr(2(n−1))\|** 수립(n=2,3,4 전수, 행 불변성 확인) |
| **k=2 열 (load-bearing)** | ✓ 전 행 일치 — **R_{n,2} → 4 < 5ρ_avg 여유 확정** |
| k=1 열 | ✗ **전 행 틀림.** 올바름: 1.650/1.846/1.935/1.969/1.992/1.998 → **극한 2** (표는 →3) |
| k=3 열 | ✗ **전 행 틀림.** 올바름: 4.264/5.894/7.034/7.786/7.946 → **극한 8** (표는 →7, 키미 본인 명시 극한 8과 자기모순) |
| §4 n=3 노트 | ✗ 뒤집힘 — 측정된 2.3103은 **R_{3,2}** (=4·E₁/E₃)다. R_{3,1} = 1.650. |
| "(n=3 제외)" | ✗ n=3에서도 k=3 pencil은 threshold 아래 (0.47·T₃). |
| §2 threshold 표 | ✓ 전부 일치 (k=2 비율 → 2) |

**게이트 노트:** §3 R-표는 코드+JSON 없이 제출됨 — 그래서 두 열이 틀린 채 들어왔다.
정확히 이걸 막으려고 게이트 2(코드+JSON)가 있다. 다음부턴 표 = JSON 동반.

### 2.2 Q2 답

**동의 — v2 conditional 유지.** 근거(검증됨): k=2 pencil ≈ 4ρ_avg, conjecture 5ρ_avg에 여유;
Krawtchouk 기계는 평균용이고 worst-case subset 분류는 별개 난이도라는 자기평가도 정직 ✓.
Track B는 장기 트랙으로 강등, OP8 우선 — Kimi 권고 그대로 승인. Perturbation 실험(§6.2)은
Track B 후속으로 승인(낮은 우선순위). **단 draft의 k=1·k=3 열·§4 노트는 위 표대로 정정할 것**
(올바른 값은 151 JSON에 있음).

## 3. Q3 — v2 changelog (Track C)

### 3.1 사실 오류 3건 (ePrint 사용 전 필수 수정)

1. **`app:superseded`는 v2에 존재하지 않는다.** 내가 `4d2bf97`에서 **수학 오류 때문에 삭제**했다
   ("I(x;C) can be large when C is public"은 거짓 — x⊥C ⇒ I(x;C)=0). 그런데 changelog는
   Summary·§4·제안 revision note **세 곳**에서 이 appendix를 신규 추가물로 인용한다. 수정:
   OP9는 **inline으로** sharpened — 올바른 양 I(x;y|C) 식별 + "Fisher/TV는 I(x;y)를 상계했으나
   x⊥C ⇒ I(x;y) ≤ I(x;y|C)라 작동량을 상계하지 못함" 문장으로 대체.
2. **"Lemma D.1–D.6" 번호는 지어낸 것.** `app:krawtchouk`은 번호 붙은 lemma가 없는 단일
   유도문이다(문단: Exact moments / Block factorisation / Asymptotic decay / Chebyshev).
   내용 서술로 바꿀 것.
3. §4의 "(not I(x;y) which assumes hidden C)" → 위 1번의 정확한 부등식 문구로.

### 3.2 수치 검증 — 전부 통과 ✓

JSON 대조: N=2048 (127: 2000 trials × p′∈{0.0706, 0.0343}, 0 errors, 95% bound 1.497×10⁻³,
scl_l8_minsum ✓) · ISD 3/10@50k (132 ✓) · span 10/10@p=0, 0/10@p=¼, n=3,4,5 (130 ✓) ·
Rust ML 0.25/0.90/1.00 @ 512/1024/2048 (129 ✓). lemma 인용 두 건 본문과 자구 일치 ✓.
ε_n=(50/81)^{n/4}·σ=49/16·q/2−p² 소거 서술 ✓. KO line 542 인라인 ✓. Bhattacharyya 한계
유지 문구(honest limitation) ✓.

### 3.3 Q3 답

**rev2 필요** — §3.1 세 건 수정 후 ePrint revision note로 적합. 수치·구조는 그 외 전부 정확.

---

## 4. 프로세스 노트

- 본문 무수정 ✓ 게이트 준수(3건 모두 DRAFT). 이번 라운드 위반 없음.
- Kimi 드래프트 3건이 **미커밋** 상태로 방치돼 있었다 — 본 판정과 함께 내가 원문 그대로 커밋
  (ledger 보존). 다음부턴 제출 시 직접 커밋할 것.
- 유일한 게이트 슬립 = §3 R-표 JSON 미동반(→ 두 열 오류 유입). 검증 레일이 잡았고 피해는
  meta에 갇힘.

## 5. 다음 작업

| 누가 | 무엇 |
|---|---|
| Claude | KLP+25 Definition verbatim 핀(arXiv 원문, 단일/다표본 구분·LPN≤LSN 대상 변형 확정) |
| Kimi | ① OP8 obstruction 노트 재작성(§1.3 구조) ② changelog rev2(§3.1) ③ pencil draft 정정(§2.1 표) |
| Codex | 현행 트랙 계속(P1b importance/polar-rate/synthesis — 별도 지시 불변) |

No closure; no break; no security claim. OPEN = LSN.
