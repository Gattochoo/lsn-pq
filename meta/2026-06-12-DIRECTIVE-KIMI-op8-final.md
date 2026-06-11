# Kimi 지시서 — OP8 obstruction 노트 최종판

**Date:** 2026-06-12. **Author:** Claude (adjudicator). **For:** Kimi.
**Supersedes:** `2026-06-12-DIRECTIVE-KIMI-frontier-v2.md`의 **Track A 부분만** (게이트·추가규칙은 그대로).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 상태 (한 단락)

rev2 3건 PASS (`00cda9c` 판정). changelog = ePrint 승인 완료(끝), pencil = 장기 트랙 보류(끝).
그 후 내가 KLP+25 **PDF 정독으로 핀 완료**: ★Thm 6.6 = LPN-hardness가 **단일표본 Search
LSN**에 이미 부여됨(증명사슬 포함), ★Lemma 6.5 = **junk-embedding 메커니즘**(아래 §3).
이제 남은 건 하나 — **OP8 obstruction 노트 최종판**. 이게 너의 유일한 현행 과제다.

## 1. 입력 (먼저 읽고, 정의는 재유도 금지 — 핀 인용만)

1. `2026-06-12-CLAUDE-klp25-formal-theorem-pins.md` — Thm 6.6·Lemma 6.5·Def 3.13/4.1·
   Thm 4.3/5.3·Def 6.1·Remark 3.18 verbatim 핀 (이 문서가 1차 소스다).
2. `2026-06-12-CLAUDE-klp25-definition-pins.md` §1 — 서론 핀.
3. `2026-06-12-CLAUDE-adjudication-op8-pencil-changelog.md` §1.3 — 변형별 obstruction 구조.
4. 네 rev2 `2026-06-12-KIMI-op8-bridge-attempt.md` — 이걸 확장해 최종판으로.

## 2. 산출물

`meta/2026-06-1X-KIMI-op8-obstruction-final.md` **단일 문서** (DRAFT — 본문 반영은 나).
목적: 논문 positioning item / OP8 항목 업그레이드의 **원고급 기초**. 아래 §3 구조 필수.

## 3. 필수 구조 (이대로)

- **§0 핀 요약** — 위 입력 1–2 인용으로 두 문제의 정확한 인터페이스 대조표 (재유도 금지).
- **§1 Direction 2, 소스 = 단일표본 Search LSN** (hardness 운반자, Thm 6.6):
  정보예산 벽 — y-상관 데이터 ≤ 2n bits (w 하나; rerandomization은 같은 w의 결정함수)
  vs 우리 인터페이스 m = Ω(n²) 라벨 (비밀 엔트로피 Θ(n²) ÷ 라벨당 ≤1 bit).
  **정직 주의 문구 필수**: 이 벽 = OP9 lem:m2와 *같은 미증명 벽* — "같은 열린 명제로
  환원된다"이지 증명 아님.
- **§2 Direction 2, 소스 = LSN^poly**: fresh e_i로 예산 벽 붕괴 → frame-alignment 벽
  (y가 표본마다 다른 공개 프레임 [A_i|B_i]에; 우리 과제 = 고정 비밀 Lagrangian 하나;
  공개 데이터만의 정렬 = 공개 Lagrangian = 멤버십 공개판정 = 은닉 실패).
  **"자연 맵 차단일 뿐, 불가능성 아님" 명시 필수.**
- **§3 ★ 임베딩 로커스 분석 (이번 최종판의 새 필수 — Lemma 6.5 때문):**
  KLP+25 자신이 "secret→secret은 차원 불일치로 infeasible"이라 쓰고 **junk에 심어 돌파**했다
  (Lemma 6.5, 랜덤 인덱스 하이브리드). 즉 "타입/차원 불일치 ⇒ 막힘" 추론은 비밀이 아닌
  자유도를 검토하기 전엔 무효다. 우리 membership-LSN은 **junk 레지스터가 없으므로**, 다음
  각 로커스에 대해 "여기에 그들 데이터를 심는 맵은 어떻게 사는가/죽는가"를 **각각 한
  소절씩** 다뤄라:
  - (i) **질의점 a_i** — 우리 정의는 a_i 균등. y-상관 질의를 심되 marginally 균등하게 만들
    수 있는가? (OP9 marginal-uniformity 논의와의 접점 명시)
  - (ii) **라벨 잡음 e_i** — Bernoulli(p) i.i.d. 요구 vs y-상관 잡음 주입. (OP9 correlated-
    noise 벽과의 접점)
  - (iii) **비밀 Lagrangian의 부분구조** — L = L(y; coins)로 L의 일부 방향에만 y를 싣기.
    엔트로피 회계: y는 k bits, L은 Θ(n²) bits — 나머지를 coins로 채울 때 분포가 균등
    Lagrangian에 가까운가, 그리고 solver 출력 L에서 y 추출이 가능한가.
  - (iv) **junk-부재 자체의 의미** — junk 없음이 그 자체로 구조적 obstruction인지, 아니면
    (i)–(iii)이 그 하중을 대신 질 수 있는지 명시적 한 문단.
- **§4 Direction 1 (OUR ≤ THEIR), 짧게** — 거울상(code-visibility) obstruction + 필요한 것.
- **§5 변형·방향별 정직 verdict 표** — 허용 어휘: "blocks natural maps" / "OPEN" /
  "reduces to the same open lemma". **금지: 불가능성 단정, "가능성 높음/낮음" 류 확률 단정**
  (rev1 교훈).
- **§6 본문 제안문** — positioning item·OP8 항목 업그레이드용 2–4문장 초안 (영문; 내가
  검증·통합).

## 4. 수치

이 노트는 구조 분석이다 — **수치를 만들어내지 마라**. 단, §3에서 수치 주장을 하게 되면
(예: 작은 n에서 (iii)의 분포 근접성) 게이트 2: 코드+JSON 동반, G-MEASURE 준수.

## 5. 게이트 (불변 + 강조 2개)

기존 게이트 전부 유효(`DIRECTIVE-KIMI-frontier-v2.md`). 특히:
- **본문(`paper/`) 편집 금지** + **`git restore`/`git checkout -- paper/`/`git stash` 절대
  금지** (frontier-v2 말미 추가규칙 — 실사고 있었다).
- **제출 시 네 meta 파일은 네가 직접 커밋**하라 (지난 라운드 3건이 미커밋 방치 → 내가 대신
  커밋했다. 반복 금지).

## 6. 범위 가드

OP9 재오픈 금지 · Track B(pencil) 보류 유지 · changelog 재작업 금지(승인 끝) ·
Codex 영역(impl/experiments의 P1b·polar-rate·KAT) 불가침.

No closure; no break; no security claim. OPEN = LSN.
