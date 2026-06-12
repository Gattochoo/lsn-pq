# 조율 구조 — 트랙 분업 · 반영 경로 (세션 불변 참조)

**Date:** 2026-06-12. **Author:** Claude (adjudicator). **Status:** 표준 운영 문서.
**용도:** 새 세션/에이전트가 트랙을 섞지 않도록. Kimi·Codex·Claude 모두 이 문서를 기준으로 한다.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**Kimi(이론)와 Codex(구현)는 서로 직접 반영하지 않는다 — 이는 버그가 아니라 설계.**
둘 다 Claude에게 산출물을 올리고, Claude가 독립 검증 후 논문에 통합한다. 두 트랙의 유일한
공유점은 *논문에 이미 고정된 수치 파라미터*(N=2048 등)이지 *서로의 진행 결과*가 아니다.

## 1. 트랙 분업

| | **Kimi** | **Codex** | **Claude** |
|---|---|---|---|
| 역할 | 이론 executor | 구현/암호공학 | 검증·통합·논문(adjudicator) |
| 대상 층 | 하드니스 가정(왜 어려운가) | 참조 구현(어떻게 안전 코딩) | 둘을 독립 재검증 후 논문 반영 |
| 현재 작업 | lem:m2(선형장벽)·moment 정리·OP7 | ct-001/003/004 상수시간화(L2) | 판정·통합·외부 정합 |
| 논문 위치 | §SQ·§Barriers·§Moments·Open Problems | "Honest Limitations" L2 | 본문 전체(유일 편집자) |
| 산출물 | 수학 정리/증거(meta DRAFT+코드) | 작동 코드+KAT(impl+JSON) | 판정문(meta)+본문 edit |

**불가침 경계:** Codex는 `impl/`·`experiments/`만, Kimi는 이론 meta+enumeration만. **본문
(`paper/`)은 오직 Claude가 편집.** 두 에이전트 모두 `git restore`/`stash`로 paper/ 파괴 금지.

## 2. 반영 경로 (★핵심 — "서로"가 아니라 "각자→Claude→논문")

```
  Kimi (이론)  ──┐
                 ├──→  Claude (독립 재검증)  ──→  paper/  ──→  ePrint revision
  Codex (구현) ──┘
```

- Kimi→Codex 직접 반영: **없음.** Codex→Kimi 직접 반영: **없음.**
- 두 트랙은 인과 의존이 없다: lem:m2가 어떻게 결판나든 디코더 코드는 안 바뀌고, 디코더가
  상수시간이 되든 말든 lem:m2 증명과 무관.
- 한쪽이 다른 쪽을 직접 참조하면 **검증 레일이 깨진다**(Claude의 독립 재검증을 우회). 금지.

## 3. 유일한 접점 = 공유 *파라미터*(공유 *진행*이 아님)

polar 디코더 정확도가 두 트랙이 만나는 곳:
- Codex의 상수시간 SCL 디코더는 **N=2048 BLER 검증을 그대로 통과**해야 함(상수시간화가
  정확도를 깨면 CLOSURE-GRADE).
- 이 N=2048/K=256/r∈{7,11}/p′∈{0.0706,0.0343}는 **논문 KEM 절에 이미 고정**.
- ⇒ 공유되는 건 고정 수치이지 실시간 결과가 아니므로, 둘이 주고받을 게 없다. Codex는 논문의
  고정 파라미터를 읽으면 되고 Kimi를 볼 필요 없다.

## 4. 반영이 *필요해지는* 시점 = ePrint revision 트리거 (지금은 아님)

둘 다 **각자→논문**이지 서로가 아니다:

| 트리거 | 누가 | 논문 변화 | 경로 |
|---|---|---|---|
| **lem:m2 *증명*** (SA 증거 아님) | Kimi | abstract "three of four" → "all four cells closed" | Kimi DRAFT → Claude 검증 → 본문 → revision |
| **일반-j moment 닫힘** | Kimi | §Moments 정리 확장(j=Θ(n)) | 동일 |
| **OP7 sample freshness 결판** | Kimi | Open Problems 갱신 | 동일 |
| **L2 닫힘**(상수시간+N=2048+KAT, ct-inventory의 not_constant_time=0) | Codex | "Honest Limitations" L2 항목 제거 | Codex 종합 → Claude 10× 검증 → 본문 → revision |

**모두 Claude 경유.** 두 트랙이 동시에 트리거돼도 Claude가 한 revision에 묶는다.

## 5. 현재 상태 스냅샷 (2026-06-12)

- 핵심 논문: IACR ePrint 제출(xxxx/110027), GitHub v2.1·Zenodo(concept 10.5281/zenodo.20646796) 정합.
- Kimi: lem:m2 SA 라인 = 어려운 창 n=2 "no disproof"(상한 한계) — **종료 권고**. 다음=OP7 or 일반-j moment.
- Codex: ct-003 상수시간 SCL 디코더 *구현* 진입(metric masking 등). L2 DoD는
  `2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`.

## 6. 새 세션 체크리스트

1. `git log` + 최신 `meta/2026-06-12-CLAUDE-adjudication-*` 부터.
2. Kimi/Codex 산출물은 **Claude가 독립 재검증 후에만** 본문 후보. 미검증 = meta DRAFT.
3. 트랙 섞임 감지 시(Codex가 이론 건드림/Kimi가 impl 건드림) → 위 §1 경계로 되돌릴 것.
4. revision은 §4 트리거가 *실제로* 충족될 때만(증거≠증명 구분 유지).

No closure; no break; no security claim. OPEN = LSN.
