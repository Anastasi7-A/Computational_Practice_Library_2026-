
from db.Connection import db
from sqlalchemy import CheckConstraint


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    book_year = db.Column(db.Integer, nullable=False)
    edition = db.Column(db.String(255))

    # nullable должен быть True, а не строкой
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=True)

    total_copies = db.Column(db.Integer)
    available_copies = db.Column(db.Integer)
    book_description = db.Column(db.Text)
    cover_path = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP)

    # Связь с жанром
    genre = db.relationship('Genre', back_populates='books')

    __table_args__ = (
        CheckConstraint('available_copies >= 0 AND available_copies <= total_copies', name='chk_available_copies'),
    )






