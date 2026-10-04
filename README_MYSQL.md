# Barangay Health Center System - MySQL Edition

This branch adds a MySQL-backed Flask API and an HTML/CSS/JavaScript frontend for local use in VS Code.

## Setup
1. Install Python 3.11+ and MySQL Server 8.x.
2. Run schema.sql in MySQL Workbench.
3. Create a virtual environment: python -m venv venv
4. Activate it in PowerShell: .\\venv\\Scripts\\Activate.ps1
5. Install packages: pip install -r requirements.txt
6. Copy .env.example to .env and set DB_PASSWORD and other MySQL values.
7. Run: python setup_admin.py
8. Start: python app.py
9. Open http://127.0.0.1:5000

The system includes login, Administrator/Staff roles, dashboard, patients, appointments, medical records, health services and user management.

Do not open frontend/index.html directly. Flask serves the frontend and API together.

For school/local use only. Add appropriate privacy, security, audit, backup and deployment controls before using real patient information.
