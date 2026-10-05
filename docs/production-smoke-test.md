# Production Smoke Test — Railway

Run these checks against the public deployment after every release candidate.

Public URL:

https://web-production-64a9f1.up.railway.app

## Prerequisites

Use an Administrator account. Do not record or commit its password.

## Test flow

| ID | Action | Expected result | Evidence |
|---|---|---|---|
| PROD-01 | Open the public HTTPS URL | Login page loads without an application error | Screenshot |
| PROD-02 | Log in with a valid Administrator account | Dashboard opens | Screenshot |
| PROD-03 | Create a patient with valid data | Success feedback appears and patient is listed | Screenshot |
| PROD-04 | Open the patient's detail/edit flow | Existing patient data is displayed | Screenshot |
| PROD-05 | Update the patient | Updated values persist after refresh | Screenshot |
| PROD-06 | Delete the test patient | Confirmation is shown; patient is removed | Screenshot |
| PROD-07 | Create an appointment for an existing patient | Appointment is saved and listed | Screenshot |
| PROD-08 | Update/delete the appointment | Changes persist; deletion is confirmed | Screenshot |
| PROD-09 | Create a medical record for an existing patient | Record is saved and listed | Screenshot |
| PROD-10 | Update/delete the record | Changes persist; deletion is confirmed | Screenshot |
| PROD-11 | View health services | Service list loads | Screenshot |
| PROD-12 | Create/update/delete a service as Administrator | Mutation succeeds with feedback | Screenshot |
| PROD-13 | Open user management as Administrator | Users load | Screenshot |
| PROD-14 | Submit invalid patient data | Visible 422-style validation feedback; no crash | Screenshot |
| PROD-15 | Open a missing record | Clear not-found message is shown | Screenshot |
| PROD-16 | Trigger/observe a recoverable network/server failure | Human-readable error and retry where safe | Screenshot |
| PROD-17 | Refresh after changes | Data remains persisted in Railway MySQL | Screenshot |

## Test record

Record the date/time, tester, and result for each executed case. Only mark a case PASS after direct observation.

## Release gate

Deliverable 4 is not fully signed off until the production CRUD and failure-path checks above are actually completed, the final automated test suite is green, and the evidence is retained for the presentation.
