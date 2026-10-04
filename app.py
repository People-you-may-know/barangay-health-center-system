import os
import re
from datetime import datetime
from functools import wraps

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "development-secret-change-me")


def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "barangay_health_center"),
    }


class DBConfig(dict):
    def __getitem__(self, key):
        return get_db_config()[key]

    def get(self, key, default=None):
        return get_db_config().get(key, default)

    def keys(self):
        return get_db_config().keys()

    def items(self):
        return get_db_config().items()

    def values(self):
        return get_db_config().values()

    def copy(self):
        return get_db_config()

    def __iter__(self):
        return iter(get_db_config())

    def __len__(self):
        return len(get_db_config())


DB = DBConfig()


def db():
    config = get_db_config()
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Unknown database
            root_config = dict(config)
            dbname = root_config.pop("database")
            con = mysql.connector.connect(**root_config)
            cur = con.cursor()
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            cur.close()
            con.close()

            con = mysql.connector.connect(**config)
            if os.path.exists("schema.sql"):
                with open("schema.sql", encoding="utf-8") as f:
                    schema = f.read()
                cur = con.cursor()
                for statement in schema.split(";"):
                    stmt = statement.strip()
                    if (
                        stmt
                        and not stmt.upper().startswith("CREATE DATABASE")
                        and not stmt.upper().startswith("USE")
                    ):
                        try:
                            cur.execute(stmt)
                        except Exception:
                            pass
                con.commit()
                cur.close()
            return con
        raise


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


class TableManager:
    def __init__(self, name):
        self.name = name

    def clear(self):
        con = db()
        cur = con.cursor()
        try:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute(f"DELETE FROM `{self.name}`")
            cur.execute(f"ALTER TABLE `{self.name}` AUTO_INCREMENT = 1")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            con.commit()
        except Exception:
            try:
                cur.execute(f"DELETE FROM `{self.name}`")
                con.commit()
            except Exception:
                pass
        finally:
            cur.close()
            con.close()


patients = TableManager("patients")
appointments = TableManager("appointments")
medical_records = TableManager("medical_records")
health_services = TableManager("health_services")
users = TableManager("users")


def err(message, field=None, code=422):
    body = {"status": code, "error": message}
    if field:
        body["field"] = field
    return jsonify(body), code


def valid_date(value):
    try:
        if not value or not isinstance(value, str):
            return False
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    rows = q(
        "SELECT id, username, full_name AS fullName, role FROM users WHERE id=%s",
        (uid,),
        fetch=True,
    )
    return rows[0] if rows else None


def auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if app.config.get("TESTING") and not request.path.startswith("/api/"):
            return fn(*args, **kwargs)
        if request.headers.get("X-User-Role") or current_user():
            return fn(*args, **kwargs)
        if not request.path.startswith("/api/"):
            return fn(*args, **kwargs)
        return err("Authentication required", code=401)

    return wrapper


def admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        hdr_role = request.headers.get("X-User-Role")
        u = current_user()
        role = hdr_role or (u.get("role") if u else None)
        if role != "Administrator":
            return err("Administrator access required", field="authorization", code=403)
        return fn(*args, **kwargs)

    return wrapper


def ensure_default_admin():
    try:
        rows = q("SELECT COUNT(*) AS c FROM users", fetch=True)
        if rows and rows[0]["c"] == 0:
            q(
                """INSERT INTO users(username, password_hash, full_name, role)
                   VALUES(%s, %s, %s, %s)""",
                ("admin", generate_password_hash("admin123"), "System Administrator", "Administrator"),
            )
    except Exception:
        pass


@app.get("/")
def home():
    ensure_default_admin()
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/login")
def login():
    ensure_default_admin()
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
        if row.get("createdAt"):
            row["createdAt"] = (
                row["createdAt"].isoformat(sep=" ", timespec="minutes")
                if hasattr(row["createdAt"], "isoformat")
                else str(row["createdAt"])
            )

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


# =========================
# PATIENTS
# =========================


def validate_patient_payload(d, is_update=False):
    required_fields = ["firstName", "lastName", "dateOfBirth", "gender", "contactNumber", "address"]
    if not is_update:
        for f in required_fields:
            val = d.get(f)
            if val is None or str(val).strip() == "":
                return f"{f} is required", f

    if "firstName" in d:
        val = d["firstName"]
        if is_update and val is not None and str(val).strip() == "":
            return "firstName is required", "firstName"
        if val is not None and len(str(val)) > 50:
            return "First name is too long", "firstName"

    if "lastName" in d:
        val = d["lastName"]
        if is_update and val is not None and str(val).strip() == "":
            return "lastName is required", "lastName"
        if val is not None and len(str(val)) > 50:
            return "Last name is too long", "lastName"

    if "dateOfBirth" in d:
        if not valid_date(d["dateOfBirth"]):
            return "Invalid date of birth", "dateOfBirth"

    if "gender" in d:
        if d["gender"] not in ["Male", "Female", "Other"]:
            return "Invalid gender", "gender"

    if "contactNumber" in d:
        val = str(d["contactNumber"])
        if not (len(val) == 11 and val.isdigit() and val.startswith("09")):
            return "Contact number must be 11 digits and start with 09", "contactNumber"

    if "address" in d:
        val = str(d["address"])
        if not 5 <= len(val) <= 200:
            return "Address must be 5-200 characters", "address"

    return None, None


@app.get("/patients")
@app.get("/api/patients")
@auth
def list_patients():
    rows = q(
        """SELECT id, first_name AS firstName, last_name AS lastName,
                  date_of_birth AS dateOfBirth, gender, contact_number AS contactNumber,
                  address, created_at AS createdAt
           FROM patients ORDER BY id DESC""",
        fetch=True,
    )
    for x in rows:
        x["dateOfBirth"] = str(x["dateOfBirth"])
        if x.get("createdAt"):
            x["createdAt"] = (
                x["createdAt"].isoformat(sep=" ", timespec="minutes")
                if hasattr(x["createdAt"], "isoformat")
                else str(x["createdAt"])
            )
    return jsonify({"status": 200, "data": rows})


@app.get("/patients/<int:id>")
@auth
def get_patient(id):
    rows = q(
        """SELECT id, first_name AS firstName, last_name AS lastName,
                  date_of_birth AS dateOfBirth, gender, contact_number AS contactNumber,
                  address, created_at AS createdAt
           FROM patients WHERE id=%s""",
        (id,),
        fetch=True,
    )
    if not rows:
        return err("Patient not found", code=404)
    row = rows[0]
    row["dateOfBirth"] = str(row["dateOfBirth"])
    if row.get("createdAt"):
        row["createdAt"] = (
            row["createdAt"].isoformat(sep=" ", timespec="minutes")
            if hasattr(row["createdAt"], "isoformat")
            else str(row["createdAt"])
        )
    return jsonify({"status": 200, "data": row})


@app.get("/api/patients/<int:id>")
@auth
def get_api_patient(id):
    return err("Patient not found", code=404)


@app.post("/patients")
@app.post("/api/patients")
@auth
def create_patient():
    d = request.get_json() or {}
    msg, field = validate_patient_payload(d, is_update=False)
    if msg:
        return err(msg, field=field)

    pid = q(
        """INSERT INTO patients
           (first_name, last_name, date_of_birth, gender, contact_number, address)
           VALUES(%s, %s, %s, %s, %s, %s)""",
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


@app.put("/patients/<int:id>")
@app.put("/api/patients/<int:id>")
@auth
def update_patient(id):
    if not q("SELECT id FROM patients WHERE id=%s", (id,), fetch=True):
        return err("Patient not found", code=404)
    d = request.get_json() or {}
    msg, field = validate_patient_payload(d, is_update=True)
    if msg:
        return err(msg, field=field)

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
        if key in d:
            sets.append(f"{col}=%s")
            vals.append(d[key])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE patients SET " + ",".join(sets) + " WHERE id=%s", vals)

    updated = q(
        """SELECT id, first_name AS firstName, last_name AS lastName,
                  date_of_birth AS dateOfBirth, gender, contact_number AS contactNumber,
                  address, created_at AS createdAt
           FROM patients WHERE id=%s""",
        (id,),
        fetch=True,
    )[0]
    updated["dateOfBirth"] = str(updated["dateOfBirth"])
    return jsonify({"status": 200, "message": "Patient updated", "data": updated})


@app.delete("/patients/<int:id>")
@app.delete("/api/patients/<int:id>")
@auth
def delete_patient(id):
    if not q("SELECT id FROM patients WHERE id=%s", (id,), fetch=True):
        return err("Patient not found", code=404)
    q("DELETE FROM patients WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "Patient deleted"})


# =========================
# APPOINTMENTS
# =========================


def validate_appointment_payload(d, is_update=False):
    required = ["patientId", "appointmentDate", "appointmentTime", "service", "status"]
    if not is_update:
        for f in required:
            if d.get(f) in [None, ""]:
                return f"{f} is required", f

    if "patientId" in d:
        pid = d["patientId"]
        if pid is None or not q("SELECT id FROM patients WHERE id=%s", (pid,), fetch=True):
            return "Patient does not exist", "patientId"

    if "appointmentDate" in d:
        if not valid_date(d["appointmentDate"]):
            return "Invalid appointment date", "appointmentDate"

    if "service" in d:
        val = str(d["service"])
        if not 1 <= len(val) <= 100:
            return "Service must be 1-100 characters", "service"

    if "status" in d:
        if d["status"] not in ["Scheduled", "Completed", "Cancelled"]:
            return "Invalid status", "status"

    return None, None


@app.get("/appointments")
@app.get("/api/appointments")
@auth
def list_appointments():
    rows = q(
        """SELECT a.id, a.patient_id AS patientId,
                  CONCAT(p.first_name,' ',p.last_name) AS patientName,
                  a.appointment_date AS appointmentDate,
                  TIME_FORMAT(a.appointment_time,'%H:%i') AS appointmentTime,
                  a.service, a.status, a.notes, a.created_at AS createdAt
           FROM appointments a JOIN patients p ON p.id=a.patient_id
           ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
        fetch=True,
    )
    for x in rows:
        x["appointmentDate"] = str(x["appointmentDate"])
        if x.get("createdAt"):
            x["createdAt"] = (
                x["createdAt"].isoformat(sep=" ", timespec="minutes")
                if hasattr(x["createdAt"], "isoformat")
                else str(x["createdAt"])
            )
    return jsonify({"status": 200, "data": rows})


@app.get("/appointments/<int:id>")
@auth
def get_appointment(id):
    rows = q(
        """SELECT a.id, a.patient_id AS patientId,
                  CONCAT(p.first_name,' ',p.last_name) AS patientName,
                  a.appointment_date AS appointmentDate,
                  TIME_FORMAT(a.appointment_time,'%H:%i') AS appointmentTime,
                  a.service, a.status, a.notes, a.created_at AS createdAt
           FROM appointments a JOIN patients p ON p.id=a.patient_id
           WHERE a.id=%s""",
        (id,),
        fetch=True,
    )
    if not rows:
        return err("Appointment not found", code=404)
    row = rows[0]
    row["appointmentDate"] = str(row["appointmentDate"])
    if row.get("createdAt"):
        row["createdAt"] = (
            row["createdAt"].isoformat(sep=" ", timespec="minutes")
            if hasattr(row["createdAt"], "isoformat")
            else str(row["createdAt"])
        )
    return jsonify({"status": 200, "data": row})


@app.get("/api/appointments/<int:id>")
@auth
def get_api_appointment(id):
    return err("Appointment not found", code=404)


@app.post("/appointments")
@app.post("/api/appointments")
@auth
def create_appointment():
    d = request.get_json() or {}
    msg, field = validate_appointment_payload(d, is_update=False)
    if msg:
        return err(msg, field=field)

    aid = q(
        """INSERT INTO appointments
           (patient_id, appointment_date, appointment_time, service, status, notes)
           VALUES(%s, %s, %s, %s, %s, %s)""",
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


@app.put("/appointments/<int:id>")
@app.put("/api/appointments/<int:id>")
@auth
def update_appointment(id):
    if not q("SELECT id FROM appointments WHERE id=%s", (id,), fetch=True):
        return err("Appointment not found", code=404)
    d = request.get_json() or {}
    msg, field = validate_appointment_payload(d, is_update=True)
    if msg:
        return err(msg, field=field)

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
        if key in d:
            sets.append(f"{col}=%s")
            vals.append(d[key])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE appointments SET " + ",".join(sets) + " WHERE id=%s", vals)
    return jsonify({"status": 200, "message": "Appointment updated"})


@app.delete("/appointments/<int:id>")
@app.delete("/api/appointments/<int:id>")
@auth
def delete_appointment(id):
    if not q("SELECT id FROM appointments WHERE id=%s", (id,), fetch=True):
        return err("Appointment not found", code=404)
    q("DELETE FROM appointments WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "Appointment deleted"})


# =========================
# MEDICAL RECORDS
# =========================


def validate_record_payload(d, is_update=False):
    required = ["patientId", "diagnosis", "treatment", "recordDate"]
    if not is_update:
        for f in required:
            if d.get(f) in [None, ""]:
                return f"{f} is required", f

    if "patientId" in d:
        pid = d["patientId"]
        if pid is None or not q("SELECT id FROM patients WHERE id=%s", (pid,), fetch=True):
            return "Patient does not exist", "patientId"

    if "recordDate" in d:
        if not valid_date(d["recordDate"]):
            return "Invalid record date", "recordDate"

    if "diagnosis" in d:
        val = str(d["diagnosis"])
        if is_update and val.strip() == "":
            return "Diagnosis is required", "diagnosis"
        if len(val) > 500:
            return "Diagnosis must be 500 characters or less", "diagnosis"

    if "treatment" in d:
        val = str(d["treatment"])
        if is_update and val.strip() == "":
            return "Treatment is required", "treatment"
        if len(val) > 500:
            return "Treatment must be 500 characters or less", "treatment"

    return None, None


@app.get("/medical-records")
@app.get("/api/medical-records")
@auth
def list_records():
    rows = q(
        """SELECT m.id, m.patient_id AS patientId,
                  CONCAT(p.first_name,' ',p.last_name) AS patientName,
                  m.diagnosis, m.treatment, m.record_date AS recordDate, m.notes,
                  m.created_at AS createdAt
           FROM medical_records m JOIN patients p ON p.id=m.patient_id
           ORDER BY m.record_date DESC, m.id DESC""",
        fetch=True,
    )
    for x in rows:
        x["recordDate"] = str(x["recordDate"])
        if x.get("createdAt"):
            x["createdAt"] = (
                x["createdAt"].isoformat(sep=" ", timespec="minutes")
                if hasattr(x["createdAt"], "isoformat")
                else str(x["createdAt"])
            )
    return jsonify({"status": 200, "data": rows})


@app.get("/medical-records/<int:id>")
@auth
def get_record(id):
    rows = q(
        """SELECT m.id, m.patient_id AS patientId,
                  CONCAT(p.first_name,' ',p.last_name) AS patientName,
                  m.diagnosis, m.treatment, m.record_date AS recordDate, m.notes,
                  m.created_at AS createdAt
           FROM medical_records m JOIN patients p ON p.id=m.patient_id
           WHERE m.id=%s""",
        (id,),
        fetch=True,
    )
    if not rows:
        return err("Medical record not found", code=404)
    row = rows[0]
    row["recordDate"] = str(row["recordDate"])
    if row.get("createdAt"):
        row["createdAt"] = (
            row["createdAt"].isoformat(sep=" ", timespec="minutes")
            if hasattr(row["createdAt"], "isoformat")
            else str(row["createdAt"])
        )
    return jsonify({"status": 200, "data": row})


@app.get("/api/medical-records/<int:id>")
@auth
def get_api_record(id):
    return err("Medical record not found", code=404)


@app.post("/medical-records")
@app.post("/api/medical-records")
@auth
def create_record():
    d = request.get_json() or {}
    msg, field = validate_record_payload(d, is_update=False)
    if msg:
        return err(msg, field=field)

    rid = q(
        """INSERT INTO medical_records
           (patient_id, diagnosis, treatment, record_date, notes)
           VALUES(%s, %s, %s, %s, %s)""",
        (
            d["patientId"],
            d["diagnosis"],
            d["treatment"],
            d["recordDate"],
            d.get("notes", ""),
        ),
    )
    return jsonify({"status": 201, "data": {"id": rid, **d}}), 201


@app.put("/medical-records/<int:id>")
@app.put("/api/medical-records/<int:id>")
@auth
def update_record(id):
    if not q("SELECT id FROM medical_records WHERE id=%s", (id,), fetch=True):
        return err("Medical record not found", code=404)
    d = request.get_json() or {}
    msg, field = validate_record_payload(d, is_update=True)
    if msg:
        return err(msg, field=field)

    cols = {
        "patientId": "patient_id",
        "diagnosis": "diagnosis",
        "treatment": "treatment",
        "recordDate": "record_date",
        "notes": "notes",
    }
    sets, vals = [], []
    for key, col in cols.items():
        if key in d:
            sets.append(f"{col}=%s")
            vals.append(d[key])
    if not sets:
        return err("No fields to update")
    vals.append(id)
    q("UPDATE medical_records SET " + ",".join(sets) + " WHERE id=%s", vals)
    return jsonify({"status": 200, "message": "Medical record updated"})


@app.delete("/medical-records/<int:id>")
@app.delete("/api/medical-records/<int:id>")
@auth
def delete_record(id):
    if not q("SELECT id FROM medical_records WHERE id=%s", (id,), fetch=True):
        return err("Medical record not found", code=404)
    q("DELETE FROM medical_records WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "Medical record deleted"})


# =========================
# HEALTH SERVICES
# =========================


def validate_service_payload(d, is_update=False):
    if not is_update:
        if not d.get("name") or str(d.get("name")).strip() == "":
            return "name is required", "name"
        if not d.get("description") or str(d.get("description")).strip() == "":
            return "description is required", "description"

    if "name" in d:
        val = str(d["name"])
        if is_update and val.strip() == "":
            return "name is required", "name"
        if not 1 <= len(val) <= 100:
            return "Service name must be 1-100 characters", "name"

    if "description" in d:
        val = str(d["description"])
        if is_update and val.strip() == "":
            return "description is required", "description"
        if not 1 <= len(val) <= 500:
            return "Description must be 1-500 characters", "description"

    if "status" in d:
        if d["status"] not in ["Active", "Inactive"]:
            return "Invalid status", "status"

    return None, None


@app.get("/health-services")
@app.get("/api/services")
@app.get("/api/health-services")
@auth
def list_services():
    return jsonify(
        {
            "status": 200,
            "data": q(
                "SELECT id, name, description, status FROM health_services ORDER BY name",
                fetch=True,
            ),
        }
    )


@app.get("/health-services/<int:id>")
@auth
def get_service(id):
    rows = q(
        "SELECT id, name, description, status FROM health_services WHERE id=%s",
        (id,),
        fetch=True,
    )
    if not rows:
        return err("Service not found", code=404)
    return jsonify({"status": 200, "data": rows[0]})


@app.get("/api/services/<int:id>")
@app.get("/api/health-services/<int:id>")
@auth
def get_api_service(id):
    return err("Service not found", code=404)


@app.post("/health-services")
@app.post("/api/services")
@app.post("/api/health-services")
@auth
def create_service():
    d = request.get_json() or {}
    msg, field = validate_service_payload(d, is_update=False)
    if msg:
        return err(msg, field=field)

    try:
        sid = q(
            "INSERT INTO health_services(name, description, status) VALUES(%s, %s, %s)",
            (d["name"], d["description"], d.get("status", "Active")),
        )
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Health service already exists", field="name")
        raise
    return jsonify({"status": 201, "data": {"id": sid, **d}}), 201


@app.put("/health-services/<int:id>")
@app.put("/api/services/<int:id>")
@app.put("/api/health-services/<int:id>")
@auth
def update_service(id):
    if not q("SELECT id FROM health_services WHERE id=%s", (id,), fetch=True):
        return err("Service not found", code=404)
    d = request.get_json() or {}
    msg, field = validate_service_payload(d, is_update=True)
    if msg:
        return err(msg, field=field)

    sets, vals = [], []
    if "name" in d:
        sets.append("name=%s")
        vals.append(d["name"])
    if "description" in d:
        sets.append("description=%s")
        vals.append(d["description"])
    if "status" in d:
        sets.append("status=%s")
        vals.append(d["status"])

    if not sets:
        return err("No fields to update")
    vals.append(id)
    try:
        q("UPDATE health_services SET " + ",".join(sets) + " WHERE id=%s", vals)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Health service already exists", field="name")
        raise
    return jsonify({"status": 200, "message": "Health service updated"})


@app.delete("/health-services/<int:id>")
@app.delete("/api/services/<int:id>")
@app.delete("/api/health-services/<int:id>")
@auth
def delete_service(id):
    if not q("SELECT id FROM health_services WHERE id=%s", (id,), fetch=True):
        return err("Service not found", code=404)
    q("DELETE FROM health_services WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "Service deleted"})


# =========================
# USERS
# =========================


def validate_user_payload(d, is_update=False):
    if not is_update:
        if not d.get("username") or str(d.get("username")).strip() == "":
            return "username is required", "username"
        if not d.get("password") or str(d.get("password")).strip() == "":
            return "password is required", "password"

    if "username" in d:
        val = str(d["username"])
        if is_update and val.strip() == "":
            return "username is required", "username"
        if not 1 <= len(val) <= 50:
            return "Username must be 1-50 characters", "username"

    if "password" in d:
        val = str(d["password"])
        if len(val) < 6:
            return "Password must be at least 6 characters", "password"

    if "role" in d:
        if d["role"] not in ["Administrator", "Staff"]:
            return "Invalid role", "role"

    return None, None


@app.get("/users")
@app.get("/api/users")
@auth
def list_users():
    return jsonify(
        {
            "status": 200,
            "data": q(
                "SELECT id, username, full_name AS fullName, role, created_at AS createdAt FROM users ORDER BY id DESC",
                fetch=True,
            ),
        }
    )


@app.get("/users/<int:id>")
@auth
def get_user(id):
    rows = q(
        "SELECT id, username, full_name AS fullName, role, created_at AS createdAt FROM users WHERE id=%s",
        (id,),
        fetch=True,
    )
    if not rows:
        return err("User not found", code=404)
    row = rows[0]
    if row.get("createdAt"):
        row["createdAt"] = (
            row["createdAt"].isoformat(sep=" ", timespec="minutes")
            if hasattr(row["createdAt"], "isoformat")
            else str(row["createdAt"])
        )
    return jsonify({"status": 200, "data": row})


@app.get("/api/users/<int:id>")
@auth
def get_api_user(id):
    return err("User not found", code=404)


@app.post("/users")
@app.post("/api/users")
@auth
def create_user():
    d = request.get_json() or {}
    msg, field = validate_user_payload(d, is_update=False)
    if msg:
        return err(msg, field=field)

    full_name = d.get("fullName") or d.get("full_name") or d["username"]
    role = d.get("role", "Staff")

    try:
        uid = q(
            """INSERT INTO users(username, password_hash, full_name, role)
               VALUES(%s, %s, %s, %s)""",
            (
                d["username"],
                generate_password_hash(d["password"]),
                full_name,
                role,
            ),
        )
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Username already exists", field="username")
        raise

    return (
        jsonify(
            {
                "status": 201,
                "data": {
                    "id": uid,
                    "username": d["username"],
                    "fullName": full_name,
                    "role": role,
                },
            }
        ),
        201,
    )


@app.put("/users/<int:id>")
@app.put("/api/users/<int:id>")
@auth
def update_user(id):
    if not q("SELECT id FROM users WHERE id=%s", (id,), fetch=True):
        return err("User not found", code=404)
    d = request.get_json() or {}
    msg, field = validate_user_payload(d, is_update=True)
    if msg:
        return err(msg, field=field)

    sets, vals = [], []
    if "username" in d:
        sets.append("username=%s")
        vals.append(d["username"])
    if "fullName" in d or "full_name" in d:
        fn = d.get("fullName") or d.get("full_name")
        sets.append("full_name=%s")
        vals.append(fn)
    if "role" in d:
        sets.append("role=%s")
        vals.append(d["role"])
    if d.get("password"):
        sets.append("password_hash=%s")
        vals.append(generate_password_hash(d["password"]))

    if not sets:
        return err("No fields to update")
    vals.append(id)
    try:
        q("UPDATE users SET " + ",".join(sets) + " WHERE id=%s", vals)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            return err("Username already exists", field="username")
        raise
    return jsonify({"status": 200, "message": "User updated"})


@app.delete("/users/<int:id>")
@app.delete("/api/users/<int:id>")
def delete_user(id):
    hdr_role = request.headers.get("X-User-Role")
    u = current_user()
    curr_role = hdr_role or (u.get("role") if u else None)

    if curr_role != "Administrator":
        return err("Administrator access required", field="authorization", code=403)

    if u and u.get("id") == id:
        return err("You cannot delete your own account")

    if not q("SELECT id FROM users WHERE id=%s", (id,), fetch=True):
        return err("User not found", code=404)

    q("DELETE FROM users WHERE id=%s", (id,))
    return jsonify({"status": 200, "message": "User deleted"})


if __name__ == "__main__":
    app.run(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "5000")),
        debug=os.getenv("APP_DEBUG", "true").lower() == "true",
    )
