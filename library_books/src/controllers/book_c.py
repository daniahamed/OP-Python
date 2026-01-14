from src.app import db
from src.models import Book, Library


def get_books(author=None, title=None, library_id=None):
    query = Book.query
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if library_id:
        if not Library.query.get(library_id):
            raise ValueError(f"Library with ID {library_id} does not exist")
        query = query.filter_by(library_id=library_id)
    return query.all()


def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        raise ValueError(f"Book with ID {book_id} does not exist")
    return book


def create_book(title, author, library_id):
    if not title or not isinstance(title, str) or not title.strip():
        raise ValueError("Title is required and must be a non-empty string")
    if len(title.strip()) > 150 :
        raise ValueError("Title character limit exceeded")
    if not author or not isinstance(author, str) or not author.strip():
        raise ValueError("Author is required and must be a non-empty string")
    if len(author.strip()) > 100 :
        raise ValueError("Author name character limit exceeded")
    if not library_id:
        raise ValueError("Library ID is required")

    library = Library.query.get(library_id)
    if not library:
        raise ValueError(f"Library with ID {library_id} does not exist")

    book = Book(title=title.strip(), author=author.strip(), library_id=library.id)
    db.session.add(book)
    db.session.commit()
    return book


def update_book(book_id, title=None, author=None, library_id=None):
    book = Book.query.get(book_id)
    if not book:
        raise ValueError(f"Book with ID {book_id} does not exist")

    if title is not None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if len(title.strip()) > 150 :
            raise ValueError("Title character limit exceeded")
        book.title = title.strip()

    if author is not None:
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string")
        if len(author.strip()) > 100 :
            raise ValueError("Author name character limit exceeded")
        book.author = author.strip()

    if library_id is not None:
        library = Library.query.get(library_id)
        if not library:
            raise ValueError(f"Library with ID {library_id} does not exist")
        book.library_id = library.id

    db.session.commit()
    return book


def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        raise ValueError(f"Book with ID {book_id} does not exist")
    db.session.delete(book)
    db.session.commit()
    return True


def transfer_book(book_id, target_library_id):
    if not target_library_id:
        raise ValueError("target_library_id is required")

    book = Book.query.get(book_id)
    target_library = Library.query.get(target_library_id)

    if not book:
        raise ValueError(f"Book with ID {book_id} does not exist")
    if not target_library:
        raise ValueError(f"Library with ID {target_library_id} does not exist")

    book.library_id = target_library.id
    db.session.commit()
    return book

