# Week 11 / Deliverable 4 — Deployment Guide

## Production platform

The application is deployed on **Railway**.

- **Web service:** Railway `web` service
- **Public URL:** https://web-production-64a9f1.up.railway.app
- **Database:** Railway MySQL service
- **Runtime:** Gunicorn serving Flask
- **Production debug:** disabled with `APP_DEBUG=false`

## Environment configuration

The Railway web service uses environment variables for production-specific configuration:

- `APP_DEBUG=false`
- `APP_HOST=0.0.0.0`
- `APP_PORT=${{PORT}}`
- `DB_HOST=${{MySQL.MYSQLHOST}}`
- `DB_PORT=${{MySQL.MYSQLPORT}}`
- `DB_USER=${{MySQL.MYSQLUSER}}`
- `DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}`
- `DB_NAME=${{MySQL.MYSQLDATABASE}}`
- `SECRET_KEY` set as a Railway environment variable

No real credentials should be committed to the repository. The example environment files remain templates only.

## Database setup

The Railway MySQL service was provisioned separately from the web service. The production database initially existed without the application's tables, so the schema was initialized in the Railway `railway` database using MySQL Workbench.

The following application tables are present:

- `users`
- `patients`
- `health_services`
- `appointments`
- `medical_records`

The application successfully created the default administrator after the `users` table existed.

## Deployment verification completed

Verified on the deployed public application:

- Public HTTPS URL loads successfully.
- Login works against Railway MySQL.
- The authenticated dashboard opens successfully.
- Railway MySQL connectivity is working.
- The production database contains the required application tables.

## Remaining release verification

The following still require a final production smoke test before claiming the entire Deliverable 4 release gate is complete:

- Create patient
- View patient
- Edit patient
- Delete patient
- Create/view/edit/delete appointments
- Create/view/edit/delete medical records
- Create/view/edit/delete health services
- User-management permission checks
- Invalid input produces visible validation feedback
- Missing record produces the expected not-found feedback
- Failure/retry behavior is verified on the deployed application

## Production smoke-test checklist

| Test | Expected result | Status |
|---|---|---|
| Public HTTPS URL | Application loads | ✅ Verified |
| Login | Administrator can sign in | ✅ Verified |
| Dashboard | Dashboard opens after login | ✅ Verified |
| Patient CRUD | Create/read/update/delete work | ⬜ Pending final smoke test |
| Appointment CRUD | Create/read/update/delete work | ⬜ Pending final smoke test |
| Medical-record CRUD | Create/read/update/delete work | ⬜ Pending final smoke test |
| Health-service CRUD | Create/read/update/delete work | ⬜ Pending final smoke test |
| User permissions | Unauthorized actions are blocked | ⬜ Pending final smoke test |
| Invalid data | Visible validation error, no crash | ⬜ Pending final smoke test |
| Missing record | Clear 404/not-found state | ⬜ Pending final smoke test |
| Failure/retry | Human-readable failure + retry where safe | ⬜ Pending final smoke test |

## Live deployment record

**Host:** Railway

**Public URL:** https://web-production-64a9f1.up.railway.app

**Database:** Railway MySQL

**Release note:** Deployment is live and login/dashboard have been verified. Full production CRUD and failure-path smoke testing remains a release-gate task.

## Security/release checklist

- [x] No passwords, API keys, or real credentials committed.
- [x] Production debug mode is disabled.
- [x] HTTPS is enabled.
- [x] Required environment variables are configured.
- [x] Database schema initialized.
- [ ] Automated suite passes on the final release commit.
- [x] Public URL works outside the development machine.
- [ ] Production CRUD works end to end.
- [ ] Failure handling is verified in production.
- [ ] Backup demo is prepared.
