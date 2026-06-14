# Claude 탐구 — lem:m2 새 각도: 비-spike W-law 신호가 n에서 decay (directional EVIDENCE, OPEN)

**Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**모드:** "새 아이디어" 탐구. **검증:** `experiments/858-...nonspike-MC.py`(Monte-Carlo, NSAMP=8000). **규율:** 두 철회 후 — EVIDENCE/OPEN, over-claim 금지.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄
**새 각도**: 문헌이 집중한 소멸 q_graph spike(W=0) 말고 **비-spike W-성분(e∉Col(A) 조건부)의 점근 구별성** 측정(857 exact m≤6는 점근 못 닿음). **결과(Monte-Carlo n=2,3)**: 고정 n에선 구별(m 따라 gap·TV 증가)하나 **n=2→3에서 신호 ~4× decay** → 비-spike W-law도 점근적으로 vanishing 시사. **메커니즘**: n↑→p_eff→1/2→LPN이 균일화→환원의 갇힌-near-균일 노이즈와 구별난망. **함의(EVIDENCE, 약함)**: 단일블록이 점근 LPN-indistinguishable일 수 있음 → lem:m2 *거짓* 가능성(선형 환원 존재→LSN 6.5th 쪽). 단 n=2,3·한 statistic뿐, 결론 아님. lem:m2 OPEN.

## 1. 데이터 (858, MC)
**n=2 (p_eff=0.342), 비-spike W:**
| m | mean_red | mean_LPN | gap | TV est |
|---|---|---|---|---|
| 8 | 2.57 | 2.10 | 0.47 | 0.20 |
| 14 | 5.11 | 4.19 | 0.92 | 0.27 |
| 22 | 8.61 | 6.98 | 1.63 | 0.36 |
| 30 | 12.18 | 9.77 | 2.41 | 0.44 |

**n=3 (p_eff=0.411):**
| m | mean_red | mean_LPN | gap | TV est |
|---|---|---|---|---|
| 9 | 2.43 | 2.28 | 0.15 | 0.06 |
| 15 | 4.78 | 4.53 | 0.25 | 0.08 |
| 24 | 8.55 | 8.10 | 0.45 | 0.11 |

gap-rate(=gap/m): n=2 ~0.06–0.08, n=3 ~0.017–0.019 (≈4× 감소). TV도 동일 m서 n=3 << n=2.

## 2. 판정 (EVIDENCE, OPEN)
- **비-spike W-law는 고정 n서 구별**(mean_red>mean_LPN, gap·TV가 m 증가). 환원의 갇힌 노이즈는 LPN보다 W가 약간 큼.
- **★신호가 n에서 decay**(n=2→3 ~4×): p_eff→1/2(n↑)로 LPN이 균일화 → 환원의 near-균일 confined 노이즈와 합쳐짐. → **비-spike W-law도 점근 vanishing 시사.**
- **함의**: 단일블록 출력이 점근적으로 LPN과 구별 안 될 가능성 → **lem:m2(no-go)가 점근적으로 *성립 안 할* 수 있음 = 선형 marginal-adaptive 환원 존재 가능** → LSN이 code-adjacent(6.5th)로 기울 (약한) 증거. **단 결정적 아님**: n=2,3·MC·W-law 한 statistic; 환원 *구성*은 안 함. 다른 statistic이 비소멸일 수도.
- **lem:m2 OPEN** — 이 탐구는 닫지도 깨지도 않음. 방향만 시사(no-go가 보장 안 됨).

## 3. 규율
두 철회(Θ(n)·floor) 후라 이 directional 발견을 **EVIDENCE/OPEN로만** 기록. paper 본문 변경 없음(lem:m2는 이미 conditional/OPEN). 이 데이터는 "no-go가 성립한다"는 과신을 *경계*하는 용도 — 외부 LPQR26도 "linear barrier가 m=ω(n)서 error weight>1/2−δ만 보장, 완전 배제엔 불충분"이라 함(우리 데이터와 정합: 점근서 구별 약화).

## 4. 다음 (제안)
- 다른 single-block statistic(Fourier/character-sum, list-size)이 비소멸인지 — 미착수.
- 또는 **construct 시도**(lem:m2 거짓 방향): marginal-uniform B가 단일블록서 LPN을 점근 모방하는 구성. 성공하면 LSN→LPN 선형환원(major, but high-stakes).
- 큰 n(4,5) MC로 decay rate 정밀화(2^{-n}? 1/n?).

No closure; no break; no security claim. OPEN = LSN.
