from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db=SQLAlchemy()

def init_db(app):

   db.init_app(app) #сохраняет ссылку на app внутри себя

   with app.app_context():
      import models.book
      import models.users
      import models.loans
      import models.fines

      db.create_all()

def test_connection(app):
   with app.app_context():
      try:
         db.session.execute(text("SELECT 1"))
         print("Подключение выполнено")
         return True

      except Exception as e:
         print(e)
         return False