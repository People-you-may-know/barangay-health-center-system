import unittest

from app import app, patients


class Week10CriticalPathTests(unittest.TestCase):
    def setUp(self):
        patients.clear()
        self.client = app.test_client()

    def payload(self):
        return {
            "firstName": "Juan",
            "lastName": "Dela Cruz",
            "dateOfBirth": "2000-01-15",
            "gender": "Male",
            "contactNumber": "09123456789",
            "address": "Barangay Sample"
        }

    def create_patient(self):
        response = self.client.post("/patients", json=self.payload())
        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["id"]

    def test_patient_crud_critical_path(self):
        patient_id = self.create_patient()
        self.assertEqual(self.client.get("/patients").status_code, 200)
        self.assertEqual(self.client.get(f"/patients/{patient_id}").status_code, 200)

        updated = self.client.put(
            f"/patients/{patient_id}",
            json={"firstName": "Maria"}
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["data"]["firstName"], "Maria")

        self.assertEqual(
            self.client.delete(f"/patients/{patient_id}").status_code,
            200
        )
        self.assertEqual(
            self.client.get(f"/patients/{patient_id}").status_code,
            404
        )

    def test_validation_and_not_found_paths(self):
        invalid = self.client.post("/patients", json={"firstName": ""})
        self.assertEqual(invalid.status_code, 422)
        self.assertEqual(invalid.get_json()["field"], "firstName")

        self.assertEqual(
            self.client.put("/patients/999", json={"firstName": "Updated"}).status_code,
            404
        )
        self.assertEqual(self.client.delete("/patients/999").status_code, 404)

    def test_user_delete_requires_administrator(self):
        denied = self.client.delete("/users/999")
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(denied.get_json()["field"], "authorization")


if __name__ == "__main__":
    unittest.main()
