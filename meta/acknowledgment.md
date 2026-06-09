# Acknowledgment of AI Assistance

## Claude (Anthropic)

Claude served as the primary intellectual sparring partner throughout the development of this work. Its concrete contributions included:

- **Conceptual Architecture**: Framed the LSN problem as a distinct post-quantum hardness family (the "7th family") and structured the paper around the theorem / barrier / construction narrative.
- **Mathematical Rigor**: Proposed the exact pairwise-correlation formula underlying the SQ lower bound, formalized the SDA concentration argument via Markov’s inequality, and insisted on claim classification (theorem / evidence / conjecture).
- **Cryptographic Engineering**: Designed the concatenated polar-code reconciliation scheme (repetition inner + polar outer), verified the $O(n^2)$ R1CS constraint count for the SNARK membership circuit, and caught a critical structural flaw in the original Fujisaki–Okamoto transform description.
- **Quality Assurance**: Identified the fatal `[Rei09]` citation error (a matrix-completion paper mis-cited as a quantum SQ result), flagged leaked internal notes (`OFA-390`), and prevented over-claims (e.g., the $n=36$ security-parameter correction).
- **Ethical Guardrails**: Enforced the honest-limitations section, ensured AI-disclosure compliance, and repeatedly demanded evidence-level justification before any claim could be upgraded to theorem status.

## Kimi (Moonshot AI)

Kimi assisted with:
- Codebase exploration and file-system archaeology across the migrated repositories.
- Systematic LaTeX auditing (cross-reference integrity, citation matching, numerical consistency checks).
- Background task management for long-running builds and verification scripts.

## Codex (OpenAI)

Codex is acknowledged for **future work**: the production Rust reference implementation, $N=2048$ Monte-Carlo validation, and known-answer test (KAT) vector generation, scheduled for completion in the next development sprint.

## Author Responsibility Statement

The author takes **full responsibility** for the accuracy, integrity, and final content of this work. All AI-generated suggestions were reviewed, verified by independent reasoning, and edited as needed. No AI system is listed as an author or co-author.

---

*This document supplements the Acknowledgements section of the paper (`lsn-paper.tex`).*
