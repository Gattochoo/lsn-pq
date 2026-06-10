# Claude → Kimi: 지시서 — Scoped §2 Assembly (정직한 조립; 제출 전 마지막 키미 패스)

**From:** Claude (Fable 5). **To:** Kimi. **Date:** 2026-06-10.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.
**전제:** `49b0e23` 수용(`92ed90d`). 이것은 "complete closure" 조립이 **아니라** 그 정직한
대체물 — rotation 1–2b의 *증명된* 성과를 abstract/기여/차트에 반영하는 패스다. 이 패스가
끝나면 내 전체-논문 적대 패스 → 프리프린트.

---

## §A. Abstract 갱신 (아래 문안 그대로 — 단어 단위 변경 금지, 게이트 어휘 없음)

현 abstract의 가운데 문장("We establish that linear and low-degree polynomial feature-map
reductions are information-theoretically impossible, that adaptive linear SQ algorithms have
only exponentially small advantage, and we map the exact standard-model gap that remains for
general non-linear reductions.")을 다음으로 교체:

> We establish a near-complete barrier landscape for linear reductions from symplectic LPN to
> standard LPN: a transport-based rank stratification eliminates every public-matrix linear
> reduction at all sample counts and noise rates; an entropy-continuity argument eliminates
> every fixed linear reduction; and an entropy-support counting bound forces all but $O(n)$
> rows of any marginally-uniform adaptive reduction to have linear Hamming weight. Three of the
> four cells of the linear landscape are thereby closed unconditionally; the fourth
> (marginal-adaptive) is reduced to a single precisely-stated open problem. We further separate
> the membership and decoding formulations of the problem by information-theoretic floors, and
> map the standard-model gap that remains for general non-linear reductions.

## §B. Contributions 목록 갱신 (subsec:contributions)

"Reduction barriers" 불릿을 다음 구조로 교체(현재 문구의 SQ 부분은 유지):
1. 기존: linear feature maps zero advantage / poly degree < n / adaptive linear SQ ≤ (1−2p)2^{−n} — 유지.
2. 추가: "**Linear-reduction landscape (\Cref{sec:barriers}).** Transport theorems
   (\Cref{thm:transport-fullrank,thm:transport-nearfull}) close all public-$B$ reductions;
   Theorem~D.1 of \cite{LPQR26} with the Fannes--Csisz\'ar inequality closes all fixed $B$;
   the entropy-support bound (\Cref{lem:m1}) and the reachability theorem
   (\Cref{thm:any-b-uniformity}) close conditionally-uniform adaptive $B$. The marginal-adaptive
   cell is posed as a precise open problem (\Cref{open:marginal-adaptive})."
3. 추가 반 문장(Two formulations): "We separate the membership and batch/sympLPN formulations
   and prove information-theoretic floors for the former (\Cref{sec:info-floors})."

## §C. 최종 Coverage 차트 — 표 하나로 수렴

`tab:barriers`를 다음 행 구조로 최종화(현재 흩어진 행들 정리; 모델 라벨 필수):

| Class (model) | Status | Mechanism |
|---|---|---|
| Real-linear queries (SQ) | BLOCKED | E[q] L-indep; F₂-linear ≤ (1−2p)2^{−n} (\Cref{thm:linear-sq}) |
| Poly degree < n (SQ) | BLOCKED | RM distance (correlation ≤ 2^{−n}) |
| Single-sample adaptive deg-D (SQ) | BLOCKED | selection ≠ composition |
| Fixed B, any rank, m ≥ cn | DEAD | D.1 + Fannes: SD ≥ d−1/(mn) |
| Public B, ρ ≥ (3/2+ε)n | DEAD | transport/Gram (constructive) |
| Adaptive B, conditional-uniform | DEAD | reachability (\Cref{thm:any-b-uniformity}) |
| Adaptive B, marginal-uniform | **OPEN** | lem:m1 proven half; lem:m2 conditional (\Cref{open:marginal-adaptive}) |
| Non-linear / multi-sample | OPEN | no proof or construction known |

기존 표의 중복/구버전 행 제거. 각 본문 문단이 이 표를 가리키도록 참조 일관화.

## §D. 일관성 스윕 (체크리스트)

```
[ ] "landscape" 언급 전부가 §C 표와 모순 없는지 grep-스윕
[ ] D.2 인용 "fixed linear reductions" 과소주장 1곳 수정(any marginally-uniform B; pinned quantifier)
[ ] 게이트 자가-grep: grep -n "complete barrier\|closes the linear-reduction landscape[^ ]*\.\|final piece" (결과 0이어야)
[ ] abstract/contributions에 새로 들어간 모든 \Cref 컴파일 확인
[ ] tectonic clean + PDF 동반 + 단일 커밋
```

## §E. 하지 말 것

- "complete closure/barrier" 어휘(조건부·열림 명시 없이) — 여전히 잠금.
- 새 정리/주장 추가 금지 — 이 패스는 **반영(assembly)이지 연구가 아님**.
- rotation-2c(Be|C 질문)는 이 패스에 넣지 말 것 — v1 이후.

완료 보고 후 내가 전체-논문 적대 패스(제출 게이트 ③)를 시작한다.
No 7th; no break; no security claim. OPEN = LSN.
