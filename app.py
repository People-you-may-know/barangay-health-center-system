import os
from datetime import datetime
from functools import wraps
import mysql.connector
from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "development-secret-change-me")

DB = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "barangay_health_center")
}

def db():
    return mysql.connector.connect(**DB)

def q(sql, params=(), fetch=False):
    con = db(); cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        if fetch: return cur.fetchall()
        con.commit(); return cur.lastrowid
    finally:
        cur.close(); con.close()

def err(message, field=None, code=422):
    body={"status":code,"error":message}
    if field: body["field"]=field
    return jsonify(body), code

def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d"); return True
    except (TypeError, ValueError): return False

def user():
    uid=session.get("user_id")
    rows=q("SELECT id,username,full_name AS fullName,role FROM users WHERE id=%s",(uid,),True) if uid else []
    return rows[0] if rows else None

def auth(fn):
    @wraps(fn)
    def w(*a,**k):
        if not user(): return err("Authentication required",code=401)
        return fn(*a,**k)
    return w

def admin(fn):
    @wraps(fn)
    def w(*a,**k):
        u=user()
        if not u: return err("Authentication required",code=401)
        if u["role"]!="Administrator": return err("Administrator access required",code=403)
        return fn(*a,**k)
    return w

@app.get("/")
def home(): return send_from_directory(app.static_folder,"index.html")

@app.post("/api/login")
def login():
    d=request.get_json() or {}
    rows=q("SELECT * FROM users WHERE username=%s LIMIT 1",(d.get("username"),),True)
    if not rows or not check_password_hash(rows[0]["password_hash"],d.get("password","")):
        return err("Invalid username or password",code=401)
    session["user_id"]=rows[0]["id"]
    return jsonify({"status":200,"data":user()})

@app.post("/api/logout")
def logout(): session.clear(); return jsonify({"status":200})

@app.get("/api/me")
def me():
    u=user()
    return jsonify({"status":200,"data":u}) if u else err("Not authenticated",code=401)

@app.get("/api/dashboard")
@auth
def dashboard():
    names={"patients":"patients","appointments":"appointments","medicalRecords":"medical_records","services":"health_services"}
    data={k:q("SELECT COUNT(*) c FROM "+t,fetch=True)[0]["c"] for k,t in names.items()}
    data["todayAppointments"]=q("SELECT COUNT(*) c FROM appointments WHERE appointment_date=CURDATE() AND status='Scheduled'",fetch=True)[0]["c"]
    return jsonify({"status":200,"data":data})

# Patients
@app.get("/api/patients")
@auth
def list_patients():
    rows=q("SELECT id,first_name firstName,last_name lastName,date_of_birth dateOfBirth,gender,contact_number contactNumber,address FROM patients ORDER BY id DESC",fetch=True)
    for x in rows:x["dateOfBirth"]=str(x["dateOfBirth"])
    return jsonify({"status":200,"data":rows})

@app.post("/api/patients")
@auth
def create_patient():
    d=request.get_json() or {}
    for f in ["firstName","lastName","dateOfBirth","gender","contactNumber","address"]:
        if not d.get(f): return err(f+" is required",f)
    if len(d["firstName"])>50 or len(d["lastName"])>50:return err("Name is too long")
    if not valid_date(d["dateOfBirth"]):return err("Invalid date of birth","dateOfBirth")
    if d["gender"] not in ["Male","Female","Other"]:return err("Invalid gender","gender")
    if not (isinstance(d["contactNumber"],str) and len(d["contactNumber"])==11 and d["contactNumber"].isdigit() and d["contactNumber"].startswith("09")):return err("Contact number must be 11 digits and start with 09","contactNumber")
    if not 5<=len(d["address"])<=200:return err("Address must be 5-200 characters","address")
    pid=q("INSERT INTO patients(first_name,last_name,date_of_birth,gender,contact_number,address) VALUES(%s,%s,%s,%s,%s,%s)",(d["firstName"],d["lastName"],d["dateOfBirth"],d["gender"],d["contactNumber"],d["address"]))
    return jsonify({"status":201,"data":{"id":pid,**d}}),201

@app.put("/api/patients/<int:id>")
@auth
def update_patient(id):
    d=request.get_json() or {}
    if not q("SELECT id FROM patients WHERE id=%s",(id,),True):return err("Patient not found",code=404)
    cols={"firstName":"first_name","lastName":"last_name","dateOfBirth":"date_of_birth","gender":"gender","contactNumber":"contact_number","address":"address"}
    sets=[];vals=[]
    for k,c in cols.items():
        if k in d:
            if k=="dateOfBirth" and not valid_date(d[k]):return err("Invalid date","dateOfBirth")
            if k=="gender" and d[k] not in ["Male","Female","Other"]:return err("Invalid gender","gender")
            if k=="contactNumber" and not (isinstance(d[k],str) and len(d[k])==11 and d[k].isdigit() and d[k].startswith("09")):return err("Invalid contact number","contactNumber")
            sets.append(c+"=%s");vals.append(d[k])
    if not sets:return err("No fields to update")
    vals.append(id);q("UPDATE patients SET "+",".join(sets)+" WHERE id=%s",vals)
    return jsonify({"status":200,"message":"Patient updated"})

@app.delete("/api/patients/<int:id>")
@admin
def delete_patient(id):
    if not q("SELECT id FROM patients WHERE id=%s",(id,),True):return err("Patient not found",code=404)
    q("DELETE FROM patients WHERE id=%s",(id,));return jsonify({"status":200,"message":"Patient deleted"})

# Appointments
@app.get("/api/appointments")
@auth
def list_appointments():
    rows=q("SELECT a.id,a.patient_id patientId,CONCAT(p.first_name,' ',p.last_name) patientName,a.appointment_date appointmentDate,a.appointment_time appointmentTime,a.service,a.status,a.notes FROM appointments a JOIN patients p ON p.id=a.patient_id ORDER BY a.appointment_date DESC,a.appointment_time DESC",fetch=True)
    for x in rows:x["appointmentDate"]=str(x["appointmentDate"]);x["appointmentTime"]=str(x["appointmentTime"])[:5]
    return jsonify({"status":200,"data":rows})

@app.post("/api/appointments")
@auth
def create_appointment():
    d=request.get_json() or {}
    for f in ["patientId","appointmentDate","appointmentTime","service","status"]:
        if d.get(f) in [None,""]:return err(f+" is required",f)
    if not q("SELECT id FROM patients WHERE id=%s",(d["patientId"],),True):return err("Patient does not exist","patientId")
    if not valid_date(d["appointmentDate"]):return err("Invalid date","appointmentDate")
    if d["status"] not in ["Scheduled","Completed","Cancelled"]:return err("Invalid status","status")
    aid=q("INSERT INTO appointments(patient_id,appointment_date,appointment_time,service,status,notes) VALUES(%s,%s,%s,%s,%s,%s)",(d["patientId"],d["appointmentDate"],d["appointmentTime"],d["service"],d["status"],d.get("notes","")))
    return jsonify({"status":201,"data":{"id":aid,**d}}),201

@app.delete("/api/appointments/<int:id>")
@auth
def delete_appointment(id):
    if not q("SELECT id FROM appointments WHERE id=%s",(id,),True):return err("Appointment not found",code=404)
    q("DELETE FROM appointments WHERE id=%s",(id,));return jsonify({"status":200})

# Medical records
@app.get("/api/medical-records")
@auth
def list_records():
    rows=q("SELECT m.id,m.patient_id patientId,CONCAT(p.first_name,' ',p.last_name) patientName,m.diagnosis,m.treatment,m.record_date recordDate,m.notes FROM medical_records m JOIN patients p ON p.id=m.patient_id ORDER BY m.record_date DESC",fetch=True)
    for x in rows:x["recordDate"]=str(x["recordDate"])
    return jsonify({"status":200,"data":rows})

@app.post("/api/medical-records")
@auth
def create_record():
    d=request.get_json() or {}
    for f in ["patientId","diagnosis","treatment","recordDate"]:
        if not d.get(f):return err(f+" is required",f)
    if not q("SELECT id FROM patients WHERE id=%s",(d["patientId"],),True):return err("Patient does not exist","patientId")
    if not valid_date(d["recordDate"]):return err("Invalid date","recordDate")
    rid=q("INSERT INTO medical_records(patient_id,diagnosis,treatment,record_date,notes) VALUES(%s,%s,%s,%s,%s)",(d["patientId"],d["diagnosis"],d["treatment"],d["recordDate"],d.get("notes","")))
    return jsonify({"status":201,"data":{"id":rid,**d}}),201

@app.delete("/api/medical-records/<int:id>")
@admin
def delete_record(id):
    if not q("SELECT id FROM medical_records WHERE id=%s",(id,),True):return err("Medical record not found",code=404)
    q("DELETE FROM medical_records WHERE id=%s",(id,));return jsonify({"status":200})

# Services
@app.get("/api/services")
@auth
def list_services():return jsonify({"status":200,"data":q("SELECT id,name,description,status FROM health_services ORDER BY name",fetch=True)})

@app.post("/api/services")
@admin
def create_service():
    d=request.get_json() or {}
    if not d.get("name") or not d.get("description"):return err("Name and description are required")
    sid=q("INSERT INTO health_services(name,description,status) VALUES(%s,%s,%s)",(d["name"],d["description"],d.get("status","Active")))
    return jsonify({"status":201,"data":{"id":sid,**d}}),201

@app.delete("/api/services/<int:id>")
@admin
def delete_service(id):
    if not q("SELECT id FROM health_services WHERE id=%s",(id,),True):return err("Service not found",code=404)
    q("DELETE FROM health_services WHERE id=%s",(id,));return jsonify({"status":200})

# Users
@app.get("/api/users")
@admin
def list_users():return jsonify({"status":200,"data":q("SELECT id,username,full_name fullName,role,created_at FROM users ORDER BY id DESC",fetch=True)})

@app.post("/api/users")
@admin
def create_user():
    d=request.get_json() or {}
    if not d.get("username") or not d.get("password") or not d.get("fullName"):return err("Username, password and full name are required")
    try: uid=q("INSERT INTO users(username,password_hash,full_name,role) VALUES(%s,%s,%s,%s)",(d["username"],generate_password_hash(d["password"]),d["fullName"],d.get("role","Staff")))
    except mysql.connector.Error as e:
        if e.errno==1062:return err("Username already exists","username")
        raise
    return jsonify({"status":201,"data":{"id":uid,"username":d["username"],"fullName":d["fullName"],"role":d.get("role","Staff")}}),201

@app.delete("/api/users/<int:id>")
@admin
def delete_user(id):
    if user()["id"]==id:return err("You cannot delete your own account")
    if not q("SELECT id FROM users WHERE id=%s",(id,),True):return err("User not found",code=404)
    q("DELETE FROM users WHERE id=%s",(id,));return jsonify({"status":200})

if __name__=="__main__":
    app.run(host=os.getenv("APP_HOST","127.0.0.1"),port=int(os.getenv("APP_PORT","5000")),debug=os.getenv("APP_DEBUG","true").lower()=="true")
