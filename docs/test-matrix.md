# Deliverable 4 — QA Test Matrix

> **Execution note:** The matrix is the required QA plan/evidence template. Automated tests must be run in the contributor's environment/CI before claiming a passing result. No live production URL is claimed by this repository change.

| ID | Area | Test | Expected result | Automated | Status |
|---|---|---|---|---|---|
| QA-01 | Patients | Create valid patient | 201 and patient returned | Yes | Ready to run |
| QA-02 | Patients | Read list/detail | 200 and correct data | Yes | Ready to run |
| QA-03 | Patients | Update valid patient | 200 and changed data | Yes | Ready to run |
| QA-04 | Patients | Delete patient | 200 then 404 on detail | Yes | Ready to run |
| QA-05 | Patients | Missing required field | 422 with field error | Yes | Ready to run |
| QA-06 | Patients | Invalid phone | 422 | Yes | Ready to run |
| QA-07 | Appointments | Full CRUD | Create/read/update/delete work | Yes | Ready to run |
| QA-08 | Appointments | Unknown patient | 422 | Yes | Ready to run |
| QA-09 | Appointments | Invalid status | 422 | Yes | Ready to run |
| QA-10 | Medical records | Full CRUD | Create/read/update/delete work | Yes | Ready to run |
| QA-11 | Medical records | Empty diagnosis | 422 | Yes | Ready to run |
| QA-12 | Health services | Full CRUD | Create/read/update/delete work | Yes | Ready to run |
| QA-13 | Health services | Invalid status | 422 | Yes | Ready to run |
| QA-14 | Users | Full CRUD | Create/read/update/delete work | Yes | Ready to run |
| QA-15 | Users | Non-admin delete | 403 | Yes | Ready to run |
| QA-16 | Routing | Unknown URL | 404 | Yes | Ready to run |
| QA-17 | UI | List loading state | Loading message is visible while request is pending | Manual | Pending manual QA |
| QA-18 | UI | Empty state | User receives clear next action | Manual | Pending manual QA |
| QA-19 | UI | Network failure | Human-readable error + Retry | Manual | Pending manual QA |
| QA-20 | UI | 422 feedback | Error appears beside affected field | Manual | Pending manual QA |
| QA-21 | UI | Delete confirmation | Destructive action requires confirmation | Manual | Pending manual QA |
| QA-22 | Production | Public HTTPS URL | App loads outside localhost | Manual | Deployment required |
| QA-23 | Production | Production CRUD | CRUD works on deployed environment | Manual | Deployment required |
| QA-24 | Production | Failure handling | Bad input produces visible error, not crash | Manual | Deployment required |

## Commands

Run the automated suite:

`python -m unittest discover -s tests -p "test_*.py" -v`

For the final submission, replace "Ready to run" with the actual result and record the CI run/commit that produced it.
