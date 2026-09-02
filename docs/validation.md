# Validation Matrix

## Team Members

| Name | Role |
|---|---|
| Jeandy Lou Pactul | Repo Lead |
| Jechele Ane Munez | Board Lead |
| Mary Cajenta | Scribe |
| Hanna Evangelista | Builder |
| Angelica Aninon | Builder |

## Patient Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /patients | firstName | required | string | 1–50 chars | letters and spaces | — | — |
| POST /patients | lastName | required | string | 1–50 chars | letters and spaces | — | — |
| POST /patients | dateOfBirth | required | date | — | YYYY-MM-DD | — | — |
| POST /patients | gender | required | string | — | — | Male, Female, Other | — |
| POST /patients | contactNumber | required | string | 11 digits | 09XXXXXXXXX | — | — |
| POST /patients | address | required | string | 5–200 chars | plain text | — | — |
| PUT /patients/:id | firstName | required | string | 1–50 chars | letters and spaces | — | — |
| PUT /patients/:id | lastName | required | string | 1–50 chars | letters and spaces | — | — |
| PUT /patients/:id | dateOfBirth | required | date | — | YYYY-MM-DD | — | — |
| PUT /patients/:id | gender | required | string | — | — | Male, Female, Other | — |
| PUT /patients/:id | contactNumber | required | string | 11 digits | 09XXXXXXXXX | — | — |
| PUT /patients/:id | address | required | string | 5–200 chars | plain text | — | — |

## Appointment Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /appointments | patientId | required | string | — | valid patient ID | — | must reference existing patient |
| POST /appointments | appointmentDate | required | date | — | YYYY-MM-DD | — | — |
| POST /appointments | appointmentTime | required | string | — | HH:MM | — | — |
| POST /appointments | service | required | string | 1–100 chars | letters and spaces | — | — |
| POST /appointments | status | required | string | — | — | Scheduled, Completed, Cancelled | — |
| PUT /appointments/:id | patientId | required | string | — | valid patient ID | — | must reference existing patient |
| PUT /appointments/:id | appointmentDate | required | date | — | YYYY-MM-DD | — | — |
| PUT /appointments/:id | appointmentTime | required | string | — | HH:MM | — | — |
| PUT /appointments/:id | service | required | string | 1–100 chars | letters and spaces | — | — |
| PUT /appointments/:id | status | required | string | — | — | Scheduled, Completed, Cancelled | — |

## Medical Records

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /medical-records | patientId | required | string | — | valid patient ID | — | must reference existing patient |
| POST /medical-records | diagnosis | required | string | 1–500 chars | plain text | — | — |
| POST /medical-records | treatment | required | string | 1–500 chars | plain text | — | — |
| POST /medical-records | prescription | optional | string | 0–500 chars | plain text | — | — |
| PUT /medical-records/:id | patientId | required | string | — | valid patient ID | — | must reference existing patient |
| PUT /medical-records/:id | diagnosis | required | string | 1–500 chars | plain text | — | — |
| PUT /medical-records/:id | treatment | required | string | 1–500 chars | plain text | — | — |
| PUT /medical-records/:id | prescription | optional | string | 0–500 chars | plain text | — | — |

## Health Services

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /health-services | serviceName | required | string | 1–100 chars | letters and spaces | — | — |
| POST /health-services | description | required | string | 1–500 chars | plain text | — | — |
| POST /health-services | availability | required | string | — | — | Available, Unavailable | — |
| PUT /health-services/:id | serviceName | required | string | 1–100 chars | letters and spaces | — | — |
| PUT /health-services/:id | description | required | string | 1–500 chars | plain text | — | — |
| PUT /health-services/:id | availability | required | string | — | — | Available, Unavailable | — |

## User Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /users | username | required | string | 3–50 chars | letters, numbers, underscore | — | — |
| POST /users | password | required | string | 8–100 chars | — | — | — |
| POST /users | fullName | required | string | 1–100 chars | letters and spaces | — | — |
| POST /users | role | required | string | — | — | Admin, Staff | — |
| PUT /users/:id | username | required | string | 3–50 chars | letters, numbers, underscore | — | — |
| PUT /users/:id | password | optional | string | 8–100 chars | — | — | — |
| PUT /users/:id | fullName | required | string | 1–100 chars | letters and spaces | — | — |
| PUT /users/:id | role | required | string | — | — | Admin, Staff | — |

## Standard Error Shape

All validation errors use the same format:

{
  "status": 422,
  "error": "human-readable message",
  "field": "field name"
}

## Authorization

Sensitive actions must check whether the current user has permission.

For this system, deleting a patient record is a sensitive action.

Forbidden actions return:

403

Example authorization response:

{
  "status": 403,
  "error": "not allowed",
  "field": "authorization"
}

Validation failures return:

422

## Break-It Test Log

| Test | Route | Bad Input/Action | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | POST /patients | Missing firstName | 422 | To be tested | PENDING |
| 2 | POST /patients | Wrong type for contactNumber | 422 | To be tested | PENDING |
| 3 | POST /patients | Invalid date format | 422 | To be tested | PENDING |
| 4 | POST /patients | Invalid gender value | 422 | To be tested | PENDING |
| 5 | DELETE /patients/:id | Unauthorized deletion | 403 | To be tested | PENDING |



