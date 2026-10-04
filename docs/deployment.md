# Deliverable 4 — Deployment Guide

## Target

Deploy the Flask application to a public HTTPS host. The repository includes a production WSGI command and a Render configuration as a reproducible deployment option.

## Local pre-deployment checks

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the automated suite:
   `python -m unittest discover -s tests -p "test_*.py" -v`
4. Start locally:
   `python app.py`
5. Verify the main CRUD flows and the failure states from `docs/test-matrix.md`.

## Render deployment

1. Create a new Web Service from the GitHub repository.
2. Use the repository's `render.yaml`, or configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Deploy from the intended release branch.
4. Open the generated HTTPS URL.
5. Verify patients, appointments, medical records, health services, and users.
6. Verify a bad request produces a visible error instead of a crash.
7. Record the final public URL in the presentation and submission materials.

## Security/release checklist

- Do not commit passwords, API keys, or other secrets.
- Do not leave debug mode enabled in production.
- Use HTTPS.
- Review environment variables before deployment.
- Keep a backup demo path (screenshots/video or a tested local copy).

## Current repository status

This documentation prepares the application for deployment, but **no public production URL is claimed by this commit**. The final live URL must be recorded only after the team actually deploys and verifies it.
