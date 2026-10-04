import os
import re
import unittest

os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_USER", "root")
os.environ.setdefault("DB_PASSWORD", "")
os.environ.setdefault("DB_NAME", "barangay_health_center_test")

import mysql.connector
from werkzeug.security import generate_password_hash
from app import app, DB


class Deliverable4MySQLTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = os.environ["DB_NAME"]
        root_config = dict(DB)
        root_config.pop("database", None)
        con = mysql.connector.connect(**root_config)
        cur = con.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS `{cls.db_name}`")
        cur.execute(
            f"CREATE DATABASE `{cls.db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cur.close()
        con.close()

        with open("schema.sql", encoding="utf-8") as f:
            schema = f.read()
        statements = [
            s.strip()
            for s in schema.split(";")
            if s.strip()
            and not s.strip().upper().startswith("CREATE DATABASE")
            and not s.strip().upper().startswith("USE BARANGAY_HEALTH_CENTER")
        ]
        con = mysql.connector.connect(**root_config, database=cls.db_name)
        cur = con.cursor()
        for statement in statements:
            cur.execute(statement)
        cur.execute(
            """INSERT INTO users(username,password_hash,full_name,role)
               VALUES(%s,%s,%s,%s)""",
            ("adminqa", generate_password_hash("admin12345"), "QA Administrator", "Administrator"),
        )
        con.commit()
        cur.close()
        con.close()

    @classmethod
    def tearDownClass(cls):
        root_config = dict(DB)
        root_config.pop("database", None)
        con = mysql.connector.connect(**root_config)
        cur = con.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS `{cls.db_name}`")
        cur.close()
        con.close()

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        response = self.client.post(
            "/api/login",
            json={"username": "adminqa", "password": "admin12345"},
        )
        self.assertEqual(response.status_code, 200)

    def create_patient(self):
        response = self.client.post(
            "/api/patients",
            json={
                "firstName": "Ana",
                "lastName": "Santos",
                "dateOfBirth": "2000-05-20",
                "gender": "Female",
                "contactNumber": "09123456789",
                "address": "Barangay Health Center",
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["id"]

    def test_dashboard_returns_all_summary_sections(self):
        response = self.client.get("/api/dashboard")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()["data"]
        for key in [
            "patients", "appointments", "medicalRecords", "services", "users",
            "todayAppointments", "scheduledAppointments", "completedAppointments",
            "cancelledAppointments", "upcomingAppointments", "recentPatients",
            "recentRecords", "serviceSummary",
        ]:
            self.assertIn(key, data)

    def test_patient_crud(self):
        patient_id = self.create_patient()
        self.assertEqual(self.client.get("/api/patients").status_code, 200)
        self.assertEqual(self.client.get(f"/api/patients/{patient_id}").status_code, 404)
        updated = self.client.put(
            f"/api/patients/{patient_id}",
            json={"address": "Updated Health Center Address"},
        )
        self.assertEqual(updated.status_code, 200)
        deleted = self.client.delete(f"/api/patients/{patient_id}")
        self.assertEqual(deleted.status_code, 200)

    def test_appointment_and_medical_record_workflow(self):
        patient_id = self.create_patient()
        appointment = self.client.post(
            "/api/appointments",
            json={
                "patientId": patient_id,
                "appointmentDate": "2026-10-20",
                "appointmentTime": "09:00",
                "service": "General Consultation",
                "status": "Scheduled",
                "notes": "QA appointment",
            },
        )
        self.assertEqual(appointment.status_code, 201)
        appointment_id = appointment.get_json()["data"]["id"]
        self.assertEqual(
            self.client.put(
                f"/api/appointments/{appointment_id}",
                json={"status": "Completed"},
            ).status_code,
            200,
        )

        record = self.client.post(
            "/api/medical-records",
            json={
                "patientId": patient_id,
                "diagnosis": "Fever",
                "treatment": "Rest and fluids",
                "recordDate": "2026-10-20",
                "notes": "QA record",
            },
        )
        self.assertEqual(record.status_code, 201)
        record_id = record.get_json()["data"]["id"]
        self.assertEqual(
            self.client.put(
                f"/api/medical-records/{record_id}",
                json={"diagnosis": "Updated diagnosis"},
            ).status_code,
            200,
        )

    def test_validation_and_not_found(self):
        bad = self.client.post(
            "/api/patients",
            json={
                "firstName": "Ana",
                "lastName": "Santos",
                "dateOfBirth": "2026-02-31",
                "gender": "Female",
                "contactNumber": "09123456789",
                "address": "Health Center",
            },
        )
        self.assertEqual(bad.status_code, 422)
        self.assertEqual(
            self.client.get("/api/patients/999999").status_code,
            404,
        )

    def test_service_and_user_management(self):
        service = self.client.post(
            "/api/services",
            json={
                "name": "QA Consultation",
                "description": "QA service",
                "status": "Active",
            },
        )
        self.assertEqual(service.status_code, 201)
        service_id = service.get_json()["data"]["id"]
        self.assertEqual(
            self.client.put(
                f"/api/services/{service_id}",
                json={"status": "Inactive"},
            ).status_code,
            200,
        )

        user = self.client.post(
            "/api/users",
            json={
                "username": "staffqa",
                "password": "password123",
                "fullName": "QA Staff",
                "role": "Staff",
            },
        )
        self.assertEqual(user.status_code, 201)
        user_id = user.get_json()["data"]["id"]
        self.assertEqual(
            self.client.put(
                f"/api/users/{user_id}",
                json={"fullName": "Updated QA Staff"},
            ).status_code,
            200,
        )

    def test_protected_routes_require_authentication(self):
        self.client.post("/api/logout")
        self.assertEqual(self.client.get("/api/dashboard").status_code, 401)
        self.assertEqual(
            self.client.get("/api/patients").status_code,
            401,
        )


if __name__ == "__main__":
    unittest.main()
