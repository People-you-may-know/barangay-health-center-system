from flask import jsonify, request

from app import (
    health_services,
    validation_error
)


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
