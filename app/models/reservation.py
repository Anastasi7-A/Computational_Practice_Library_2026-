from app.db.Connection import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    reservation_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    reservation_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime)

    # waiting   — в очереди, ждёт освобождения экземпляра
    # reserved  — экземпляр удержан за пользователем (окно на получение)
    # fulfilled — превращено в выдачу (создан Loan)
    # cancelled — отменено пользователем
    # expired   — не забрал вовремя, бронь сгорела, очередь двигается дальше

    status_res = db.Column(
        db.Enum('reserved', 'waiting', 'fulfilled', 'cancelled', 'expired', name='reservation_status')
    )

    book = db.relationship('Book')
    user = db.relationship('User')

    def __repr__(self):
        return f"<Reservation {self.reservation_id}: book={self.book_id} user={self.user_id} status={self.status_res}>"
