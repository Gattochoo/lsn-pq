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
| S5 | **★OP7 궤도-family 정리**(Track B): 모든 $n$·모든 $S_1,S_2\in\mathrm{Sp}$에서 SD$=1-\tfrac{p^2+(1-p)^2}{4^n}=1-\tfrac{5}{8\cdot4^n}$ — freshness 음성 결판(T-독립성 전단사 + 대각질량) | ecacd48 + OP7-upgrade commit | Open Problems "Sample freshness" 격상: n=2 경험적→모든 n 정리; 열린 질문을 궤도-family 밖으로 정밀화 | exp/**251** 직접구성(전단사 우회): n=2 random T 10개·n=3 random T 3개·n=1 경계 전부 폐형 일치; Q 대각질량 5/128·5/512 확인 |
| S6 | **★sympLPN 정확 상관 + SQ 하한**(Track E, 정정 통합): likelihood-ratio diag $(1+\tau)^{2n}{-}1$·off $-\,$diag$/(2^{2n}{-}1)$ (unconstrained=0과 대조, OP1 상관-수준 답) + $2^{c_pn}$-쿼리 SQ 하한($c_p{=}1{-}2\log_2(1{+}\tau)\approx0.356$@p=1/4) | aa02290 + sympLPN-integrate commit | §4 끝 subsec:symplpn-sq 신설(thm:symplpn-corr + cor:symplpn-sq, σ-twist 수정 증명); abstract·기여 bullet 갱신. **Kimi §6 SDA 적용은 3중 결함으로 기각·정정본만 수록**(인덱싱 스왑/singleton 대각/지수 대각 VSTAT 잠식) | exp/**253** 전 앙상블 전수(90·22680행렬): character 평균 전 S×w, n=2 (A,y) 완전직접+주변화 항등식, σ-twist 반례 자동발견 |
| S7 | **conj:pencil 소규모 정확 검증**(Track D, evidence): n=2 전수(2^15, max ratio 5/2, singleton만; size-3 최대=k=1 pencils) + n=3 size-3/4 **전수 정확 최대** 3·81/32(k=2 pencil 달성) + 대형 크기 탐색 ratio>3 없음 | trackD commits + pencil-evidence commit | conj:pencil 동기 단락에 evidence 한 문장(명시적 "evidence, not proof") — conjecture 지위 불변 | exp/**254** from-scratch: 관행 검증(선형성·대각포함=thm:distance), n=2 전수 재현, n=3 size-3(398K)·size-4(13.2M) 전수 정확화 |
| S8 | **★t의 정확 법칙**(Track C, prop:tdist): $\Pr[t{=}\ell]=\sum_j(-1)^{j-\ell}\binom{j}{\ell}B_j$ — t를 통과하는 모든 통계(전 moment·cumulant·$V_k$) 정확 계산 가능; TV(dist(t), Bin(2n,1/4)) 정확표 n≤10, rate $2^{-(n+1)}$ evidence | a517440 + tdist-integrate commit | §Moments prop:tdist 신설 + remarks 정합 + Honest-Lim 재정밀화(남은 것 = 4-카테고리 결합 조성·다중쌍 수준·rate 증명) | exp/**255** from-scratch: pmf 3중 동일(직접열거==Kimi==역변환, n=2,3,4), TV 분수 9개 전부 일치, 구조 sanity(B_j 재수축 등) |
| S9 | **★TV rate 정리**(Track H): $2^n\mathrm{TV}=\tfrac12+O(2^{-n})$ — 3항 분해·$r_\ell$ GF $((5{+}2z{+}z^2)/4)^n$·$\sum r_\ell=2^n$ | 0c064c2 + round2 commit | prop:tdist의 rate 문장을 증명 포함 정리로 승격 | exp/**257**: 분해==역변환(n=2..10 전 ℓ)·잔차 유계·스퓨리어스 j=0 보정 확인 |
| S10 | **★joint 4-카테고리 GF**(Track I, thm:joint-gf): $G_n=[\tfrac12(T^{2n}{+}S^n)-A^{2n}-B^{2n}-C^{2n}+2x_{00}^{2n}]/P$ — **pairwise 수준 완전 종결**; cor:disagree($c_1{+}c_2$ 비영 균등) | 6e3d55f + round2 commit | thm:joint-gf+cor:disagree 신설; Honest-Lim "multi-pair만 open"으로 | exp/**258**: 계수사전 동일(n=2,3,4)·특수화 재생(n≤6)·한줄 v-불변 증명 확인 |
| S11 | **★pencil-ratio 정리**(Track J): ratio$(n,k)=(2^n{+}1)/(2^{n-k}{+}1)$ 전 (n,k) + $C_n=2^{n+1}/(2^n{+}1)$ 정확폐형 — k=2가 $4\rho_{\rm avg}$를 아래서 강제(추측 상수의 근거) | f904dec + round2 commit | lem:avg-corr $C_n$ 폐형; conj:pencil 동기 단락 정리 격상(k≥3 scale-미달 포함) | exp/**259**: thm:distance 합·q-이항(n≤10)·n=4 몫-리프트 독자 구현 17/9·17/5·17/3·17/2 일치 |
| S12 | **OP7 보편 label-preserving 하한**(Track G 정정판): same-secret에서 SD$=1-4^{-n}[2p(1{-}p)+(1{-}2p)^2A]$, $A\le1$ ⟹ SD$\ge1-(p^2{+}(1{-}p)^2)/4^n$, 등호 iff $f_1{=}f_2$ — **Kimi G.3(모든 쌍 등식)은 순환실험으로 기각, 정정판만 수록** | 0eb7126 + round2 commit | OP7 항목에 보편 하한·열린 질문을 label-modifying으로 재정밀화 | exp/**256**: 공식==열거(n=2 12쌍·n=3 1쌍), 등호-iff 확인, G.1 폐형·흡수 확인; 192 버그값과의 일치(루프 폐쇄) |

(새 결과 통합 시 이 표에 한 줄씩 추가할 것.)

## 3. ★ revision을 *지금* 트리거하는 조건 (이 중 하나라도면 batch revision 권고)
1. **lem:m2 진전**: 무조건 증명(→ abstract "all four cells") **또는** 의미있는 부분결과.
2. **L2 닫힘**(Codex): 상수시간 참조구현 + N=2048 + KAT → "Honest Limitations" L2 제거.
3. **새 정리** 2건 이상 누적(예: 일반-j moment 닫힘, OP7 결판) → S-표가 충분히 두꺼워짐.
4. 사용자 명시 요청.
**단독 S1만으로는 트리거 안 함**(incremental, 권고대로 대기).

### 3.1 현재 상태(2026-06-14): 트리거 #3 *기술적으로* 충족, 그러나 대기 권고
- 새 **정리** 누적: S1(결정론 하한) + S3(일반-j 폐형) + S4(V_{2n} 폐형) + S5(OP7 궤도-family
  정리) + S6(sympLPN 상관+SQ) = **5건** → #3의 글자상 조건 충족. (S2는 evidence-sharpen이라
  정리 카운트 제외; S5 도착으로 S2는 S5에 흡수됨.) S-표가 충분히 두꺼워져 사용자가 원하면 지금
  묶어도 자연스러운 분량이나, posture 변화(lem:m2/L2)는 여전히 없음 → 기본 권고는 대기 유지.
  (참고: lem:m2 트랙은 meta-수준 진전만 — mixture 정리·m-단조성·coarse 하한·n=3 분수 정정·
  충분통계량 환원으로 m≤48 frontier — 본문 델타 없음이라 S-표 비등재.)
- **라운드 2 갱신(2026-06-14)**: S9–S12 추가로 누적 정리 **10건**(S1·S3·S4·S5·S6·S8·S9·S10·
  S11·S12). §Moments(pairwise 완전 종결)·§SQ(sympLPN+pencil 정리)·OP7(보편 하한)이 대폭
  강화됨 — posture는 여전히 불변(lem:m2/L2 미동)이나 **분량상 사용자가 원하면 1회 revision으로
  묶는 것이 자연스러운 시점**. 기본 권고는 여전히 대기(posture 사건 대기).
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
> cumulants) of growing bundles. (5) Upgraded the sample-freshness open problem to a theorem
> for the symplectic-orbit family: for every n and every pair of public symplectic maps, the
> statistical distance between the transformed pair and fresh samples is exactly
> 1 - (p^2+(1-p)^2)/4^n (= 1 - 5/(8 4^n) at p = 1/4), so the orbit family cannot manufacture
> freshness at any n; the open problem is correspondingly narrowed to transformations outside
> the orbit family. (6) Added exact likelihood-ratio correlations for the sympLPN formulation
> (the isotropic conditioning contributes exactly -((1+tau)^{2n}-1)/(2^{2n}-1) off-diagonal,
> versus 0 for the unconstrained ensemble) and a 2^{c_p n}-query SQ lower bound at constant
> VSTAT strength (c_p = 1 - 2 log2(1+tau), about 0.356 at p = 1/4), answering the
> correlation-level form of Open Problem 1 for the sympLPN formulation. (7) Documented exact
> small-case support for the pencil-extremality conjecture (explicitly labeled evidence):
> exhaustive n=2 verification (max ratio 5/2 over all 2^15 subsets) and exact n=3 maxima at
> sizes 3 and 4 (ratios 3 and 81/32, attained by pencils). (8) Added the exact law of the
> pair-level quadrant count t (binomial inversion of the closed-form moments), making every
> statistic that factors through t exactly computable, with exact total-variation distances
> to the unconstrained Bin(2n,1/4) law for n <= 10 (empirical rate 2^{-(n+1)}, labeled
> evidence); the honest-limitations item is narrowed to the joint four-category composition
> and the multi-pair level. (9) Proved the TV rate: 2^n TV -> 1/2 with remainder O(2^{-n})
> (three-term decomposition; r_ell generating function ((5+2z+z^2)/4)^n). (10) Closed the
> entire pairwise level: exact joint generating function for the four-category row
> composition of the isotropic pair, with the disagreement-count corollary (c_1+c_2 is
> exactly uniform over non-zero vectors). (11) Exact pencil ratios for all (n,k):
> ratio = (2^n+1)/(2^{n-k}+1), via the exact C_n = 2^{n+1}/(2^n+1); the k=2 family forces
> any pencil-extremality threshold above 4 rho_avg, matching the conjectured constant.
> (12) Universal label-preserving freshness obstruction: for arbitrary public bijections,
> the same-secret SD is exactly 1 - 4^{-n}[2p(1-p) + (1-2p)^2 A] >= 1 - (p^2+(1-p)^2)/4^n
> with equality iff f_1 = f_2; the open problem is narrowed to label-modifying
> transformations. [+ 이후 항목 추가]

## 6. 비고
- lsn-core 소스 ≠ 제출 PDF는 **의도된 상태**(staging). 혼동 금지 — 제출본은 v2.1 PDF, 소스는 앞섬.
- 본문 편집은 Claude 전용(에이전트 직접편집 금지) 그대로.

No closure; no break; no security claim. OPEN = LSN.
