from flask import Flask
from app.config import DevelopmentConfig
from app.db.Connection import init_db, test_connection


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    init_db(app)

    with app.app_context():
        test_connection(app)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)


    return app