# Validation Matrix

## Patient Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /patients | firstName | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| POST /patients | lastName | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| POST /patients | dateOfBirth | [your rule] | [your rule] | — | [your rule] | — | — |
| POST /patients | gender | [your rule] | [your rule] | — | — | [your values] | — |
| POST /patients | contactNumber | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| POST /patients | address | [your rule] | [your rule] | [your rule] | — | — | — |
| PUT /patients/:id | firstName | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| PUT /patients/:id | lastName | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| PUT /patients/:id | dateOfBirth | [your rule] | [your rule] | — | [your rule] | — | — |
| PUT /patients/:id | gender | [your rule] | [your rule] | — | — | [your values] | — |
| PUT /patients/:id | contactNumber | [your rule] | [your rule] | [your rule] | [your rule] | — | — |
| PUT /patients/:id | address | [your rule] | [your rule] | [your rule] | — | — | — |

## Appointment Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /appointments | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |
| PUT /appointments/:id | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |

## Medical Records

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /medical-records | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |
| PUT /medical-records/:id | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |

## Health Services

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /health-services | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |
| PUT /health-services/:id | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |

## User Management

| Route | Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|---|
| POST /users | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |
| PUT /users/:id | [field] | [rule] | [rule] | [rule] | [rule] | [rule] | [rule] |

## Standard Error Shape

All validation errors should use the team's agreed format.

Example structure:

{
  "status": 422,
  "error": "[human-readable message]",
  "field": "[field name]"
}

## Authorization

Sensitive actions must check whether the current user has permission.

Forbidden actions return:

403

Validation failures return:

422

## Break-It Test Log

| Test | Route | Bad Input/Action | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | [route] | Missing required field | 422 | [actual] | [PASS/FAIL] |
| 2 | [route] | Wrong type | 422 | [actual] | [PASS/FAIL] |
| 3 | [route] | Out-of-range value | 422 | [actual] | [PASS/FAIL] |
| 4 | [route] | Invalid allowed value | 422 | [actual] | [PASS/FAIL] |
| 5 | [route] | Forbidden action | 403 | [actual] | [PASS/FAIL] |

