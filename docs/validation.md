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

### POST /patients

| Field | Rules |
|---|---|
| firstName | required, string, 1–50 chars |
| lastName | required, string, 1–50 chars |
| dateOfBirth | required, date, YYYY-MM-DD format |
| gender | required, one of: Male, Female, Other |
| contactNumber | required, string, 11 digits, format 09XXXXXXXXX |
| address | required, string, 5–200 chars |

### PUT /patients/:id

| Field | Rules |
|---|---|
| firstName | optional, string, 1–50 chars |
| lastName | optional, string, 1–50 chars |
| dateOfBirth | optional, date, YYYY-MM-DD format |
| gender | optional, one of: Male, Female, Other |
| contactNumber | optional, string, 11 digits, format 09XXXXXXXXX |
| address | optional, string, 5–200 chars |

---

## Appointment Management

### POST /appointments

| Field | Rules |
|---|---|
| patientId | required, referential, must reference an existing patient |
| appointmentDate | required, date, YYYY-MM-DD format |
| appointmentTime | required, time, HH:MM format |
| service | required, string, 1–100 chars |
| status | required, one of: Scheduled, Completed, Cancelled |

### PUT /appointments/:id

| Field | Rules |
|---|---|
| patientId | optional, referential, must reference an existing patient |
| appointmentDate | optional, date, YYYY-MM-DD format |
| appointmentTime | optional, time, HH:MM format |
| service | optional, string, 1–100 chars |
| status | optional, one of: Scheduled, Completed, Cancelled |

---

## Medical Records

### POST /medical-records

| Field | Rules |
|---|---|
| patientId | required, referential, must reference an existing patient |
| diagnosis | required, string, 1–500 chars |
| treatment | required, string, 1–500 chars |
| recordDate | required, date, YYYY-MM-DD format |

### PUT /medical-records/:id

| Field | Rules |
|---|---|
| patientId | optional, referential, must reference an existing patient |
| diagnosis | optional, string, 1–500 chars |
| treatment | optional, string, 1–500 chars |
| recordDate | optional, date, YYYY-MM-DD format |

---

## Health Services

### POST /health-services

| Field | Rules |
|---|---|
| name | required, string, 1–100 chars |
| description | required, string, 1–500 chars |
| status | required, one of: Active, Inactive |

### PUT /health-services/:id

| Field | Rules |
|---|---|
| name | optional, string, 1–100 chars |
| description | optional, string, 1–500 chars |
| status | optional, one of: Active, Inactive |

---

## User Management

### POST /users

| Field | Rules |
|---|---|
| username | required, string, 3–50 chars |
| password | required, string, 8–100 chars |
| role | required, one of: Administrator, Staff |

### PUT /users/:id

| Field | Rules |
|---|---|
| username | optional, string, 3–50 chars |
| password | optional, string, 8–100 chars |
| role | optional, one of: Administrator, Staff |

---

# Standard Error Response

All validation failures use the same format:

```json
{
  "status": 422,
  "error": "field is invalid",
  "field": "field"
}
---

# Break-It Test Log

| Test | Expected Result | Actual Result |
|---|---|---|
| Missing required patient field | HTTP 422 | Pending |
| Invalid patient contact number | HTTP 422 | Pending |
| Invalid patient gender | HTTP 422 | Pending |
| Invalid appointment date | HTTP 422 | Pending |
| Invalid appointment status | HTTP 422 | Pending |
| Invalid medical record patientId | HTTP 422 | Pending |
| Invalid health service status | HTTP 422 | Pending |
| Invalid user role | HTTP 422 | Pending |
| Forbidden delete action | HTTP 403 | Pending |

## Break-It Testing Notes

- Invalid input must not create or update a record.
- Validation errors must use the standard error response.
- Validation failures must return HTTP 422.
- Forbidden actions must return HTTP 403.
- Actual results will be recorded after testing each route.
