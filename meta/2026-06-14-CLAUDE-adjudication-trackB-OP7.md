# Claude 판정 — Track B: OP7 T-독립성 정리 + f(n) 폐형 (ecacd48)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi `ecacd48`(THEOREM B.1 T-독립성, THEOREM B.2 $f(n)=1-\tfrac{p^2+(1-p)^2}{4^n}$).
**검증:** from-scratch(`experiments/251-CLAUDE-trackB-OP7-verification.py`) — **전단사 논증을 우회한
직접 구성**(T를 분포 안에 넣고 P_T, Q_T를 정의대로 구축 후 SD 정확 계산).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**두 정리 모두 ACCEPT — OP7의 심플렉틱-궤도 family가 모든 n에서 정리로 음성 결판.**
$f(n)=1-5/(8\cdot4^n)$ (p=1/4): $123/128$(n=2)·$507/512$(n=3)·$2043/2048$(n=4)→1.
본문 OP7 항목을 "n=2 경험적"에서 "**모든 n 정리**"로 승격, 열린 부분은 궤도-family **밖**의
공개 변환만으로 좁힘. 거버넌스 완벽(블록 210 ✓·track-B prefix ✓·PRE-REGISTER 3점 완비 ✓·scope
guard ✓) — 지난 피드백 전부 반영된 모범 산출물.

## 1. THEOREM B.1 (T-독립성) — ACCEPT

**증명 건전성(손 재유도):** 지시서가 경고한 함정("재색인하면 두 번째 비밀이 $T^{-1}L$로 바뀜")을
정확히 피함 — **corrected rerandomized-secret convention에서** fresh 분포 $Q_T$의 T-의존이
두 번째 공개부의 결정론적 재라벨링 $z=Tw$에만 있으므로($\mathbf 1_{T\cdot L}(Tw)=\mathbf 1_L(w)$가
T를 라벨에서 제거), 전단사 $\Phi_T:(u,b_1,z,b_2)\mapsto(u,b_1,Tz,b_2)$가 $P_I\mapsto P_T$,
$Q_I\mapsto Q_T$ 동시 수송. $(S_1,S_2)\to(I,T)$ 환원도 확인($y_i=S_1u_i$ 재매개변수화, $L$ 균등이라
재라벨 불요).

**독립 수치 확인(전단사 미사용):** 직접 구성으로 n=2에서 **random T 10개 + I 전부 SD=123/128**,
n=3에서 **random T 3개 + I 전부 SD=507/512** (transvection 곱으로 생성, symplectic 검증 후 사용). ✓

## 2. THEOREM B.2 (폐형) — ACCEPT

**증명 핵심 재유도:** $P_I$는 대각 $(u,b,u,b)$ 지지; 핵심 항등식
$\sum_b q_{u,b,L}^2 = p^2+(1-p)^2$ (L,u 무관!) → Q의 대각 질량 $=(p^2+(1-p)^2)/4^n$;
$\min(P,Q)=Q|_{\rm diag}$ 단계는 $Q\le(1-p)^2/16^n < p/4^n\le P$로 성립(n=1 경계 포함).
**독립 확인:** Q 대각질량 = $5/128$(n=2)·$5/512$(n=3) 정확 일치; **n=1 직접계산 = 폐형 = 27/32**
(경계 케이스) ✓; |Lagr(6,2)|=135 from-scratch 열거 ✓.

## 3. 본문 반영(lsn-core, Claude 편집) — 완료

Open Problems의 "Sample freshness" 항목 격상: "remains open for $n\ge3$ + n=2 enumeration" →
**모든 n 정리**(폐형+증명 스케치+검증 명기), 열린 질문을 "궤도-family 밖 공개 변환"으로 정밀화.
빌드 ✓(293 KB, 에러 0).

## 4. 의미(과대해석 가드)

- 이 정리는 **multi-user/rerandomization 구조론**: 자연 family로는 fresh 샘플 제조 불가
  → hybrid argument의 사용자수 인자 손실이 궤도-family 한정으로 설명됨.
- **lem:m2·선형장벽·7th 지위와 무관**(posture 불변). 일반 공개 변환의 가능성은 여전히 OPEN.
- f(n)→1은 "궤도 변환이 점점 더 멀어진다"이지 LSN hardness 증거가 아님(noise-bit 공유의 구조적 귀결).

## 5. staging

**S5 등록**(OP7 궤도-family 정리). 누적 정리 S1+S3+S4+S5 = 4건 — 전부 posture-불변이므로
batch 대기 권고 유지(트리거=lem:m2 진전 or L2 닫힘 or 사용자 요청). 단 S-표가 충분히 두꺼워져
**사용자가 원하면 지금 묶어도 자연스러운 분량**임을 명기.

## 6. 다음 (Kimi Track B)

B3 잔여: (i) 일반 p의 $f$ 표현은 이미 B.2가 줌 — 완료로 간주. (ii) **궤도-family 밖** 자연 후보
(affine shift 포함 $x\mapsto Sx+t$, 좌표 치환 외 비선형 공개 맵)에 같은 질문 — 단 scope를
사전 정의하고 들어갈 것(전 공개변환은 무한정 — family를 명시·동기화한 뒤 each를 정리로).
혹은 Track B 종료 선언하고 C/D/E 진행도 타당.

No closure; no break; no security claim. OPEN = LSN.
