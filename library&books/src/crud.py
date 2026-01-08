from flask import request, jsonify
from src.app import create_app, db
from src.models import Library, Book

app = create_app()


@app.route('/libraries', methods=['GET', 'POST', 'PUT', 'DELETE'])
def libraries():
    if request.method == 'GET':
        libraries = Library.query.all()
        result = [{"id": lib.id, "name": lib.name} for lib in libraries]
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400
        library = Library(name=name)
        db.session.add(library)
        db.session.commit()
        return jsonify({"id": library.id, "name": library.name}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        library_id = data.get('id')
        if not library_id:
            return jsonify({"error": "Library id is required"}), 400
        library = Library.query.get_or_404(library_id)

        name = data.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400

        library.name = name
        db.session.commit()
        return jsonify({"id": library.id, "name": library.name})

    elif request.method == 'DELETE':
        data = request.get_json()
        library_id = data.get('id')
        if not library_id:
            return jsonify({"error": "Library id is required"}), 400
        library = Library.query.get_or_404(library_id)
        db.session.delete(library)
        db.session.commit()
        return jsonify({"message": "Library deleted"})
    

@app.route('/books', methods=['GET', 'POST', 'PUT', 'DELETE'])
def books():
    if request.method == 'GET':
        library_id = request.args.get('library_id')  
        search = request.args.get('search') 

        query = Book.query

        if library_id:
            query = query.filter_by(library_id=int(library_id))

        if search:
            search = f"%{search}%"
            query = query.filter(
                db.or_(
                    Book.title.ilike(search),
                    Book.author.ilike(search)
                )
            )

        books = query.all()
        result = []
        for b in books:
            result.append({
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "library_id": b.library_id,
                "created_at": b.created_at.isoformat()
            })
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        library_id = data.get('library_id')

        if not all([title, author, library_id]):
            return jsonify({"error": "Title, author, and library_id are required"}), 400

        library = Library.query.get(library_id)
        if not library:
            return jsonify({"error": "Library not found"}), 404

        book = Book(title=title, author=author, library_id=library_id)
        db.session.add(book)
        db.session.commit()
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id
        }), 201

    elif request.method == 'PUT':
        data = request.get_json()
        book_id = data.get('id')
        if not book_id:
            return jsonify({"error": "Book id is required"}), 400

        book = Book.query.get_or_404(book_id)

        title = data.get('title')
        author = data.get('author')
        library_id = data.get('library_id')

        if title:
            book.title = title
        if author:
            book.author = author
        if library_id:
            library = Library.query.get(library_id)
            if not library:
                return jsonify({"error": "Library not found"}), 404
            book.library_id = library_id

        db.session.commit()
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id
        })

    elif request.method == 'DELETE':
        data = request.get_json()
        book_id = data.get('id')
        if not book_id:
            return jsonify({"error": "Book id is required"}), 400

        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"})

