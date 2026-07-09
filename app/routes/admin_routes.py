import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import func
from werkzeug.utils import secure_filename

from app.db.Connection import db
from app.models.book import Book
from app.models.genres import Genre
from app.models.users import User
from app.models.loans import Loan
from app.utils.auth import is_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def check_admin():
    if not is_admin():
        return "Доступ запрещен. Вы не администратор.", 403


@admin_bp.route('/')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/books')
def manage_books():
    all_books = Book.query.all()
    return render_template('admin/books.html', books=all_books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        cover = request.files.get('cover')
        filename = None
        if cover:
            filename = secure_filename(cover.filename)
            cover.save(os.path.join('app/static/covers', filename))

        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            book_year=request.form.get('year'),
            edition=request.form.get('edition'),
            genre_id=request.form.get('genre_id'),
            total_copies=request.form.get('total_copies'),
            available_copies=request.form.get('total_copies'),
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
        cover = request.files.get('cover')
        if cover and cover.filename != '':
            filename = secure_filename(cover.filename)
            cover.save(os.path.join('app/static/covers', filename))
            book.cover_path = filename

        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.book_year = request.form.get('year')
        book.edition = request.form.get('edition')
        book.genre_id = request.form.get('genre_id')

        diff = int(request.form.get('total_copies')) - book.total_copies
        book.total_copies = int(request.form.get('total_copies'))
        book.available_copies += diff

        book.book_description = request.form.get('description')

        db.session.commit()
        return redirect(url_for('admin.manage_books'))

    genres = Genre.query.all()
    return render_template('admin/book_form.html', genres=genres, book=book)


@admin_bp.route('/books/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin.manage_books'))


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


@admin_bp.route('/statistics')
def statistics():
    top_books = db.session.query(
        Book,
        func.count(Loan.loan_id).label('loan_count')
    ).join(Loan, Book.book_id == Loan.book_id) \
     .group_by(Book.book_id) \
     .order_by(func.count(Loan.loan_id).desc()) \
     .limit(10).all()

    return render_template('statistics.html', top_books=top_books)