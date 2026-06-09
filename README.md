# lsn-pq

**Lagrangian Subspace Noise (LSN): A New Framework for Post-Quantum Cryptography**

Author: Kwanghoo Choo

## Paper

- `paper/lsn-paper.tex` — Main LaTeX source (21 pages)
- `paper/lsn-paper.pdf` — Compiled PDF

## Repository Structure

```
paper/           LaTeX source and PDF
experiments/     Python prototypes for parameter validation
kat/             Known-answer test vectors
test_vectors/    Additional test vectors
```

## Build

The paper builds with [Tectonic](https://tectonic-typesetting.github.io/):

```bash
cd paper
tectonic lsn-paper.tex
```

## Status

Work in progress. A production Rust reference implementation and N=2048 empirical validation are planned.

## License

TBD
