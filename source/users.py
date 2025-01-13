from flask import (
    request, jsonify, Blueprint, redirect,
    url_for, flash, render_template)
from flask_login import login_user, login_required, logout_user

from source.models import User, db


users_bp = Blueprint('users', __name__)


@users_bp.route('/create_user', methods=['POST'])
def create_user():
    """Вью для эндпоинта создания пользователя в БД."""

    data = request.get_json()
    db.session.add(User(
        username=data.get('username'),
        email=data.get('email'),
        balance=data.get('balance')
    ))
    db.session.commit()
    return jsonify({'status': 'Пользователь зарегистрирован'})


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        user = db.session.query(User).filter_by(
            username=username, email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Неверный логин или пароль')
            return redirect(url_for('users.login'))
    return render_template('users/login.html')


@users_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
