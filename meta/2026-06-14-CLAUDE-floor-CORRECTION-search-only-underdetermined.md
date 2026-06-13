# Claude 자기정정 — floor 결과 over-claim 교정: search-only + underdetermined, decisional 앵커 미확립

**Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** 직전 커밋 `0568686` / meta `...hardness-floor-LPN-le-worstcase-sympLPN.md`의 "첫 positive 앵커" 주장.
**검증:** `experiments/855-CLAUDE-sympLPN-search-underdetermined.py`.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**★내가 floor를 over-claim했다.** "LPN ≤ worst-case sympLPN = 첫 positive 앵커"는 두 caveat을 빠뜨렸다: (a) sympLPN single-instance **search는 정보이론적으로 underdetermined**(855: H(x|A,y)가 n=2,3,4서 엔트로피 67–73% 유지) → search-sympLPN은 "trivially/info-theoretically hard"라 search-floor가 약함; (b) crypto-relevant는 **decisional**인데 zero-padding이 **decisional floor를 안 줌**(LPN-uniform → (uniform-top, Bernoulli-bottom) ≠ sympLPN-uniform). **올바른 진술: search-only 환원(determined instance에 한정), decisional 앵커는 미확립.** 판정 레일이 내 자신의 over-claim을 잡음.

## 1. caveat (a) — search underdetermined (855)

sympLPN(def:symplpn)은 n비트 비밀에 **2n 샘플뿐**. LPN capacity 1−H₂(1/4)=0.19 bit/sample → n비트 복구엔 ~5.3n 샘플 필요, 2n은 한참 모자람. 직접 계산 H(x|A,y)(uniform Lagrangian 평균):

| n | H(x\|A,y) | H(x) | 유지율 |
|---|---|---|---|
| 2 | 1.46 | 2 | 73% |
| 3 | 2.07 | 3 | 69% |
| 4 | 2.67 | 4 | 67% |

⟹ **single-instance search는 x를 결정 못 함**(membership-LSN의 info-secure와 같은 성격). "search-sympLPN oracle이 x 복구"는 *determined instance에서만* 의미. 854의 floor는 **충분한 LPN 샘플(determined)을 심으므로 valid하나, 환원 대상이 "determined instance에 한정된 worst-case search-sympLPN"이라 narrow.**

## 2. caveat (b) — decisional floor 미확립 (reasoned)

crypto 가정은 **decisional**(distinguish (A, Ax+e) vs (A, uniform); paper line 211 "All hardness results stated for decisional"). zero-padding을 decisional로:
- real LPN z'=A'x+e' → z=(z'; e_bot)=real sympLPN(e'=e_top) ✓.
- **uniform LPN z'=uniform → z=(uniform; Bernoulli e_bot) ≠ sympLPN-uniform**(bottom이 Bernoulli지 uniform 아님) ✗ → decisional distinguisher가 구별.
bottom을 양쪽 다 uniform으로? real case가 깨짐(real sympLPN noise는 전 좌표 Bernoulli). bottom을 양쪽 다 Bernoulli? uniform case가 깨짐. **어느 쪽도 decisional 구조 보존 안 됨.** ⟹ **decisional-LPN ≤ decisional-sympLPN은 zero-padding으로 안 됨.**

## 3. 교정된 정직한 status

| 주장 | 교정 전 | 교정 후 |
|---|---|---|
| LPN ≤ worst-case sympLPN | "첫 positive 앵커" | **search-only, determined-instance 한정** (valid but narrow) |
| decisional 앵커 | (암시됨) | **미확립**(zero-padding 실패) — OPEN |
| graph-L ≡ [I;S]-LPN (853) | 유지 | 유지(구조 결과, 영향 없음) |
| floor↔worst-to-avg lock (850–854) | 유지 | 유지(obstruction 논증은 별개로 valid) |

**살아남는 것**: 구조 결과(graph-Lagrangian 재구성, worst-to-avg obstruction)는 멀쩡. **약해지는 것**: "positive 앵커"의 강도 — clean decisional hardness 앵커가 아니라 caveat 붙은 search 환원.

## 4. (d-지위) 재평가 + 다음

- **순 진전 정직 버전**: no-go(linear) + **(약한) search-floor**. 진짜 앵커(decisional)는 여전히 미확립. worst-to-avg도 막힘. → LSN은 아직 "survival-trusted"에 머물고, **clean hardness 앵커 없음**(정직).
- **남은 길**: (i) **decisional floor**를 다른 환원으로(zero-padding 아닌) — bottom을 uniform/Bernoulli 양립시키는 트릭? (ii) **multi-sample sympLPN**(2n 샘플 한계 우회) 가정에서 floor; (iii) [I;S]-LPN structured-hardness; (iv) 외부 stabilizer-LSN 다리(KLP+ decisional floor 상속).
- **교훈**: floor를 너무 빨리 "positive 앵커"로 발표함. search vs decisional + sample budget을 먼저 확인했어야. (docs-drift 가드는 def는 잡았으나 search/decisional 구분을 늦게 잡음.)

No closure; no break; no security claim. OPEN = LSN.
