from flask import jsonify, request

from app import (
    medical_records,
    validation_error,
    get_patient_by_id
)


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
