# Claude 판정 — OP9 라운드 4 (`785a1bc`): Krawtchouk ACCEPT·논문 격상 / Fisher 정직 / E-OP9e G-FLAG 미해소(내가 보충)

**Adjudicator:** Claude (Opus 4.8). **Date:** 2026-06-12.
**검증:** Krawtchouk 닫힌형 n≤6 exact + 블록인수분해 + 점근; E-OP9e 200-trial 복원 재측정.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 1. Krawtchouk 격상 DRAFT — ACCEPT, 논문 반영함
- 닫힌형 Var exact 일치(n≤6, 내가 확인). **블록인수분해 rigorous**: Ω가 n개 좌표블록으로
  분해 → per-block σ=(7/4)²=49/16(16항 재계산 확인). C_full 닫힌형 정확. 점근 Var/E²=O((50/81)ⁿ)
  지수감쇠(실측 비율 0.66→0.617 수렴). Chebyshev → 1−2^{−Ω(n)}.
- **조치: lem:affine-coset-bias-whp 신설(EN+KO), 빌드 클린.** = paper v2 첫 실질 개선.
- 미세(향후): Prop5의 (81/64)ⁿ 소거를 명시적으로(내가 확인: q/2≈p²(1−2^{−n}) ⇒ 소거 후 α^n+β^n).

## 2. Fisher-info 이론 초안 — ACCEPT (정직한 DRAFT, 올바른 잔여)
깔끔한 조건부 논증: `TV(P_C,U)≤δ ⇒ I(x;y)≤δn=o(n) ⇒ x 복원불가`(Pinsker). **막힌 지점 정확히
명시**: weight-w B에서 `TV(P_C,U)→0` 증명. per-row Krawtchouk Fourier `∏ᵢ E[(-1)^{ΣT_{ij}B}]`로
환원 — **방금 검증한 character-sum 기계와 직결.** 이게 sharpened OP9. 좋은 방향(공격 가능성 有).

## 3. E-OP9e — G-MEASURE OK, ★G-FLAG 미해소(내가 보충)
- G-MEASURE 준수: joint test(대칭·rank·dot) ✓. 단 **G-FLAG 위반**: rec/ch 거대비율(n=12 w=8:409,
  n=14 w=9:819)을 표에 남기고 **신호/노이즈 해소 안 함**(trials 20-30뿐).
- **내 200-trial 재측정:** 약한 m-의존 복원(n=10 w=7: m=40→1%, m=160→3.5% *성장*) — ≤2n차원
  잡음구조가 소n에서 부분 악용됨(실제 효과). **단 n에서 감소**(3.5%@n10 → 1%@n12). ⇒ 닫힘쪽이나
  깨끗한 0 아님. **Path-B 경보 아님**(n=65에선 무시). Fisher의 "TV→0이면 복원불가"와 정합
  (소n은 TV 큼=복원有, n↑이면 TV→0=복원→0).
- **교훈:** G-FLAG = 거대비율을 표에 남기지 말고 *그 자리에서* 200-trial+m-스케일로 해소하라.

## 4. 종합
라운드4 = 라운드3 수준 유지(Krawtchouk 자기수정→격상 성공, Fisher 정직). 유일 미스 = G-FLAG
절차(거대비율 미해소) — 내가 보충, benign. 모서리 OPEN, **닫힘쪽 + 잔여가 단일 명제(TV(P_C,U)→0)로
정밀화**. 이게 라운드5 표적.

No 7th; no break; no security claim. OPEN = LSN.
