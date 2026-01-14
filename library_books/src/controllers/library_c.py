from src.app import db
from src.models import Library, User 


def create_library(name, owner_id):
    if not name or not isinstance(name, str) or not name.strip():
        raise ValueError("Name is required and must be a non-empty string")
    if len(name.strip()) > 100 :
        raise ValueError("Name character limit exceeded")
    if owner_id is None:
        raise ValueError("Owner ID is required")

    owner = User.query.get(owner_id)
    if not owner:
        raise ValueError(f"Owner with ID {owner_id} does not exist")
    
    owned_library = Library.query.filter_by(owner_id=owner_id).first()

    if owned_library:
        raise ValueError(f"This owner already has a library with ID {owned_library.id}")

    library = Library(name=name.strip(), owner_id=owner_id)
    db.session.add(library)
    db.session.commit()
    return library


def get_all_libraries():
    return Library.query.all()


def get_library_by_id(library_id):
    library = Library.query.get(library_id)
    if not library:
        raise ValueError(f"Library with ID {library_id} does not exist")
    return library


def update_library(library_id, name=None, owner_id=None):
    library = Library.query.get(library_id)
    if not library:
        raise ValueError(f"Library with ID {library_id} does not exist")
    
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if len(name.strip()) > 100 :
            raise ValueError("Name character limit exceeded")
        library.name = name.strip()

    if owner_id is not None:
        owner = User.query.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} does not exist")

        owned_library = Library.query.filter_by(owner_id=owner_id).first()
        if owned_library and owned_library.id != library_id:
            raise ValueError(f"This owner already has a library with ID {owned_library.id}")

        library.owner_id = owner_id

    db.session.commit()
    return library


def delete_library(library_id):
    library = Library.query.get(library_id)
    if not library:
        raise ValueError(f"Library with ID {library_id} does not exist")
    db.session.delete(library)
    db.session.commit()
    return True



