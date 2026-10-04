# Week 9 AI Notes

## AI-generated prompts

- Review the Barangay Health Center patient API for edge cases and correctness problems.
- Find a realistic bug in the patient ID generation logic and propose a minimal safe fix.
- Generate focused tests for 201 create, 422 validation, 404 not-found, update failure, and ID uniqueness after deletion.
- Review Week 8 error handling against the Week 9 checklist for silent failures, destructive actions, and technical messages.

## Hand-written review

- The patient API uses standardized JSON responses with status, data/error, and field information for validation failures.
- The original `len(patients) + 1` ID logic can reuse an existing ID after deletion. This was treated as a blocking correctness issue and fixed.
- The Week 8 feedback implementation already addresses 422, 404, server/network failures, retry, loading states, and delete confirmation.
- The new tests focus on the patient API paths most relevant to the review findings.

## Review labels

- **Blocking:** duplicate IDs, silent failures, unsafe destructive actions, technical errors exposed to users.
- **Nit:** wording or formatting improvements that do not affect correctness.

## Peer review requirement

This branch is intended to be reviewed by a teammate before merge. The Week 9 lab requires a substantive review comment and an approving review before merge.
