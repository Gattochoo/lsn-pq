# lsn-pq

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20646796.svg)](https://doi.org/10.5281/zenodo.20646796)

**The Lagrangian Subspace Noise (LSN) Problem**

Author: Kwanghoo Choo (ORCID [0009-0005-5682-8098](https://orcid.org/0009-0005-5682-8098))

LSN is a *candidate* new post-quantum hardness assumption: an LPN variant whose secret is a
Lagrangian subspace of a symplectic vector space over F₂. This repository contains the papers,
all verification experiments, and the complete research/adjudication record.

**Papers** (in `paper/`):
- `lsn-core.pdf` — *The Lagrangian Subspace Noise Problem: Statistical-Query Lower Bounds and
  Barriers for Linear Reductions* (the core mathematical paper, 31 pp).
- `lsn-paper.pdf` — companion technical report including cryptographic constructions
  (KEM, succinct arguments).

**Cite this archive** (all versions, always resolves to the latest): DOI [10.5281/zenodo.20646796](https://doi.org/10.5281/zenodo.20646796).
The current snapshot (v2.1, the submitted bibliography-audited paper) is DOI [10.5281/zenodo.20665389](https://doi.org/10.5281/zenodo.20665389).

## Claims posture (read this first)

Every claim in the paper is classified as **theorem / evidence / conjecture**.
In particular: no "7th family" is claimed as proven; LSN hardness is an OPEN assumption
supported by SQ lower bounds and a near-complete linear-reduction barrier landscape
(three of four cells closed unconditionally; the fourth — marginal-adaptive — is a
precisely-stated open problem). No production-security claim is made.

## Building

Build with [Tectonic](https://tectonic-typesetting.github.io/):

```bash
cd paper
tectonic lsn-core.tex   # core paper (submitted to IACR ePrint)
tectonic lsn-paper.tex  # companion technical report (constructions)
```

## Repository structure

```
paper/           LaTeX sources and PDFs (lsn-core = submitted core paper;
                 lsn-paper = companion technical report).
experiments/     Numbered Python verification scripts + result JSONs.
                 Every numerical claim in the paper has a reproducing script here.
impl/            Rust crates: lsn_ref (reference scaffold + KAT), lsn_cryptanalysis
                 (attack screens), polar_validation (polar-code decoder validation).
meta/            Research record: source-accuracy pins (verbatim quotes of cited
                 theorems with page numbers), adjudication reports, research
                 directives, and dated decision documents.
docs/            Design and planning documents.
```

The `meta/` directory is the project's audit trail: external citations are pinned verbatim
(e.g. `meta/LPQR26-appendixD-quotes.md`), and every result went through independent
re-derivation before entering the paper (`meta/2026-06-10-CLAUDE-*` adjudication files).

## Status

- Paper: the core paper (`lsn-core.pdf`) has been submitted to the IACR Cryptology ePrint
  Archive. arXiv submission pending.
- Open research: the marginal-adaptive corner of the linear-reduction landscape, and the
  membership↔stabilizer-decoding bridge. Both are stated as open problems in the paper,
  with named obstructions that block the natural maps but do **not** constitute
  impossibility results.
- Implementation: Python prototypes validate parameters and algorithms; Rust reference
  implementations (`impl/lsn_ref/`, `impl/lsn_cryptanalysis/`, `impl/polar_validation/`)
  are active. A production constant-time Rust implementation with full N=2048 validation
  and KAT generation is in progress.

## License

Dual-licensed:

- **Code** (`experiments/`, `impl/`, and future implementations): [Apache License 2.0](LICENSE) — permissive, with an explicit patent grant and retaliation clause.
- **Documents** (`paper/`, `meta/`, this README): [CC BY 4.0](LICENSE-docs) — free to share and adapt with attribution.

See `NOTICE` for the attribution line. No patents are or will be sought on the LSN constructions by the author; the scheme is offered royalty-free to maximize community analysis and adoption.
