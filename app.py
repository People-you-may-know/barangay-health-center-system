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


def list_patients():
    return jsonify({
        "status": 200,
        "data": get_patients()
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
    data = request.get_json() or {}

    if "firstName" not in data:
        return validation_error("firstName is required", "firstName")

    if not isinstance(data["firstName"], str):
        return validation_error("firstName must be a string", "firstName")

    if not 1 <= len(data["firstName"]) <= 50:
        return validation_error(
            "firstName must be 1-50 characters",
            "firstName"
        )

    if "lastName" not in data:
        return validation_error("lastName is required", "lastName")

    if not isinstance(data["lastName"], str):
        return validation_error("lastName must be a string", "lastName")

    if not 1 <= len(data["lastName"]) <= 50:
        return validation_error(
            "lastName must be 1-50 characters",
            "lastName"
        )

    if "dateOfBirth" not in data:
        return validation_error(
            "dateOfBirth is required",
            "dateOfBirth"
        )

    if not isinstance(data["dateOfBirth"], str):
        return validation_error(
            "dateOfBirth must be a string",
            "dateOfBirth"
        )

    if len(data["dateOfBirth"]) != 10:
        return validation_error(
            "dateOfBirth must use YYYY-MM-DD format",
            "dateOfBirth"
        )

    if "gender" not in data:
        return validation_error("gender is required", "gender")

    if data["gender"] not in ["Male", "Female", "Other"]:
        return validation_error(
            "gender must be Male, Female, or Other",
            "gender"
        )

    if "contactNumber" not in data:
        return validation_error(
            "contactNumber is required",
            "contactNumber"
        )

    if not isinstance(data["contactNumber"], str):
        return validation_error(
            "contactNumber must be a string",
            "contactNumber"
        )

    if (
        len(data["contactNumber"]) != 11
        or not data["contactNumber"].isdigit()
        or not data["contactNumber"].startswith("09")
    ):
        return validation_error(
            "contactNumber must be 11 digits and start with 09",
            "contactNumber"
        )

    if "address" not in data:
        return validation_error("address is required", "address")

    if not isinstance(data["address"], str):
        return validation_error("address must be a string", "address")

    if not 5 <= len(data["address"]) <= 200:
        return validation_error(
            "address must be 5-200 characters",
            "address"
        )

    patient = save_patient(data)

    return jsonify({
        "status": 201,
        "data": patient
    }), 201


def update_patient(patient_id):
    data = request.get_json() or {}

    if "firstName" in data:
        if not isinstance(data["firstName"], str):
            return validation_error(
                "firstName must be a string",
                "firstName"
            )

        if not 1 <= len(data["firstName"]) <= 50:
            return validation_error(
                "firstName must be 1-50 characters",
                "firstName"
            )

    if "lastName" in data:
        if not isinstance(data["lastName"], str):
            return validation_error(
                "lastName must be a string",
                "lastName"
            )

        if not 1 <= len(data["lastName"]) <= 50:
            return validation_error(
                "lastName must be 1-50 characters",
                "lastName"
            )

    if "dateOfBirth" in data:
        if not isinstance(data["dateOfBirth"], str):
            return validation_error(
                "dateOfBirth must be a string",
                "dateOfBirth"
            )

        if len(data["dateOfBirth"]) != 10:
            return validation_error(
                "dateOfBirth must use YYYY-MM-DD format",
                "dateOfBirth"
            )

    if "gender" in data:
        if data["gender"] not in ["Male", "Female", "Other"]:
            return validation_error(
                "gender must be Male, Female, or Other",
                "gender"
            )

    if "contactNumber" in data:
        if not isinstance(data["contactNumber"], str):
            return validation_error(
                "contactNumber must be a string",
                "contactNumber"
            )

        if (
            len(data["contactNumber"]) != 11
            or not data["contactNumber"].isdigit()
            or not data["contactNumber"].startswith("09")
        ):
            return validation_error(
                "contactNumber must be 11 digits and start with 09",
                "contactNumber"
            )

    if "address" in data:
        if not isinstance(data["address"], str):
            return validation_error(
                "address must be a string",
                "address"
            )

        if not 5 <= len(data["address"]) <= 200:
            return validation_error(
                "address must be 5-200 characters",
                "address"
            )

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


# =====================================================
# APPOINTMENT MANAGEMENT
# =====================================================

appointments = []


def save_appointment(data):
    appointment = {
        "id": len(appointments) + 1,
        **data
    }
    appointments.append(appointment)
    return appointment


def get_appointments():
    return appointments


def get_appointment_by_id(appointment_id):
    for appointment in appointments:
        if appointment["id"] == int(appointment_id):
            return appointment
    return None


def update_appointment_by_id(appointment_id, data):
    for index, appointment in enumerate(appointments):
        if appointment["id"] == int(appointment_id):
            appointments[index] = {
                **appointment,
                **data
            }
            return appointments[index]
    return None


def delete_appointment_by_id(appointment_id):
    for index, appointment in enumerate(appointments):
        if appointment["id"] == int(appointment_id):
            return appointments.pop(index)
    return None


def list_appointments():
    return jsonify({
        "status": 200,
        "data": get_appointments()
    }), 200


def show_appointment(appointment_id):
    appointment = get_appointment_by_id(appointment_id)

    if appointment is None:
        return jsonify({
            "status": 404,
            "error": "Appointment not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": appointment
    }), 200


def create_appointment():
    data = request.get_json() or {}

    if "patientId" not in data:
        return validation_error(
            "patientId is required",
            "patientId"
        )

    try:
        patient_id = int(data["patientId"])
    except (TypeError, ValueError):
        return validation_error(
            "patientId must be a valid patient ID",
            "patientId"
        )

    if get_patient_by_id(patient_id) is None:
        return validation_error(
            "patientId must reference an existing patient",
            "patientId"
        )

    if "appointmentDate" not in data:
        return validation_error(
            "appointmentDate is required",
            "appointmentDate"
        )

    if not isinstance(data["appointmentDate"], str):
        return validation_error(
            "appointmentDate must be a string",
            "appointmentDate"
        )

    if len(data["appointmentDate"]) != 10:
        return validation_error(
            "appointmentDate must use YYYY-MM-DD format",
            "appointmentDate"
        )

    if "appointmentTime" not in data:
        return validation_error(
            "appointmentTime is required",
            "appointmentTime"
        )

    if not isinstance(data["appointmentTime"], str):
        return validation_error(
            "appointmentTime must be a string",
            "appointmentTime"
        )

    if len(data["appointmentTime"]) != 5:
        return validation_error(
            "appointmentTime must use HH:MM format",
            "appointmentTime"
        )

    if "service" not in data:
        return validation_error(
            "service is required",
            "service"
        )

    if not isinstance(data["service"], str):
        return validation_error(
            "service must be a string",
            "service"
        )

    if not 1 <= len(data["service"]) <= 100:
        return validation_error(
            "service must be 1-100 characters",
            "service"
        )

    if "status" not in data:
        return validation_error(
            "status is required",
            "status"
        )

    if data["status"] not in [
        "Scheduled",
        "Completed",
        "Cancelled"
    ]:
        return validation_error(
            "status must be Scheduled, Completed, or Cancelled",
            "status"
        )

    appointment = save_appointment(data)

    return jsonify({
        "status": 201,
        "data": appointment
    }), 201


def update_appointment(appointment_id):
    data = request.get_json() or {}

    if "patientId" in data:
        try:
            patient_id = int(data["patientId"])
        except (TypeError, ValueError):
            return validation_error(
                "patientId must be a valid patient ID",
                "patientId"
            )

        if get_patient_by_id(patient_id) is None:
            return validation_error(
                "patientId must reference an existing patient",
                "patientId"
            )

    if "appointmentDate" in data:
        if not isinstance(data["appointmentDate"], str):
            return validation_error(
                "appointmentDate must be a string",
                "appointmentDate"
            )

        if len(data["appointmentDate"]) != 10:
            return validation_error(
                "appointmentDate must use YYYY-MM-DD format",
                "appointmentDate"
            )

    if "appointmentTime" in data:
        if not isinstance(data["appointmentTime"], str):
            return validation_error(
                "appointmentTime must be a string",
                "appointmentTime"
            )

        if len(data["appointmentTime"]) != 5:
            return validation_error(
                "appointmentTime must use HH:MM format",
                "appointmentTime"
            )

    if "service" in data:
        if not isinstance(data["service"], str):
            return validation_error(
                "service must be a string",
                "service"
            )

        if not 1 <= len(data["service"]) <= 100:
            return validation_error(
                "service must be 1-100 characters",
                "service"
            )

    if "status" in data:
        if data["status"] not in [
            "Scheduled",
            "Completed",
            "Cancelled"
        ]:
            return validation_error(
                "status must be Scheduled, Completed, or Cancelled",
                "status"
            )

    appointment = update_appointment_by_id(
        appointment_id,
        data
    )

    if appointment is None:
        return jsonify({
            "status": 404,
            "error": "Appointment not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": appointment
    }), 200


def delete_appointment(appointment_id):
    appointment = delete_appointment_by_id(appointment_id)

    if appointment is None:
        return jsonify({
            "status": 404,
            "error": "Appointment not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": appointment
    }), 200


# =====================================================
# MEDICAL RECORDS MANAGEMENT
# =====================================================

medical_records = []


def save_medical_record(data):
    record = {
        "id": len(medical_records) + 1,
        **data
    }
    medical_records.append(record)
    return record


def get_medical_records():
    return medical_records


def get_medical_record_by_id(record_id):
    for record in medical_records:
        if record["id"] == int(record_id):
            return record
    return None


def update_medical_record_by_id(record_id, data):
    for index, record in enumerate(medical_records):
        if record["id"] == int(record_id):
            medical_records[index] = {
                **record,
                **data
            }
            return medical_records[index]
    return None


def delete_medical_record_by_id(record_id):
    for index, record in enumerate(medical_records):
        if record["id"] == int(record_id):
            return medical_records.pop(index)
    return None


def list_medical_records():
    return jsonify({
        "status": 200,
        "data": get_medical_records()
    }), 200


def show_medical_record(record_id):
    record = get_medical_record_by_id(record_id)

    if record is None:
        return jsonify({
            "status": 404,
            "error": "Medical record not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": record
    }), 200


def create_medical_record():
    data = request.get_json() or {}

    if "patientId" not in data:
        return validation_error(
            "patientId is required",
            "patientId"
        )

    try:
        patient_id = int(data["patientId"])
    except (TypeError, ValueError):
        return validation_error(
            "patientId must be a valid patient ID",
            "patientId"
        )

    if get_patient_by_id(patient_id) is None:
        return validation_error(
            "patientId must reference an existing patient",
            "patientId"
        )

    if "diagnosis" not in data:
        return validation_error(
            "diagnosis is required",
            "diagnosis"
        )

    if not isinstance(data["diagnosis"], str):
        return validation_error(
            "diagnosis must be a string",
            "diagnosis"
        )

    if not 1 <= len(data["diagnosis"]) <= 500:
        return validation_error(
            "diagnosis must be 1-500 characters",
            "diagnosis"
        )

    if "treatment" not in data:
        return validation_error(
            "treatment is required",
            "treatment"
        )

    if not isinstance(data["treatment"], str):
        return validation_error(
            "treatment must be a string",
            "treatment"
        )

    if not 1 <= len(data["treatment"]) <= 500:
        return validation_error(
            "treatment must be 1-500 characters",
            "treatment"
        )

    if "recordDate" not in data:
        return validation_error(
            "recordDate is required",
            "recordDate"
        )

    if not isinstance(data["recordDate"], str):
        return validation_error(
            "recordDate must be a string",
            "recordDate"
        )

    if len(data["recordDate"]) != 10:
        return validation_error(
            "recordDate must use YYYY-MM-DD format",
            "recordDate"
        )

    record = save_medical_record(data)

    return jsonify({
        "status": 201,
        "data": record
    }), 201


def update_medical_record(record_id):
    data = request.get_json() or {}

    if "patientId" in data:
        try:
            patient_id = int(data["patientId"])
        except (TypeError, ValueError):
            return validation_error(
                "patientId must be a valid patient ID",
                "patientId"
            )

        if get_patient_by_id(patient_id) is None:
            return validation_error(
                "patientId must reference an existing patient",
                "patientId"
            )

    if "diagnosis" in data:
        if not isinstance(data["diagnosis"], str):
            return validation_error(
                "diagnosis must be a string",
                "diagnosis"
            )

        if not 1 <= len(data["diagnosis"]) <= 500:
            return validation_error(
                "diagnosis must be 1-500 characters",
                "diagnosis"
            )

    if "treatment" in data:
        if not isinstance(data["treatment"], str):
            return validation_error(
                "treatment must be a string",
                "treatment"
            )

        if not 1 <= len(data["treatment"]) <= 500:
            return validation_error(
                "treatment must be 1-500 characters",
                "treatment"
            )

    if "recordDate" in data:
        if not isinstance(data["recordDate"], str):
            return validation_error(
                "recordDate must be a string",
                "recordDate"
            )

        if len(data["recordDate"]) != 10:
            return validation_error(
                "recordDate must use YYYY-MM-DD format",
                "recordDate"
            )

    record = update_medical_record_by_id(
        record_id,
        data
    )

    if record is None:
        return jsonify({
            "status": 404,
            "error": "Medical record not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": record
    }), 200


def delete_medical_record(record_id):
    record = delete_medical_record_by_id(record_id)

    if record is None:
        return jsonify({
            "status": 404,
            "error": "Medical record not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": record
    }), 200


# =====================================================
# HEALTH SERVICES MANAGEMENT
# =====================================================

health_services = []


def save_health_service(data):
    service = {
        "id": len(health_services) + 1,
        **data
    }
    health_services.append(service)
    return service


def get_health_services():
    return health_services


def get_health_service_by_id(service_id):
    for service in health_services:
        if service["id"] == int(service_id):
            return service
    return None


def update_health_service_by_id(service_id, data):
    for index, service in enumerate(health_services):
        if service["id"] == int(service_id):
            health_services[index] = {
                **service,
                **data
            }
            return health_services[index]
    return None


def delete_health_service_by_id(service_id):
    for index, service in enumerate(health_services):
        if service["id"] == int(service_id):
            return health_services.pop(index)
    return None


def list_health_services():
    return jsonify({
        "status": 200,
        "data": get_health_services()
    }), 200


def show_health_service(service_id):
    service = get_health_service_by_id(service_id)

    if service is None:
        return jsonify({
            "status": 404,
            "error": "Health service not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": service
    }), 200


def create_health_service():
    data = request.get_json() or {}

    if "name" not in data:
        return validation_error(
            "name is required",
            "name"
        )

    if not isinstance(data["name"], str):
        return validation_error(
            "name must be a string",
            "name"
        )

    if not 1 <= len(data["name"]) <= 100:
        return validation_error(
            "name must be 1-100 characters",
            "name"
        )

    if "description" not in data:
        return validation_error(
            "description is required",
            "description"
        )

    if not isinstance(data["description"], str):
        return validation_error(
            "description must be a string",
            "description"
        )

    if not 1 <= len(data["description"]) <= 500:
        return validation_error(
            "description must be 1-500 characters",
            "description"
        )

    if "status" not in data:
        return validation_error(
            "status is required",
            "status"
        )

    if data["status"] not in ["Active", "Inactive"]:
        return validation_error(
            "status must be Active or Inactive",
            "status"
        )

    service = save_health_service(data)

    return jsonify({
        "status": 201,
        "data": service
    }), 201


def update_health_service(service_id):
    data = request.get_json() or {}

    if "name" in data:
        if not isinstance(data["name"], str):
            return validation_error(
                "name must be a string",
                "name"
            )

        if not 1 <= len(data["name"]) <= 100:
            return validation_error(
                "name must be 1-100 characters",
                "name"
            )

    if "description" in data:
        if not isinstance(data["description"], str):
            return validation_error(
                "description must be a string",
                "description"
            )

        if not 1 <= len(data["description"]) <= 500:
            return validation_error(
                "description must be 1-500 characters",
                "description"
            )

    if "status" in data:
        if data["status"] not in ["Active", "Inactive"]:
            return validation_error(
                "status must be Active or Inactive",
                "status"
            )

    service = update_health_service_by_id(
        service_id,
        data
    )

    if service is None:
        return jsonify({
            "status": 404,
            "error": "Health service not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": service
    }), 200


def delete_health_service(service_id):
    service = delete_health_service_by_id(service_id)

    if service is None:
        return jsonify({
            "status": 404,
            "error": "Health service not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": service
    }), 200


# =====================================================
# USER MANAGEMENT
# =====================================================

users = []


def save_user(data):
    user = {
        "id": len(users) + 1,
        **data
    }
    users.append(user)
    return user


def get_users():
    return users


def get_user_by_id(user_id):
    for user in users:
        if user["id"] == int(user_id):
            return user
    return None


def update_user_by_id(user_id, data):
    for index, user in enumerate(users):
        if user["id"] == int(user_id):
            users[index] = {
                **user,
                **data
            }
            return users[index]
    return None


def delete_user_by_id(user_id):
    for index, user in enumerate(users):
        if user["id"] == int(user_id):
            return users.pop(index)
    return None


def list_users():
    return jsonify({
        "status": 200,
        "data": get_users()
    }), 200


def show_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({
            "status": 404,
            "error": "User not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": user
    }), 200


def create_user():
    data = request.get_json() or {}

    if "username" not in data:
        return validation_error(
            "username is required",
            "username"
        )

    if not isinstance(data["username"], str):
        return validation_error(
            "username must be a string",
            "username"
        )

    if not 3 <= len(data["username"]) <= 50:
        return validation_error(
            "username must be 3-50 characters",
            "username"
        )

    if "password" not in data:
        return validation_error(
            "password is required",
            "password"
        )

    if not isinstance(data["password"], str):
        return validation_error(
            "password must be a string",
            "password"
        )

    if not 8 <= len(data["password"]) <= 100:
        return validation_error(
            "password must be 8-100 characters",
            "password"
        )

    if "role" not in data:
        return validation_error(
            "role is required",
            "role"
        )

    if data["role"] not in ["Administrator", "Staff"]:
        return validation_error(
            "role must be Administrator or Staff",
            "role"
        )

    user = save_user(data)

    return jsonify({
        "status": 201,
        "data": user
    }), 201


def update_user(user_id):
    data = request.get_json() or {}

    if "username" in data:
        if not isinstance(data["username"], str):
            return validation_error(
                "username must be a string",
                "username"
            )

        if not 3 <= len(data["username"]) <= 50:
            return validation_error(
                "username must be 3-50 characters",
                "username"
            )

    if "password" in data:
        if not isinstance(data["password"], str):
            return validation_error(
                "password must be a string",
                "password"
            )

        if not 8 <= len(data["password"]) <= 100:
            return validation_error(
                "password must be 8-100 characters",
                "password"
            )

    if "role" in data:
        if data["role"] not in ["Administrator", "Staff"]:
            return validation_error(
                "role must be Administrator or Staff",
                "role"
            )

    user = update_user_by_id(
        user_id,
        data
    )

    if user is None:
        return jsonify({
            "status": 404,
            "error": "User not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": user
    }), 200


def delete_user(user_id):
    # Authorization guard
    user_role = request.headers.get("X-User-Role")

    if user_role != "Administrator":
        return jsonify({
            "status": 403,
            "error": "not allowed",
            "field": "authorization"
        }), 403

    user = delete_user_by_id(user_id)

    if user is None:
        return jsonify({
            "status": 404,
            "error": "User not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": user
    }), 200


# =====================================================
# ROUTES
# =====================================================

# Patient Routes

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


# Appointment Routes

app.add_url_rule(
    "/appointments",
    "list_appointments",
    list_appointments,
    methods=["GET"]
)

app.add_url_rule(
    "/appointments/<int:appointment_id>",
    "show_appointment",
    show_appointment,
    methods=["GET"]
)

app.add_url_rule(
    "/appointments",
    "create_appointment",
    create_appointment,
    methods=["POST"]
)

app.add_url_rule(
    "/appointments/<int:appointment_id>",
    "update_appointment",
    update_appointment,
    methods=["PUT"]
)

app.add_url_rule(
    "/appointments/<int:appointment_id>",
    "delete_appointment",
    delete_appointment,
    methods=["DELETE"]
)


# Medical Records Routes

app.add_url_rule(
    "/medical-records",
    "list_medical_records",
    list_medical_records,
    methods=["GET"]
)

app.add_url_rule(
    "/medical-records/<int:record_id>",
    "show_medical_record",
    show_medical_record,
    methods=["GET"]
)

app.add_url_rule(
    "/medical-records",
    "create_medical_record",
    create_medical_record,
    methods=["POST"]
)

app.add_url_rule(
    "/medical-records/<int:record_id>",
    "update_medical_record",
    update_medical_record,
    methods=["PUT"]
)

app.add_url_rule(
    "/medical-records/<int:record_id>",
    "delete_medical_record",
    delete_medical_record,
    methods=["DELETE"]
)


# Health Services Routes

app.add_url_rule(
    "/health-services",
    "list_health_services",
    list_health_services,
    methods=["GET"]
)

app.add_url_rule(
    "/health-services/<int:service_id>",
    "show_health_service",
    show_health_service,
    methods=["GET"]
)

app.add_url_rule(
    "/health-services",
    "create_health_service",
    create_health_service,
    methods=["POST"]
)

app.add_url_rule(
    "/health-services/<int:service_id>",
    "update_health_service",
    update_health_service,
    methods=["PUT"]
)

app.add_url_rule(
    "/health-services/<int:service_id>",
    "delete_health_service",
    delete_health_service,
    methods=["DELETE"]
)


# User Routes

app.add_url_rule(
    "/users",
    "list_users",
    list_users,
    methods=["GET"]
)

app.add_url_rule(
    "/users/<int:user_id>",
    "show_user",
    show_user,
    methods=["GET"]
)

app.add_url_rule(
    "/users",
    "create_user",
    create_user,
    methods=["POST"]
)

app.add_url_rule(
    "/users/<int:user_id>",
    "update_user",
    update_user,
    methods=["PUT"]
)

app.add_url_rule(
    "/users/<int:user_id>",
    "delete_user",
    delete_user,
    methods=["DELETE"]
)


# =====================================================
# START FLASK
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
