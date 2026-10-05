# Week 10 / Deliverable 4 — QA Test Matrix

> This matrix is the release QA checklist. Do not mark a manual or production test PASS until it has actually been executed and recorded.

## Scenario legend
- **Happy** — valid expected use
- **Boundary** — minimum/maximum valid values
- **Invalid** — malformed or rejected input
- **Empty** — required values omitted
- **Permissions** — authorization-sensitive action

| Feature | Happy | Boundary | Invalid | Empty | Permissions |
|---|---|---|---|---|---|
| Patient list/detail | List and detail load | Empty collection shows empty state | Missing ID returns 404 | Empty state renders | Auth required |
| Patient create | Valid payload returns 201 | Field limits are validated | Invalid field returns 422 | Missing required field returns 422 | Auth required |
| Patient update | Valid update returns 200 | Supported field lengths validated | Invalid field returns 422 | No-update payload returns 422 | Auth required |
| Patient delete | Existing patient can be deleted | Delete last remaining record | Unknown ID returns 404 | N/A | Auth required |
| Appointment list/detail | List and detail load | Supported date/time values | Unknown ID/invalid status returns 404/422 | Empty state | Auth required |
| Appointment create/update/delete | CRUD works | Required fields validated | Invalid patient/date/status rejected | Required fields rejected | Auth required |
| Medical record list/detail | List and detail load | Text/date limits validated | Invalid patient/date/text rejected | Required fields rejected | Auth required |
| Medical record create/update/delete | CRUD works | Supported lengths | Invalid values return 422 | Required fields rejected | Auth required |
| Health service list/detail | List and detail load | Name/description limits validated | Invalid status/text rejected | Required fields rejected | Administrator for mutations |
| User list/detail | List and detail load | Username/password limits validated | Invalid role/credentials rejected | Required fields rejected | Administrator-sensitive mutations |
| Authentication | Valid login succeeds | N/A | Invalid credentials return 401 | Empty credentials rejected | Protected routes require auth |

## Expanded automated QA

| ID | Area | Test | Expected result | Status |
|---|---|---|---|---|
| QA-01 | Patients | Full CRUD including detail GET | Create/read/update/delete work | CI |
| QA-02 | Patients | Missing required field | 422 with field error | CI |
| QA-03 | Patients | Invalid phone/date | 422 | CI |
| QA-04 | Appointments | Create/read/update | 201/200 | CI |
| QA-05 | Appointments | Unknown patient | 422 | CI |
| QA-06 | Appointments | Invalid status | 422 | CI |
| QA-07 | Medical records | Create/read/update | 201/200 | CI |
| QA-08 | Medical records | Empty diagnosis | 422 | CI |
| QA-09 | Health services | Create/read/update | 201/200 | CI |
| QA-10 | Health services | Invalid status | 422 | CI |
| QA-11 | Users | Create/read/update | 201/200 | CI |
| QA-12 | Users | Non-admin delete | 403 | CI |
| QA-13 | Routing | Unknown record | 404 | CI |

## Adversarial/manual session

| Scenario | Expected result | Status |
|---|---|---|
| Huge numeric/string input | Validation prevents unsafe/invalid data | Manual verification |
| Emoji/unusual text | Valid text is handled and rendered safely | Manual verification |
| Script-like input | Rendered values are escaped | Manual verification |
| Double-click submit | Submit button is disabled while pending | Manual verification |
| Refresh/back during request | No corrupted UI state | Manual verification |
| Direct URL to missing record | Clear 404 feedback | Manual verification |
| Act on deleted record | Update/delete returns 404 | Manual verification |
| Network off/slow | Retry and connection feedback | Manual verification |

## Production release checks

| ID | Test | Expected result | Status |
|---|---|---|---|
| QA-14 | Public HTTPS URL | App loads outside localhost | ✅ Verified |
| QA-15 | Production login/dashboard | Login succeeds and dashboard opens | ✅ Verified |
| QA-16 | Production CRUD | CRUD works end to end | ⬜ Requires manual smoke test |
| QA-17 | Production bad input | Visible error, no crash | ⬜ Requires manual smoke test |
| QA-18 | Production missing record | Clear 404/not-found behavior | ⬜ Requires manual smoke test |
| QA-19 | Production failure/retry | Human-readable failure + retry where safe | ⬜ Requires manual smoke test |
| QA-20 | Backup demo | Screenshots/recording available | ⬜ Preparation required |

## Automated command

`python -m unittest discover -s tests -p "test_*.py" -v`

Automated cases should only be considered PASS after the corresponding CI/local run completes successfully.
