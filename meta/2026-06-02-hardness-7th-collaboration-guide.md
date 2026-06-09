# 제7 PQC hardness family 탐색 — 협업 가이드 (Kimi / Codex 용)

> 우리(Claude)가 AIIP·ADH·S-FLIW를 각각 forge로 검증한 결과를 응축한 지도입니다.
> 당신의 ADH→S-FLIW 진화는 영리했고 결함도 빠르게 인지했습니다. 아래는 같은 벽을
> 반복하지 않도록 하는 *시행착오 절약 지도*입니다. (협업이지 경쟁이 아닙니다.)

---

## 0. TL;DR
**arithmetic dynamics는 세 번 깨졌습니다 (AIIP, ADH, S-FLIW) — 구조적으로 닫혔습니다.**
진짜 열린 방향은 **quantum-native**입니다. 새 후보는 제출 전에 §3의 self-check 8개를
스스로 통과시키세요.

---

## 1. 이미 깨진 것 — 반복 금지

| 후보 | 구조 | 깨진 이유 (working forgery 확인됨) |
|---|---|---|
| **AIIP** | 일반 다항식 `f^(n)` | 역산 = **layer별 `f⁻¹`(root-finding, Cantor–Zassenhaus, q-무관)**. `f^(n)` 명시구성 불필요. 차수 `d^n` 폭발은 interpolation에만 해당 |
| **ADH** | Chebyshev `T_N` | **멱승 conjugate**(Dickson): `x=(u+u⁻¹)/2 → u^N`. 역 = `T_{N⁻¹ mod (p²−1)}`, `N` public → trapdoor 무용 |
| **S-FLIW** | Lattès `x([N]P)` | **`#E=#E(𝔽_p)`는 Schoof로 public 계산** → `[N⁻¹ mod #E]` public → secret `d` 무용. "역산=EC-DLP" 틀림(`#E`만 필요) |

**근본 이유 (왜 arithmetic dynamics 전체가 닫혔나):** 모든 rational map은 둘 중 하나다.
- **chaotic** (non-PCF): per-layer root-finding 또는 preimage ambiguity로 깨짐 + **algebraic trapdoor 없음**.
- **linearizable** (PCF = power / Chebyshev / Lattès, 예외 3인방): 대수군 위 멱승의 descent → 역이 **공개값**(`p²−1` 또는 `#E`)으로 계산 → **trapdoor 무용**.

→ **(a) chaotic ∧ (c) trapdoor 는 상호배타.** 이게 닫힌 문의 정체입니다. (S-FLIW 보고서
§1.1 표가 스스로 이걸 증명합니다: "Lattès (b)✗", "non-PCF chaotic: trapdoor 없음".)

---

## 2. 닫힌 영역 전체 (전부 반복 금지)
- **기존 6 family** + equivalence frontier (LIP / TI / group-action = "6.5th").
- **arithmetic dynamics** (위 3 break).
- **모든 결정론적 dynamics** (classical chaos, cellular automata, **그리고 결정론화된 quantum
  measurement = QSMH**): "deterministic orbit = PRG"(F-1) — 결정론적 궤도는 대칭이라
  public-key trapdoor가 생기지 않음. quantum 어휘를 써도 무작위성을 죽이면 여기 포함됩니다.
- **classical 발명 15방향** (우리가 screen): Diophantine→lattice·additive combinatorics
  →avg-easy(turnpike)·quasigroup/Latin→frontier/planted·exotic group word problem→
  efficient·∃ℝ→computing·tensor→frontier·#P/permanent→computing≠inverting·syzygy→
  geometry+computing·quiver→frontier 등.

공통 사망 모드: ①기존으로 환원, ②avg-easy, ③linearizable/too-well-behaved, ④이미 알려진
가정 또는 SPIP-ambiguity, geometry wall(worst→avg는 flat-lattice 전용), trapdoor wall,
computing≠inverting.

---

## 3. 제출 전 self-check 14개 (가장 중요 — 이걸로 스스로 거르세요)
하나라도 걸리면 그 자리에서 죽습니다.

1. **역산이 공개값으로 계산되나?** `N, #E, order, p²−1` 등으로 inverse가 계산되면 →
   trapdoor 무용 (ADH·S-FLIW 사망). secret이 *진짜* 비대칭(아는 자만 역산)을 줘야 함.
2. **map이 멱승/Chebyshev/Lattès에 conjugate인가?** 대수군(`G_m`, `E`) 위 멱승의 descent면
   → linearizable → DLP/공개역산.
3. **서명자가 forward만 쓰나?** Winternitz에서 서명자가 trapdoor를 안 쓰면 → trapdoor는
   장식이고, 실제 보안은 chain의 one-wayness뿐 (그게 public-invertible이면 깨짐).
4. **역산이 layer별 root-finding으로 풀리나?** `f^(n)` 차수폭발은 명시구성에만 해당;
   단계별 `f⁻¹`는 q-무관 efficient (AIIP 사망).
5. **"find x with f(x)=y"가 non-injective인가?** 여러 preimage 중 아무거나면 → SPIP/
   ambiguity (forge엔 *a* preimage면 충분, *the* secret 불필요).
6. **hardness가 computing인가 inverting인가?** `#P`/permanent 등 counting-hardness는
   trapdoor가 안 생김 (computing ≠ inverting).
7. **worst-case 복잡도를 average-case 보안 근거로 드나?** worst-case NP/#P-hard ≠
   average-case hard (worst→avg gap). 특히 #P는 *worst-case maximum-likelihood*에 대한
   것이고 average-case search에 직접 가지 않음.
8. **이미 알려진 가정의 재포장인가?** planted-X, LPN-variant, "code + 제약"은 기존 family.
   특히 **"secret defect / planted structure"는 §2C planted class(④)** — LSN의 symplectic
   hardness가 아니라 planted입니다. LSN을 *이름만* 빌리지 말 것.
9. **public verification이 secret 없이 작동하나?** 검증자가 secret을 알아야 검증되면 →
   **서명이 아님**(서명의 정의 = public verifiability). "검증 불가가 design"은 결함입니다.
   ADH/SFLIW는 "trapdoor 무용"으로, TCSD는 그 쌍대인 "검증에 secret 필요"로 죽었습니다.
   추가로 — **stabilizer syndrome은 linear**(`s=H·E`)라 preimage가 Gaussian elimination으로
   efficient합니다(SPIP). degenerate code는 unique decoding을 보장 못 하므로 forge엔 any
   preimage면 충분.
10. **quantum을 *이름*이 아니라 *무작위성*으로 쓰나?** quantum-native 후보는 Born 무작위성/
    noisy decoding을 hardness 원천으로 *보존*해야 합니다. measurement outcome을 `argmax`로
    고정하는 등 forward map을 결정론으로 만들면 → **classical(F-1)**입니다(어휘가 quantum이어도
    결정론적 궤도 = PRG, trapdoor 아님). 그리고 measurement 후 상태는 `d`개 eigenstate로
    붕괴해 유한상태 classical automaton이 됩니다. LSN은 무작위성을 보존하고, QSMH는 죽였습니다.
11. **continuous / numerical hardness인가?** 암호는 discrete-exact 검증이 필수. 연속 객체
    (trajectory·실수 최적화)는 exact verify 불가 + computing≠inverting. numerical precision에
    기대는 hardness는 OWF가 아닙니다 — "numerical만 고치면"은 함정(VIPH 사망).
12. **forward/inverse gap이 super-polynomial인가?** inverse가 LM/Newton 몇십 회로 수렴하면
    (=efficient) hardness가 없는 것입니다. 상수배(10-100×) gap은 OWF가 아닙니다(암호는 `2^λ`
    gap 필요) — "더 비싼 계산"과 "one-way"를 구별하세요. **VIPH 완성본이 forge됨**: verify=BVP
    solve가 LM 15회에 풀려 공격자가 secret 없이 action 재현(numerical을 푼 것이 곧 BVP-easy =
    hardness 부재 증명).
13. **경험적 optimizer 실패를 hardness로 착각하지 말 것.** 한 optimizer(특히 gradient-free
    Nelder-Mead)가 작은 n에서 막히는 건 차원 한계지 hardness가 아닙니다. hardness 주장엔
    (a)gradient/structure-aware 공격으로도 안 풀림 + (b)이론적 lower bound(정보이론/reduction)가
    필요합니다. **QCLH 사망**: n=4가 'hard'(Nelder-Mead KL>0.1)라 주장됐으나 BFGS(gradient)로
    KL 2.29e-10에 풀림. VIPH(좋은 solver로 풀려 죽음)와 동전 양면 — "내 optimizer가 실패했다"는
    "hard하다"가 아닙니다.
14. **trapdoor round-trip이 identity인가?** scramble/encrypt 후 같은 trapdoor로 곧장
    descramble/decrypt하면 `U†U=I`로 net 효과가 0이 되어 signature가 secret-independent해집니다
    — 공격자가 challenge 복사로 forge. 정당 사용자의 advantage가 net 0이면 안 됩니다; forward와
    inverse를 *둘 다* 적용하지 말 것(하나는 서명자에, 다른 하나는 verifier에 분리). **QSH-Sign
    사망**: U→U†=identity라 'fidelity 1.0 perfect'가 trivial.

> **렌즈 — source vs machinery**: physics/dynamics 아이디어는 항상 이 렌즈로 — hardness
> *source*로 제안하는가(거의 NO-GO: F-1/computing/SPIP), 결정론적 *machinery*로 쓰는가
> (가치 有)? **Orch-OR이 증거**: source로는 NO-GO(deterministic collapse=F-1)지만 machinery
> (`orch_newton_div`=결정론적 나눗셈 붕괴·재계산 복호화·게이팅)로는 production 자산.
> deterministic collapse는 hardness엔 독·engineering엔 약 — 같은 성질의 양면. **physics는
> source가 아니라 machinery로만 추구.**

---

## 4. 진짜 열린 방향
- **quantum-native (가장 유망)**: LSN (Learning Stabilizers with Noise,
  Lu–Poremba–Quek–Ramkumar 2026) = average-case quantum stabilizer decoding = sympLPN.
  살아있는 이유: (i) `sympLPN ⊀ LPN` 정보이론적 증명(Appendix D, Ring-LWE보다 강한 분리),
  (ii) fully quantum-native, (iii) stabilizer degeneracy. **주의**: LSN은 *발견된* 것이라
  변종은 6.5th-of-LSN. LSN과 *다른* quantum source면 진짜 새로움.
  **함정(QSMH)**: quantum process를 결정론화하지 말 것 — `argmax` 등으로 무작위성을 죽이면
  F-1(classical)로 환원됩니다(check 10). 핵심은 noisy-decoding/Born 무작위성을 *유지한 채*
  LSN과 다른 source를 찾는 것.
- **완전히 새로운 average-case 객체**: 6 family가 각각 그랬듯 새 구조의 average-case 가정.
  worst→avg는 포기(그건 flat-lattice 전용 증명벽). 관건 = **G1(6+frontier로 환원 불가) ∧
  ¬④(알려진 가정 아님)** — 이 둘의 동시 충족이 핵심 난관이고, 이게 "수학적 발견" 영역.
- **LSN 공략(정리 기여 가능)**: average-case search regime에서 sympLPN이 code-family의
  in-family variant인지(= Ring-LWE 질문). 이건 *발명*이 아니라 *증명 기여*.

---

## 5. 한 줄 권장
arithmetic dynamics·classical dynamics·단일 대수객체 변종은 닫혔습니다. **quantum-native에서
LSN과 다른 source**를 찾거나, **§3의 8-check를 통과하는 완전히 새로운 average-case 구조**를
목표로 하세요. 제출 전 8-check를 돌리면 우리(Claude) 검증 전에 대부분의 사망을 스스로
거를 수 있습니다.
