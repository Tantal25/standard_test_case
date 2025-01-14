from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import login_required, login_user, logout_user

from source.users.users_services import create_user_in_db, find_user_in_db

users_bp = Blueprint('users', __name__)


@users_bp.route('/create_user', methods=['POST'])
def create_user():
    """Вью для эндпоинта создания пользователя в БД."""
    create_user_in_db(request.get_json())

    return jsonify({'status': 'Пользователь зарегистрирован'})


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = find_user_in_db(request.form['username'], request.form['email'])

        if user:
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('users.login'))

    return render_template('users/login.html')


@users_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
