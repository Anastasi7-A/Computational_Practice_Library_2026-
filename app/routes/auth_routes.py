from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, session

from app.db.Connection import db
from app.models.users import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            session['user_id'] = user.user_id
            session['user_name'] = user.full_name
            session['user_role'] = user.user_role
            return redirect(url_for('catalog.index'))
        else:
            return "Пользователь не найден. Пожалуйста, зарегистрируйтесь."

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        role = request.form.get('role')
        faculty = request.form.get('faculty')
        phone = request.form.get('phone')

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
            return redirect(url_for('catalog.index'))

        return redirect(url_for('catalog.index'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('catalog.index'))