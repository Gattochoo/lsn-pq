# Claude 검증 — Codex P3 toy-KAT 레일 (de1080d·6655ee3·b605eaf) ACCEPT

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 1. 독립 재현 (내 실행)

| 항목 | Codex 보고 | 내 재현 |
|---|---|---|
| `cargo test` (lsn_ref 전체) | 6 passed | ✓ 4(lib)+2(CLI) = 6 passed |
| `--profile n3-search --check` (153) | verified | ✓ byte-for-byte verified |
| `--profile n2 --check` (152) | — | ✓ verified |
| wrong-secret 음성 control | 실패해야 함 | ✓ 키 불일치 (b760… ≠ ebc7…) |
| fixture 변조 음성 control | 실패해야 함 | ✓ (CLI 테스트 2 중 1) |

수작업 점검: 153의 honest Lagrangian {0,13,22,27,39,42,49,60} — XOR 닫힘 확인(13⊕22=27,
13⊕39=42, 22⊕39=49, 27⊕39=60) ✓ dim-3 부분공간. 시드 전부 고정 = 결정론 재생성 ✓.

## 2. 판정: ACCEPT (P3 toy 레일로서)

게이트 전수 준수: meta 보고 동반 ✓ · JSON(152/153) ✓ · 본문 무접촉 ✓ · 빌드 산출물 repo
밖(.gitignore+CARGO_TARGET_DIR) ✓ · **정직 고지 명시**("not production constant-time, not
L2-complete, not a security claim, not evidence of a public recovery path") ✓.
P1b(145–147·154 checker)·rate sweep(148–150) 마무리 후 Track 4(P3)로 넘어간 순서도 지시서와
부합.

**중요한 정직 사항(현 상태의 한계 — Codex도 자인):** toy 레일은 `public_noise_rate: 0.0`
(무잡음 공개표본)·n=2,3 — **L2(상수시간 참조구현 부재)를 닫는 물건이 아직 아니다.**
correctness 레일일 뿐.

## 3. Codex 다음 increment (P3 계속 — 이 순서로)

1. **noise>0 KAT 프로파일** — 공개표본에 p=1/4 잡음 + repetition/polar가 실제로 정정하는
   프로파일 추가 (실패 시 CLOSURE-GRADE 규칙 적용: BLER-fail = 정지+로그+내 검증 대기).
2. **paper-parameter 프로파일** — 논문 설계점(N=2048, K=256, r∈{7,11}, p′∈{0.0706,0.0343})
   과 `impl/polar_validation` 디코더를 잇는 KAT 1세트 (n은 toy여도 polar 단은 실물).
3. **상수시간 규율 문서화** — lib에서 어떤 연산이 CT이고 어떤 게 아직 아닌지 목록
   (`meta/` 노트). L2를 닫으려면 이 목록이 영(0)이 되어야 한다 — 그때까지 L2는 open.
4. KAT 픽스처는 지금처럼: 시드 고정·체커 CLI·음성 control 2종(변조·wrong-secret) 유지.

게이트 불변. `git restore`/`checkout -- paper/` 금지 규칙은 너에게도 적용된다
(frontier-v2 directive 말미).

No closure; no break; no security claim. OPEN = LSN.
