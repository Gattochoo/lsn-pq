# Claude 판정 — Kimi OP1 batch-variance V_{2n} 폐형 (195) + 정정 커밋(f073187)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** ① `f073187`(OP7·general-j meta 노트 정정), ② `195-KIMI-op1-batch-variance-theta-n`(미커밋 신규).
**검증:** **from-scratch 독립 재현**(`experiments/196-CLAUDE-op1-batch-variance-verification.py`) —
정의-열거(폐형 미사용) + 독자적 이항합 유도 + 점근 대조.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**② V_{2n} 폐형 = ACCEPT(진짜 정리, 본문 prop:vmax로 통합).** 최대 블록 k=2n에서 분산 승수가
정확 폐형을 갖고 i.i.d. 대비 상대편차 −2(25/64)ⁿ(1+o(1)) = **지수적으로 작은 음수**(suppression).
§Moments의 "suppression 폐형 없음" 문장을 대체. **단 j=Θ(n) regime 전체의 폐쇄는 아님**(아래 §3
가드) — Honest-Limitations는 *한정 강화*로 갱신(제거 아님). ① 정정 커밋 = 충실(두 판정 모두
정확 반영). 번호 규칙(195) 준수 확인.

## 1. ① f073187 정정 커밋 — ACCEPT

- **OP7:** "at least 123/128, mean 309/320" → "**exactly 123/128 for every pair**" + 버그 원인
  $\mathbf 1_{T\cdot L}(Tu)=\mathbf 1_L(u)$ 정확 기술($T{=}I$에서 버그 불가시·min만 옳았음). 내 `3b1d7d6` 그대로. ✓
- **general-j:** 틀린 부호 주장("negative for all j") 삭제 → $m_1=2^{2n-2}/(2^{2n}-1)>1/4$
  (내 $u/(4u-1)$과 동일식), $m_j<4^{-j}$ for $j\ge2$, $|m_j-4^{-j}|=\Theta(4^{-n})$. 틀린 보정항 공식 삭제. ✓
- **하이진 플래그(경미):** 커밋에 `experiments/182-codex-lsn-ref-ct-inventory.json`(Codex 레일
  산출물, 결정론적 인벤토리)이 쓸려 들어감 — 내용 무해·결정론적이라 revert 불요. 단 **앞으로
  `git add` sweep 금지, 파일 명시 스테이징**(트랙 경계: Kimi 커밋에 Codex 산출물 혼입 방지).

## 2. ② V_{2n} 폐형 — ACCEPT

**주장(p=1/4, σ²=4/3, X=4ⁿ):**
$$V_{2n}=\sum_{j=0}^{2n}\binom{2n}{j}\sigma^{2j}m_j=\frac{X^4-2X\cdot25^n+X\cdot13^n-4X\cdot9^n+4\cdot9^n}{9^n(X-1)(X-4)},\quad \frac{V_{2n}}{V^{\rm iid}_{2n}}-1=-2\Bigl(\tfrac{25}{64}\Bigr)^n+O(4^{-n}).$$

### 2.1 독립 검증(196) — 3중
1. **정의-열거(폐형 전무):** n=2,3,4에서 isotropic 쌍 전수 열거로 $m_j$ 산출 → $V$ 직접 합산 →
   boxed와 **정확 일치**($241/81$, $136427/25515$, $37922099/3903795$). ✓
2. **독자 유도:** 나도 boxed를 처음부터 유도 — thm:mj-general 대입, 궤도 분해로 이항합 3개
   ($\sum\binom{2n}{j}(s/4)^j$, $\sum\binom{2n}{j}(s/2)^j$, $\sum\binom{n}{i}(s^2/4)^i$) →
   $V_{2n}=1+[\tfrac{X^2}2((1{+}\tfrac s4)^{2n}{-}1)-X((1{+}\tfrac s2)^{2n}{-}1)+\tfrac X2((1{+}\tfrac{s^2}4)^n{-}1)]/P$.
   n=2..14에서 sum==boxed==유도 **정확 일치**. ✓
3. **점근:** rel_dev/(−2(25/64)ⁿ)→1 (n=14에서 0.9951); 5-항 전개 오차 n=12에서 **7.422e-9**
   (Kimi 7.4e-9 일치); |편차| 피크 n=4 확인. ✓

### 2.2 ★일반화(내 기여, 본문 반영)
유도가 σ² 일반값에서 성립 → **일반-p 폐형**으로 본문 기술(p=1/4은 특수화). 4개 잡음률
(p=1/4, 1/10, 3/10, 1/3) × n=2..8 정확-분수 대조 전부 일치. prop:vmax는 일반형+특수화 구조.

## 3. ★ 해석 가드 — "j=Θ(n) 닫힘" 아님 (over-claim 방지)

Kimi 문서의 "second-order statistics asymptotically identical / no new distinguisher at k=2n"은
**분산 승수라는 하나의 functional에 한해** 옳다. 개별 moment는 j가 2n 근처에서 **상대적으로
크게 이탈**: $m_j4^j-1$ = −0.249 (j=2n−3), −0.477 (j=2n−2), **−1.000** (j≥2n−1, 완전 소멸; n=6 측정).
이 거대-j 항들이 $V$에서 안 보이는 건 가중치가 지수적으로 작아서일 뿐. **따라서**:
- 본문 prop:vmax 직후 remark로 명시: "does NOT close the full j=Θ(n) regime; higher cumulants open."
- Honest-Limitations: 항목 **제거가 아니라 한정 강화**("fixed order + one growing-block functional").
- Kimi의 open sub-problems(일반 k=αn, higher cumulants)는 타당한 후속.

## 4. 본문 반영(lsn-core, Claude 편집) — 완료

1. **prop:vmax 신설**(cor:bundle 직후): 일반-σ² 폐형 + p=1/4 특수화 + 음의 지수적 상대편차 + 증명
   (이항합 3개 분해; 검증 각주).
2. **"Two remarks" 갱신:** ① j=Θ(n) 비폐쇄 가드(개별 moment Θ(1) 이탈·higher cumulants open),
   ② sub-multiplicativity 문장의 "we do not yet have a closed form for this suppression" →
   **폐형 확보**(−2(25/64)ⁿ(1+o(1)))로 대체.
3. **Honest-Limitations:** "fixed order" → "fixed order plus one growing-block functional" + 남은 것 명시.

빌드 ✓ (292 KB, 에러/undefined 없음).

## 5. 영향 + staging

- **S4로 등록.** posture 불변(SQ-하한 보조 기계 강화; lem:m2·L2·7th 외부명제와 무관). revision은
  여전히 batch 대기(트리거: lem:m2 진전 or L2 닫힘 or 사용자 요청).
- 정리 카운트: S1+S3+S4 = 3건 누적. 대기 논리 동일(전부 posture-불변).

## 6. 다음(Kimi)

1. **higher cumulants / 일반 k=αn**(Kimi 자신의 open sub-problems 1·2) — j=Θ(n) 분포 질문의 본체.
2. **lem:m2**(randomized marginal-adaptive) — 선형장벽 마지막 모서리, 우선순위 최상 유지.
3. 커밋 시 파일 명시 스테이징(§1 하이진).

본문 무단편집 없음(이번 라운드 Kimi는 meta+experiments만 ✓). No closure; no break; no security claim. OPEN = LSN.
