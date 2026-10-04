import os
from datetime import datetime
from functools import wraps

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "development-secret-change-me")

DB = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "barangay_health_center"),
}


def db():
    return mysql.connector.connect(**DB)


def q(sql, params=(), fetch=False):
    con = db()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        if fetch:
            return cur.fetchall()
        con.commit()
        return cur.lastrowid
    finally:
        cur.close()
        con.close()


def err(message, field=None, code=422):
    body = {"status": code, "error": message}
    if field:
        body["field"] = field
    return jsonify(body), code


def valid_date(value):
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def current_user():
    uid = session.get("user_id")
    rows = (
        q(
            "SELECT id,username,full_name AS fullName,role FROM users WHERE id=%s",
            (uid,),
            True,
        )
        if uid
        else []
    )
    return rows[0] if rows else None


def auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return err("Authentication required", code=401)
        return fn(*args, **kwargs)

    return wrapper


def admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u:
            return err("Authentication required", code=401)
        if u["role"] != "Administrator":
            return err("Administrator access required", code=403)
        return fn(*args, **kwargs)

    return wrapper


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/login")
def login():
    d = request.get_json() or {}
    username = str(d.get("username", "")).strip()
    password = str(d.get("password", ""))
    rows = q("SELECT * FROM users WHERE username=%s LIMIT 1", (username,), True)
    if not rows or not check_password_hash(rows[0]["password_hash"], password):
        return err("Invalid username or password", code=401)
    session["user_id"] = rows[0]["id"]
    return jsonify({"status": 200, "data": current_user()})


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"status": 200})


@app.get("/api/me")
def me():
    u = current_user()
    return jsonify({"status": 200, "data": u}) if u else err("Not authenticated", code=401)


@app.get("/api/dashboard")
@auth
def dashboard():
    counts = {
        "patients": q("SELECT COUNT(*) c FROM patients", fetch=True)[0]["c"],
        "appointments": q("SELECT COUNT(*) c FROM appointments", fetch=True)[0]["c"],
        "medicalRecords": q("SELECT COUNT(*) c FROM medical_records", fetch=True)[0]["c"],
        "services": q("SELECT COUNT(*) c FROM health_services", fetch=True)[0]["c"],
        "activeServices": q(
            "SELECT COUNT(*) c FROM health_services WHERE status='Active'", fetch=True
        )[0]["c"],
        "users": q("SELECT COUNT(*) c FROM users", fetch=True)[0]["c"],
        "todayAppointments": q(
            "SELECT COUNT(*) c FROM appointments WHERE appointment_date=CURDATE() AND status='Scheduled'",
            fetch=True,
        )[0]["c"],
        "completedAppointments": q(
            "SELECT COUNT(*) c FROM appointments WHERE status='Completed'", fetch=True
        )[0]["c"],
        "scheduledAppointments": q(
            "SELECT COUNT(*) c FROM appointments WHERE status='Scheduled'", fetch=True
        )[0]["c"],
        "cancelledAppointments": q(
            "SELECT COUNT(*) c FROM appointments WHERE status='Cancelled'", fetch=True
        )[0]["c"],
    }

    upcoming = q(
        """SELECT a.id, a.appointment_date appointmentDate,
                  TIME_FORMAT(a.appointment_time,'%H:%i') appointmentTime,
                  CONCAT(p.first_name,' ',p.last_name) patientName,
                  a.service, a.status
           FROM appointments a
           JOIN patients p ON p.id=a.patient_id
           WHERE a.appointment_date >= CURDATE()
             AND a.status='Scheduled'
           ORDER BY a.appointment_date, a.appointment_time
           LIMIT 8""",
        fetch=True,
    )
    for row in upcoming:
        row["appointmentDate"] = str(row["appointmentDate"])

    recent_patients = q(
        """SELECT id, CONCAT(first_name,' ',last_name) name,
                  date_of_birth dateOfBirth, gender, contact_number contactNumber,
                  created_at createdAt
           FROM patients ORDER BY created_at DESC, id DESC LIMIT 8""",
        fetch=True,
    )
    for row in recent_patients:
        row["dateOfBirth"] = str(row["dateOfBirth"])
        row["createdAt"] = row["createdAt"].isoformat(sep=" ", timespec="minutes")

    recent_records = q(
        """SELECT m.id, m.record_date recordDate,
                  CONCAT(p.first_name,' ',p.last_name) patientName,
                  m.diagnosis, m.treatment
           FROM medical_records m
           JOIN patients p ON p.id=m.patient_id
           ORDER BY m.record_date DESC, m.id DESC LIMIT 6""",
        fetch=True,
    )
    for row in recent_records:
        row["recordDate"] = str(row["recordDate"])

    service_summary = q(
        """SELECT status, COUNT(*) count
           FROM health_services GROUP BY status ORDER BY status""",
        fetch=True,
    )

    return jsonify(
        {
            "status": 200,
            "data": {
                **counts,
                "upcomingAppointments": upcoming,
                "recentPatients": recent_patients,
                "recentRecords": recent_records,
                "serviceSummary": service_summary,
            },
        }
    )


# Patients
@app.get("/api/patients")
@auth
def list_patients():
    rows = q(
        """SELECT id,first_name firstName,last_name lastName,
                  date_of_birth dateOfBirth,gender,contact_number contactNumber,
                  address,created_at createdAt
           FROM patients ORDER BY id DESC""",
        fetch=True,
    )
    for x in rows:
        x["dateOfBirth"] = str(x["dateOfBirth"])
        x["createdAt"] = x["createdAt"].isoformat(sep=" ", timespec="minutes")
    return jsonify({"status": 200, "data": rows})


@app.post("/api/patients")
@auth
def create_patient():
    d = request.get_json() or {}
    for f in ["firstName", "lastName", "dateOfBirth", "gender", "contactNumber", "address"]:
        if not str(d.get(f, "")).strip():
            return err(f"{f} is required", f)
    if len(d["firstName"]) > 50 or len(d["lastName"]) > 50:
        return err("Name is too long")
    if not valid_date(d["dateOfBirth"]):
        return err("Invalid date of birth", "dateOfBirth")
    if d["gender"] not in ["Male", "Female", "Other"]:
        return err("Invalid gender", "gender")
    if not (
        isinstance(d["contactNumber"], str)
        and len(d["contactNumber"]) == 11
        and d["contactNumber"].isdigit()
        and d["contactNumber"].startswith("09")
    ):
        return err("Contact number must be 11 digits and start with 09", "contactNumber")
    if not 5 <= len(d["address"]) <= 200:
        return err("Address must be 5-200 characters", "address")
    pid = q(
        """INSERT INTO patients
           (first_name,last_name,date_of_birth,gender,contact_number,address)
           VALUES(%s,%s,%s,%s,%s,%s)""",
        (
            d["firstName"],
            d["lastName"],
            d["dateOfBirth"],
            d["gender"],
            d["contactNumber"],
            d["address"],
        ),
    )
    return jsonify({"status": 201, "data": {"id": pid, **d}}), 201


@app.put("/api/patients/<int:id>")
@auth
def update_patient(id):
    d = request.get_json() or {}
    if not q("SELECT id FROM patients WHERE id=%s", (id,), True):
        return err("Patient not found", code=404)
    cols = {
        "firstName": "first_name",
        "lastName": "last_name",
        "dateOfBirth": "date_of_birth",
        "gender": "gender",
        "contactNumber": "contact_number",
        "address": "address",
    }
    sets, vals = [], []
    for key, col in cols.items():
        if key not in d:
            continue
        value = d[key]
        if key in ("firstName", "lastName") and not value:
            return err(f"{key} is required", key)
        if key in ("firstName", "lastName") and len(value) > 50:
            return err(f"{key} is too long", key)
        if key == "dateOfBirth" and not valid_date(value):
            return err("Invalid date", key)
        if key == "gender" and value not in ["Male", "Female", "Other"]:
            return err("Invalid gender", key)
        if key == "contactNumber" and not (
            isinstance(value, str)
            and len(value) == 11
            and value.isdigit()
            and value.startswith("09")
        ):
            return err("Invalid contact number", key)
        if key == "address" and not 5 <= len(value) <= 200:
            return err("Address must be 5-200 characters", key)
        sets.append(f"{col}=%s")
        vals.append(value)
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE patients SET " + ",".join(sets) + " WHERE id=%s", vals)
    return jsonify({"status": 200, "message": "Patient updated"})


@app.delete("/api/patients/<int:id>")
@admin
def delete_patient(id):
    if not q("SELECT id FROM patients WHERE id=%s", (id,), True):
        return err("Patient not found", code=404)
    q("DELETE FROM patients WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "Patient deleted"})


# Appointments
@app.get("/api/appointments")
@auth
def list_appointments():
    rows = q(
        """SELECT a.id,a.patient_id patientId,
                  CONCAT(p.first_name,' ',p.last_name) patientName,
                  a.appointment_date appointmentDate,
                  TIME_FORMAT(a.appointment_time,'%H:%i') appointmentTime,
                  a.service,a.status,a.notes,a.created_at createdAt
           FROM appointments a JOIN patients p ON p.id=a.patient_id
           ORDER BY a.appointment_date DESC,a.appointment_time DESC""",
        fetch=True,
    )
    for x in rows:
        x["appointmentDate"] = str(x["appointmentDate"])
        x["createdAt"] = x["createdAt"].isoformat(sep=" ", timespec="minutes")
    return jsonify({"status": 200, "data": rows})


def validate_appointment(d):
    for f in ["patientId", "appointmentDate", "appointmentTime", "service", "status"]:
        if d.get(f) in [None, ""]:
            return f"{f} is required", f
    if not q("SELECT id FROM patients WHERE id=%s", (d["patientId"],), True):
        return "Patient does not exist", "patientId"
    if not valid_date(d["appointmentDate"]):
        return "Invalid date", "appointmentDate"
    if len(str(d["service"])) > 100:
        return "Service is too long", "service"
    if d["status"] not in ["Scheduled", "Completed", "Cancelled"]:
        return "Invalid status", "status"
    return None


@app.post("/api/appointments")
@auth
def create_appointment():
    d = request.get_json() or {}
    problem = validate_appointment(d)
    if problem:
        return err(*problem)
    aid = q(
        """INSERT INTO appointments
           (patient_id,appointment_date,appointment_time,service,status,notes)
           VALUES(%s,%s,%s,%s,%s,%s)""",
        (
            d["patientId"],
            d["appointmentDate"],
            d["appointmentTime"],
            d["service"],
            d["status"],
            d.get("notes", ""),
        ),
    )
    return jsonify({"status": 201, "data": {"id": aid, **d}}), 201


@app.put("/api/appointments/<int:id>")
@auth
def update_appointment(id):
    if not q("SELECT id FROM appointments WHERE id=%s", (id,), True):
        return err("Appointment not found", code=404)
    d = request.get_json() or {}
    cols = {
        "patientId": "patient_id",
        "appointmentDate": "appointment_date",
        "appointmentTime": "appointment_time",
        "service": "service",
        "status": "status",
        "notes": "notes",
    }
    sets, vals = [], []
    for key, col in cols.items():
        if key not in d:
            continue
        if key == "patientId" and not q("SELECT id FROM patients WHERE id=%s", (d[key],), True):
            return err("Patient does not exist", key)
        if key == "appointmentDate" and not valid_date(d[key]):
            return err("Invalid date", key)
        if key == "status" and d[key] not in ["Scheduled", "Completed", "Cancelled"]:
            return err("Invalid status", key)
        if key == "service" and not 1 <= len(str(d[key])) <= 100:
            return err("Service must be 1-100 characters", key)
        sets.append(f"{col}=%s")
        vals.append(d[key])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE appointments SET " + ",".join(sets) + " WHERE id=%s", vals)
    return jsonify({"status": 200, "message": "Appointment updated"})


@app.delete("/api/appointments/<int:id>")
@auth
def delete_appointment(id):
    if not q("SELECT id FROM appointments WHERE id=%s", (id,), True):
        return err("Appointment not found", code=404)
    q("DELETE FROM appointments WHERE id=%s", (id,))
    return jsonify({"status": 200})


# Medical records
@app.get("/api/medical-records")
@auth
def list_records():
    rows = q(
        """SELECT m.id,m.patient_id patientId,
                  CONCAT(p.first_name,' ',p.last_name) patientName,
                  m.diagnosis,m.treatment,m.record_date recordDate,m.notes,
                  m.created_at createdAt
           FROM medical_records m JOIN patients p ON p.id=m.patient_id
           ORDER BY m.record_date DESC,m.id DESC""",
        fetch=True,
    )
    for x in rows:
        x["recordDate"] = str(x["recordDate"])
        x["createdAt"] = x["createdAt"].isoformat(sep=" ", timespec="minutes")
    return jsonify({"status": 200, "data": rows})


@app.post("/api/medical-records")
@auth
def create_record():
    d = request.get_json() or {}
    for f in ["patientId", "diagnosis", "treatment", "recordDate"]:
        if d.get(f) in [None, ""]:
            return err(f"{f} is required", f)
    if not q("SELECT id FROM patients WHERE id=%s", (d["patientId"],), True):
        return err("Patient does not exist", "patientId")
    if not valid_date(d["recordDate"]):
        return err("Invalid date", "recordDate")
    if len(d["diagnosis"]) > 500 or len(d["treatment"]) > 500 or len(d.get("notes", "")) > 500:
        return err("Diagnosis, treatment, and notes must be 500 characters or less")
    rid = q(
        """INSERT INTO medical_records
           (patient_id,diagnosis,treatment,record_date,notes)
           VALUES(%s,%s,%s,%s,%s)""",
        (
            d["patientId"],
            d["diagnosis"],
            d["treatment"],
            d["recordDate"],
            d.get("notes", ""),
        ),
    )
    return jsonify({"status": 201, "data": {"id": rid, **d}}), 201


@app.put("/api/medical-records/<int:id>")
@auth
def update_record(id):
    if not q("SELECT id FROM medical_records WHERE id=%s", (id,), True):
        return err("Medical record not found", code=404)
    d = request.get_json() or {}
    cols = {
        "patientId": "patient_id",
        "diagnosis": "diagnosis",
        "treatment": "treatment",
        "recordDate": "record_date",
        "notes": "notes",
    }
    sets, vals = [], []
    for key, col in cols.items():
        if key not in d:
            continue
        if key == "patientId" and not q("SELECT id FROM patients WHERE id=%s", (d[key],), True):
            return err("Patient does not exist", key)
        if key == "recordDate" and not valid_date(d[key]):
            return err("Invalid date", key)
        if key in ("diagnosis", "treatment", "notes") and len(str(d[key])) > 500:
            return err(f"{key} must be 500 characters or less", key)
        sets.append(f"{col}=%s")
        vals.append(d[key])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE medical_records SET " + ",".join(sets) + " WHERE id=%s", vals)
    return jsonify({"status": 200, "message": "Medical record updated"})


@app.delete("/api/medical-records/<int:id>")
@admin
def delete_record(id):
    if not q("SELECT id FROM medical_records WHERE id=%s", (id,), True):
        return err("Medical record not found", code=404)
    q("DELETE FROM medical_records WHERE id=%s", (id,))
    return jsonify({"status": 200})


# Health services
@app.get("/api/services")
@auth
def list_services():
    return jsonify(
        {
            "status": 200,
            "data": q(
                "SELECT id,name,description,status FROM health_services ORDER BY name",
                fetch=True,
            ),
        }
    )


@app.post("/api/services")
@admin
def create_service():
    d = request.get_json() or {}
    if not d.get("name") or not d.get("description"):
        return err("Name and description are required")
    if len(d["name"]) > 100 or len(d["description"]) > 500:
        return err("Service name or description is too long")
    if d.get("status", "Active") not in ["Active", "Inactive"]:
        return err("Invalid status", "status")
    try:
        sid = q(
            "INSERT INTO health_services(name,description,status) VALUES(%s,%s,%s)",
            (d["name"], d["description"], d.get("status", "Active")),
        )
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Health service already exists", "name")
        raise
    return jsonify({"status": 201, "data": {"id": sid, **d}}), 201


@app.put("/api/services/<int:id>")
@admin
def update_service(id):
    if not q("SELECT id FROM health_services WHERE id=%s", (id,), True):
        return err("Service not found", code=404)
    d = request.get_json() or {}
    sets, vals = [], []
    if "name" in d:
        if not 1 <= len(str(d["name"])) <= 100:
            return err("Service name must be 1-100 characters", "name")
        sets.append("name=%s")
        vals.append(d["name"])
    if "description" in d:
        if not 1 <= len(str(d["description"])) <= 500:
            return err("Description must be 1-500 characters", "description")
        sets.append("description=%s")
        vals.append(d["description"])
    if "status" in d:
        if d["status"] not in ["Active", "Inactive"]:
            return err("Invalid status", "status")
        sets.append("status=%s")
        vals.append(d["status"])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    try:
        q("UPDATE health_services SET " + ",".join(sets) + " WHERE id=%s", vals)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Health service already exists", "name")
        raise
    return jsonify({"status": 200, "message": "Health service updated"})


@app.delete("/api/services/<int:id>")
@admin
def delete_service(id):
    if not q("SELECT id FROM health_services WHERE id=%s", (id,), True):
        return err("Service not found", code=404)
    q("DELETE FROM health_services WHERE id=%s", (id,))
    return jsonify({"status": 200})


# Users
@app.get("/api/users")
@admin
def list_users():
    return jsonify(
        {
            "status": 200,
            "data": q(
                "SELECT id,username,full_name fullName,role,created_at FROM users ORDER BY id DESC",
                fetch=True,
            ),
        }
    )


@app.post("/api/users")
@admin
def create_user():
    d = request.get_json() or {}
    if not d.get("username") or not d.get("password") or not d.get("fullName"):
        return err("Username, password and full name are required")
    if len(d["username"]) > 50 or len(d["fullName"]) > 100:
        return err("Username or full name is too long")
    if len(d["password"]) < 8:
        return err("Password must be at least 8 characters", "password")
    if d.get("role", "Staff") not in ["Administrator", "Staff"]:
        return err("Invalid role", "role")
    try:
        uid = q(
            """INSERT INTO users(username,password_hash,full_name,role)
               VALUES(%s,%s,%s,%s)""",
            (
                d["username"],
                generate_password_hash(d["password"]),
                d["fullName"],
                d.get("role", "Staff"),
            ),
        )
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Username already exists", "username")
        raise
    return (
        jsonify(
            {
                "status": 201,
                "data": {
                    "id": uid,
                    "username": d["username"],
                    "fullName": d["fullName"],
                    "role": d.get("role", "Staff"),
                },
            }
        ),
        201,
    )


@app.put("/api/users/<int:id>")
@admin
def update_user(id):
    if not q("SELECT id FROM users WHERE id=%s", (id,), True):
        return err("User not found", code=404)
    d = request.get_json() or {}
    sets, vals = [], []
    if "username" in d:
        if not 1 <= len(str(d["username"])) <= 50:
            return err("Username must be 1-50 characters", "username")
        sets.append("username=%s")
        vals.append(d["username"])
    if "fullName" in d:
        if not 1 <= len(str(d["fullName"])) <= 100:
            return err("Full name must be 1-100 characters", "fullName")
        sets.append("full_name=%s")
        vals.append(d["fullName"])
    if "role" in d:
        if d["role"] not in ["Administrator", "Staff"]:
            return err("Invalid role", "role")
        sets.append("role=%s")
        vals.append(d["role"])
    if d.get("password"):
        if len(d["password"]) < 8:
            return err("Password must be at least 8 characters", "password")
        sets.append("password_hash=%s")
        vals.append(generate_password_hash(d["password"]))
    if not sets:
        return err("No fields to update")
    vals.append(id)
    try:
        q("UPDATE users SET " + ",".join(sets) + " WHERE id=%s", vals)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Username already exists", "username")
        raise
    return jsonify({"status": 200, "message": "User updated"})


@app.delete("/api/users/<int:id>")
@admin
def delete_user(id):
    if current_user()["id"] == id:
        return err("You cannot delete your own account")
    if not q("SELECT id FROM users WHERE id=%s", (id,), True):
        return err("User not found", code=404)
    q("DELETE FROM users WHERE id=%s", (id,))
    return jsonify({"status": 200})


if __name__ == "__main__":
    app.run(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "5000")),
        debug=os.getenv("APP_DEBUG", "true").lower() == "true",
    )
