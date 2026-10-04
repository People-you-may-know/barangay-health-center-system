# Week 11 — Deployment Notes

## Environment configuration

Set these variables on the deployment host:

- `APP_DEBUG=false` — keeps Flask debug mode disabled in production.
- `APP_HOST=0.0.0.0` — binds the web process to the host interface.
- `APP_PORT` — use the port supplied by the hosting platform when required.

Do not commit `.env` or real credentials. Use `.env.example` only as a template.

## Build and start

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the production WSGI process:

```bash
gunicorn app:app
```

## Database note

The current project stores data in in-memory Python lists and does not define a persistent database schema or migration system. Therefore, there is no database migration command to run for this Week 11 deployment. A future persistent database implementation should add its migration step here.

## Live deployment record

**Host:** Pending team selection

**Public URL:** Pending deployment

**Deployed commit:** Pending deployment

## Smoke-test checklist

- [ ] Open the public URL from a device/browser outside the development machine.
- [ ] Create a valid patient.
- [ ] View the patient.
- [ ] Edit the patient.
- [ ] Delete the patient.
- [ ] Submit an invalid date such as `2026-99-99` and confirm HTTP 422 validation feedback.
- [ ] Confirm production debug mode is disabled.
- [ ] Record the final public URL and deployed commit above.
