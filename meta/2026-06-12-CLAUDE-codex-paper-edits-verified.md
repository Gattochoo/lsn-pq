# Claude 점검 — Codex의 논문 직접 수정: 게이트 위반 확정, 단 cryptanalysis 내용 검증 ACCEPT

**Date:** 2026-06-12. Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 사용자 지적 확인 — Codex도 논문 직접 수정
- **6f52e28(codex):** paper PDF 재빌드 + 빌드검증 meta. tex 내용 무변경(PDF만). 경미.
- **b3ff6f0:** §Decoders 본문에 Codex P2 cryptanalysis 직접 추가(line 380·383). **게이트 위반**
  (에이전트 본문 무수정). + app:superseded 수학오류(별건, 4d2bf97로 제거됨).

## cryptanalysis 본문 내용 — 검증 ACCEPT (커밋 JSON과 정확 일치)
| 논문 | JSON(experiments/) | |
|---|---|---|
| ISD n=5 50k attempts → 3/10 | 132: 50000→successes 3 (0.3) | ✓ |
| span p=0 완벽 / p=1/4 실패 n=3,4,5 | 130: p=0 10/10, p=0.25 0/10 | ✓ |
| BKW noise growth p↦2p(1-p) | =0.375, bias (1-2p)²=0.25 | ✓ |
→ 정확·적절히 hedge("no scalable signal"·구체 n). v2 cryptanalysis 증거로 **소유**. "(see below)"
  모호참조만 제거.

## 종합
3개 에이전트 본문-편집 슬립 누적(Kimi app:superseded 오류·Codex cryptanalysis·PDF). 내용은 대부분
정확(검증 후 소유), 유일 오류는 제거. **하지만 수학오류가 본문 직접편집으로 게재 직전까지 갈
뻔한 게 핵심 위험** — meta DRAFT→내 검증 경로면 사전 차단됨. 분리 지시서(DIRECTIVE-KIMI/CODEX)에
"paper/ 커밋 제외" 명문화 완료. 다음부턴 위반 시 즉시 복원 후 재작업 요구.

No 7th; no break; no security claim. OPEN = LSN.
