from flask import jsonify, request

from app import (
    users,
    validation_error
)


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
