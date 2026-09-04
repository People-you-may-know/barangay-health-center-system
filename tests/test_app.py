import unittest

from app import (
    app,
    patients,
    appointments,
    medical_records,
    health_services,
    users
)


class TestBarangayHealthCenterSystem(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True

        # Clear data before every test
        patients.clear()
        appointments.clear()
        medical_records.clear()
        health_services.clear()
        users.clear()

        self.client = app.test_client()

    def tearDown(self):
        # Clear data after every test
        patients.clear()
        appointments.clear()
        medical_records.clear()
        health_services.clear()
        users.clear()

    def create_patient(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-15",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Barangay Poblacion"
            }
        )

        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["id"]

    # -------------------------
    # PATIENT TESTS
    # -------------------------

    def test_create_patient_success(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-15",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Barangay Poblacion"
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
                "dateOfBirth": "2000-01-15",
                "gender": "Male",
                "contactNumber": "09123456789",
                "address": "Barangay Poblacion"
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["status"], 422)
        self.assertIn("error", response.get_json())
        self.assertIn("field", response.get_json())

    def test_create_patient_invalid_contact_number(self):
        response = self.client.post(
            "/patients",
            json={
                "firstName": "Juan",
                "lastName": "Dela Cruz",
                "dateOfBirth": "2000-01-15",
                "gender": "Male",
                "contactNumber": "12345",
                "address": "Barangay Poblacion"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_get_patient_not_found(self):
        response = self.client.get("/patients/999")

        self.assertEqual(response.status_code, 404)

    # -------------------------
    # APPOINTMENT TESTS
    # -------------------------

    def test_create_appointment_success(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/appointments",
            json={
                "patientId": patient_id,
                "appointmentDate": "2026-09-10",
                "appointmentTime": "09:00",
                "service": "General Consultation",
                "status": "Scheduled"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_create_appointment_invalid_patient(self):
        response = self.client.post(
            "/appointments",
            json={
                "patientId": 999,
                "appointmentDate": "2026-09-10",
                "appointmentTime": "09:00",
                "service": "General Consultation",
                "status": "Scheduled"
            }
        )

        self.assertEqual(response.status_code, 422)

    # -------------------------
    # MEDICAL RECORD TESTS
    # -------------------------

    def test_create_medical_record_success(self):
        patient_id = self.create_patient()

        response = self.client.post(
            "/medical-records",
            json={
                "patientId": patient_id,
                "diagnosis": "Fever",
                "treatment": "Rest and hydration",
                "recordDate": "2026-09-05"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_create_medical_record_invalid_patient(self):
        response = self.client.post(
            "/medical-records",
            json={
                "patientId": 999,
                "diagnosis": "Fever",
                "treatment": "Rest and hydration",
                "recordDate": "2026-09-05"
            }
        )

        self.assertEqual(response.status_code, 422)

    # -------------------------
    # HEALTH SERVICE TESTS
    # -------------------------

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

    # -------------------------
    # USER TESTS
    # -------------------------

    def test_create_user_success(self):
        response = self.client.post(
            "/users",
            json={
                "username": "adminuser",
                "password": "password123",
                "role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_password(self):
        response = self.client.post(
            "/users",
            json={
                "username": "adminuser",
                "password": "123",
                "role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_delete_user_without_authorization(self):
        # Create a user first
        create_response = self.client.post(
            "/users",
            json={
                "username": "staffuser",
                "password": "password123",
                "role": "Staff"
            }
        )

        user_id = create_response.get_json()["data"]["id"]

        # Try deleting without Administrator role
        response = self.client.delete(
            f"/users/{user_id}"
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_user_with_authorization(self):
        # Create a user first
        create_response = self.client.post(
            "/users",
            json={
                "username": "staffuser",
                "password": "password123",
                "role": "Staff"
            }
        )

        user_id = create_response.get_json()["data"]["id"]

        # Delete as Administrator
        response = self.client.delete(
            f"/users/{user_id}",
            headers={
                "X-User-Role": "Administrator"
            }
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
