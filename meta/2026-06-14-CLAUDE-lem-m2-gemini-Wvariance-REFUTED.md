# Claude 판정 — Gemini의 lem:m2 closure(W-variance gap) REFUTED (직접 검증, endorse 안 함)

**Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Gemini-3.1-Pro(agy)의 lem:m2 단일블록 OBSTRUCT 주장(W-law 분산 gap). **검증:** `experiments/857-CLAUDE-Wlaw-variance-gap-test.py`(n=2 exact, m=4,5,6).
**규율(Θ(n) 철회 직후):** Gemini를 endorse하지 않고 직접 계산으로 판정.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄
**Gemini의 "lem:m2 holds via min-syndrome-weight W의 분산 gap"(환원=covering-radius 좁은 spike var O(1) vs LPN=Binomial var Θ(m))은 REFUTED.** 직접계산: **var_red가 증가(0.53→0.82→1.19)하고 var_LPN보다 *크며*, ratio varLPN/varRed 감소(0.85→0.71→0.60)** — Gemini 예측의 정반대. 핵심 단계("marginal-uniform→Be uniform→random coset")가 틀림(Be는 ≤2n차원에 갇혀 *더 넓은* W-분포). **lem:m2 단일블록 OPEN 유지.** ★Θ(n)과 달리 endorse 전 직접 검증 → 제때 catch.

## 1. 데이터 (857, n=2 exact)
| m | mean_red | var_red | mean_LPN | var_LPN | P0_red(q_graph) | P0_LPN | SD(W) | varLPN/varRed |
|---|---|---|---|---|---|---|---|---|
| 4 | 0.557 | 0.534 | 0.816 | 0.456 | 0.577 | 0.331 | 0.250 | 0.85 |
| 5 | 0.761 | 0.824 | 1.127 | 0.583 | 0.518 | 0.203 | 0.323 | 0.71 |
| 6 | 0.972 | 1.193 | 1.449 | 0.712 | 0.487 | 0.124 | 0.370 | 0.60 |

## 2. 판정
- **Gemini 분산-gap = REFUTED**: var_red flat(O(1)) 아님 — 증가하고 LPN보다 큼. 환원 W-분포는 좁은 spike 아니라 더 넓음. "uniform random coset→covering radius" 추론 틀림(Be 갇힘 무시 — 내가 사전 의심한 지점).
- **W-law는 n=2서 구별(SD 0.25→0.37 증가)** — 단 P0_red(q_graph spike 0.49–0.58)가 지배하고 이는 **n에서 소멸**(q_graph→2^{−n}). mean/var 차이의 n-scaling은 미지. 기존 fixed-n distinguisher일 뿐, 새 점근 메커니즘 아님.
- **lem:m2 단일블록 OPEN 유지.** Gemini의 closure 접근(분산 gap) 사망.

## 3. 규율 메모
Θ(n) 철회 직후라 Gemini를 **endorse 전 직접 계산**(857). var_red 직접 측정이 Gemini 예측을 즉시 반증 — proxy/hand-wave 신뢰 금지 교훈 적용 성공. (Θ(n) 때는 proxy를 endorse→철회; 이번엔 catch.)

## 4. 다음
- Gemini의 W-variance 접근 사망 → lem:m2 점근은 여전히 미해결. mean/var의 n-scaling(n=3,4) or 다른 통계가 필요(미착수).
- lem:m2 정면 닫기는 진짜 hard(여러 라운드 open) — 무리한 closure 주장 금지.

No closure; no break; no security claim. OPEN = LSN.
