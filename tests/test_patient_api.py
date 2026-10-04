import unittest

from app import app, patients


class PatientApiReviewTests(unittest.TestCase):
    def setUp(self):
        patients.clear()
        self.client = app.test_client()

    def patient_payload(self, first_name="Juan"):
        return {
            "firstName": first_name,
            "lastName": "Dela Cruz",
            "dateOfBirth": "2000-01-15",
            "gender": "Male",
            "contactNumber": "09123456789",
            "address": "Barangay Sample"
        }

    def test_create_returns_201(self):
        response = self.client.post("/patients", json=self.patient_payload())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["data"]["id"], 1)

    def test_validation_returns_422(self):
        response = self.client.post("/patients", json={"firstName": ""})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()["field"], "firstName")

    def test_missing_patient_returns_404(self):
        response = self.client.get("/patients/999")
        self.assertEqual(response.status_code, 404)

    def test_deleted_id_is_not_reused(self):
        first = self.client.post("/patients", json=self.patient_payload("First"))
        self.assertEqual(first.status_code, 201)

        second = self.client.post("/patients", json=self.patient_payload("Second"))
        self.assertEqual(second.status_code, 201)
        self.assertEqual(second.get_json()["data"]["id"], 2)

        deleted = self.client.delete("/patients/1")
        self.assertEqual(deleted.status_code, 200)

        third = self.client.post("/patients", json=self.patient_payload("Third"))
        self.assertEqual(third.status_code, 201)
        self.assertEqual(third.get_json()["data"]["id"], 3)

    def test_update_missing_patient_returns_404(self):
        response = self.client.put(
            "/patients/999",
            json={"firstName": "Updated"}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
