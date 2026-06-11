# Claude v2 최종 점검 보고 (ePrint v2 출시 전)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**범위:** ① Codex 최신 작업 검수 ② v1(`b3afcd4`)→HEAD 본문 전체 diff(407줄) 정독
③ 일관성 grep·빌드·KO 동기화 ④ ePrint revision note 최종본.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. Codex 최신 작업 (`c0696b5`·`7717957`) — ACCEPT

- **polar-rate checker**: 직접 재현 — cli 테스트 2+2 passed, smoke 픽스처(N=128: K=8/12
  pass·K=16 fail = 양/음성 쌍) verified ✓. legacy 148 sweep의 파라미터 프로파일
  (`--k-end 768`) 기록 ✓. **rate 권고 변경 없음**(K=151@p′=0.0706·K=304@p′=0.0343는
  여전히 후보 — v3 재료, v2 본문 불변).
- **n9 ambient ML pilot**: 3-trial cost probe로 정직 신고("not paper-ready") ✓, p=0.5
  control 실패 ✓, cmp 재현 신고 ✓. 본문 무관.
- **ledger 노트**: 실험번호 **155 충돌** (`155-CLAUDE-op8-locus-i…`와
  `155-codex-polar-rate-check-smoke…`) — 파일명이 달라 무해. 이후 번호는 최신 파일 확인
  후 발급할 것(전 에이전트).

## 2. v2 본문 최종 정독 — 발견·수정 (이 커밋)

| # | 발견 | 심각도 | 조치 |
|---|---|---|---|
| 1 | **`lem:affine-coset-bias` 증명 소실** — v2 통합(`b3ff6f0`)이 원 MacWilliams 증명 블록을 삭제; appendix는 분산/w.h.p.만 다뤄 per-instance 한계·기대값 한계가 무증명 상태였고, lemma 문장이 존재하지 않는 "MacWilliams sum"을 참조 | **중대** | v1에서 증명 원문 복원(lemma 직후 `\begin{proof}`). ※내 당시 검증이 appendix 내용만 보고 원 증명 삭제를 놓침 — 감독 실수 기록 |
| 2 | `isotropic\-column` → PDF에서 "isotropiccolumn"으로 렌더(discretionary hyphen) — pdftotext로 확인 | 중 | `isotropic-column matrix~$A$`로 수정, 렌더 재확인(0건) |
| 3 | `lem:m1` 증명 "divided by 0.094n **is** 16n+O(1)" — 실제 15.96n이라 등식으론 Θ(n) 오차 | 소 | "is **at most** 16n+O(1)" (상계 방향만 필요, 성립) |
| 4 | `$n=6\!\!\sim\!\!8$` 비표준 범위 표기 | 미세 | `$n=6$--$8$` (en-dash) |
| 5 | moments 문단 인라인 합 44pt overfull(여백 침범) | 소 | display 수식으로 전환, overfull 0건 확인 |
| 6 | KO Decoders에 v2 실증 스크리닝 미동기(ISD 3/10@50k·BKW bucket·span p=0/p=¼·Rust ML 교차검증) | 중 | KO 281–285 영역에 압축 동기화 |

## 3. 검증 통과 항목 (수정 불요)

- 새 인용 10종(Sho94/FV19/NIS22/GGPR13/PHGR13/BCTV14/Gro16/BBB+18/komm/Sei15) bibitem 전수
  존재 ✓ · 미정의 참조/인용 0 ✓ · `mathtools`(psmallmatrix) 로드 ✓ · `prop:chi2-sample`
  label 존재 ✓.
- SNARK 카운트 41²=1,681·n=41 일관 ✓. j-분포 "모든 0≤j≤n 발생" ✓(이전의 잘못된 even-
  codimension 주장 제거 확인). 꼬리 주장 k=14: 2^{-105}<2^{-100} ✓. CLOSED→DEAD 용어 전
  영역 일관(잔존 0) ✓.
- 수치 전수 JSON 대조(이전 라운드 포함): N=2048 2000회×2·1.5×10⁻³(127) ✓ · ISD 3/10@50k
  (132) ✓ · span(130) ✓ · ML 0.25/0.90/1.00(129) ✓ · 컨트롤 0.965–1.000(126) ✓.
- 복원 증명의 일관성: 2^{-n}(1+(9/8)ⁿ) = 2^{-n}+(9/16)ⁿ ✓ (p=1/4, 1−2p=1/2).
- changelog rev2 대비 본문 diff 잔여(編集성): 저자 소속·AI 고지 후면 이동·Shor 인용·Ω의
  J-형 명시·SNARK 프레임워크 인용·lem:m1 단순화 — 전부 editorial, 보안 주장 무변.
  **실질 추가 1건 = KLP+25 positioning 정밀화**(아래 revision note 5항으로 반영).

## 4. ePrint v2 revision note (최종 승인본 — 이걸 사용)

> **Revision v2 (2026-06-12):** Strengthened security evidence and sharpened the
> open-problem landscape in five areas: (i) the affine-coset bias bound is upgraded from
> expectation to w.h.p. with a full closed-form proof in a new appendix; (ii) the $N=2048$
> polar decoder is empirically validated (2000 trials per design noise point, zero errors,
> one-sided 95\% BLER bound $1.5\times10^{-3}$, with high-noise negative controls);
> (iii) systematic cryptanalysis screens (ISD, BKW, span-of-positives, Rust ML cross-check)
> are reported, all consistent with the brute-force scale; (iv) Open Problem 9 is sharpened
> to the conditional mutual information $I(x;y|C)$, with an explicit note that earlier
> Fisher/TV approaches bounded $I(x;y)$ and therefore could not upper-bound the working
> quantity; (v) the positioning against the stabilizer-decoding LSN of Khesin et al.\ is
> made precise (their Theorem~6.6 attaches LPN-hardness to the single-sample Search
> variant; the bridge open problem now records the information-budget and frame-alignment
> obstructions and the junk-register asymmetry). No security claim is changed; all
> additions are evidence-based or structural.

## 5. 출시 체크리스트

| 항목 | 상태 |
|---|---|
| EN 빌드 (tectonic) | ✓ clean, 37pp, overfull 0 |
| KO 빌드 | ✓ clean, 18pp |
| 미정의 참조/인용 | ✓ 0 |
| 수치-JSON 대조 | ✓ 전수 |
| 증명 무결성(소실 복원 포함) | ✓ |
| KO 동기화(v2 영역) | ✓ |
| revision note | ✓ §4 최종본 |
| **ePrint v2 제출** | **사용자 액션** — lsn-paper.pdf + §4 note |

No closure; no break; no security claim. OPEN = LSN.
