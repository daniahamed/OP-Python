from datetime import datetime
from src.app import db


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
        unique=True
    )

    books = db.relationship(
        'Book',
        backref='library',
        lazy=True,
        cascade='all, delete-orphan'
    )


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    library_id = db.Column(
        db.Integer,
        db.ForeignKey('library.id'),
        nullable=False
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    library = db.relationship(
        'Library',
        backref='owner',
        lazy=True,
        uselist=False,
        cascade='all, delete-orphan'
    )
