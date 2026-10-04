# Week 10 / Deliverable 4 — QA Test Matrix

> This matrix combines the existing Week 10 QA evidence with the expanded Deliverable 4 release checks. Automated results should only be marked PASS after the suite is actually run.

## Scenario legend
- **Happy** — valid expected use
- **Boundary** — minimum/maximum valid values
- **Invalid** — malformed or rejected input
- **Empty** — required values omitted
- **Permissions** — authorization-sensitive action

| Feature | Happy | Boundary | Invalid | Empty | Permissions |
|---|---|---|---|---|---|
| Patient list | GET /patients returns data | Empty collection has an empty state | Non-2xx response has visible feedback | Empty state renders | N/A |
| Patient create | Valid payload returns 201 | Field limits are validated | Invalid field returns 422 | Missing required field returns 422 | N/A |
| Patient read | Existing patient returns 200 | Integer route ID accepted | Unknown ID returns 404 | N/A | N/A |
| Patient update | Valid update returns 200 | Supported field lengths validated | Invalid field returns 422 | Partial update supported | N/A |
| Patient delete | Existing patient can be deleted | Delete last remaining record | Unknown ID returns 404 | N/A | N/A |
| Appointment API | Valid appointment path works | Required fields validated | Invalid patient/date/status rejected | Required fields rejected | N/A |
| Medical records API | Valid record path works | Text/date limits validated | Invalid patient/date/text rejected | Required fields rejected | N/A |
| Health services API | Valid service path works | Name/description limits validated | Invalid status/text rejected | Required fields rejected | N/A |
| User API | Valid user path works | Username/password limits validated | Invalid role/credentials rejected | Required fields rejected | DELETE requires Administrator |
| Patient date validation | Valid dates accepted | Leap-day/month-length rules enforced | Impossible dates return 422 | N/A | N/A |

## Expanded automated QA

| ID | Area | Test | Expected result | Status |
|---|---|---|---|---|
| QA-01 | Patients | Full CRUD | Create/read/update/delete work | Run required |
| QA-02 | Patients | Missing required field | 422 with field error | Run required |
| QA-03 | Patients | Invalid phone | 422 | Run required |
| QA-04 | Appointments | Full CRUD | Create/read/update/delete work | Run required |
| QA-05 | Appointments | Unknown patient | 422 | Run required |
| QA-06 | Appointments | Invalid status | 422 | Run required |
| QA-07 | Medical records | Full CRUD | Create/read/update/delete work | Run required |
| QA-08 | Medical records | Empty diagnosis | 422 | Run required |
| QA-09 | Health services | Full CRUD | Create/read/update/delete work | Run required |
| QA-10 | Health services | Invalid status | 422 | Run required |
| QA-11 | Users | Full CRUD | Create/read/update/delete work | Run required |
| QA-12 | Users | Non-admin delete | 403 | Run required |
| QA-13 | Routing | Unknown URL | 404 | Run required |

## Adversarial/manual session checklist

| Scenario | Expected result | Status |
|---|---|---|
| Huge numeric/string input | Backend length validation and frontend limits reviewed | Manual QA |
| Emoji/unusual text | String validation and HTML escaping reviewed | Manual QA |
| Script-like input | Rendered values are escaped | Manual QA |
| Double-click submit | Submit button disabled while request is pending | Manual QA |
| Refresh/back during request | No corrupted UI state | Manual QA |
| Direct URL to missing patient | 404 feedback | Manual QA |
| Act on deleted patient | DELETE/UPDATE return 404 | Manual QA |
| Network off/slow | Retry and connection feedback | Manual QA |

## Week 11 date verification

- Impossible date: `2026-99-99` → expected 422.
- Non-leap-year February 29: `2025-02-29` → expected 422.
- Valid leap day: `2024-02-29` → expected 201.
- Production debug setting is controlled by `APP_DEBUG` and should be false on the host.

## Production release checks

| ID | Test | Expected result | Status |
|---|---|---|---|
| QA-14 | Public HTTPS URL | App loads outside localhost | Deployment required |
| QA-15 | Production CRUD | CRUD works end to end | Deployment required |
| QA-16 | Production bad input | Visible error, no crash | Deployment required |
| QA-17 | Production failure/retry | Human-readable failure and retry | Deployment required |
| QA-18 | Backup demo | Local/screenshots/recording available | Preparation required |

## Automated command

`python -m unittest discover -s tests -p "test_*.py" -v`

Do not label automated cases as PASS until the command or CI run has actually completed successfully.
