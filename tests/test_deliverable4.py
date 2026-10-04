import unittest

from app import app, patients, appointments, medical_records, health_services, users


class Deliverable4QATestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        patients.clear()
        appointments.clear()
        medical_records.clear()
        health_services.clear()
        users.clear()

    def tearDown(self):
        patients.clear()
        appointments.clear()
        medical_records.clear()
        health_services.clear()
        users.clear()

    def patient_payload(self):
        return {
            "firstName": "Ana",
            "lastName": "Santos",
            "dateOfBirth": "2000-05-20",
            "gender": "Female",
            "contactNumber": "09123456789",
            "address": "Barangay Health Center"
        }

    def create_patient(self):
        response = self.client.post("/patients", json=self.patient_payload())
        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["id"]

    def test_patient_full_crud(self):
        created = self.client.post("/patients", json=self.patient_payload())
        self.assertEqual(created.status_code, 201)
        patient_id = created.get_json()["data"]["id"]

        listed = self.client.get("/patients")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.get_json()["data"]), 1)

        detail = self.client.get(f"/patients/{patient_id}")
        self.assertEqual(detail.status_code, 200)

        updated = self.client.put(
            f"/patients/{patient_id}",
            json={"address": "Updated Barangay Address"}
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["data"]["address"], "Updated Barangay Address")

        deleted = self.client.delete(f"/patients/{patient_id}")
        self.assertEqual(deleted.status_code, 200)

        missing = self.client.get(f"/patients/{patient_id}")
        self.assertEqual(missing.status_code, 404)

    def test_patient_missing_required_field(self):
        payload = self.patient_payload()
        payload.pop("lastName")
        response = self.client.post("/patients", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["field"], "lastName")

    def test_patient_bad_phone(self):
        payload = self.patient_payload()
        payload["contactNumber"] = "123"
        response = self.client.post("/patients", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_appointment_full_crud(self):
        patient_id = self.create_patient()
        payload = {
            "patientId": patient_id,
            "appointmentDate": "2026-10-20",
            "appointmentTime": "09:00",
            "service": "Medical Checkup",
            "status": "Scheduled"
        }
        created = self.client.post("/appointments", json=payload)
        self.assertEqual(created.status_code, 201)
        appointment_id = created.get_json()["data"]["id"]

        self.assertEqual(self.client.get("/appointments").status_code, 200)
        self.assertEqual(self.client.get(f"/appointments/{appointment_id}").status_code, 200)

        updated = self.client.put(
            f"/appointments/{appointment_id}",
            json={"status": "Completed"}
        )
        self.assertEqual(updated.status_code, 200)

        deleted = self.client.delete(f"/appointments/{appointment_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(self.client.get(f"/appointments/{appointment_id}").status_code, 404)

    def test_appointment_rejects_unknown_patient(self):
        response = self.client.post("/appointments", json={
            "patientId": 999,
            "appointmentDate": "2026-10-20",
            "appointmentTime": "09:00",
            "service": "Checkup",
            "status": "Scheduled"
        })
        self.assertEqual(response.status_code, 422)

    def test_appointment_rejects_bad_status(self):
        patient_id = self.create_patient()
        response = self.client.post("/appointments", json={
            "patientId": patient_id,
            "appointmentDate": "2026-10-20",
            "appointmentTime": "09:00",
            "service": "Checkup",
            "status": "Unknown"
        })
        self.assertEqual(response.status_code, 422)

    def test_medical_record_full_crud(self):
        patient_id = self.create_patient()
        payload = {
            "patientId": patient_id,
            "diagnosis": "Fever",
            "treatment": "Rest",
            "recordDate": "2026-10-20"
        }
        created = self.client.post("/medical-records", json=payload)
        self.assertEqual(created.status_code, 201)
        record_id = created.get_json()["data"]["id"]

        self.assertEqual(self.client.get("/medical-records").status_code, 200)
        self.assertEqual(self.client.get(f"/medical-records/{record_id}").status_code, 200)

        updated = self.client.put(
            f"/medical-records/{record_id}",
            json={"diagnosis": "Updated Diagnosis"}
        )
        self.assertEqual(updated.status_code, 200)

        deleted = self.client.delete(f"/medical-records/{record_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(self.client.get(f"/medical-records/{record_id}").status_code, 404)

    def test_medical_record_rejects_empty_diagnosis(self):
        patient_id = self.create_patient()
        response = self.client.post("/medical-records", json={
            "patientId": patient_id,
            "diagnosis": "",
            "treatment": "Rest",
            "recordDate": "2026-10-20"
        })
        self.assertEqual(response.status_code, 422)

    def test_health_service_full_crud(self):
        payload = {
            "name": "Prenatal Checkup",
            "description": "Basic prenatal consultation",
            "status": "Active"
        }
        created = self.client.post("/health-services", json=payload)
        self.assertEqual(created.status_code, 201)
        service_id = created.get_json()["data"]["id"]

        self.assertEqual(self.client.get("/health-services").status_code, 200)
        self.assertEqual(self.client.get(f"/health-services/{service_id}").status_code, 200)

        updated = self.client.put(
            f"/health-services/{service_id}",
            json={"status": "Inactive"}
        )
        self.assertEqual(updated.status_code, 200)

        deleted = self.client.delete(f"/health-services/{service_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(self.client.get(f"/health-services/{service_id}").status_code, 404)

    def test_health_service_rejects_invalid_status(self):
        response = self.client.post("/health-services", json={
            "name": "Vaccination",
            "description": "Vaccination service",
            "status": "Unknown"
        })
        self.assertEqual(response.status_code, 422)

    def test_user_full_crud(self):
        payload = {
            "username": "staffqa",
            "password": "password123",
            "role": "Staff"
        }
        created = self.client.post("/users", json=payload)
        self.assertEqual(created.status_code, 201)
        user_id = created.get_json()["data"]["id"]

        self.assertEqual(self.client.get("/users").status_code, 200)
        self.assertEqual(self.client.get(f"/users/{user_id}").status_code, 200)

        updated = self.client.put(
            f"/users/{user_id}",
            json={"role": "Administrator"}
        )
        self.assertEqual(updated.status_code, 200)

        deleted = self.client.delete(
            f"/users/{user_id}",
            headers={"X-User-Role": "Administrator"}
        )
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(self.client.get(f"/users/{user_id}").status_code, 404)

    def test_user_delete_requires_admin(self):
        created = self.client.post("/users", json={
            "username": "staffqa",
            "password": "password123",
            "role": "Staff"
        })
        user_id = created.get_json()["data"]["id"]

        response = self.client.delete(
            f"/users/{user_id}",
            headers={"X-User-Role": "Staff"}
        )
        self.assertEqual(response.status_code, 403)

    def test_unknown_routes_return_404(self):
        response = self.client.get("/this-route-does-not-exist")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
