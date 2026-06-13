# Claude 판정 — 라운드 9 종합 (II/JJ/KK/LL) + ★★ I=Θ(n) 철회 (proxy 버그, 직접계산이 o(n) 지지)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi 라운드9 4트랙(II db552a0·JJ 3de78a5·KK ...·LL 28a33c6) + 내 848/849 Θ(n) 주장.
**검증:** 646(n=2 exact, Kimi 독립 cross-check)·LL 공식(646 재현)·subadditivity 논증·856-style 직접 확인.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**★★내 "I(x;y|C)=Θ(n)"(이번 세션 최대 발견이라 보고)는 틀렸다 — 철회.** 848/849의 per-form-bias **proxy**가 엔트로피 **subadditivity를 위반**(각 방향 marginal bias~0.5면 I≥0.2n인데, 직접계산 646/LL은 I<0.2n) = **proxy 버그**. **직접 계산(646 Kimi-cross-checked·LL closed-form이 646 재현)이 authoritative → I/n이 n=2,3,4서 DECREASING → paper 원래 `I=o(n)` framing이 맞음.** 드래프트한 Θ(n) 본문 편집 **취소.** (이번 세션 두 번째 철회: floor → Θ(n).)

## 1. ★★ Θ(n) 철회 (상세)

**내 주장(848 commit e738807, 849 commit 906303b)**: 메시지 형식이 syndrome 조건부에서도 bias~0.5 유지(848), 편향 독립방향 #=n(849) → I=Θ(n).

**반증(직접 계산):**
- 646(내 Sage/Python, n=2 exact, **Kimi와 독립 cross-check**): I(x;y|C) m에 수렴 → I_∞(2)≈0.30=0.15n. m=6서 I=0.263.
- LL(Kimi, closed-form α/β/rank, **646을 n=2서 정확 재현**): **I/n이 comparable m/n에서 n 따라 DECREASING**(m/n=2: 0.102→0.077→0.054 for n=2,3,4). → o(n) 일치.
- **subadditivity 논증(결정타)**: 848/849 proxy(각 방향 H(form|s)≈0.72)가 맞으면 n방향 합 H(u|s)≤0.72n → I=n−H(u|s)≥0.28n. 하지만 646은 I_∞(2)≈0.30<0.28·2=0.56, m=6서 I=0.263<0.394(=2−2·0.80). **proxy의 marginal bias가 H(u|s)>Σmarginal을 함의 = 불가능 = proxy 버그.**
- **결론**: per-form-bias proxy(848/849)는 **misleading**(joint I를 잘못 추정). 직접 I(x;y|C)가 진실. **Θ(n) 철회, o(n) 지지(EVIDENCE, 점근 여전히 OPEN).**

**교훈**: heuristic/proxy는 fundamental inequality(subadditivity)로 sanity-check해야. 직접 계산 + 독립 cross-check만 신뢰. **사용자가 "본문은 Kimi 완료 후"로 게이트한 덕에 틀린 Θ(n) 편집이 논문에 안 들어감 — LL(마지막 트랙)이 뒤집음.**

## 2. 라운드9 종합 판정

- **II(db552a0) ACCEPT**: GG ~5% gap = **A-sampling measure**(ordered-basis 90 vs canonical 15). paper 모델=ordered-basis(line 602 직접확인). 내 646=canonical-correct. 두-measure 독립재현(m=4: 0.2040 vs 0.2141). [round8b서 판정]
- **JJ(3de78a5) ACCEPT**: H(C_L·Be|HBe,C)=H(x|y,C)(THEOREM). n=2서 1.86→1.72. **단 n=2만** — 이걸 Θ(n)로 읽은 건 내 오류(철회 §1).
- **KK ACCEPT**: rank-n 극단 family B=C·A_L 누설 0.38→0.54(n=2→3). **단 이건 HBe=0인 MAX-leak 극단**(uniform-B 아님)이라 uniform의 Θ(n) 함의 안 함. honest(OPEN).
- **LL(28a33c6) ACCEPT — ★결정적**: uniform-B I(x;y|C) n=3(m≤10)·n=4(m≤8) closed-form. **I/n comparable m/n서 n 따라 DECREASING(least-sq slope 음수) → o(n) 일치.** 646 n=2 재현. honest EVIDENCE/OPEN(점근 미증명, small-n). **이 직접계산이 내 proxy-Θ(n)을 뒤집음.**

## 3. 본문 영향 (정정)

- **open:marginal-adaptive 변경 안 함** — 원래 `I(x;y|C)=o(n) remains open` framing이 **맞고 LL이 지지**. 드래프트한 Θ(n)/SD-route 재정렬 **취소.**
- (선택) LL의 n=3,4 I/n-decreasing을 o(n) 증거로 **보강** 가능(기존 framing 강화). 단 EVIDENCE/OPEN 라벨 유지.
- II의 GG ordered-basis 표(canonical-correct)는 GG 수치 인용 시 사용.
- worst-to-avg/floor은 별개(open:marginal-adaptive 아님).

## 4. 정직성 회계 (이번 세션 두 철회)

1. **floor**(4c6aed4): "첫 positive 앵커" → search-only·underdetermined·decisional 미확립. 855가 잡음.
2. **Θ(n)**(본 노트): proxy 버그 → o(n). LL이 잡음.
**공통**: 흥분해서 발견을 너무 빨리 선언. proxy/heuristic을 직접계산·fundamental inequality로 검증 안 함. **교훈: 직접 계산 + 독립 cross-check 전엔 "발견" 선언 금지. multi-agent(LL)+게이팅(사용자)이 둘 다 잡음 — 시스템이 작동.**

## 5. 다음

- 라운드9 종결. **본문: 큰 변경 없음**(I=o(n) 유지, GG ordered-basis 보강 정도). consolidate=II GG 표 + LL o(n) 증거 한 줄.
- floor thread(LPN≤sympLPN 외부)는 bridge로 OPEN(bb1ccae 매핑).
- 더 이상 proxy 기반 주장 금지.

No closure; no break; no security claim. OPEN = LSN.
