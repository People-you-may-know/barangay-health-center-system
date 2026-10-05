# Deliverable 4 — Final Presentation & Live Demo

The course handout requires the presentation to follow **problem → solution → architecture → demo → lessons** and include a live demo.

## Slide 1 — Title
**Barangay Health Center Patient Record and Appointment Management System**

- Team members
- Course/section
- Deliverable 4

## Slide 2 — Problem
- Paper/manual patient records can be difficult to retrieve.
- Manual appointment handling can cause delays and conflicts.
- Staff need organized patient, appointment, medical record, service, and user information.

## Slide 3 — Solution
- Web-based CRUD system
- Patient management
- Appointment scheduling
- Medical records
- Health services
- User management
- Validation and user-friendly failure feedback

## Slide 4 — Architecture
Show:

**Browser/UI → Flask routes/controllers → validation → MySQL database → JSON response → UI feedback**

Explain:
- HTML/CSS provides the interface.
- JavaScript uses Fetch API for asynchronous CRUD.
- Flask validates requests and handles database operations.
- MySQL stores users, patients, appointments, medical records, and health services.
- Automated tests exercise backend behavior.
- Railway hosts the production web application and MySQL service.

## Slide 5 — QA Strategy
- Automated CRUD tests
- Validation/422 tests
- 404 not-found tests
- 403 authorization test
- Manual loading/empty/error/network tests
- Production smoke tests
- Bug triage and P0/P1 release gate

## Slide 6 — Live Demo
Use the deployed public URL:

**https://web-production-64a9f1.up.railway.app**

Recommended sequence:
1. Sign in.
2. Create patient.
3. Show patient in list.
4. Edit patient.
5. Delete patient.
6. Create appointment.
7. Create medical record.
8. Show health services.
9. Show user management.
10. Trigger invalid input and demonstrate the helpful error.
11. Demonstrate a missing-record/error state.

## Slide 7 — Failure Demo
Demonstrate:
- invalid patient data
- invalid appointment status
- missing record
- retry behavior

The handout specifically warns against demonstrating only the happy path.

## Slide 8 — Lessons
- Reusable UI behavior reduces duplication.
- Automated tests catch regressions.
- Persistent database configuration must be verified separately from local development.
- Production deployment requires environment-specific configuration and smoke testing.
- Clear errors are part of the user experience.

## Slide 9 — Retrospective
Summarize:
- what went well
- what was difficult
- what changed
- what the team will improve

## Slide 10 — Backup
Keep ready:
- screenshots
- recorded demo if permitted
- test results
- repository/PR link
- local fallback

## Defense preparation

Each student should be able to explain their own committed work without AI or teammate assistance, including request flow, validation, missing records, tests, and known limitations.
