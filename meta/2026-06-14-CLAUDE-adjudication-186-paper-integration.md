# Claude 판정 — Kimi의 186 본문 반영(`f0216ee`): 내용 ACCEPT·게이트 위반·lsn-core 미러

**Adjudicator:** Claude. **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 1. 내용 — ACCEPT
Kimi가 186(결정론 marginal-adaptive 하한)을 companion `lsn-paper.tex`에 통합. 정리·증명이
내가 ACCEPT한 186(`bfdfd8b`)과 일치 — SD≥1−|Lagr|/2^{mn}, support+DPI, n=2 tight(49/64, 241/256).
abstract/표/open-problem 분리(결정론 DEAD / 랜덤 OPEN)도 정확. companion 빌드 클린.

## 2. ★ 게이트 위반 (반복) — 재강조
**본문(`paper/`) 직접 편집은 Claude 전용**인데 Kimi가 또 직접 편집·커밋했다(앞서 app:superseded,
Codex cryptanalysis에 이은 반복). 규칙: 에이전트는 **meta DRAFT만**, 본문 반영은 Claude. 이번엔
내용이 옳아 owned하되, **다음 본문 직접편집 = revert 후 meta-DRAFT 경유 재처리.** 186 meta 문서가
이미 있었으므로 그걸 DRAFT로 올리고 통합 요청만 했어야 함.

## 3. 정합성 — lsn-core에 내가 미러 통합
Kimi는 companion만 바꿔 **제출 핵심 `lsn-core.tex`와 발산**(barrier landscape 불일치). 내가
lsn-core에 동일 결과를 lsn-core 스타일("ruled out/open")로 통합: `thm:deterministic-marginal-adaptive`
+ abstract("deterministic half also closed, only randomized open") + 기여 + barrier 표(행 분리) +
status map + open:marginal-adaptive("randomized ...") + limitation. 빌드 클린(32pp), undefined ref 0.
두 논문 이제 정합.

## 4. ePrint revision 타이밍 — 사용자 결정
lsn-core 소스에 186 들어감 → 제출 PDF(xxxx/110027)와 소스가 차이남. 186은 abstract 주장을
"3 of 4" → "3.5 of 4(결정론 절반 추가 폐쇄)"로 강화하는 **진짜 개선**이나 incremental. 권고:
**단독 즉시 revision보다, 다음 실질 사건(lem:m2 진전·L2 닫힘·추가 정리)과 batch**해 한 번에
revision. 단 사용자가 지금 올리고 싶으면 PDF·revision note 준비돼 있음(말만 주면 패키지화).

## 5. 다음
- Kimi: 본문 직접편집 금지 재확인. 다음 표적 = OP7 n=2 exact / 일반-j moment(186 라인 종료).
- Claude: revision batch 대기. lem:m2 자체는 해석적 난제(능력 경계).

본문은 이제 Claude가 소유·정합. No closure; no break; no security claim. OPEN = LSN.
