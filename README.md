# lsn-pq

**The Lagrangian Subspace Noise Problem: A New Framework for Post-Quantum Cryptography**

Author: Kwanghoo Choo (ORCID [0009-0005-5682-8098](https://orcid.org/0009-0005-5682-8098))

LSN is a *candidate* new post-quantum hardness assumption: an LPN variant whose secret is a
Lagrangian subspace of a symplectic vector space over F₂. This repository contains the paper,
all verification experiments, and the complete research/adjudication record.

## Claims posture (read this first)

Every claim in the paper is classified as **theorem / evidence / conjecture**.
In particular: no "7th family" is claimed as proven; LSN hardness is an OPEN assumption
supported by SQ lower bounds and a near-complete linear-reduction barrier landscape
(three of four cells closed unconditionally; the fourth — marginal-adaptive — is a
precisely-stated open problem). No production-security claim is made.

## Paper

- `paper/lsn-paper.tex` / `paper/lsn-paper.pdf` — **English, canonical**
- `paper/lsn-paper-ko.tex` / `paper/lsn-paper-ko.pdf` — Korean reading edition
  (저자 통독용 번역판; 불일치 시 영어판이 우선)

Build with [Tectonic](https://tectonic-typesetting.github.io/):

```bash
cd paper && tectonic lsn-paper.tex
```

(The Korean edition additionally requires the macOS system font "Apple SD Gothic Neo".)

## Repository structure

```
paper/           LaTeX sources and PDFs (EN canonical + KO reading edition)
experiments/     Numbered Python verification scripts + result JSONs.
                 Every numerical claim in the paper has a reproducing script here.
meta/            Research record: source-accuracy pins (verbatim quotes of cited
                 theorems with page numbers), adjudication reports, research
                 directives, and dated decision documents.
kat/             Known-answer test vectors
test_vectors/    Additional test vectors
```

The `meta/` directory is the project's audit trail: external citations are pinned verbatim
(e.g. `meta/LPQR26-appendixD-quotes.md`), and every result went through independent
re-derivation before entering the paper (`meta/2026-06-10-CLAUDE-*` adjudication files).

## Status

- Paper: **preprint-ready** (v1); arXiv / IACR ePrint submission pending.
- Open research: the marginal-adaptive corner of the linear-reduction landscape
  (Open Problem 9) and the membership↔stabilizer-decoding bridge (Open Problem 8).
- Implementation: Python prototypes validate parameters and algorithms; a production
  constant-time Rust implementation with full N=2048 validation and KAT generation is planned.

## License

TBD (to be decided before public release announcement).
