from db.Connection import db


class Fine(db.Model):
    __tablename__ = 'fines'

    fine_id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    amount = db.Column(db.Numeric(8, 2), nullable=False)
    per_day_rate = db.Column(db.Numeric(6, 2), nullable=False, default=0.10)
    days_overdue = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    paid_at = db.Column(db.DateTime)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)

    loan = db.relationship('Loan')
    user = db.relationship('User')

    def __repr__(self):
        return f"<Fine {self.fine_id}: {self.amount} BYN, paid={self.is_paid}>"
