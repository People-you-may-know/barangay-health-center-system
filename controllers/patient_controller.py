from flask import jsonify, request

from app import patients, validation_error


def list_patients():
    return jsonify({
        "status": 200,
        "data": patients
    }), 200


def show_patient(patient_id):
    patient = next(
        (p for p in patients if p["id"] == patient_id),
        None
    )

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

    first_name = data.get("firstName")
    last_name = data.get("lastName")
    date_of_birth = data.get("dateOfBirth")
    gender = data.get("gender")
    contact_number = data.get("contactNumber")
    address = data.get("address")

    if not isinstance(first_name, str) or not 1 <= len(first_name) <= 50:
        return validation_error(
            "firstName is required and must be 1-50 characters",
            "firstName"
        )

    if not isinstance(last_name, str) or not 1 <= len(last_name) <= 50:
        return validation_error(
            "lastName is required and must be 1-50 characters",
            "lastName"
        )

    if not isinstance(date_of_birth, str) or len(date_of_birth) != 10:
        return validation_error(
            "dateOfBirth must use YYYY-MM-DD format",
            "dateOfBirth"
        )

    if gender not in ["Male", "Female", "Other"]:
        return validation_error(
            "gender must be Male, Female, or Other",
            "gender"
        )

    if (
        not isinstance(contact_number, str)
        or len(contact_number) != 11
        or not contact_number.isdigit()
        or not contact_number.startswith("09")
    ):
        return validation_error(
            "contactNumber must be 11 digits and start with 09",
            "contactNumber"
        )

    if not isinstance(address, str) or not 5 <= len(address) <= 200:
        return validation_error(
            "address is required and must be 5-200 characters",
            "address"
        )

    patient = {
        "id": len(patients) + 1,
        "firstName": first_name,
        "lastName": last_name,
        "dateOfBirth": date_of_birth,
        "gender": gender,
        "contactNumber": contact_number,
        "address": address
    }

    patients.append(patient)

    return jsonify({
        "status": 201,
        "data": patient
    }), 201


def update_patient(patient_id):
    patient = next(
        (p for p in patients if p["id"] == patient_id),
        None
    )

    if patient is None:
        return jsonify({
            "status": 404,
            "error": "Patient not found"
        }), 404

    data = request.get_json() or {}

    if "firstName" in data:
        if not isinstance(data["firstName"], str) or not 1 <= len(data["firstName"]) <= 50:
            return validation_error(
                "firstName must be 1-50 characters",
                "firstName"
            )
        patient["firstName"] = data["firstName"]

    if "lastName" in data:
        if not isinstance(data["lastName"], str) or not 1 <= len(data["lastName"]) <= 50:
            return validation_error(
                "lastName must be 1-50 characters",
                "lastName"
            )
        patient["lastName"] = data["lastName"]

    if "dateOfBirth" in data:
        if not isinstance(data["dateOfBirth"], str) or len(data["dateOfBirth"]) != 10:
            return validation_error(
                "dateOfBirth must use YYYY-MM-DD format",
                "dateOfBirth"
            )
        patient["dateOfBirth"] = data["dateOfBirth"]

    if "gender" in data:
        if data["gender"] not in ["Male", "Female", "Other"]:
            return validation_error(
                "gender must be Male, Female, or Other",
                "gender"
            )
        patient["gender"] = data["gender"]

    if "contactNumber" in data:
        if (
            not isinstance(data["contactNumber"], str)
            or len(data["contactNumber"]) != 11
            or not data["contactNumber"].isdigit()
            or not data["contactNumber"].startswith("09")
        ):
            return validation_error(
                "contactNumber must be 11 digits and start with 09",
                "contactNumber"
            )
        patient["contactNumber"] = data["contactNumber"]

    if "address" in data:
        if not isinstance(data["address"], str) or not 5 <= len(data["address"]) <= 200:
            return validation_error(
                "address must be 5-200 characters",
                "address"
            )
        patient["address"] = data["address"]

    return jsonify({
        "status": 200,
        "data": patient
    }), 200


def delete_patient(patient_id):
    patient = next(
        (p for p in patients if p["id"] == patient_id),
        None
    )

    if patient is None:
        return jsonify({
            "status": 404,
            "error": "Patient not found"
        }), 404

    patients.remove(patient)

    return jsonify({
        "status": 200,
        "data": patient
    }), 200
