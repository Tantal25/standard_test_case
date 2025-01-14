from flask import jsonify

from source.models import db, Transaction, TransactionStatus, User
from source.constants import DEFAULT_COMISSION_RATE
from source.users.users_services import get_user


def create_transaction_in_db(amount, comission, user_id):
    """Функция создающая запись транзакции в БД."""

    transaction = Transaction(
        amount=amount,
        comission=comission,
        user_id=user_id,
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'transaction_status': 'Транзакция создана'})


def change_transaction_status_on_canceled(transaction):
    """Функция меняющая статус транзакции в БД на canceled."""

    if transaction.status.value == 'pending':
        transaction.status = TransactionStatus.CANCELED
        db.session.commit()
        return jsonify({'transaction_status': 'Транзакция отменена'})

    return jsonify({
        'error': 'Tранзакция не может быть отменена,'
        f' статус транзакции - {transaction.status.value}'}), 400


def get_transaction(transaction_id):
    """
    Получает транзакцию по идентификатору или возвращает сообщение об ошибке.
    """
    result = db.session.get(Transaction, transaction_id)
    return result if result else {'error': 'Такой транзакции не существует'}


def calculate_comission(amount, user_id):
    """Вычисляет комиссию на основе user_id."""
    if user_id:
        user = get_user(user_id)
        if isinstance(user, User):
            return amount * user.comission_rate
        else:
            return user
    else:
        return amount * DEFAULT_COMISSION_RATE
