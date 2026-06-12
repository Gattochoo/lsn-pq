# 186 결정론 marginal-adaptive 하한 — 논문 반영

**Date:** 2026-06-14

## Theorem

For deterministic $B=g(A)$, the output public matrix $C=BA$ is a deterministic
function of $A$.  Since $A$ ranges over the Lagrangian Grassmannian,
$|\operatorname{supp}(C)|\le |\Lagr(2n,\F_2)|$.  Therefore
$$
  \operatorname{SD}\bigl((C,y),\;\mathrm{LPN}_{p'}\bigr)
  \;\ge\;
  \operatorname{SD}\bigl(C,\;\operatorname{Uniform}_{\F_2^{m\times n}}\bigr)
  \;\ge\;
  1-\frac{|\Lagr(2n,\F_2)|}{2^{mn}}.
$$
For $n=2$ this is $1-15/4^m$; Experiments~185 and~186 verify tightness for
$m=3$ ($49/64$) and $m=4$ ($241/256$).

## What changed in the paper

- `paper/lsn-paper.tex`에 \Cref{thm:deterministic-marginal-adaptive} 추가.
- \Cref{tab:barriers} 행을 둘로 분리:
  - deterministic marginal-uniform → **DEAD**
  - randomized marginal-uniform → **OPEN**
- \Cref{thm:marginal-adaptive} 제목/내용을 "Randomized marginal-adaptive"로 수정.
- 초록, introduction, \Cref{open:marginal-adaptive}에서 deterministic 반은 닫혔음을 반영.
- 종합된 honest map:
  - fixed-$B$ **DEAD**
  - public-$B$ **DEAD**
  - conditionally-uniform adaptive **DEAD**
  - deterministic marginal-adaptive **DEAD**
  - randomized marginal-adaptive **OPEN**

## Compilation

`tectonic lsn-paper.tex` successfully produced `lsn-paper.pdf` with only minor
underfull hbox warnings.

## Implication

This sharpens the linear-reduction landscape: the only remaining open cell is
randomized marginal-adaptive $B=g(A,R)$.  All deterministic dependence on $A$
is unconditionally ruled out by support size alone.
