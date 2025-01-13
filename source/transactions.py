from flask import request, jsonify, Blueprint
from sqlalchemy.exc import NoResultFound

from source.models import User, Transaction, db, TransactionStatus


DEFAULT_COMISSION_RATE = 0.05


transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/create_transaction', methods=['POST'])
def create_transaction():
    """Вью для эндпоинта создающего транзакцию."""

    data = request.get_json()
    amount = data.get('amount')
    if not amount:
        return jsonify({'error': 'Введите amount транзакции'}), 400

    user_id = data.get('user_id')

    if user_id:
        try:
            user = db.session.get_one(User, user_id)
            comission = amount * user.comission_rate
        except NoResultFound:
            return jsonify({'error': 'Такого пользователя не существует'}), 404
    else:
        comission = amount * DEFAULT_COMISSION_RATE

    create_transaction_in_db(amount, comission, user_id)
    return jsonify({'transaction_status': 'Транзакция создана'})


@transactions_bp.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    """Вью для эндпоинта меняющего статус транзакции на canceled."""

    data = request.get_json()

    transaction_id = data.get('transaction_id')
    if not transaction_id:
        return jsonify({'error': 'Введите transaction_id'}), 40

    try:
        transaction = db.session.get_one(Transaction, transaction_id)
    except NoResultFound:
        return jsonify({'error': 'Такой транзакции не существует'}), 404

    return change_transaction_status_on_canceled(transaction)


@transactions_bp.route('/check_transaction/<int:id>', methods=['GET'])
def check_transaction(id):
    """Вью для эндпоинта проверяющего статус транзакции."""

    try:
        transaction = db.session.get_one(Transaction, id)
        return jsonify({
            'id': transaction.id,
            'status': transaction.status.value
            })
    except NoResultFound:
        return jsonify({'error': 'Такой транзакции не существует'}), 404


def create_transaction_in_db(amount, comission, user_id):
    """Функция создающая запись транзакции в БД."""

    transaction = Transaction(
        amount=amount,
        comission=comission,
        user_id=user_id,
    )
    db.session.add(transaction)
    db.session.commit()


def change_transaction_status_on_canceled(transaction):
    """Функция меняющая статус транзакции в БД на canceled."""

    if transaction.status.value == 'pending':
        transaction.status = TransactionStatus.CANCELED
        db.session.commit()
        return jsonify({'transaction_status': 'Транзакция отменена'})

    return jsonify({
        'error': 'Tранзакция не может быть отменена,'
        f' статус транзакции - {transaction.status.value}'}
        ), 400
