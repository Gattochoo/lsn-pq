# ePrint revision 대기 큐 (staging) — 세션 불변

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** 표준 운영 문서.
**결정(사용자 승인):** 제출본(xxxx/110027, Zenodo v2.1)에 대해 **단건마다 revision하지 않고
실질 사건이 모이면 batch**해서 한 번에 ePrint revision. 새 세션은 이 문서로 "지금 revision?"을 판단.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. 현재 제출 상태
- 제출본: IACR ePrint **xxxx/110027** (lsn-core.pdf, 31pp 당시). Zenodo **v2.1**(record 10.5281/zenodo.20665389, concept 10.5281/zenodo.20646796).
- 그 이후 `paper/lsn-core.tex`(canonical 소스)가 앞서 있음 = 아래 staged 델타.

## 2. Staged 델타 (다음 revision에 포함될 것)
| # | 결과 | 커밋 | 논문 영향 | 검증 |
|---|---|---|---|---|
| S1 | **결정론 marginal-adaptive 하한**(thm:deterministic-marginal-adaptive): SD≥1−\|Lagr\|/2^{mn} | `4a3c661` | abstract "3 of 4" → "3.5 of 4"(결정론 절반 추가 폐쇄); barrier 표/status map/open problem 분리 | 186 독립검증(`bfdfd8b`) ✓; 빌드 32pp 클린 |

(새 결과 통합 시 이 표에 한 줄씩 추가할 것.)

## 3. ★ revision을 *지금* 트리거하는 조건 (이 중 하나라도면 batch revision 권고)
1. **lem:m2 진전**: 무조건 증명(→ abstract "all four cells") **또는** 의미있는 부분결과.
2. **L2 닫힘**(Codex): 상수시간 참조구현 + N=2048 + KAT → "Honest Limitations" L2 제거.
3. **새 정리** 2건 이상 누적(예: 일반-j moment 닫힘, OP7 결판) → S-표가 충분히 두꺼워짐.
4. 사용자 명시 요청.
**단독 S1만으로는 트리거 안 함**(incremental, 권고대로 대기).

## 4. revision 실행 시 (체크리스트 — 트리거 충족 후)
1. lsn-core.tex 최종 빌드, 수치·참조·bib 전수(이전 감사 루틴).
2. revision note 작성 = S-표의 모든 항목 요약(아래 누적 초안 사용).
3. PDF + note → 사용자 ePrint revision 제출(계정 권한상 사용자 액션).
4. 새 GitHub release v-next + Zenodo 새 버전(concept DOI 자동 최신); README snapshot DOI 갱신.
5. companion(lsn-paper.tex)·KO(로컬)도 동기화 확인.

## 5. 누적 revision note 초안 (S-표 반영, 계속 갱신)
> **Revision (예정):** Sharpened the linear-reduction barrier landscape: the deterministic
> half of the marginal-adaptive cell is now closed unconditionally by a support-counting
> bound (SD((C,y),LPN) >= 1 - |Lagr(2n)|/2^{mn}), leaving only the randomized marginal-adaptive
> case open; abstract, barrier table, and Open Problem 9 updated accordingly. [+ 이후 항목 추가]

## 6. 비고
- lsn-core 소스 ≠ 제출 PDF는 **의도된 상태**(staging). 혼동 금지 — 제출본은 v2.1 PDF, 소스는 앞섬.
- 본문 편집은 Claude 전용(에이전트 직접편집 금지) 그대로.

No closure; no break; no security claim. OPEN = LSN.
