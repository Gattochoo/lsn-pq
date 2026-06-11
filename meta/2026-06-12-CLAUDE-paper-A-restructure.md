# Paper A 재구성 기록 + ePrint 재제출 패키지

**Actor:** Claude (paper editor). **Date:** 2026-06-12. **배경:** ePrint 리젝(기준: clear/
self-contained · new and interesting · proofs for claims) → 사용자 결정 = A안(분할+재구성).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. Paper A — `paper/lsn-core.tex` (31pp, 클린 빌드·overfull 0·미정의 참조 0)

**제목:** *The Lagrangian Subspace Noise Problem: Statistical-Query Lower Bounds and
Barriers for Linear Reductions* (구 "A New Framework for PQC" 폐기)

**남긴 것:** 정의·two-forms positioning(KLP+25 정밀화 포함)·정확 상관 공식·SQ 하한
(무조건+조건부)·Krawtchouk w.h.p.+appendix·Decoder 스크린·선형 장벽 지형 전체(lem:m1·
lem:m2 conditional)·정보 바닥·Quantum(압축 유지)·Open Problems(8개)·Limitations(재작성)·
F_q appendix.

**새로 추가:** §Exact Moments of the Isotropic Row Ensemble — **m₂·m₃ 닫힌형 정리**
(세 counting lemma 증명 포함, in-paper proof; Witt 추이성으로 (c₁,c₂) 환원; μ_row 1줄 증명
$L\subseteq\{x_i{=}0\}\iff e_{\sigma(i)}\in L$; 고정-k 번들 corollary + 두 qualification).
→ "new and interesting" 보강 + OP1 항목에 부분 해소 명시.

**제거 (→ companion):** §Cryptographic Primitives 전체(SNARK·KEM·구현보안), polar/KEM
related-work 문단, 파라미터 표 PK 열, polar-rate open problem, KEM성 limitations.
Intro에 "Applications" 한 문단(companion report = repo의 lsn-paper 모놀리스).

**톤 패스:** DEAD→ruled out·honest map→status map·Honesty notes→Remarks 등. 초록 전면
재작성(3분류: lower bounds/barriers/separations + "every claim is a proved theorem, labeled
evidence, or labeled conjecture"). bibitem 17개 prune(인용 35개만 잔존).

**Paper B(구성물):** 모놀리스 `lsn-paper.tex`가 당분간 companion technical report 역할.
KEM/SNARK 단독 논문화는 추후.

## 2. ePrint 재제출 패키지 (paste-ready)

**Title:** The Lagrangian Subspace Noise Problem: Statistical-Query Lower Bounds and Barriers for Linear Reductions

**Abstract:** lsn-core.tex의 새 초록 그대로 (plain-text 변환해 사용).

**Note field:** 31 pages. Companion technical report (constructions: KEM and succinct arguments) and all code, exact-fraction data, and test vectors: https://github.com/Gattochoo/lsn-pq

**Message to editors:**
> This is a substantially restructured resubmission of an earlier submission (xxxx/109987). Following the editors' criteria, the paper has been narrowed to its mathematical core: the constructions have been removed to a companion technical report, the title and abstract now describe exactly what is proved, and every claim in the paper is a proved theorem (with proof in the body or appendix), an explicitly labeled piece of empirical evidence, or an explicitly labeled conjecture. The resubmission also adds a new section with exact closed-form moment theorems for the isotropic row ensemble, including full proofs. The use of large language model assistants is disclosed in the acknowledgements; the author takes full responsibility for the content. The paper is licensed CC BY 4.0.

**Category:** Foundations (구 "Cryptographic protocols"에서 변경 권고).

## 3. 남은 사용자 액션

1. (권장, 즉시) Zenodo에 `lsn-core.pdf`+`lsn-paper.pdf` 스냅샷 업로드 → DOI(타임스탬프).
2. ePrint 재제출: 위 패키지. Category=Foundations.
3. (선택) arXiv endorsement 진행되면 cs.CR 병행.

## 4. 검증 기록

PDF 텍스트 14항목 체크 전부 통과(새 제목·구성물 부재·DEAD 부재·moments 정리·counting
lemma·AI 고지·CC BY·limitations 재작성 등). KO 통독판은 모놀리스 기준 유지(Paper A 안정화
후 갱신 여부 결정).

No closure; no break; no security claim. OPEN = LSN.
