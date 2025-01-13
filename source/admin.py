from datetime import datetime

from flask import Blueprint, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user
from sqlalchemy import func

from source.models import User, Transaction, db, UserRole
from source.forms import TransactionForm


admin_cli_bp = Blueprint('admin_cli', __name__)

TRANSACTIONS_PER_PAGE = 5


class CustomAdminIndexView(AdminIndexView):
    """Вью главной страницы админ-панели."""

    @expose('/')
    @login_required
    def index(self):

        if current_user.role != UserRole.ADMIN:
            return redirect(url_for('user.index_view'))

        # Подсчитываем количество пользователей и транзакций
        user_count = db.session.query(User).count()
        transaction_count = db.session.query(Transaction).count()

        # Подсчитываем сумму транзакций за сегодняшний день
        today_transaction_sum = db.session.query(
            func.sum(Transaction.amount)).filter(
                func.date(Transaction.created_at) == datetime.now(
                    ).date()).scalar() or 0

        # Выводим установленное количество транзакций
        recent_transactions = db.session.query(
            Transaction).order_by(Transaction.created_at.desc()).limit(
                TRANSACTIONS_PER_PAGE).all()

        return self.render('admin/dashboard.html',
                           user_count=user_count,
                           transaction_count=transaction_count,
                           today_transaction_sum=today_transaction_sum,
                           recent_transactions=recent_transactions)


class AdminUserView(ModelView):

    def get_query(self):
        if current_user.role != UserRole.ADMIN:
            return self.session.query(User).filter(User.id == current_user.id)
        return super().get_query()

    def get_count_query(self):
        if current_user.role != UserRole.ADMIN:
            return self.session.query(1)
        return super().get_count_query()


class AdminTransactionView(ModelView):
    """Вью для страницы транзакций в админ панели."""
    form = TransactionForm
    column_list = [
        'id', 'amount', 'comission',
        'status', 'created_at', 'user_id'
        ]
    column_labels = {
        "id": "ID транзакции",
        "amount": "Сумма",
        'comission': "Комиссия",
        'status': "Статус",
        'created_at': "Дата создания",
        'user_id': "ID пользователя"
    }
    column_editable_list = ['status']
    column_filters = ['user_id', 'status']

    def get_query(self):
        if current_user.role != UserRole.ADMIN:
            return self.session.query(Transaction).filter_by(
                user_id=current_user.id)
        return super().get_query()

    def get_count_query(self):
        if current_user.role != UserRole.ADMIN:
            return self.session.query(
                func.count('*')).select_from(Transaction).filter(
                    Transaction.user_id == current_user.id)
        return super().get_count_query()

    def on_model_change(self, form, model, is_created):
        if current_user.role != UserRole.ADMIN:
            model.user_id = current_user.id
        return super().on_model_change(form, model, is_created)

    def create_form(self, obj=None):
        form = super().create_form()
        if current_user.role != UserRole.ADMIN:
            del form.user_id
        return form


def init_admin(app):
    """Метод для инициализации всей админ панели."""

    admin = Admin(
        app,
        name='Transactions API',
        template_mode='bootstrap4',
        index_view=CustomAdminIndexView()
        )
    admin.add_view(AdminUserView(
            User,
            db.session,
            name='Пользователи')
            )
    admin.add_view(AdminTransactionView(
            Transaction,
            db.session,
            name='Транзакции')
            )


@admin_cli_bp.cli.command('create-admin')
def create_admin():
    """CLI команда для создания дефолтного админа в БД."""

    admin = User(
        username='admin',
        email='admin@test.ru',
        balance=100000.0,
        comission_rate=0.0,
        url_webhook='admin_transactions',
        role=UserRole.ADMIN
        )
    db.session.add(admin)
    db.session.commit()
