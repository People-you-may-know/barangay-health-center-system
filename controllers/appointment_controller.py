from flask import jsonify, request

from app import (
    appointments,
    validation_error,
    get_patient_by_id
)


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
