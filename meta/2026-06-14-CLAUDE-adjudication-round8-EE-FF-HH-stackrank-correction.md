# Claude 판정 — 라운드 8 (EE/FF/HH) + stacked-rank 정정 (2n→n)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 3트랙(EE 78b81fc·FF ee9d65f·HH 34d6321) + 2nd-Claude-session의 stacked-rank catch.
**검증:** from-scratch(`experiments/740-CLAUDE-stacked-rank-tightening.py` v2). 빌드: **tectonic 로컬**(CI 26일까지 정지), EXIT=0, 336 KB, citation 0 미해소.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**★라운드 8은 라운드 7의 "shared-B 닫힘=돌파"를 정직하게 디플레이트한다.** EE: lem:m2는 **단일-블록**(shared-C)이고 stacked-rank는 **다중샘플(k≥2) 통계**라 단일-블록에선 trivial → stacked-rank가 닫는 건 lem:m2가 **아닌** 다중샘플 shared-C 변형. 게다가 그 bound 자체도 정정: **Gemini의 2n은 2배 느슨, 샤프 bound는 rank(HY)≤rank(HB)≤n** (740). FF·HH: fresh-C/fresh-B residual은 모든 distinguisher rate→0로 **여전히 OPEN**(닫힘도 깨짐도 아님). 진짜 residual = fresh 단일-블록의 점근 distinguishability.

## 1. ★ stacked-rank 정정 (740 v2) — 2n→n, 2nd-session catch를 정밀형으로 확증

2nd Claude session이 "Gemini의 rank(HY)≤2n은 느슨; Col(C)=Col(BA)⊆Col(B)라 H가 Col(C)(dim n)를 죽이면 rank(HB)=rank(B)−n"이라 catch. **740 v1이 바로 그 `rank(B)−n`을 테스트했고 FAIL** — 저랭크 B에서 rank(HY)가 rank(B)−n 초과. 실패가 곧 발견: 전제 `rank(C)=n`이 거짓(rank(BA)<n 가능).

**샤프 항등식**(740 v2, n=2 전 케이스 정확):
```
Col(C)=Col(BA)⊆Col(B),  ker H=Col(C)
rank(HB) = rank(B) − rank(BA)        [Col(C)⊆Col(B)라 교집합=Col(C)]
         = n − corank(B) + dim(Col(A)∩ker B)
rank(HY) ≤ rank(HB) ≤ n              ← 보편 bound (Gemini 2n은 2배 느슨)
```
- **full-rank B**: rank(BA)=n → rank(HB)=n **정확**(degenerate 안 됨). 60/60.
- **rank(B)≤n 극단**: HB=0 가능(73/200) → 그때 Col(B)=Col(C) → y∈Col(C) **항상** → W=0 spike(prob 1로 잡힘). **탈출 불가**.
- uniform B는 full-rank w.h.p.(88%) → rank(HB)=n이 전형.
- 2nd-session의 `rank(B)−n`은 **full-rank 특수형**(거기선 =n으로 정확); 일반형은 `rank(B)−rank(BA)`.

**효과**: 분리 임계 2n→n으로 강화 → LPN rank min(m−n,k)>n은 **m≥2n, k>n**이면 충족(Gemini의 m≥4n,k>2n보다 빠름). distinguisher가 **더 강함**.

## 2. ★ Track EE (decisive) — lem:m2 = 단일-블록 shared-C; stacked-rank의 범위 한정

paper verbatim(def:symplpn 227–231, §9 883–884, lem:m2 1166–1177, open:marginal-adaptive 1232–1238) 직접 확인 → EE 인용 정확.
- **THEOREM(정의적)**: lem:m2는 단일 블록 (C,y), 하나의 2n-bit e. 환원 출력=단일 블록.
- **NO-GO**: 단일 블록에서 Y는 **1열** → rank(HY)∈{0,1} trivial. **stacked-rank는 lem:m2를 닫지 못함**.
- 단일-블록 신호 = Be의 **저차원 support**(SD→1 at fixed n; n점근 rate OPEN).
- 다중샘플 shared-C(k≥2, 같은 C 재사용)만 stacked-rank로 닫힘 — 이건 lem:m2가 아닌 **별도(다소 인위적) 모델**.
- **본문 반영**: open:marginal-adaptive의 stacked-rank 문단을 (a) 2n→n 샤프화 + 항등식 + degenerate→W-spike, (b) "k≥2 다중샘플 통계; k=1 단일-블록은 trivial하여 lem:m2는 저차원-support 신호로 남고 점근 OPEN"으로 정정. 빌드 ✓.

## 3. Track FF (710) — fresh-C shared-x 교차블록 **누설 없음** (OPEN)

k 블록 (C⁽ⁱ⁾, y⁽ⁱ⁾), **공유 x**, fresh (A⁽ⁱ⁾,B⁽ⁱ⁾,e⁽ⁱ⁾). 정확 열거(n=2).
- per-block SD: fixed-n에서 m 따라 증가(0.07→0.37) — fixed-n 구별성(이미 알던 것).
- **교차블록 MI**: fresh-C가 matched-LPN과 **사실상 같은 rate로 집중**(I(x;blocks) fresh 0.189 vs LPN 0.212 @(2,2); 0.303 vs 0.310 @(3,2)). 공유-x 자세 posterior가 LPN과 동률.
- fresh-C 고유 신호 = q-graph spike → **2^{−n}** (n=2서 1/4로 위에서 수렴); m=poly(n)서 advantage가 **n에서 지수적으로 소멸**.
- **판정 ACCEPT(NO-GO/OPEN)**: 공유-x를 써도 fresh-C는 비소멸 누설 없음. q_graph(n)→2^{−n} backbone(640서 독립 확인)과 구조적으로 일치. residual 안 닫힘.

## 4. Track HH (730/731) — permutation-of-uniform(첫 below-baseline) + residual no-go map

- **HH1 신규 family**: B = F_2^4의 **서로 다른** m-벡터 순서쌍(injection). 각 행 marginal-uniform(lem:m1 충족)이나 행 반복 금지. 정확 SD n=2, m=2..6. m=4 brute-force = count-vector SD **일치** 확인(내부 건전성).
  - **m=2,3,4서 uniform-B baseline 아래로**(ΔSD −0.0008/−0.025/−0.016) = **첫 reducing 방향(ESCALATE)**.
  - 그러나 **m=5,6서 baseline 위로 교차**(+0.016/+0.055) → 점근 reducing rate 없음 → **NO-GO**.
- **판정 ACCEPT(ESCALATE→NO-GO, OPEN)**: ESCALATE가 진짜 break인지 = **구조적으로 불가** 확인. 740의 **B-무관** 항등식(rank(HB)≤n)과 W=0 spike, q_graph→0는 permutation-of-uniform에도 그대로 적용(Be는 ≤2n차원, syndrome ≤n차원, q_graph→0). small-m below-baseline은 fixed-n 요동. **점근 환원 아님**.
- **HH2 residual map**(731): shared-B CLOSED(정정: rate non-vanishing via rank n) · W·k-rank·structured-SD 다 →0 · I(x;y|C) OPEN(≈0.04–0.05 bit/sample, o(n) 정합) · perm-of-uniform ESCALATE/NO-GO · **전체 fresh residual OPEN**. **DRAFT** — 본문 통합 전 m=5,6 교차 독립확인 필요(NO-GO의 hinge).

## 5. 본문 반영 + staging

open:marginal-adaptive stacked-rank 문단 정정(§2 본문 반영). 빌드 tectonic EXIT=0 336 KB. FF·HH는 residual map DRAFT라 **본문 미통합**(라운드 7 fresh-residual 문장과 이미 정합). 커밋: paper/lsn-core.tex(+pdf), experiments/740, 본 meta만 명시적 staging. polar_validation·.agents·641(실행중)은 **내 트랙 아님 → 제외**.

## 6. 메타 — 정직성 회계

라운드 7이 "shared-B 닫힘"을 돌파로 본 것을 EE가 교정: **닫힌 건 다중샘플 shared-C(인위적)이고 lem:m2(단일-블록)는 untouched.** over-claim을 finding으로 기록. 동시에 2nd-session·Gemini 둘 다 catch당함(2n 느슨·rank(B)−n은 특수형). **3+1 에이전트(Gemini 구조·Kimi 계산·2nd-session catch·Claude 정밀판정) 수렴 — 그러나 수렴점은 "닫힘"이 아니라 "정확히 무엇이 닫혔고 무엇이 OPEN인가"의 정밀화.** 진짜 residual = fresh 단일-블록 점근 distinguishability(= I(x;y|C)=o(n) 미증명).

## 7. 다음

- 641(BB column-pair SD, 실행중 PID 74876) 완료 시 incremental 판정(I↓≠SD↓ 예상, lem:m2 지지).
- GG(720, I(x;y|C) 점근) 미착수 — 라운드 8 우선순위 EE>FF>GG>HH 중 GG 남음.
- residual map 본문화 전 perm-of-uniform 교차 독립확인.

No closure; no break; no security claim. OPEN = LSN.
