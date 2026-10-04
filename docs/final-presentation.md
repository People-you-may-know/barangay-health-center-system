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
**Browser/UI → Flask routes/controllers → application data layer**

Explain:
- HTML/CSS provides the views.
- JavaScript uses Fetch API for asynchronous CRUD.
- Flask validates requests and returns JSON responses.
- Automated tests exercise backend behavior.

## Slide 5 — QA Strategy
- Automated CRUD tests
- Validation/422 tests
- 404 not-found tests
- 403 authorization test
- Manual loading/empty/error/network tests
- Production smoke tests

## Slide 6 — Live Demo
Recommended sequence:
1. Open public URL.
2. Create patient.
3. Show patient in list.
4. Edit patient.
5. Create appointment for the patient.
6. Create medical record.
7. Show health services.
8. Show user management.
9. Trigger invalid input and demonstrate the helpful error.
10. Show a missing record/404 handling.
11. Explain the loading/error/retry behavior.

## Slide 7 — Failure Demo
Do not show only the happy path. Demonstrate:
- invalid patient data
- invalid appointment status
- missing record
- retry behavior

The handout specifically warns against demonstrating only the happy path.

## Slide 8 — Lessons
- Reusable components reduce duplicated UI logic.
- Automated tests catch regressions early.
- Production deployment requires a separate release checklist.
- Clear errors are part of the user experience.

## Slide 9 — Retrospective
Summarize:
- what went well
- what was difficult
- what changed
- what the team will improve

## Slide 10 — Backup
Keep ready:
- local copy
- screenshots
- recorded demo if permitted
- test results
- repository/PR link

A backup is important because the handout explicitly cautions against a live demo with no backup.

## Defense preparation

Each student should be able to explain their own commits without AI or teammate assistance. The handout gives the unassisted defense 25 individual points and states that a student who cannot defend their code cannot pass the individual half on commits alone.
