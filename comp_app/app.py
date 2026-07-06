from flask import Flask, render_template, session, Blueprint, abort, request, redirect, url_for, flash
from config import DevelopmentConfig
from db.Connection import db, init_db, test_connection
from datetime import date
from werkzeug.utils import secure_filename
import os


# Импортируем модели, чтобы SQLAlchemy видел их
from models.book import Book
from models.genres import Genre
from models.users import User

# Создаем Blueprint для книг
books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def index():
    # Получаем параметры поиска из URL
    search_query = request.args.get('search', '')
    genre_id = request.args.get('genre', '')

    # Получаем все жанры для выпадающего списка
    all_genres = Genre.query.all()

    # Начинаем строить запрос к базе книг
    query = Book.query

    # Если ввели текст в поиск
    if search_query:
        query = query.filter(
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query))
        )

    # Если выбрали конкретный жанр
    if genre_id and genre_id.isdigit():
        query = query.filter(Book.genre_id == int(genre_id))

    all_books = query.all()

    return render_template(
        'index.html',
        books=all_books,
        genres=all_genres,
        selected_genre=genre_id # Чтобы сохранить выбор после перезагрузки
    )
@books_bp.route('/book/<int:book_id>')
def book_detail(book_id):

    book = Book.query.get_or_404(book_id)

    # Проверяем, залогинен ли пользователь (есть ли в сессии user_id)
    is_authenticated = 'user_id' in session

    return render_template('book_detail.html', book=book, is_authenticated=is_authenticated)


@books_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        # Ищем пользователя по email
        user = User.query.filter_by(email=email).first()

        if user:
            # Сохраняем данные в сессию
            session['user_id'] = user.user_id
            session['user_name'] = user.full_name
            session['user_role'] = user.user_role
            return redirect(url_for('books.index'))
        else:
            return "Пользователь не найден. Пожалуйста, зарегистрируйтесь."

    return render_template('login.html')


@books_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        role = request.form.get('role')
        faculty = request.form.get('faculty')
        phone = request.form.get('phone')

        # Проверка на существование
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email уже занят."

        new_user = User(
            full_name=full_name,
            email=email,
            user_role=role,
            faculty=faculty,
            phone=phone,
            reg_date=date.today(),
            is_active=True
        )

        db.session.add(new_user)
        db.session.commit()

        if 'user_id' not in session:
            session['user_id'] = new_user.user_id
            session['user_name'] = new_user.full_name
            session['user_role'] = new_user.user_role
            return redirect(url_for('books.index'))

        # Если сейчас в системе АДМИН (создает другого пользователя)
        elif session.get('user_role') == 'admin':
            flash(f"Пользователь {full_name} успешно создан!")
            return redirect(url_for('admin.manage_users'))


        return redirect(url_for('books.index'))

    return render_template('register.html')


@books_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('books.index'))

@books_bp.route('/logout_test')
def logout_test():

    session.pop('user_id', None)
    return "Вы вышли из системы. <a href='/'>Назад в каталог</a>"





admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Проверка: является ли пользователь админом
def is_admin():
    return session.get('user_role') == 'admin'


@admin_bp.before_request
def check_admin():
    if not is_admin():
        return "Доступ запрещен. Вы не администратор.", 403


# --- ПАНЕЛЬ УПРАВЛЕНИЯ ---
@admin_bp.route('/')
def dashboard():
    return render_template('admin/dashboard.html')


# --- CRUD КНИГ ---
@admin_bp.route('/books')
def manage_books():
    all_books = Book.query.all()
    return render_template('admin/books.html', books=all_books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Обработка загрузки обложки
        cover = request.files.get('cover')
        filename = None
        if cover:
            filename = secure_filename(cover.filename)
            cover.save(os.path.join('static/covers', filename))

        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            book_year=request.form.get('year'),
            edition=request.form.get('edition'),
            genre_id=request.form.get('genre_id'),
            total_copies=request.form.get('total_copies'),
            available_copies=request.form.get('total_copies'),  # При добавлении все в наличии
            book_description=request.form.get('description'),
            cover_path=filename
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('admin.manage_books'))

    genres = Genre.query.all()
    return render_template('admin/book_form.html', genres=genres)


@admin_bp.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        # Обработка загрузки новой обложки
        cover = request.files.get('cover')
        if cover and cover.filename != '':
            filename = secure_filename(cover.filename)
            cover.save(os.path.join('static/covers', filename))
            book.cover_path = filename

        # Обновляем данные из формы
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.book_year = request.form.get('year')
        book.edition = request.form.get('edition')
        book.genre_id = request.form.get('genre_id')

        # Обновляем количество (логика: если общее кол-во меняется, доступное тоже должно сдвинуться)
        diff = int(request.form.get('total_copies')) - book.total_copies
        book.total_copies = int(request.form.get('total_copies'))
        book.available_copies += diff

        book.book_description = request.form.get('description')

        db.session.commit()
        return redirect(url_for('admin.manage_books'))

    genres = Genre.query.all()
    # Передаем объект book в шаблон, чтобы поля заполнились данными
    return render_template('admin/book_form.html', genres=genres, book=book)

@admin_bp.route('/books/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin.manage_books'))


# --- CRUD ПОЛЬЗОВАТЕЛЕЙ ---
@admin_bp.route('/users')
def manage_users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.user_id == session.get('user_id'):
        return "Вы не можете удалить самого себя!", 400
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.manage_users'))

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
    app.register_blueprint(admin_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)