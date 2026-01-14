from flask import Blueprint, request, jsonify
from src.controllers.library_c import (create_library, get_all_libraries, get_library_by_id, update_library, delete_library)

libraries_bp = Blueprint("libraries", __name__)

# Get all libraries
@libraries_bp.route("/libraries", methods=["GET"])
def get_libraries_route():
    libraries = get_all_libraries()
    return jsonify([
        {
            "id": lib.id,
            "name": lib.name,
            "owner_id": lib.owner_id
        } for lib in libraries
    ])


# Get single library
@libraries_bp.route("/libraries/<int:library_id>", methods=["GET"])
def get_library_route(library_id):
    try:
        library = get_library_by_id(library_id)
        books = [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "created_at": b.created_at.isoformat()
            }
            for b in library.books
        ]
        return jsonify({
            "id": library.id,
            "name": library.name,
            "owner_id": library.owner_id,
            "books": books
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Create library
@libraries_bp.route("/libraries", methods=["POST"])
def create_library_route():
    data = request.get_json()
    try:
        library = create_library(
            name=data.get("name"),
            owner_id=data.get("owner_id")
        )
        return jsonify({
            "id": library.id,
            "name": library.name,
            "owner_id": library.owner_id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Update library
@libraries_bp.route("/libraries/<int:library_id>", methods=["PUT"])
def update_library_route(library_id):
    data = request.get_json()
    try:
        library = update_library(
            library_id,
            name=data.get("name"),
            owner_id=data.get("owner_id")
        )
        return jsonify({
            "id": library.id,
            "name": library.name,
            "owner_id": library.owner_id
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Delete library
@libraries_bp.route("/libraries/<int:library_id>", methods=["DELETE"])
def delete_library_route(library_id):
    try:
        delete_library(library_id)
        return jsonify({"message": "Library deleted"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Get books for a library
@libraries_bp.route("/libraries/<int:library_id>/books", methods=["GET"])
def get_library_books_route(library_id):
    try:
        library = get_library_by_id(library_id)
        books = [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "library_id": b.library_id,
                "created_at": b.created_at.isoformat()
            }
            for b in library.books
        ]
        return jsonify(books)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

