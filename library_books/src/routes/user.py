from flask import Blueprint, request, jsonify
from src.controllers.user_c import (create_user, get_all_users, get_user_by_id, update_user, delete_user, get_user_book_count)

users_bp = Blueprint("users", __name__)

# Get all users
@users_bp.route("/users", methods=["GET"])
def get_users_route():
    users = get_all_users()
    return jsonify([{"id": u.id, "name": u.name} for u in users])


# Get single user
@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify({"id": user.id, "name": user.name})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Create user
@users_bp.route("/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    try:
        user = create_user(data.get("name"))
        return jsonify({"id": user.id, "name": user.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Update user
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    try:
        user = update_user(user_id, name=data.get("name"))
        return jsonify({"id": user.id, "name": user.name})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Delete user
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": "User deleted"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Get user book count
@users_bp.route("/users/<int:user_id>/books/count", methods=["GET"])
def get_user_book_count_route(user_id):
    try:
        count = get_user_book_count(user_id)
        return jsonify({"user_id": user_id, "book_count": count})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

