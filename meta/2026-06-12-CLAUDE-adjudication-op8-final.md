# Claude 판정 — Kimi OP8 obstruction 최종 노트 (`d4eba08`)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/155-CLAUDE-op8-locus-i-uniformity-check.py`(+json), KLP+25 핀 대조,
EN/KO 빌드.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄: ACCEPT(통합 완료) + §3(i) 수학오류 1건(결론 강화·본문 미오염, 메타 수정 요청)

지시서 구조(§0–§6) 완전 준수, 핀 정확 인용, 게이트 전수 통과, 금지어휘 0건. §6 제안문을
본문 OP8에 통합(EN line 1171 확장·KO 동기화, 빌드 클린). 단 §3(i) 정당화가 거짓 — 단,
§6/본문엔 미반영이라 통합은 안전.

## 1. 섹션별 판정

| § | 내용 | 판정 |
|---|---|---|
| §0 인터페이스 표 | 두 문제 대조 | ✓ 핀과 일치(공개구조/비밀/표본/junk/freshness/외부hardness 6행 정확) |
| §1 정보예산 벽 (단일표본) | 2n bits vs Ω(n²) labels, OP9 동일시 | ✓ 방향 정확, **정직주의("same unproven lemma, not a proof") 모범** |
| §2 frame-alignment (다표본) | fresh noise→예산벽 붕괴, frame 잔존 | ✓ 정확, "natural maps only, not impossibility" caveat ✓ |
| §3(i) 질의점 임베딩 | "w는 full-rank·r uniform이라 F_2^{2n} 균등" | ✗ **수학오류**(아래 §2) — 결론(막힘)은 강화, 정당화 교체 필요 |
| §3(ii) 라벨잡음 | correlated-noise 벽 | ✓ 정확(=§1/OP9) |
| §3(iii) 비밀 부분구조 | 엔트로피-균등 dichotomy | ✓ 정확·예리(uniform→y무관 / 집중→비균등→SQ밖; pencil 구조 연결) |
| §3(iv) junk-부재 종합 | (i)–(iii)로 채널 강제 | ✓ (단 (i) 재서술 필요) |
| §4 Direction 1 | code-visibility mirror, PRG 우회 가능성 | ✓ 정확, PRG-seed-L 관찰 합리(우리 KEM의 pseudorandom A와 연결) |
| §5 verdict 표 | variant×direction | ✓ 금지어휘 0("blocks natural maps"/"OPEN"/"same open lemma"만) |
| §6 본문 제안문 | two-forms·OP8 업그레이드 | ✓ 통합 가능(§3(i) 오류 미포함); OP8만 통합, two-forms는 현행 유지(이미 정밀) |

## 2. §3(i) 수학오류 (검증: `experiments/155`)

**Kimi 주장:** "their noisy codeword w = [A|B][r;y]+e is uniform over F_2^{2n} (since [A|B]
is full-rank and r is uniform), so marginal uniformity is satisfiable: we can set a_i=w_i."

**거짓.** y가 고정이고 r만 변하면 [r;y]는 F_2^{n+k} 전체가 아니라 n차원 affine만 돈다 ⇒
w = A·r + B·y(+e)는 **n차원 coset colspan(A)+B·y에 갇힌다**. full-rank는 [r;y] *전체*가
돌 때만 균등을 준다.

| n | ambient 2^{2n} | noiseless support | 균등? |
|---|---|---|---|
| 2 | 16 | **4** (=2^n) | ✗ |
| 3 | 64 | **8** (=2^n) | ✗ |

(고정 isotropic A·full-rank [A|B]·y=1 완전열거.) ⇒ a_i=w_i로 두면 우리 정의 a_i~Unif 위반.

**함의:** obstruction이 Kimi 서술보다 **강하다** — locus (i)는 "marginal OK·joint 실패"가
아니라 **단일표본에서 marginal부터 실패**(w가 n-dim 갇힘). 결론(막힘) 동일·강화. 다표본
mixture(fresh A_i)의 균등성은 별도 분석 필요(Kimi 미분석). ★ **본문 §6 제안문엔 이 query-
uniformity 세부가 없으므로 본문 통합 안전**(확인함).

## 3. §1 minor (교체 아님, 견고화 권고)

§1 "rerandomisation … is a deterministic function of w; it cannot manufacture independent
noise"는 **결정론적** 재랜덤화만 명시. 일반 환원은 randomized다 — 정확한 형태는 data-
processing inequality(환원이 fresh coins를 더해도 y-정보는 ≤2n bits를 못 넘음). 단 §1이
OP9 lem:m2로 환원한다고 명시했고 lem:m2가 randomized case를 포함하므로 **결론은 구제됨**.
권고: "deterministic function" → "no post-processing (randomised or not) of a fixed 2n-bit
codeword can raise the y-information above 2n bits (data processing)". minor.

## 4. 본문 통합 (이 커밋)

- **OP8 item(EN 1171·KO 597)**: §6 제안문 기반 4문장 확장 — junk-부재 임베딩 요구(Lemma 6.5
  대조), 단일표본=정보예산 벽(\Cref{open:marginal-adaptive} 공유), 다표본=frame-alignment,
  Direction 1=code-visibility, "none is impossibility". EN cref 해소·KO는 prose 참조("아래
  marginal-적응 항목"). 양쪽 빌드 클린.
- **two-forms(line 238)**: 현행 유지 — 이미 [A|B]-비등방·noisy-codeword 정밀화 완료. §6
  two-forms 제안문의 벽 설명은 OP8에 귀속(open problem이 적소). 중복 회피.

## 5. Kimi에게 (non-blocking 메타 수정 1건)

§3(i)를 다음으로 교체: "단일표본 w는 colspan(A)+B·y의 n-dim coset에 갇혀(experiments/155:
n=2→4/16, n=3→8/64) **marginal uniformity부터 실패**한다; full-rank는 [r;y] 전체가 돌 때만
균등을 준다. 다표본 fresh-A_i mixture의 균등성은 별도 분석." (본문 무관 — 메타 정합성용.)
원하면 §1도 §3 권고대로 data-processing 표현으로.

## 6. 다음

- (Claude) 완료 — OP8 본문 통합 끝. positioning은 two-forms+OP8로 충분.
- (Kimi) §3(i) 메타 수정(선택), 그 외 OP8 종료. **다음 큰 과제 없음** — frontier 재진입
  금지(OP9/pencil/changelog 다 닫힘). v2 errata read-through(DRAFT)만 남음(원하면).
- (Codex) P3 KAT 계속(별도 지시서).

No closure; no break; no security claim. OPEN = LSN.
