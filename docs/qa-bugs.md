# Week 10 — QA Bug Log

## BUG-001 — Invalid calendar dates can pass date validation

**Severity:** P1 — significant data-integrity problem with a workaround.  
**Status:** Fixed in Week 11 branch; pending reviewed PR/merge.  
**Area:** Patient creation/update

### Steps to reproduce
1. Open the patient create form or send a POST request to /patients.
2. Submit a patient with a date such as 2026-99-99.
3. Observe the API validation behavior.

### Expected
The API should reject a date that is not a real calendar date and return a 422 validation response.

### Actual (Week 10)
The backend checked only that the date was a string of length 10, so an impossible month/day combination could be accepted.

### Week 11 fix
The API now parses the value as a real YYYY-MM-DD calendar date. Impossible dates return HTTP 422.

### Impact
Invalid patient dates can enter the in-memory data store, reducing data quality.

### Next action
Fixed by validating the value with real YYYY-MM-DD calendar parsing. The change is covered by automated tests for impossible dates and leap-year behavior.

## QA note
This finding was identified from the adversarial invalid-input scenario and current backend validation logic. Browser/manual execution should be repeated by the team and the observed result added to the reproduction record.
