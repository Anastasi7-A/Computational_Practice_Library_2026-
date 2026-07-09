from datetime import datetime, timedelta

from flask import Blueprint, redirect, url_for, flash, session, current_app, abort

from app.db.Connection import db
from app.models.book import Book
from app.models.users import User
from app.models.loans import Loan
from app.models.reservation import Reservation
from app.utils.auth import login_required

reservation_bp = Blueprint('reservations', __name__)


def process_queue(book_id):
    """Если после возврата книги есть свободный экземпляр и в очереди кто-то ждёт —
    удерживает этот экземпляр за первым в очереди."""
    book = Book.query.get(book_id)
    if not book or book.available_copies <= 0:
        return

    next_in_queue = Reservation.query.filter_by(
        book_id=book_id, status_res='waiting'
    ).order_by(Reservation.reservation_date.asc()).first()

    if next_in_queue:
        next_in_queue.status_res = 'reserved'
        hold_days = current_app.config['RESERVATION_HOLD_DAYS']
        next_in_queue.expiry_date = datetime.now() + timedelta(days=hold_days)
        book.available_copies -= 1
        db.session.commit()


def expire_reservations(book_id=None):
    """Снимает брони, которые пользователь не забрал вовремя, и двигает очередь дальше."""
    now = datetime.now()
    query = Reservation.query.filter(
        Reservation.status_res == 'reserved',
        Reservation.expiry_date < now
    )
    if book_id is not None:
        query = query.filter(Reservation.book_id == book_id)

    expired = query.all()
    touched_books = {res.book_id for res in expired}
    for res in expired:
        res.status_res = 'expired'
    if expired:
        db.session.commit()

    for bid in touched_books:
        process_queue(bid)


@reservation_bp.before_app_request
def _sync_reservations_state():
    from flask import request
    if request.endpoint and request.endpoint.startswith('static'):
        return
    expire_reservations()


@reservation_bp.route('/reserve_book/<int:book_id>', methods=['POST'])
@login_required
def reserve_book(book_id):
    book = Book.query.get_or_404(book_id)
    user = User.query.get(session['user_id'])

    if book.available_copies > 0:
        flash('Сейчас есть свободные экземпляры — просто возьмите книгу.')
        return redirect(url_for('catalog.book_detail', book_id=book_id))

    existing = Reservation.query.filter(
        Reservation.book_id == book_id,
        Reservation.user_id == user.user_id,
        Reservation.status_res.in_(['waiting', 'reserved'])
    ).first()
    if existing:
        flash('Вы уже в очереди на эту книгу.')
        return redirect(url_for('catalog.book_detail', book_id=book_id))

    reservation = Reservation(
        book_id=book_id,
        user_id=user.user_id,
        reservation_date=datetime.now(),
        status_res='waiting'
    )
    db.session.add(reservation)
    db.session.commit()

    flash('Вы встали в очередь на книгу.')
    return redirect(url_for('catalog.book_detail', book_id=book_id))


@reservation_bp.route('/reservation/cancel/<int:res_id>', methods=['POST'])
@login_required
def cancel_reservation(res_id):
    reservation = Reservation.query.get_or_404(res_id)
    user = User.query.get(session['user_id'])

    if reservation.user_id != user.user_id:
        abort(403)

    was_holding_copy = reservation.status_res == 'reserved'
    reservation.status_res = 'cancelled'

    if was_holding_copy:
        reservation.book.available_copies += 1

    db.session.commit()

    if was_holding_copy:
        process_queue(reservation.book_id)

    flash('Бронирование отменено.')
    return redirect(url_for('loans.profile'))


@reservation_bp.route('/reservation/claim/<int:res_id>', methods=['POST'])
@login_required
def claim_reservation(res_id):
    reservation = Reservation.query.get_or_404(res_id)
    user = User.query.get(session['user_id'])

    if reservation.user_id != user.user_id:
        abort(403)

    if reservation.status_res != 'reserved':
        flash('Срок бронирования истёк, либо книга ещё не освободилась.')
        return redirect(url_for('loans.profile'))

    from datetime import date
    today = date.today()
    loan = Loan(
        book_id=reservation.book_id,
        user_id=user.user_id,
        loan_date=today,
        due_date=today + timedelta(days=current_app.config['LOAN_PERIOD_DAYS']),
        status_loan='active'
    )
    reservation.status_res = 'fulfilled'
    db.session.add(loan)
    db.session.commit()

    flash(f'Книга выдана по брони. Верните её до {loan.due_date.strftime("%d.%m.%Y")}.')
    return redirect(url_for('loans.profile'))