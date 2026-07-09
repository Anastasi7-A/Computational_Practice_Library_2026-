from app.db.Connection import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_role = db.Column(db.Enum('admin', 'teacher', 'student', name='user_role'))
    faculty = db.Column(db.String(100))
    is_active = db.Column(db.Boolean)
    phone = db.Column(db.String(20))
    reg_date = db.Column(db.Date)
    loans = db.relationship('Loan', back_populates='user')

    def __repr__(self):
        return f"<User {self.full_name}>"