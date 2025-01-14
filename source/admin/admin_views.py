from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from sqlalchemy import func

from source.admin.admin_services import (day_transaction_sum,
                                         recent_transactions,
                                         transaction_count, user_count)
from source.forms import AdminTransactionForm, UserTransactionForm
from source.models import Transaction, User, UserRole, db


class CustomAdminIndexView(AdminIndexView):
    """Вью главной страницы (дашборда) админ-панели."""

    @expose('/')
    @login_required
    def index(self):
        # Доступ к дашборду только у админа
        if current_user.role != UserRole.ADMIN:
            return redirect(url_for('user.index_view'))

        return self.render(
            'admin/dashboard.html',
            # Подсчитываем количество пользователей и транзакций в БД
            user_count=user_count(),
            transaction_count=transaction_count(),

            # Подсчитываем сумму всех транзакций за сегодня
            today_transaction_sum=day_transaction_sum(),

            # Выводим последние транзакции
            recent_transactions=recent_transactions()
        )


class AdminUserView(ModelView):
    """Вью страницы пользователей в админ-панели."""

    column_list = [
        'id', 'username', 'balance', 'comission_rate',
        'url_webhook', 'role', 'usdt_wallet_number'
        ]
    column_labels = {
        'id': 'ID',
        'username': 'Имя пользователя',
        'balance': 'Баланс',
        'comission_rate': 'Ставка комиссии',
        'url_webhook': 'URL Webhook',
        'usdt_wallet_number': 'USDT кошелек'
    }

    def _handle_view(self, name, **kwargs):
        if current_user.role != UserRole.ADMIN:
            return redirect(url_for('transaction.index_view'))
        return super()._handle_view(name, **kwargs)


class AdminTransactionView(ModelView):
    """Вью для страницы транзакций в админ панели."""

    form = AdminTransactionForm
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
            model.comission = model.amount * current_user.comission_rate
        return super().on_model_change(form, model, is_created)

    def create_form(self, obj=None):
        form = super().create_form()
        if current_user.role != UserRole.ADMIN:
            form = UserTransactionForm()
        return form


def init_admin(app):
    """Метод для инициализации всей админ-панели."""

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
