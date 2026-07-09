from datetime import date, timedelta
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app, abort
from app.db.Connection import db
from app.models.book import Book
from app.models.users import User
from app.models.loans import Loan
from app.models.fines import Fine
from app.utils.auth import login_required
from app.routes.reservation_routes import process_queue

loan_bp = Blueprint('loans', __name__)


def calculate_fine(loan):
    """Считает штраф за просрочку возврата и создаёт/обновляет запись Fine."""
    if not loan.return_date or loan.return_date <= loan.due_date:
        return None

    days_overdue = (loan.return_date - loan.due_date).days
    rate = Decimal(str(current_app.config['FINE_PER_DAY']))
    amount = rate * days_overdue

    fine = loan.fine
    if not fine:
        fine = Fine(loan_id=loan.loan_id, user_id=loan.user_id)
        db.session.add(fine)

    fine.amount = amount
    fine.per_day_rate = rate
    fine.days_overdue = days_overdue
    return fine

def sync_overdue_status():
    """Переводит активные выдачи с истёкшим сроком в статус 'overdue'."""
    today = date.today()
    overdue_loans = Loan.query.filter(
        Loan.status_loan == 'active',
        Loan.due_date < today
    ).all()
    for loan in overdue_loans:
        loan.status_loan = 'overdue'
    if overdue_loans:
        db.session.commit()


@loan_bp.before_app_request
def _sync_loans_state():
    from flask import request
    if request.endpoint and request.endpoint.startswith('static'):
        return
    sync_overdue_status()


@loan_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    active_loans = Loan.query.filter(
        Loan.user_id == user.user_id,
        Loan.status_loan.in_(['active', 'overdue'])
    ).order_by(Loan.due_date.asc()).all()
    past_loans = Loan.query.filter(
        Loan.user_id == user.user_id,
        Loan.status_loan.in_(['returned', 'lost'])
    ).order_by(Loan.return_date.desc()).all()
    unpaid_fines = Fine.query.filter_by(user_id=user.user_id, is_paid=False).all()
    return render_template(
        'profile.html',
        user=user,
        active_loans=active_loans,
        past_loans=past_loans,
        unpaid_fines=unpaid_fines,
        today=date.today()
    )

@loan_bp.route('/take_book/<int:book_id>', methods=['POST'])
@login_required
def take_book(book_id):
    book = Book.query.get_or_404(book_id)
    user = User.query.get(session['user_id'])

    if book.available_copies <= 0:
        flash('Свободных экземпляров нет.')
        return redirect(url_for('catalog.book_detail', book_id=book_id))

    already_has = Loan.query.filter(
        Loan.book_id == book_id,
        Loan.user_id == user.user_id,
        Loan.status_loan.in_(['active', 'overdue'])
    ).first()
    if already_has:
        flash('Эта книга уже числится за вами.')
        return redirect(url_for('catalog.book_detail', book_id=book_id))

    today = date.today()
    loan = Loan(
        book_id=book_id,
        user_id=user.user_id,
        loan_date=today,
        due_date=today + timedelta(days=current_app.config['LOAN_PERIOD_DAYS']),
        status_loan='active'
    )
    book.available_copies -= 1
    db.session.add(loan)
    db.session.commit()

    flash(f'Книга выдана. Верните её до {loan.due_date.strftime("%d.%m.%Y")}.')
    return redirect(url_for('catalog.book_detail', book_id=book_id))


@loan_bp.route('/return_book/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    user = User.query.get(session['user_id'])

    if loan.user_id != user.user_id:
        abort(403)

    if loan.status_loan not in ('active', 'overdue'):
        flash('Эта книга уже возвращена.')
        return redirect(url_for('loans.profile'))

    loan.return_date = date.today()
    fine = calculate_fine(loan)
    loan.status_loan = 'returned'
    book = loan.book
    book.available_copies += 1
    db.session.commit()
    process_queue(book.book_id)
    if fine:
        flash(f'Книга возвращена с опозданием на {fine.days_overdue} дн. Начислен штраф: {fine.amount} BYN.')
    else:
        flash('Книга успешно возвращена, спасибо!')
    return redirect(url_for('loans.profile'))