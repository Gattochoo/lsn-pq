# CODEX OFA: Top-L Domain Labels

Date: 2026-06-12

Scope:
- Added `FixedScheduleTopLSelectionDomainFailureLabel`.
- Added `FIXED_TOP_L_SELECTION_DOMAIN_FAILURE_LABELS`.
- Added `fixed_top_l_selection_domain_failure_label`.
- The SCL work-shape audit JSON now records `top_l_selection_domain_failure_codes`.

Discipline:
- This is an audit-only/source-level prototype surface.
- It is not wired into `decode_scl`.
- The active decoder remains `not_constant_time`.
- This does not support a security, constant-time, PQ, or 7th-source claim.

Verification target:
- RED: `fixed_top_l_selection_domain_failure_labels_cover_public_codes` initially failed on missing label API.
- GREEN: top-L selection domain codes now expose stable public labels, including unknown-code fallback.
