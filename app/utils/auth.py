from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view):
    """Требует, чтобы пользователь был авторизован (есть user_id в сессии)."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему.')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


def is_admin():
    return session.get('user_role') == 'admin'