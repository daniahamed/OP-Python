from flask import Blueprint, request, jsonify
from src.controllers.book_c import (get_books, get_book_by_id, create_book, update_book, delete_book, transfer_book)

books_bp = Blueprint("books", __name__)

# Get all books (with optional filters)
@books_bp.route("/books", methods=["GET"])
def get_books_route():
    author = request.args.get("author")
    title = request.args.get("title")
    library_id = request.args.get("library_id")
    try:
        books = get_books(author=author, title=title, library_id=library_id)
        return jsonify([
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "library_id": b.library_id,
                "created_at": b.created_at.isoformat()
            } for b in books
        ])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Get single book
@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book_route(book_id):
    try:
        book = get_book_by_id(book_id)
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Create book
@books_bp.route("/books", methods=["POST"])
def create_book_route():
    data = request.get_json()
    try:
        book = create_book(
            title=data.get("title"),
            author=data.get("author"),
            library_id=data.get("library_id")
        )
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Update book
@books_bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book_route(book_id):
    data = request.get_json()
    try:
        book = update_book(
            book_id,
            title=data.get("title"),
            author=data.get("author"),
            library_id=data.get("library_id")
        )
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Delete book
@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_route(book_id):
    try:
        delete_book(book_id)
        return jsonify({"message": "Book deleted"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Transfer book to another library
@books_bp.route("/books/<int:book_id>/transfer", methods=["POST"])
def transfer_book_route(book_id):
    data = request.get_json()
    target_library_id = data.get("target_library_id")
    try:
        book = transfer_book(book_id, target_library_id)
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



