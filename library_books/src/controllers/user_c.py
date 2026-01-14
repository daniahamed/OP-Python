from src.app import db
from src.models import User
from sqlalchemy.exc import SQLAlchemyError

def create_user(name):
    if not name or not isinstance(name, str) or not name.strip():
        raise ValueError("Name is required and must be a non-empty string")
    if len(name.strip()) > 100 :
        raise ValueError("Name character limit exceeded")
    
    user = User(name=name.strip())
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    return user


def update_user(user_id, name=None):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if len(name.strip()) > 100 :
            raise ValueError("Name character limit exceeded")
        user.name = name.strip()
    
    db.session.commit()
    return user



def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    db.session.delete(user)
    db.session.commit()


def get_user_book_count(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    if not user.library:
        return 0
    return len(user.library.books)

