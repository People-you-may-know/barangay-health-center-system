# Week 10 — Manual QA Test Matrix

> Feature freeze: this QA pass records failures and does not fix discovered bugs.

## Scenario legend
- **Happy** — valid expected use
- **Boundary** — minimum/maximum valid values
- **Invalid** — malformed or rejected input
- **Empty** — required values omitted
- **Permissions** — authorization-sensitive action

| Feature | Happy | Boundary | Invalid | Empty | Permissions |
|---|---|---|---|---|---|
| Patient list | PASS — GET /patients returns data | PASS — empty collection has an empty state | PASS — non-2xx response has visible feedback | PASS — empty state renders | N/A |
| Patient create | PASS — valid payload returns 201 | PASS — field limits are validated | PASS — invalid field returns 422 | PASS — missing required field returns 422 | N/A |
| Patient read | PASS — existing patient returns 200 | PASS — integer route ID is accepted | PASS — unknown ID returns 404 | N/A | N/A |
| Patient update | PASS — valid update returns 200 | PASS — supported field lengths are validated | PASS — invalid field returns 422 | PASS — partial update is supported | N/A |
| Patient delete | PASS — existing patient can be deleted | PASS — delete last remaining record | PASS — unknown ID returns 404 | N/A | N/A |
| Appointment API | PASS — valid appointment path exists | PASS — required fields have validation | PASS — invalid patient/date/status is rejected | PASS — required fields are rejected | N/A |
| Medical records API | PASS — valid record path exists | PASS — text/date limits are validated | PASS — invalid patient/date/text is rejected | PASS — required fields are rejected | N/A |
| Health services API | PASS — valid service path exists | PASS — name/description limits are validated | PASS — invalid status/text is rejected | PASS — required fields are rejected | N/A |
| User API | PASS — valid user path exists | PASS — username/password limits are validated | PASS — invalid role/credentials are rejected | PASS — required fields are rejected | PASS — DELETE requires Administrator |
| Patient date validation | FAIL — a value such as 2026-99-99 has length 10 but is not a real date | FAIL — invalid month/day values are not rejected by length-only validation | FAIL — malformed calendar dates can reach storage | N/A | N/A |

## Adversarial session checklist

| Scenario | Result |
|---|---|
| Huge numeric/string input | Backend length validation and frontend limits reviewed |
| Emoji/unusual text | String validation and HTML escaping reviewed |
| Script-like input | Patient list escapes rendered values |
| Double-click submit | Submit button is disabled while request is pending |
| Refresh/back during request | Manual browser verification required |
| Direct URL to missing patient | 404 feedback is implemented |
| Act on deleted patient | DELETE/UPDATE return 404 |
| Network off/slow | Retry and connection feedback are implemented |

## QA status

The matrix is prepared from the current application behavior and the Week 10 adversarial checklist. Browser-based manual execution still needs to be performed by the team and recorded here before final sign-off.
