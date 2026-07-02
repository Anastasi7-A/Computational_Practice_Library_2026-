from flask import Flask, render_template, session, Blueprint, abort
from config import DevelopmentConfig
from db.Connection import db, init_db, test_connection

# Импортируем модели, чтобы SQLAlchemy видел их
from models.book import Book
from models.genres import Genre

# Создаем Blueprint для книг
books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def index():

    try:
        all_books = Book.query.all()
        return render_template('index.html', books=all_books)
    except Exception as e:
        return f"Ошибка при загрузке книг: {e}"


@books_bp.route('/book/<int:book_id>')
def book_detail(book_id):

    book = Book.query.get_or_404(book_id)

    # Проверяем, залогинен ли пользователь (есть ли в сессии user_id)
    is_authenticated = 'user_id' in session

    return render_template('book_detail.html', book=book, is_authenticated=is_authenticated)


# --- Вспомогательные маршруты для теста (можно удалить потом) ---
@books_bp.route('/login_test')
def login_test():

    session['user_id'] = 1
    return "Вы вошли как тестовый пользователь! <a href='/'>Назад в каталог</a>"


@books_bp.route('/logout_test')
def logout_test():

    session.pop('user_id', None)
    return "Вы вышли из системы. <a href='/'>Назад в каталог</a>"


# ---------------------------------------------------------------

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # Инициализация БД
    init_db(app)

    # Проверка соединения (выведет в консоль результат)
    with app.app_context():
        test_connection(app)

    # Регистрация синих бланков (Blueprints)
    app.register_blueprint(books_bp, url_prefix='/')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)