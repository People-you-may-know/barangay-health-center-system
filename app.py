from flask import Flask, jsonify, request

app = Flask(__name__)


# =====================================================
# STANDARD VALIDATION ERROR
# =====================================================

def validation_error(message, field):
    return jsonify({
        "status": 422,
        "error": message,
        "field": field
    }), 422


# =====================================================
# PATIENT MANAGEMENT
# =====================================================

patients = []


def save_patient(data):
    # Use the highest existing ID + 1 so deleting a record
    # cannot cause a later create to reuse an existing ID.
    next_id = max((patient["id"] for patient in patients), default=0) + 1
    patient = {
        "id": next_id,
        **data
    }
    patients.append(patient)
    return patient


def get_patients():
    return patients


def get_patient_by_id(patient_id):
    for patient in patients:
        if patient["id"] == int(patient_id):
            return patient
