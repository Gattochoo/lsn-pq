# ePrint revision 대기 큐 (staging) — 세션 불변

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** 표준 운영 문서.
**결정(사용자 승인):** 제출본(xxxx/110027, Zenodo v2.1)에 대해 **단건마다 revision하지 않고
실질 사건이 모이면 batch**해서 한 번에 ePrint revision. 새 세션은 이 문서로 "지금 revision?"을 판단.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. 현재 제출 상태
- 제출본: IACR ePrint **xxxx/110027** (lsn-core.pdf, 31pp 당시). Zenodo **v2.1**(record 10.5281/zenodo.20665389, concept 10.5281/zenodo.20646796).
- 그 이후 `paper/lsn-core.tex`(canonical 소스)가 앞서 있음 = 아래 staged 델타.

## 2. Staged 델타 (다음 revision에 포함될 것)
| # | 결과 | 커밋 | 논문 영향 | 검증 |
|---|---|---|---|---|
| S1 | **결정론 marginal-adaptive 하한**(thm:deterministic-marginal-adaptive): SD≥1−\|Lagr\|/2^{mn} | `4a3c661` | abstract "3 of 4" → "3.5 of 4"(결정론 절반 추가 폐쇄); barrier 표/status map/open problem 분리 | 186 독립검증(`bfdfd8b`) ✓; 빌드 32pp 클린 |

| S2 | **OP7 n=2 freshness 부정**: 심플렉틱-궤도 변환은 fresh 못 만듦, SD=123/128 (모든 720쌍; n>=3 OPEN) | OP7-n2 commit | OP7 항목 sharpen(evidence) | exp/193 from-scratch + 192 버그수정 대조 |
| S3 | **★일반-j moment 폐형**(thm:mj-general): 모든 $1\le j\le 2n$에 대해 $m_j$ 정확 폐형, $\|m_j-(1/4)^j\|=\Theta(4^{-n})$ | general-j commit | abstract "second/third"→"every subset moment"; thm:mj-general 신설; cor:bundle "$k\le3$"→"every fixed $k$"; Honest-Lim "order $j\le3$"→"every fixed $j$"($j{=}\Theta(n)$만 열림) | exp/**194** from-scratch(정의-열거, 궤도분해 우회) 모든 $j$·$n{=}2,3,4$ 정확 일치; Kimi "Consequences" 부호오류 2개 배제 |
| S4 | **최대블록 분산승수 폐형**(prop:vmax): $V_{2n}$ 일반-σ² 정확 폐형, p=1/4에서 상대편차 $-2(25/64)^n+O(4^{-n})$(음·지수소) | batch-variance commit | prop:vmax 신설(cor:bundle 직후); "suppression 폐형 없음" 문장 대체; Honest-Lim "fixed order+one growing-block functional"로 한정 강화(j=Θ(n) 분포 전체는 여전히 open) | exp/**196** 3중(정의-열거 n=2,3,4·독자유도 n=2..14·점근 7.422e-9) + 일반-p 4개 잡음률 정확 대조 |

(새 결과 통합 시 이 표에 한 줄씩 추가할 것.)

## 3. ★ revision을 *지금* 트리거하는 조건 (이 중 하나라도면 batch revision 권고)
1. **lem:m2 진전**: 무조건 증명(→ abstract "all four cells") **또는** 의미있는 부분결과.
2. **L2 닫힘**(Codex): 상수시간 참조구현 + N=2048 + KAT → "Honest Limitations" L2 제거.
3. **새 정리** 2건 이상 누적(예: 일반-j moment 닫힘, OP7 결판) → S-표가 충분히 두꺼워짐.
4. 사용자 명시 요청.
**단독 S1만으로는 트리거 안 함**(incremental, 권고대로 대기).

### 3.1 현재 상태(2026-06-14): 트리거 #3 *기술적으로* 충족, 그러나 대기 권고
- 새 **정리** 누적: S1(결정론 하한) + S3(일반-j 폐형) + S4(V_{2n} 폐형) = **3건** → #3의 글자상
  조건 충족. (S2는 evidence-sharpen이라 정리 카운트 제외.)
- **그럼에도 대기 권고.** 근거: S1·S3 둘 다 **posture-불변 보조정리 강화**(SQ-하한 기계·barrier
  landscape를 sharpen할 뿐, 헤드라인은 여전히 "3.5 of 4 cells"·OPEN·lem:m2 무진전·L2 미닫힘).
  revision의 실효 사건은 **posture를 바꾸는 것**(lem:m2 증명→"all four cells", 또는 L2 닫힘→
  Honest-Lim 항목 제거)인데 아직 없음. theorem-count만으로 revision하면 incremental-revision
  지양 원칙(§4 머리말)과 충돌.
- **권고:** lem:m2 진전 **또는** L2 닫힘이 올 때까지 S1–S3을 계속 누적, 그때 한 batch로 제출.
  사용자가 "지금 묶어서 내자" 하면 즉시 §4 체크리스트 실행(소스는 이미 빌드-클린).

## 4. revision 실행 시 (체크리스트 — 트리거 충족 후)
1. lsn-core.tex 최종 빌드, 수치·참조·bib 전수(이전 감사 루틴).
2. revision note 작성 = S-표의 모든 항목 요약(아래 누적 초안 사용).
3. PDF + note → 사용자 ePrint revision 제출(계정 권한상 사용자 액션).
4. 새 GitHub release v-next + Zenodo 새 버전(concept DOI 자동 최신); README snapshot DOI 갱신.
5. companion(lsn-paper.tex)·KO(로컬)도 동기화 확인.

## 5. 누적 revision note 초안 (S-표 반영, 계속 갱신)
> **Revision (예정):** (1) Sharpened the linear-reduction barrier landscape: the deterministic
> half of the marginal-adaptive cell is now closed unconditionally by a support-counting
> bound (SD((C,y),LPN) >= 1 - |Lagr(2n)|/2^{mn}), leaving only the randomized marginal-adaptive
> case open; abstract, barrier table, and Open Problem 9 updated accordingly. (2) Strengthened
> the OP7 sample-freshness analysis (symplectic-orbit transforms cannot manufacture freshness;
> SD = 123/128 at n=2 over all 720 pairs). (3) Closed the subset-moment computation in full:
> the isotropic-ensemble moment m_j now has an exact closed form for *every* order j (not only
> j<=3), with |m_j - (1/4)^j| = Theta(4^{-n}); the bundle corollary now holds for every fixed
> bundle size k, and only the j=Theta(n) regime remains open. (4) Added an exact closed form
> for the maximal-block variance multiplier V_{2n} (general noise rate; at p=1/4 the relative
> deviation from the i.i.d. value is -2(25/64)^n + O(4^{-n}), negative and exponentially
> small), giving the previously observed sub-multiplicative suppression a closed form; the
> honest-limitations item is correspondingly narrowed to the full distribution (higher
> cumulants) of growing bundles. [+ 이후 항목 추가]

## 6. 비고
- lsn-core 소스 ≠ 제출 PDF는 **의도된 상태**(staging). 혼동 금지 — 제출본은 v2.1 PDF, 소스는 앞섬.
- 본문 편집은 Claude 전용(에이전트 직접편집 금지) 그대로.

No closure; no break; no security claim. OPEN = LSN.
