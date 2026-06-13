# Claude 판정 — 병렬 라운드 6 (Tracks W/X/Y/Z)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi — W(fbcb43b)·X(ff4036c)·Z(028525b)·Y(TBD). CLI 직접 채널. 정직 의무 라운드.
**검증:** from-scratch(`experiments/540–543-CLAUDE-*`) + 증명 손 재유도.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**W ACCEPT(극한 정리·explicit rate·본문 후보)·X ACCEPT(lem:m2 음성결과)·Z ACCEPT(비선형
converse)·Y[TBD].** lem:m2 본체: **uniform-B-per-A 전략이 정리로 닫힘**(W), 한 상관-B family는
위협 방향 아님(X) — 그러나 일반 randomized B는 여전히 OPEN(진짜 핵심). 정직 의무 잘 지켜진 라운드.

## 1. Track W — ACCEPT (542): 극한 정리화

lim_{m→∞} SD(P_out, P_lpn)=1 (uniform-B-per-A, 고정 n), explicit rate. 내 442 메커니즘의 엄밀화.
- **W-a**(full-component): SD(P_full, P_lpn)≥1−ρ(n)^m, ρ(n)=1−(1/2ⁿ)(1−√((1−p_eff)/2)−√(p_eff/2)).
  **내 542: ρ을 두 방법으로 재계산**(Kimi closed form == 직접 per-row Hellinger affinity, n=2,3,4
  표값 0.99677 등 일치) + Hellinger tensorization sanity(small m: exact SD ≥ 1−ρ^m). ✓
- **W-b**(graph): Pr_lpn[y∈col(C)]≤2ⁿ(1−p_eff)^m → 0. 증명 건전(e∈col(C), max point mass).
- **W-c**(혼합): 1−SD ≤ (2−q)ρ^m+(1−q)2^{n−m}+2ⁿ(1−p_eff)^m. **내 542: 실제 1-SD(Track F/L,
  m=8..80)의 유효 upper bound 확인**(bound≥1-SD 전부). 증명의 test A=S∪E 논증 건전.
- **rate 정직**: ρ(2)=0.9968≈1이라 bound 느슨(큰 m에서만 →0); ρ(n)→1(p_eff→1/2)이 cross-n
  둔화 설명. δ(n)=(1/2ⁿ)(1/2−p_eff)>0(442 일치).
- **의미**: marginal-adaptive 모서리의 uniform-B-per-A 전략 = 정리로 닫힘. 본문 후보(lem:m2
  논의 sharpen: uniform-B 닫힘, 일반 B만 남음). 단 lem:m2 전체 아님(S3 정직).

## 2. Track X — ACCEPT (541): lem:m2 음성결과

λ-coupled 상관 B(λ로 전행 동일·1−λ로 iid; marginal-uniform 유지). **결과: SD가 λ로 단조 증가,
λ>0이면 baseline보다 큼** = 상관 B는 출력을 **덜 LPN처럼** 만듦(위협 방향 아님).
- **내 541 from-scratch**: λ=0 baseline == Track F/L matched(36575/524288 등)+LPN_{1/4}(3225/32768
  등) 정확 일치; λ=1 값·monotone(grid [0,1/4,..,1]) 일치; **rank-collapse obstruction**(λ=1은
  C rank≤1 → full-rank LPN과 singular) 확인.
- **명명 obstruction**: detectable signature = Be의 support 차원 붕괴(per-coordinate rate 아님,
  marginal-uniform이라 동일). 상관이 강하면 rank-collapse로 더 구분됨.
- **정직**: 한 family·n=2·small m. 일반 randomized B는 OPEN(X3). 위협 방향 음성결과.

## 3. Track Z — ACCEPT (540): 비선형 converse

n=2: f(0)=0인 Lagrangian-보존 permutation = 정확히 720개(전부 linear+symplectic=Sp(4,2)).
- **내 540 독립 backtracking**(Kimi 530 미사용): 720 확인·전부 linear·전부 symplectic·Sp(4,2)와
  동일. 엔진(Lagrangian=subspace → 합 닫힘 → isotropic 쌍에서 f(a+b)=f(a)+f(b) 강제) 확인.
- general n: polar space automorphism 정리 인용(PΓSp(2n,2)=Sp over F₂), THEOREM-with-citation
  (직접 미증명, 정직 라벨).
- **의미**: n=2에서 **모든**(비선형 포함) valid-output bijection = Sp rerandomization. 본문 OP7의
  "linear" qualifier 제거 가능(n=2).

## 4. Track Y — [TBD]

n=4 cross-n 셋째 점. [도착 시 작성. T의 GL(4) 버그 수정 or 무축소 m=8.]

## 5. 본문 반영

1. **OP7(Z)**: valid-output=Sp 문장의 "linear" qualifier 완화(n=2 비선형 converse·general n 인용).
2. **W**: lem:m2 논의에 uniform-B 극한 정리 추가 고려(meta or 본문 — uniform-B 닫힘 명시).
   단 신중 — uniform-B-per-A는 lem:m2의 한 전략이고 본문은 lem:m2 OPEN 유지. meta 기록 우선,
   본문은 한 문장(uniform-B 전략은 정리로 배제됨) 고려.

## 6. staging

S17(W 극한 정리·uniform-B)·S18(Z 비선형 converse, OP7 "linear" 완화). X=lem:m2 meta 음성결과.
누적 정리 다수. posture 불변(일반 randomized B=lem:m2 핵심 OPEN). batch 대기.

## 7. 다음

1. **일반 randomized B**(lem:m2 핵심): X의 한 family 넘어 — 다른 상관 구조, 또는 marginal-uniform
   B 전체에 대한 구조 정리. 진짜 관문.
2. **W 본문화**: uniform-B 극한 정리를 lem:m2 절에 정식 반영(전략별 배제 지도).
3. Y 후속(n=4 데이터) or T/Y NO-GO면 무축소 m 한계 명시.

No closure; no break; no security claim. OPEN = LSN.
