# Claude — Paper A (lsn-core) ePrint 재제출 최종 점검: PASS

**Actor:** Claude (paper editor/verifier). **Date:** 2026-06-12.
**목적:** 1차 리젝(self-contained / new and interesting / proofs for claims) 재발 방지 전수검사.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 결론: 재제출 GO. 세 리젝 기준 모두 정면 충족. 본문 수정 불요(검증 패스).

## 1. 빌드·정합성 (자동)

| 검사 | 결과 |
|---|---|
| tectonic 빌드 | ✅ clean, 31pp, 경고 0, overfull 0 |
| 미정의 ref / cite | ✅ 0 (전수: ref↔label, cite↔bibitem) |
| 미사용 bibitem | ✅ 0 (17개 prune 후) |
| dangling construction ref (sec:kem/snark/tab:r1cs…) | ✅ 0 |
| 깨진 "??" / "Section ?" | ✅ 0 |

## 2. 리젝 3기준 대응

**(A) self-contained.** 구성물(KEM/SNARK/구현) 전부 companion으로 분리. 코어의 어떤 정리도
companion에 의존 안 함("present paper is concerned only with the hardness landscape").
"Applications" 1문단만 포인터(의존 아님). 모든 증명 = 본문 또는 appendix 내재.

**(B) new and interesting.** 신규 §7 Exact Moments — $m_2,m_3$ 닫힌형 **정리**(리젝본에 없던 결과).
Witt 환원 → 세 counting lemma(7.1–7.3) 통합증명 완결.

**(C) proofs for claims.** 모든 주장이 정리/증거/추측으로 분류(abstract 명문화). 조건부 2건
(pencil conj 6.5, lem:m2 9.12) 발생 지점마다 명시. §7 lemma 완전증명.

## 3. 수학 재검증 (§7, 독립)

공개 공식이 내 검증값과 **정확 일치**(Sage 기호 + 완전열거 n≤6 + 블라인드 n=7, P=134,176,770):
- $m_2 = \frac{(2n-1)u^2-(4n-3)u}{4(2n-1)(4u^2-5u+1)}$ ✓
- $m_3 = \frac{u(u-4)}{16(4u^2-5u+1)}$ ✓ ($n$-무관, $u=4$서 0 → $m_3^{(2)}=0$ 설명)
- 점근 $\frac1{16}-m_2=\frac{3}{64u}$, $\frac1{64}-m_3=\frac{11}{256u}$ ✓
- counting lemma 증명 골격($q_S=\sum_{c_1\in V_S}(|V_S\cap c_1^{\perp_\Omega}|-1)$, $W_S^{\perp_\Omega}=\{c:\mathrm{supp}\subseteq\sigma(S)\}$) 손검토 정확.
- "machine-verified symbolically + blind n=7" 귀속 = 정직(증명은 본문, 검증은 코드).

## 4. 톤·필수요소

위험어 0(no 7th / DEAD / rotation / OFA / "we break" / stale title). 필수요소 전부:
소버 제목·AI 고지(back matter)·CC BY 4.0 ©·Independent Researcher·KLP+25/LPQR26 positioning
(Thm 6.6 단일표본 정밀화)·재작성 Limitations 5항(worst-case 부재·SQ=증거·조건부 2건·moment
차수 한계·양자 추측).

## 5. 재제출 패키지 (그대로 사용)

- **제출물:** `paper/lsn-core.pdf` (31pp).
- **Category:** Foundations (구 Cryptographic protocols에서 변경).
- **Abstract / Note / Message-to-editor:** `2026-06-12-CLAUDE-paper-A-restructure.md` §2.
  편집자 메시지에 이전 제출번호(xxxx/109987) + 변경 요지(범위 축소·구성물 분리·전 주장
  증명/라벨·신규 §7 정리) 포함.

## 6. 정직한 잔여 리스크 (내 통제 밖)

수학·구조·자체완결성은 충족. 단 ePrint 스킴의 무명저자+AI고지 회의는 변수 — 그래서 Zenodo
DOI(10.5281/zenodo.20646796)로 우선권은 이미 확보됨(재제출 결과와 무관). 재제출은 정정된
물건으로, 같은 패턴매칭 위험을 구조적으로 낮춤.

No closure; no break; no security claim. OPEN = LSN.
