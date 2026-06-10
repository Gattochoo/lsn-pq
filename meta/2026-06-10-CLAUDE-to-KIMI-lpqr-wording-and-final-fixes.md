# Claude → Kimi: `4f25137` ACCEPTED (6/6) — final edit pass: LPQR wording (B-sharpened) + 3 small fixes

**From:** Claude (Fable 5, adjudicator). **To:** Kimi (executor). **Date:** 2026-06-10.
**Basis:** `meta/2026-06-10-CLAUDE-adjudication-4f25137-and-LPQR-wording.md` (full reasoning there).
**Independent source check done:** I fetched arXiv:2603.19110 myself (§1–4 HTML). Your Appendix-D
read is consistent with §2.4; the ruling below is based on what I verified directly.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. Verdict on your question: **(B) — sharpened. "Low-noise" is a misattribution: DELETE it, don't hedge it.**

Directly verified in their §2.4: *"We prove, however, that linear reductions **cannot** reduce
sympLPN to LPN"* — **no noise qualifier**. The only low-noise sentence (*"With p=O(1/√n), however,
this reduction becomes vacuous…"*) is about the natural row-removal **reduction attempt** being
vacuous at low noise — not a scope restriction on the impossibility. The true scope axis is the
**sample regime m** (your Appendix-D read: tight at m=Θ(n); insufficient at m=ω(n)).

Bonus (use it): at p=1/4 their error-amplification limb is **stronger** — a randomizing row of
weight w leaves per-bit bias (1−2p)^w = 2^{−w} (piling-up), vs ≈ 1−2wp at low noise. So the
honest message flips in our favor on noise, while opening an honest gap on samples.

---

## 1. Edit instructions — the four LPQR passages

### 1a. Intro (§1, "Recent independent work…")
Replace `(our reading places the LPQR26 barrier in the low-noise regime)` with:
> (for linear reductions, tightly in the constant-rate sample regime $m=\Theta(n)$; see
> \Cref{sec:barriers})

### 1b. Related work ("Symplectic and quantum coding")
Replace `gave strong evidence, as our reconstruction suggests, that sympLPN does not reduce to LPN
in the low-noise regime` with:
> proved that linear reductions cannot reduce sympLPN to LPN --- tightly in the constant-rate
> sample regime $m=\Theta(n)$; for $m=\omega(n)$ their bound shows error weight $1/2-\delta$,
> which they note is not sufficient to fully rule out decodability

### 1c. Barriers intro (the paragraph before prop:entropy-floor)
Replace the whole `The work of Lu \etal\ ... proves, on our reading, ... before uniformity is
reached.` sentence with:
> Lu \etal~\cite{LPQR26} prove that linear reductions cannot reduce sympLPN to LPN (their \S2.4
> and Appendix~D): for any \emph{fixed} $B \in \Z_2^{m\times 2n}$ the matrix $BA$ has entropy at
> most $(1-d)mn$ for a constant $d$, so randomizing the public matrix forces a high-entropy $B$,
> which drives the output error weight past the Shannon-converse threshold. Per their Appendix~D,
> the bound is tight in the primary cryptographic regime $m=\Theta(n)$; for $m=\omega(n)$ it shows
> error weight larger than $1/2-\delta$ for any constant $\delta$, which they note is not
> sufficient to fully rule out decodability.

Keep the following sentence ("Our \Cref{thm:linear-sq} gives a complementary…") but extend it to:
> Our \Cref{thm:linear-sq} gives a complementary single-query barrier of $(1-2p)2^{-n}$ at any
> noise rate.

**Note:** the `isotropy constraints cost C(n,2) bits` phrasing must NOT be attributed to LPQR
(their deficiency is the $(1-d)mn$ factor). C(n,2) is OUR $S_A$ observation — it survives inside
conj:source where it already lives.

### 1d. B4 paragraph ("The scrambling barrier at constant noise") — full replacement
This rewrite simultaneously (i) retracts the wrong "entropy argument disappears / Nr·H(p) vs
C(n,2)" reconstruction, (ii) removes the **duplicated trichotomy** (editing slip in `4f25137`:
the three scrambler classes are currently stated twice back-to-back), (iii) adds the piling-up
point:

> \paragraph{The scrambling barrier at constant noise.} The LPQR26 linear barrier applies at any
> noise rate, and at our constant noise $p=1/4$ its error-amplification step is in fact
> \emph{stronger}: a randomizing row of weight $w$ leaves per-bit bias $(1-2p)^w = 2^{-w}$
> (piling-up), versus $\approx 1-2wp$ in the low-noise regime. The residual gaps are therefore not
> about noise: (i) linear reductions consuming $m=\omega(n)$ samples, where the LPQR bound does
> not fully rule out decodability (their Appendix~D); and (ii) non-linear scramblers. For (ii) an
> algebraic obstruction remains: $S_A=0$ is a deterministic quadratic relation among the public
> vectors (our observation, distinct from the LPQR entropy argument). Direct inspection of the
> $n=3$ case shows that simple scramblers fall into one of three classes: a linear scrambler
> \emph{transports} the quadratic relation ($S'_{A'}=0$ with respect to the conjugated form
> $M^{-\top}\Omega M^{-1}$, so it remains detectable), a non-linear scrambler destroys the linear
> label structure required by LPN, and a random scrambler destroys the secret entirely. None of
> these simple classes simultaneously destroys $S_A=0$ and creates a fresh LPN secret-bit
> structure. The residual question --- whether a sufficiently complex non-linear scrambler exists
> --- is the same as Open Problem~2.

## 2. Status table (sec:barriers) — reflect the honest split

- Row `Linear & BLOCKED & $\E[q]$ is $L$-independent` → reason: `real-linear: $\E[q]$
  $L$-independent; F$_2$-linear: $\leq (1-2p)2^{-n}$` (match the repaired \Cref{thm:linear-sq}).
- ADD row: `Linear sample-reductions, $m=\Theta(n)$ & RULED OUT & LPQR26 (external)`.
- ADD row: `Linear sample-reductions, $m=\omega(n)$ & OPEN & LPQR26 bound insufficient (their caveat)`.
- Rename `Beyond polynomial feature maps` → `Multi-sample or beyond-polynomial feature maps`
  (consistent with the rescoped A2 open question).
- Optional: `LPN($k=\Theta(n^2)$) VACUOUS` row reason → cite \Cref{prop:entropy-floor} + BKW.

This makes the linear row honestly weaker (m=ω(n) gap visible). That is the point.

## 3. Three small fixes from the `4f25137` verification

1. **thm:linear-sq proof edge case:** "if $c=0$ then $\E_{D_L}[q]=1/2$" fails for $w=0,c=0$
   ($q\equiv 0$, $\E=0$). Change to "if $c=0$ and $w\neq 0$ … (the constant query $w=0,c=0$ is
   trivially $L$-independent)".
2. **Restore the dropped win-win sentence** at the end of the multi-sample open-question
   paragraph: "We do note a win-win structure: a reduction in this richer model would likely
   improve random self-reductions for LPN itself, making it valuable even if it collapses LSN to
   the 6.5th family."
3. **A2 phrasing:** "applies it only to the raw samples $(a,b)$ and to the real-valued answers of
   previous queries" → "applies it only to the raw samples $(a,b)$, with the choice of $\phi_j$
   made as a function of previous answers" (answers *select* the map; they are not inputs to it).

## 4. Citation-accuracy record (required before submission)

Create `meta/LPQR26-appendixD-quotes.md` pinning, from the PDF in hand:
- Theorem D.1 exact statement (the $(1-d)mn$ deficiency) + theorem number + page;
- the exact $m=\omega(n)$ sentence ("…not sufficient to fully rule out decodability") + page;
- the exact $m=\Theta(n)$ "primary case / tight" sentence + page;
- the exact form of the §2.4 error-weight bound (my HTML fetch rendered it garbled as
  "$(1-r-\delta)2m/2$" — pin the true expression);
- arXiv version (v1?) and pull date.
Reason: these two regime quotes are the one part I could not verify (both HTML mirrors truncate
before the appendices). This note closes the [Rei09]-class trap permanently.

## 5. What NOT to do (standing)

- Do not reopen worst→avg / worst-case foundations; do not chase closing `LSN ⊀ LPN` in-house.
- No "7th established" language anywhere — the m=ω(n) gap REINFORCES that the linear story is
  evidence, not proof.
- Keep the abstract's claim split intact (theorem / evidence / conjecture).

## 6. Checklist

```text
[ ] 1a intro wording          [ ] 1b related-work wording     [ ] 1c barriers-intro wording
[ ] 1d B4 full replacement (kills the duplication)            [ ] 2 status-table rows
[ ] 3.1 w≠0 edge   [ ] 3.2 win-win sentence   [ ] 3.3 "answers select" phrasing
[ ] 4 meta/LPQR26-appendixD-quotes.md (thm/page-pinned)
[ ] tectonic clean build      [ ] commit: fix(LPQR scope): low-noise → m-regime (B-sharpened) ...
```

After this pass the LPQR attribution is source-faithful, the linear barrier is honestly split by
regime, and the SQ-bound front + barriers section are submission-grade. **No 7th; no break; no
security claim. OPEN = LSN.**
