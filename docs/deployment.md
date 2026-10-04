# Week 11 / Deliverable 4 — Deployment Guide

## Environment configuration

Set these variables on the deployment host as required by the current application:

- `APP_DEBUG=false` — keeps Flask debug mode disabled in production.
- `APP_HOST=0.0.0.0` — binds the web process to the host interface.
- `APP_PORT` — use the port supplied by the hosting platform when required.
- For the MySQL-backed variant, configure the database variables documented in `.env.mysql.example`.

Do not commit `.env` or real credentials. Use the example environment files only as templates.

## Local pre-deployment checks

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the automated suite:
   `python -m unittest discover -s tests -p "test_*.py" -v`
4. Start locally:
   `python app.py`
5. Verify the CRUD flows and failure states from `docs/test-matrix.md`.

## Production build and start

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the production WSGI process:

```bash
gunicorn app:app
```

The repository includes `Procfile` and `render.yaml` for a reproducible Render deployment configuration.

## Render deployment

1. Create a new Web Service from the GitHub repository.
2. Use the repository's `render.yaml`, or configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Configure required environment variables and database credentials when using the MySQL-backed variant.
4. Deploy from the intended release branch.
5. Open the generated HTTPS URL.
6. Verify patients, appointments, medical records, health services, and users.
7. Verify a bad request produces a visible error instead of a crash.
8. Record the final public URL and deployed commit below.

## Database note

The repository has both the earlier in-memory Flask implementation and a MySQL-backed implementation in the project's development history. The deployment target must be matched to the branch being released. If the MySQL-backed implementation is deployed, create the schema from `schema.sql` and create the initial administrator with `setup_admin.py` before the production smoke test.

## Live deployment record

**Host:** Pending team selection

**Public URL:** Pending deployment

**Deployed commit:** Pending deployment

## Security/release checklist

- [ ] No passwords, API keys, or real credentials committed.
- [ ] Production debug mode is disabled.
- [ ] HTTPS is enabled.
- [ ] Required environment variables are configured.
- [ ] Database schema/admin setup completed if deploying the MySQL variant.
- [ ] Automated suite passes.
- [ ] Public URL works outside the development machine.
- [ ] Production CRUD works end to end.
- [ ] Failure handling is verified.
- [ ] Backup demo is prepared.

## Current repository status

This documentation prepares the application for deployment, but **no public production URL is claimed by this commit**. The final live URL must be recorded only after the team actually deploys and verifies it.
