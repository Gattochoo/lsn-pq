# KLP+25 Formal Theorem Pins (PDF 정독) — 잔여 질문 해소

**Actor:** Claude (adjudicator). **Date:** 2026-06-12.
**Source:** arXiv:2509.20697v1 PDF 직접 정독 (pp. 28–31, 36–39, 44–46, 59–66 — 정의·정리 원문 확인).
**Supersedes:** `2026-06-12-CLAUDE-klp25-definition-pins.md` **§2의 미해소 잔여만** (§1 핀은 그대로 유효).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: ★ LPN-hardness는 **단일표본 Search LSN**에 떨어진다 (Thm 6.6).

이전 pins 문서 §2의 질문("하드니스가 어느 변형에?")이 해소됐다 — **가장 강한 형태**로:
m=1 합성 추정이 옳았고, 심지어 그들이 정리 자체를 단일표본으로 명시했다.

## 1. Formal 정리·정의 (verbatim, PDF)

### Theorem 6.6 (= informal Thm 1.6의 formal counterpart) — p.66

> "**Theorem 6.6** (Average-case hardness of stabilizer decoding with any logical dimension).
> Let p = Ω(n^{−(1−ε)}), for ε ∈ (0,1) a constant, and let k ≥ 1 be an arbitrary number of
> logical qubits (which may depend on n). Suppose that there is an oracle O which solves the
> classical representation of **Search LSN(k,n,p)** with probability 1/2^k + 1/poly(n). Then
> there is a classical algorithm running in poly(n) time which solves **Decision
> LPN(⌊np/6⌋, 2n, p/6)** with advantage 1/poly(n), calling O as a subroutine. By the
> equivalence of LSN and its classical representation, if O instead solves the conventional
> formulation of Search LSN(k,n,p) there is also a quantum algorithm…"

증명 사슬(p.66 proof verbatim 요지): LPN(k′,2n,p′) →[행 버리기]→ LPN(k′,⌈2n−(1+ε)np′⌉,p′)
→[**Thm 6.4**]→ Decision sympLPN(n,3q) →[**Lemma 6.5**]→ Decision LSN^poly(k,n,3q)
→[**Thm 5.3**]→ Search LSN^poly(k,n,3q) → "which reduces easily to **Search LSN(k,n,3q)
by ignoring all but the first sample**." (3q ≤ p, ε=1/3 선택.)

### 받치는 핀들

- **Def 3.13** (p.29): Search LSN(k,n,p) = 입력 **표본 1개** (C ~ C_n, EC|0^{n−k}, x⟩),
  과제 = x 복원. Decision = structured vs (C, I^{⊗n}/2^n) 구별. LSN^m = fresh C_i·E_i,
  동일 x. Remark 3.15: m=poly(n)일 때 표기 LSN^poly.
- **Def 4.1** (p.37): classical rep, **표본 1개** ([A|B], [A|B]·[r;y]+e); A∈Z₂^{2n×n},
  B∈Z₂^{2n×k} 각자 열들끼리 쌍별 심플렉틱 직교, [A|B] full-rank; r=junk, y=secret;
  e=Symp(E), E~D_p^{⊗n}. Eq (4.3): LSN^m = fresh [A_i|B_i]·r_i·e_i, y 고정.
  ✓ 본문 정밀화(be2745b·97b8d3c의 "[A|B]는 등방 아님")가 원문과 일치 확인.
- **Thm 4.3** (p.39): quantum LSN^m ↔ classical rep, strongly quantum-equivalent (1회 호출,
  확률 보존).
- **Thm 5.3** (p.45): Search LSN^m 오라클(prob ≥ 1/2^k+1/poly) ⇒ Decision LSN^{2m} 해결
  (2회 호출). **§5.2 서두 (p.45): "This reduction relies crucially on the ability to obtain
  multiple samples; it is an open question as to whether the equivalence holds with a
  single sample."** — 단일표본 decision→search는 그들에게도 OPEN.
- **Def 6.1** (p.60): sympLPN(n,p) — A∈Z₂^{2n×n} 열 선형독립+쌍별 심플렉틱 직교,
  표본 (A, Ax+e), e = depolarizing의 symplectic 표현. (우리 def:symplpn과 형태 일치.)
- **Thm 6.4** (p.63): LPN → sympLPN (Decision, 1회 호출, advantage η−negl).
- **Remark 3.18–3.19** (p.31): LSN은 **성공확률 증폭 불가**(표본 분할 불가 + 해 검증 불가 —
  검증 자체가 short-vector 문제) · 잡음 단조 증가 가능.

### ★ Lemma 6.5의 junk-embedding 메커니즘 (p.65 verbatim — OP8에 직결)

> "Our basic strategy is to **embed the sympLPN data (A, z) into the junk matrix and vector**
> of one of the samples. **This is a strict departure from the typical forms of coding
> reductions, wherein the secret from one problem becomes the secret in the other. This
> usual strategy is infeasible in our case, as the dimensions are completely mismatched,
> e.g. it is impossible to embed a secret of length n into the secret of LSN if k = 1.**"

즉 **저자들 자신이** "naive secret→secret 임베딩은 차원 불일치로 불가"를 명시하고, **junk로
우회**해서 환원을 완성했다. 랜덤 인덱스 j 하이브리드(첫 j−1 unstructured / j번째 embed /
나머지 structured)로 advantage η/m 보존.

## 2. OP8에 주는 함의 (obstruction 노트의 최종 입력)

1. **bridge 소스 메뉴 확정**: 외부 hardness는 단일표본 Search LSN에 *이미* 붙어 있고
   (Thm 6.6), 다표본 변형은 그로부터 자명하게 hard. ⇒ Direction 2 (THEIR ≤ OUR) 설계자는
   **아무 변형이나 소스로 골라도** LPN-hardness를 수입한다:
   - 소스 = 단일표본: **정보예산 벽** (y-상관 데이터 2n bits vs 우리 인터페이스 Ω(n²) 라벨
     — OP9 lem:m2 동류; 단 같은 *미증명* 벽).
   - 소스 = LSN^poly: 예산 벽 붕괴, **frame-alignment 벽** (y가 표본마다 다른 공개 프레임에;
     우리 과제는 고정 비밀 Lagrangian 하나).
2. **★ 정직성 요구 강화 — junk-embedding 반례 패턴**: Lemma 6.5는 "차원/타입 불일치 ⇒ 환원
   불가" 류 추론의 **in-paper 반례**다 (그들은 비밀이 아니라 junk에 심어 돌파). 따라서 우리
   obstruction 노트는 secret→secret 맵만 검토하고 "자연 맵 막힘"을 선언하면 안 되고, **비밀이
   아닌 자유도에 심는 맵**을 명시적으로 검토해야 한다. 우리 membership-LSN의 자유도 목록:
   junk 레지스터 **없음**, 후보 = (i) 질의점 a_i 분포, (ii) 라벨 잡음 e_i, (iii) 비밀
   Lagrangian의 부분구조(예: L의 일부 방향만 y-의존). Kimi 노트는 (i)–(iii) 각각에 대해
   "여기에 심으면 어떻게 죽는가/사는가"를 다뤄야 논문급이다.
3. **단일표본 decision→search가 그들에게도 OPEN**(§5.2)이라는 사실은 positioning 문장에
   쓸 수 있는 외부 확증: 단일표본 영역의 정보구조가 미묘하다는 것을 그들도 인정.

## 3. 본문 반영 (이 커밋)

- OP8 항목(EN·KO): "(constant-rate LPN ≤ their LSN)"에 **Thm 6.6 정밀화** 추가 — 하드니스가
  단일표본 Search LSN에 이미 붙음(PDF 검증). 그 외 본문 무변경.

## 4. 다음

- (Kimi) OP8 obstruction 노트 최종판: 본 문서 §1–2 기초, **§2.2의 (i)–(iii) 임베딩 로커스
  검토 필수**, 변형별 벽 분리 유지, 불가능성 어휘 금지.
- (Claude) Kimi 노트 검증 후 positioning item 업그레이드 본문 통합.

No closure; no break; no security claim. OPEN = LSN.
