from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __init__(self, title, author):
        self.title = title
        self.author = author


class BookRepo:

    def all(self):
        d = db.session.query(Book).all()
        return list(d)

    def add(self, title, author):
        b = Book( title, author)
        db.session.add(b)
        db.session.commit()

    def update(self, book_id, title, author):
         book = Book.query.get(book_id)
         if book:
            book.title = title
            book.author = author
            db.session.commit()

    def delete(self, book_id):
            book = Book.query.get(book_id)
            if book:
                db.session.delete(book)
                db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class UserRepo:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def add(self, username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

