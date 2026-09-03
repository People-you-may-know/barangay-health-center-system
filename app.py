from flask import Flask, jsonify, request

app = Flask(__name__)


# GET /patients
def list_patients():
    return jsonify({
        "status": 200,
        "data": []
    }), 200


# GET /patients/<id>
def show_patient(patient_id):
    return jsonify({
        "status": 200,
        "data": {
            "id": patient_id
        }
    }), 200


# POST /patients
def create_patient():
    patient = request.get_json()

    return jsonify({
        "status": 201,
        "data": patient
    }), 201


# PUT /patients/<id>
def update_patient(patient_id):
    patient = request.get_json()

    return jsonify({
        "status": 200,
        "data": {
            "id": patient_id,
            **patient
        }
    }), 200


# DELETE /patients/<id>
def delete_patient(patient_id):
    return jsonify({
        "status": 200,
        "data": {
            "id": patient_id
        }
    }), 200


# Routes
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


if __name__ == "__main__":
    app.run(debug=True)
