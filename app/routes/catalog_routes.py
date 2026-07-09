from flask import Blueprint, render_template, request, session

from app.models.book import Book
from app.models.genres import Genre
from app.models.loans import Loan
from app.models.reservation import Reservation

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    genre_id = request.args.get('genre', '')

    all_genres = Genre.query.all()
    query = Book.query

    if search_query:
        query = query.filter(
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query))
        )

    if genre_id and genre_id.isdigit():
        query = query.filter(Book.genre_id == int(genre_id))

    all_books = query.all()

    return render_template(
        'index.html',
        books=all_books,
        genres=all_genres,
        selected_genre=genre_id
    )


@catalog_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    is_authenticated = 'user_id' in session
    my_loan = None
    my_reservation = None
    queue_position = None

    if is_authenticated:
        user_id = session['user_id']
        my_loan = Loan.query.filter(
            Loan.book_id == book_id,
            Loan.user_id == user_id,
            Loan.status_loan.in_(['active', 'overdue'])
        ).first()

        my_reservation = Reservation.query.filter(
            Reservation.book_id == book_id,
            Reservation.user_id == user_id,
            Reservation.status_res.in_(['waiting', 'reserved'])
        ).first()

        if my_reservation and my_reservation.status_res == 'waiting':
            queue_position = Reservation.query.filter(
                Reservation.book_id == book_id,
                Reservation.status_res == 'waiting',
                Reservation.reservation_date <= my_reservation.reservation_date
            ).count()

    return render_template(
        'book_detail.html',
        book=book,
        is_authenticated=is_authenticated,
        my_loan=my_loan,
        my_reservation=my_reservation,
        queue_position=queue_position
    )

    return render_template(
        'book_detail.html',
        book=book,
        is_authenticated=is_authenticated,
        my_loan=my_loan,
        my_reservation=None,
        queue_position=None
    )