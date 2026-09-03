from flask import Flask, jsonify, request

app = Flask(__name__)

# Patient data
patients = []


# -------------------------
# Patient Data Functions
# -------------------------

def save_patient(data):
    patient = {
        "id": len(patients) + 1,
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

    return None


def update_patient_by_id(patient_id, data):
    for index, patient in enumerate(patients):
        if patient["id"] == int(patient_id):
            patients[index] = {
                **patient,
                **data
            }

            return patients[index]

    return None


def delete_patient_by_id(patient_id):
    for index, patient in enumerate(patients):
        if patient["id"] == int(patient_id):
            return patients.pop(index)

    return None


# -------------------------
# Patient Handlers
# -------------------------

def list_patients():
    patients_list = get_patients()

    return jsonify({
        "status": 200,
        "data": patients_list
    }), 200


def show_patient(patient_id):
    patient = get_patient_by_id(patient_id)

    if patient is None:
        return jsonify({
            "status": 404,
            "error": "Patient not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": patient
    }), 200


def create_patient():
    data = request.get_json()

    patient = save_patient(data)

    return jsonify({
        "status": 201,
        "data": patient
    }), 201


def update_patient(patient_id):
    data = request.get_json()

    patient = update_patient_by_id(patient_id, data)

    if patient is None:
        return jsonify({
            "status": 404,
            "error": "Patient not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": patient
    }), 200


def delete_patient(patient_id):
    patient = delete_patient_by_id(patient_id)

    if patient is None:
        return jsonify({
            "status": 404,
            "error": "Patient not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": patient
    }), 200


# -------------------------
# Patient Routes
# -------------------------

app.add_url_rule(
    "/patients",
    "list_patients",
    list_patients,
    methods=["GET"]
)

app.add_url_rule(
    "/patients/<int:patient_id>",
    "show_patient",
    show_patient,
    methods=["GET"]
)

app.add_url_rule(
    "/patients",
    "create_patient",
    create_patient,
    methods=["POST"]
)

app.add_url_rule(
    "/patients/<int:patient_id>",
    "update_patient",
    update_patient,
    methods=["PUT"]
)

app.add_url_rule(
    "/patients/<int:patient_id>",
    "delete_patient",
    delete_patient,
    methods=["DELETE"]
)


# -------------------------
# Start Flask
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
