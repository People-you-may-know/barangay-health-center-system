# Week 12 — Final Presentation & Live Demo Plan

The Week 12 handout calls for a short presentation following this arc: problem → solution → architecture → live demo → what we learned.

## Slide 1 — Title

**Barangay Health Center Patient Record and Appointment Management System**

Include the team members and course/project information.

## Slide 2 — Problem

Explain the original problem: paper-based patient records, slow retrieval, appointment scheduling difficulties, and the need for more organized health-center information management.

## Slide 3 — Solution

Show the system's main areas:

- Patient records
- Appointments
- Medical records
- Health services
- User management

## Slide 4 — Architecture / Request Flow

Explain one request from start to finish:

**Browser/UI → HTTP request → Flask route/controller → validation → MySQL database → JSON response → UI feedback**

Use one patient create/update example rather than trying to explain every route.

## Slide 5 — Quality & Review

Show the progression:

- Async UI and feedback
- Error handling
- Code review
- Automated tests
- Manual QA and adversarial testing
- P1 bug fixes
- Environment/deployment preparation
- Railway deployment with MySQL

## Slide 6 — Live Demo

Use the deployed public URL, not localhost:

**https://web-production-64a9f1.up.railway.app**

Recommended click path:

1. Sign in.
2. Create a valid patient.
3. Show the patient in the list.
4. Edit the patient.
5. Delete the patient.
6. Create an appointment for a patient.
7. Create a medical record.
8. Show health services.
9. Show user management as Administrator.
10. Submit invalid data and demonstrate the validation feedback.

## Slide 7 — Failure Demo

Do not show only the happy path.

Demonstrate at least one failure case, such as:

- invalid patient data
- missing record
- invalid appointment status
- network/server failure with a helpful message and retry where safe

## Slide 8 — What We Learned

Cover technical lessons, QA lessons, teamwork, code review, deployment, MySQL integration, and responsible AI use.

## Backup Demo

Prepare screenshots or a short recording of the main demo flow in case the public deployment fails during presentation.

## Speaker Assignment

| Part | Presenter |
|---|---|
| Problem | Team assignment required |
| Solution | Team assignment required |
| Architecture | Team assignment required |
| Live demo | Team assignment required |
| Lessons learned | Team assignment required |

Replace the placeholders with the team's actual assignments before presentation day.
