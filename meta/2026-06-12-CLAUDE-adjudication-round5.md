# Claude 판정 — OP9 라운드 5 (`46acb0c`,`01e752c`): 수학 ACCEPT / ★위협모형 미스(라운드4 전파, 자기수정) / TV 과대주장

**Adjudicator:** Claude (Opus 4.8). **Date:** 2026-06-12. **검증:** `experiments/124`.
Discipline: Sound Verifier (나에게도). No 7th; no break; no security claim. OPEN = LSN.

## 1. ACCEPT (검증) — per-row Krawtchouk + 점근 완성
- **φ_w(d) = K_w(d;2n)/C(2n,w)** 닫힌형 — 생성함수 유도 정확, **n=6에서 검증**(키미 n≤5 너머).
  φ_n(2)=−1/(2n−1) 확인. 깔끔한 결과.
- **TV(P_C,U)=Ω(1/n) 하계** — φ_n(2)≠0의 weight-2 test, rigorous.
- **Prop 5 (81/64)ⁿ 소거 명시화**(`q/2−p² = −1/(2(2^{n-1}+1)(2^n+1)²)` 직접) → Krawtchouk 보조정리
  점근이 **완전 rigorous**. (라운드4 미세갭 닫힘. 부록용 full proof로 채택.)

## 2. ★ 위협모형 미스 — 전체 Fisher/TV 노선이 잘못된 양을 공략 (라운드4 전파; 내 책임 일부)
- 라운드4 Fisher 초안이 "adversary sees y but **not C**"로 설정 → `I(x;y)`를 bound. 하지만 LPN
  환원의 솔버는 **(C,y) 둘 다** 본다(C=BA = 공개 LPN 행렬). 관련 양은 **`I(x; y|C)`**.
- 연쇄법칙: `I(x;y) ≤ I(x;C,y) = I(x;y|C)`. ⇒ TV(P_C,U)가 작아도 `I(x;y|C)`는 클 수 있다.
  **TV(P_C,U) 해결(소멸이든 아니든)은 모서리를 닫지 못한다.** 라운드5의 TV 분석은 수학은
  맞지만 *잘못 조준된 논증*에 feed됨.
- **자기수정:** 라운드4에서 Fisher 초안을 "정직·blocked point 명시"로 받으며 이 모형 오류를 충분히
  안 짚었다. Sound Verifier는 나에게도 적용 — 지금 바로잡는다.
- **진짜 잔여 = `I(x;y|C)`**: 공개 C 하에서 ≤2n차원 잡음 `Be`가 복원-무용한가(= 원래 M2). OPEN.

## 3. TV 과대주장 (softening 필요)
- "TV does not vanish (or at all)" / "TV ≥ 1/2 − o(1)"(chi-squared doc) = **과대주장**. rigorous
  경계는 `Ω(1/n) ≤ TV ≤ O(1)`뿐. χ²=Θ(1)은 TV를 *하계*하지 못한다(TV ≤ √χ²/2는 상계). "상수
  수렴"은 n≤5 + trivial Parseval. → "TV ≥ Ω(1/n); χ²은 비소멸 시사하나 matching 상계는 OPEN"으로.
- 단 키미의 물리적 직관(§4 Path2)은 옳다: "비균등성이 고차 Fourier 모드에 있고 복원엔 무용".
  실측(`experiments/122` 복원→0)과 정합 — **올바른 모형의 증거는 닫힘쪽으로 견고**(이론 노선만 오조준).

## 4. 종합 + 정직한 전환
5라운드째 OP9 이론 닫기는 **≈0**(M2 = `I(x;y|C)` 잔여, 깊은 문제). 실측 닫힘 증거는 견고(올바른
모형). **이론 grinding은 수확 체감** — Krawtchouk 격상(v2)은 건졌고, OP9는 정직하게 OPEN.
- 라운드4 Fisher 초안 + 라운드5 TV 문서: **머리에 "SUPERSEDED — wrong threat model (C public ⇒
  target I(x;y|C)); see adjudication-round5 §2" 추가** 권고.
- 다음(§directive): OP9 grinding 멈추고 정직한 상태정리 + Codex 협업 + v2 마무리로 전환.

No 7th; no break; no security claim. OPEN = LSN.
