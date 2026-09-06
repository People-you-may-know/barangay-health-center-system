import unittest

from app import (
    app,
    patients,
    appointments,
    medical_records,
    health_services,
    users
)


class AppTestCase(unittest.TestCase):

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

    # =========================
    # Helper
    # =========================

    def create_patient(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-01",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Bukidnon"
            }
        )

        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["id"]

    # =========================
    # Patient Tests
    # =========================

    def test_create_patient_success(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-01",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Bukidnon"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], 201)

    def test_create_patient_validation_failure(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-01",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Bukidnon"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_create_patient_invalid_contact_number(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-01",
                "gender": "Male",
                "contactNumber": "12345",
                "address": "Bukidnon"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_update_patient_validation_failure(self):
        patient_id = self.create_patient()

        response = self.client.put(
            f"/patients/{patient_id}",
            json={
                "contactNumber": "123"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_patient_not_found(self):
        response = self.client.put(
            "/patients/999",
            json={
                "firstName": "Updated"
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    def test_get_patient_not_found(self):
        response = self.client.get("/patients/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    # =========================
    # Appointment Tests
    # =========================

    def test_create_appointment_success(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/appointments",
            json={
                "patientId": patient_id,
                "appointmentDate": "2026-09-10",
                "appointmentTime": "09:00",
                "service": "Medical Checkup",
                "status": "Scheduled"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], 201)

    def test_create_appointment_invalid_patient(self):
        response = self.client.post(
            "/appointments",
            json={
                "patientId": 999,
                "appointmentDate": "2026-09-10",
                "appointmentTime": "09:00",
                "service": "Medical Checkup",
                "status": "Scheduled"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_update_appointment_validation_failure(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/appointments",
            json={
                "patientId": patient_id,
                "appointmentDate": "2026-09-10",
                "appointmentTime": "09:00",
                "service": "Medical Checkup",
                "status": "Scheduled"
            }
        )

        appointment_id = response.get_json()["data"]["id"]

        response = self.client.put(
            f"/appointments/{appointment_id}",
            json={
                "status": "Invalid"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_appointment_not_found(self):
        response = self.client.put(
            "/appointments/999",
            json={
                "status": "Completed"
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    # =========================
    # Medical Record Tests
    # =========================

    def test_create_medical_record_success(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/medical-records",
            json={
                "patientId": patient_id,
                "diagnosis": "Fever",
                "treatment": "Rest and medication",
                "recordDate": "2026-09-10"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], 201)

    def test_create_medical_record_invalid_patient(self):
        response = self.client.post(
            "/medical-records",
            json={
                "patientId": 999,
                "diagnosis": "Fever",
                "treatment": "Rest and medication",
                "recordDate": "2026-09-10"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_update_medical_record_validation_failure(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/medical-records",
            json={
                "patientId": patient_id,
                "diagnosis": "Fever",
                "treatment": "Rest",
                "recordDate": "2026-09-10"
            }
        )

        record_id = response.get_json()["data"]["id"]

        response = self.client.put(
            f"/medical-records/{record_id}",
            json={
                "diagnosis": ""
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_medical_record_not_found(self):
        response = self.client.put(
            "/medical-records/999",
            json={
                "diagnosis": "Updated Diagnosis"
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    # =========================
    # Health Service Tests
    # =========================

    def test_create_health_service_success(self):
        response = self.client.post(
            "/health-services",
            json={
                "name": "Medical Checkup",
                "description": "Basic health consultation",
                "status": "Active"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], 201)

    def test_create_health_service_validation_failure(self):
        response = self.client.post(
            "/health-services",
            json={
                "name": "",
                "description": "Basic health consultation",
                "status": "Active"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_health_service_validation_failure(self):
        response = self.client.post(
            "/health-services",
            json={
                "name": "Medical Checkup",
                "description": "Basic health consultation",
                "status": "Active"
            }
        )

        service_id = response.get_json()["data"]["id"]

        response = self.client.put(
            f"/health-services/{service_id}",
            json={
                "name": ""
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_health_service_not_found(self):
        response = self.client.put(
            "/health-services/999",
            json={
                "name": "Updated Service"
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    # =========================
    # User Tests
    # =========================

    def test_create_user_success(self):
        response = self.client.post(
            "/users",
            json={
                "username": "admin",
                "password": "password123",
                "role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], 201)

    def test_create_user_invalid_password(self):
        response = self.client.post(
            "/users",
            json={
                "username": "admin",
                "password": "123",
                "role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_update_user_validation_failure(self):
        response = self.client.post(
            "/users",
            json={
                "username": "admin",
                "password": "password123",
                "role": "Administrator"
            }
        )

        user_id = response.get_json()["data"]["id"]

        response = self.client.put(
            f"/users/{user_id}",
            json={
                "password": "123"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())

    def test_update_user_not_found(self):
        response = self.client.put(
            "/users/999",
            json={
                "username": "updateduser"
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["status"], 404)
        self.assertIn("error", response.get_json())

    def test_delete_user_without_authorization(self):
        response = self.client.post(
            "/users",
            json={
                "username": "admin",
                "password": "password123",
                "role": "Administrator"
            }
        )

        user_id = response.get_json()["data"]["id"]

        response = self.client.delete(
            f"/users/{user_id}"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()["status"], 403)

    def test_delete_user_with_authorization(self):
        response = self.client.post(
            "/users",
            json={
                "username": "admin",
                "password": "password123",
                "role": "Administrator"
            }
        )

        user_id = response.get_json()["data"]["id"]

        response = self.client.delete(
            f"/users/{user_id}",
            headers={
                "X-User-Role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], 200)


if __name__ == "__main__":
    unittest.main()
