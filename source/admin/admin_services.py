from datetime import datetime

from sqlalchemy import func

from source.constants import TRANSACTIONS_PER_PAGE
from source.models import Transaction, User, db


def user_count():
    """Функция, которая подсчитывает количество пользователей в БД."""
    return db.session.query(User).count()


def transaction_count():
    """Функция, которая подсчитывает количество транзакций в БД.
    """
    return db.session.query(Transaction).count()


def day_transaction_sum():
    """Функция, которая подсчитывает сумму всех транзакций за текущий день."""
    return (
        db.session.query(func.sum(Transaction.amount))
        .filter(func.date(Transaction.created_at) == datetime.now().date())
        .scalar() or 0
    )


def recent_transactions():
    """
    Функция возвращающая, установленное в константе,
    количество последних транзакций.
    """
    return (
        db.session.query(Transaction).order_by(Transaction.created_at.desc())
        .limit(TRANSACTIONS_PER_PAGE).all()
    )
