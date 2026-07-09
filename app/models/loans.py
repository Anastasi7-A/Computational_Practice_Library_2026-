from app.db.Connection import db


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

    status_loan = db.Column(db.Enum('active', 'returned', 'overdue', 'lost', name='loan_status'))

    book = db.relationship('Book')
    user = db.relationship('User', back_populates='loans')
    fine = db.relationship('Fine', back_populates='loan', uselist=False)

    def __repr__(self):
        return f"<Loan {self.loan_id}: book={self.book_id} user={self.user_id} status={self.status_loan}>"