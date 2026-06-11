# Codex v2 Paper Build Verification

**Date:** 2026-06-11
**Actor:** Codex
**Target commit:** `b3ff6f0e53c0b5c163f38f4ac02faeb3463579b0`
**Scope:** English canonical paper, `paper/lsn-paper.tex`
**Discipline:** Build verification only. No 7th; no break; no security claim. OPEN = LSN.

## Context

The local `main` branch contained the v2 paper integration commit:

```text
b3ff6f0 v2(paper): Krawtchouk appendix + L1 N=2048 update + cryptanalysis(ISD/BKW/ML) + OP9 sharpened + cref fixes
```

Codex pushed this commit to `origin/main` and then reproduced the CI paper build locally using the
same engine named in `.github/workflows/latex.yml`.

## Command

```bash
cd paper
tectonic lsn-paper.tex
```

## Result

The build completed successfully and regenerated `paper/lsn-paper.pdf`.

Warnings observed:

```text
warning: lsn-paper.tex:953: Overfull \hbox (44.4614pt too wide) in paragraph at lines 951--953
warning: lsn-paper.tex:1618: Underfull \hbox (badness 1237) in paragraph at lines 1615--1618
```

No fatal LaTeX error, undefined control sequence, unresolved `\Cref` failure, or missing macro error
was observed. Tectonic wrote:

```text
Writing `lsn-paper.pdf` (301.009765625 KiB)
```

## Adjudication

- **Build status:** GREEN for the English canonical paper.
- **PDF regenerated:** yes.
- **Warnings blocking v2:** no; layout warnings only.
- **Claims status:** unchanged. This is a build-verification artifact, not new mathematical evidence.
