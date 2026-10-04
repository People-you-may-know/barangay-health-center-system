# Week 10 — QA Bug Log

## BUG-001 — Invalid calendar dates can pass date validation

**Severity:** P1 — significant data-integrity problem with a workaround.  
**Status:** Open — intentionally not fixed during Week 10 feature freeze.  
**Area:** Patient creation/update

### Steps to reproduce
1. Open the patient create form or send a POST request to /patients.
2. Submit a patient with a date such as 2026-99-99.
3. Observe the API validation behavior.

### Expected
The API should reject a date that is not a real calendar date and return a 422 validation response.

### Actual
The current backend checks that the date is a string of length 10, but does not validate whether the month/day combination is an actual calendar date.

### Impact
Invalid patient dates can enter the in-memory data store, reducing data quality.

### Next action
Fix date parsing/validation in the Week 11 bug-fix cycle. Do not fix it in the Week 10 feature-freeze branch.

## QA note
This finding was identified from the adversarial invalid-input scenario and current backend validation logic. Browser/manual execution should be repeated by the team and the observed result added to the reproduction record.
