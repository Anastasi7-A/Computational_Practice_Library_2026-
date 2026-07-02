from db.Connection import db


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    status_loan = db.Column(db.Enum('active', 'returned', 'overdue', 'lost', name='loan_status'))

    # Настраиваем связи правильно
    book = db.relationship('Book')
    user = db.relationship('User', back_populates='loans')