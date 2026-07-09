from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        import app.models.users  # noqa: F401
        import app.models.genres  # noqa: F401
        import app.models.book  # noqa: F401
        import app.models.loans  # noqa: F401

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
