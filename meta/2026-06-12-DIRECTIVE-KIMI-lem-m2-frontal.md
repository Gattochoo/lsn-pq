# Kimi 지시서 — lem:m2 정면 공략 (선형 지형 마지막 칸 + black-box 분리 첫 벽돌)

**Date:** 2026-06-12. **Author:** Claude (adjudicator). **For:** Kimi.
**대체:** OP1 Track A를 **lem:m2로 수렴**(OP1 Step 4 multi-row가 같은 수학이라 흡수). OP7(Track B)·게이트·추가규칙 전부 유지.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 전략 (사용자 결정: 과감하게 ①, 단 ②로 가는 1)

사용자가 lem:m2 정면 공략을 택했다. 프레이밍 **이중**:
- (즉시 가치) lem:m2 증명 = marginal-adaptive 칸이 **무조건 사망** → 논문의 conditional
  barrier가 unconditional 정리로 격상. "모든 선형 환원 사망"을 우리 이름으로.
- (장기 상금) lem:m2의 핵심 — "고정 $\le 2n$차원 잡음이 i.i.d. Bernoulli를 위조 못 한다" —
  는 **black-box separation의 핵심 보조정리**와 같은 구조. ①을 통과하면 ②의 출발선에 선다.

**OP1 Step 4(multi-row bundle)와 합류:** 번들의 correlated-noise $e'_i=\langle b_i,e\rangle$가
바로 lem:m2의 "고정 $2n$-bit 잡음 $e$의 선형상"이다. 새 트랙 아님 — OP1 흐름을 여기로 수렴.

## 1. 핀: 증명/반증할 정확한 명제 (본문 `lem:m2`, 자구 그대로)

> $p'\in(0,1/2)$, $1-2p'\ge1/\operatorname{poly}(n)$. $m$개 표본 $(c_i,a_i)$, $a_i=\langle c_i,x\rangle+e'_i$,
> $e'_i$의 bias $\le 2^{-0.19n}$ (단 $\ell=o(m)$ 행 제외). 그러면 $m\ge\frac{4n}{(1-2p')^2}\operatorname{polylog}(n)$
> 일 때 $\operatorname{SD}((C,y),\mathrm{LPN}_{p'})\ge 1-o(1)$.

**핵심 구조(본문이 명시한 장애):** $e'=Be$는 고정 $2n$-bit $e$의 $m$개 선형상 → 차원 $\le 2n$
부분공간 거주, $m=\omega(n)$에서 강상관. 두 표준 우회가 막힌 지점:
- (i) 복원-환원: cor:recovery-barrier가 correlated noise에 견고해야 하나 $\le 2n$ 누출행이
  $x$ 과결정 가능(솔버는 $B$ 모름).
- (ii) 잡음-엔트로피: $H(Be)\le H(e)=O(n)$은 고정 $B$엔 성립하나 고엔트로피 $B$엔 실패($Be$
  거의 균등 가능).

## 2. 작업 (단계별, 각 DRAFT+코드+JSON, 내 판정 후 진행)

### Step A — 핵심 질문의 결정적 정식화 + 작은 n 실측
"고정 $e\in\F_2^{2n}$, 적응 $B\in\F_2^{m\times2n}$에 대해, $Be$의 분포가 i.i.d. $\mathrm{Bernoulli}(p')^m$와
얼마나 가까운가"를 $\operatorname{SD}$로 핀. $n=2,3(,4)$, 작은 $m$ 완전열거/표집으로:
- 고정 $e$(여러 weight)에서 $Be$ 분포 측정, i.i.d. 기준 대비 $\operatorname{SD}$.
- $B$의 가시성 두 모형 분리 측정: **공개 $B$**(솔버가 $C=BA$의 생성 $B$ 봄) vs **비밀 $B$**.
- ★ **결정적 비대칭 가설:** $\le2n$차원 구속이 **검출 가능한 통계적 흔적**(예: $C=BA$ 위
  $e'$의 저차원 support)을 남기는가? 남기면 distinguisher 존재 → lem:m2 **참** 쪽. 안 남기면
  위조 가능 → lem:m2 **거짓** 쪽.

### Step B — 두 우회 벽을 정면으로
- (i)에 대해: $\le2n$ 누출행이 $x$를 과결정하면 그게 **솔버에게 distinguisher를 준다**(LPN은
  과결정 안 됨) — 이걸 정리로? 단 "솔버가 $B$를 모른다"를 정직 처리(비밀-$B$ 모형).
- (ii)에 대해: 고엔트로피 $B$에서 $Be$가 균등에 가까워도, $Be$는 여전히 $e$의 **선형함수**라
  $C=BA$와 **결합분포**에 상관이 남는다. $H(Be|C)$ 또는 $I(e';C)$가 진짜 양인지 — 이게
  핵심. (OP9의 $I(x;y|C)$와 같은 구조 — 그 정밀화를 재사용.)

### Step C — 닫힌형 시도 or 반례
- 참 경로: $\operatorname{SD}((C,y),\mathrm{LPN}_{p'})\ge1-o(1)$의 닫힌형/점근 논증.
- 거짓 경로: $Be$가 $C$에서 i.i.d.를 탐지 불가능하게 위조하는 **구체적 적응 $B$** 구성(작은 n
  실증 동반). **이 결과도 똑같이 중요**(LSN 선형경로 열림을 정직히 보고).

### Step D — 격상 or obstruction
- 증명 → 내가 본문 `lem:m2`/`thm:marginal-adaptive`를 conditional→unconditional 격상.
- 반례 → 본문에 "marginal-adaptive 선형 환원 존재" 정직 보고(보안 함의 명시).
- 부분 → OP9/lem:m2 잔여를 한 외부명제로 더 좁힘 + black-box 분리용 보조정리 초안.

## 3. 정직 주의 (메모리·세션 교훈 강제)

- **양날 인식:** lem:m2 참=marginal칸 사망(좋음)·거짓=선형환원 존재(LSN에 나쁨, 그러나 알아야
  할 사실). **어느 쪽도 회피 말 것** — 데이터를 따른다. "참이길 바람"으로 측정 왜곡 금지.
- **공개-$B$ vs 비밀-$B$ 분리 필수**(G-MEASURE 연장): distinguisher가 보는 게 $C=BA$뿐인지
  생성 $B$까지인지로 결론이 갈린다. 매 측정에 위협모형 핀.
- **작은 n 단정 금지**: 닫힌형 또는 극단 $m,n$. (Krawtchouk 라운드2 교훈.)
- **표=JSON·보고수치=유도/스크립트.** (pencil·감사 교훈.)
- **"공허 SDA ≠ SQ-쉬움"** 류 reference 함정 재인지(OP1 교훈).
- black-box 분리는 **언급만**, 본문 진입 금지(연구 초기). lem:m2가 우선.

## 4. 범위

- OP1 단일행/batch는 settled(`165`/`163` 닫힌형) — 재방문 금지. multi-row는 여기 lem:m2로 흡수.
- OP9 봉인 유지(단 $I(x;y|C)$ 기계는 Step B(ii)에 **재사용**). pencil 보류. LWE/저잡음 금지.
- Codex 영역 불가침. 본문 무수정·`git restore paper/` 금지. 제출=직접 커밋.

## 우선순위 한 줄

**Step A(결정적 정식화 + $Be$ vs i.i.d. 의 $\operatorname{SD}$ 실측, 공개/비밀-$B$ 분리) 먼저.**
참이든 거짓이든 보고. 이건 "우리가 직접 여는 정리"이자 black-box 분리의 첫 벽돌이다.

No closure; no break; no security claim. OPEN = LSN.
