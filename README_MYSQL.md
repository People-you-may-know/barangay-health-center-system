# Barangay Health Center System — Fully Functional MySQL Edition

A local Flask + MySQL Barangay Health Center Management System with a complete dashboard and role-based CRUD workflows.

## Included

- Secure login with hashed passwords and session authentication
- Administrator and Staff roles
- Dashboard with:
  - total patients
  - total appointments
  - medical records
  - active health services
  - users
  - today's scheduled appointments
  - scheduled/completed/cancelled appointment overview
  - upcoming appointments
  - recently added patients
  - recent medical records
  - health service status
  - quick actions
- Patient management: Create, Read, Update, Delete
- Appointment management: Create, Read, Update, Delete
- Medical record management: Create, Read, Update, Delete
- Health service management: Create, Read, Update, Delete
- User management: Create, Read, Update, Delete
- Server-side validation and permission checks
- Friendly frontend error messages and confirmation dialogs
- Responsive HTML/CSS/JavaScript interface
- MySQL persistence

## Local setup in VS Code

### 1. Database

Open MySQL Workbench and run `schema.sql`.

This creates:

`barangay_health_center`

and the tables:

- users
- patients
- health_services
- appointments
- medical_records

### 2. Python environment

From the project root:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

### 3. Environment variables

Copy:

` .env.mysql.example `

to:

` .env `

Then set your actual MySQL password and secret key.

Example:

```text
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=barangay_health_center
SECRET_KEY=change-this-to-a-long-random-value
APP_HOST=127.0.0.1
APP_PORT=5001
APP_DEBUG=true
```

The application loads `.env` automatically.

### 4. Administrator

Run:

```powershell
py setup_admin.py
```

Choose the administrator username, password, and full name.

### 5. Start the system

```powershell
py app.py
```

Open the URL shown by Flask, for example:

`http://127.0.0.1:5001`

**Do not open `frontend/index.html` directly.** Flask must serve both the frontend and the API.

## Roles

### Administrator

Can manage:

- patients
- appointments
- medical records
- health services
- users

### Staff

Can manage normal patient/appointment/record workflows, but administrator-only destructive actions and user management are protected.

## Important privacy note

This is a school/local project. Do not use real patient information in development unless your school/team has the required privacy, security, access-control, audit, backup, and legal safeguards.
