from db.Connection import db


class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    # Имя колонки должно совпадать с SQL (genre_name)
    genre_name = db.Column(db.String(100), nullable=False, unique=True)

    books = db.relationship('Book', back_populates='genre')