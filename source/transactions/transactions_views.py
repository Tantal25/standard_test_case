from flask import Blueprint, jsonify, request

from source.models import Transaction
from source.transactions.transactions_services import (
    calculate_comission, change_transaction_status_on_canceled,
    create_transaction_in_db, get_transaction)


transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/create_transaction', methods=['POST'])
def create_transaction():
    """Вью для эндпоинта создающего транзакцию."""

    data = request.get_json()
    amount = data.get('amount')

    if not amount:
        return jsonify({'error': 'amount - обязательное поле'}), 400

    user_id = data.get('user_id')
    comission = calculate_comission(amount, user_id)

    if isinstance(comission, float):
        return create_transaction_in_db(amount, comission, user_id)
    return jsonify(comission), 404


@transactions_bp.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    """Вью для эндпоинта меняющего статус транзакции на canceled."""

    data = request.get_json()
    transaction_id = data.get('transaction_id')

    if not transaction_id:
        return jsonify({'error': 'transaction_id - обязательное поле'}), 400

    transaction = get_transaction(transaction_id)
    if not isinstance(transaction, Transaction):
        return jsonify(transaction), 404

    return change_transaction_status_on_canceled(transaction)


@transactions_bp.route('/check_transaction/<int:id>', methods=['GET'])
def check_transaction(id):
    """Вью для эндпоинта проверяющего статус транзакции."""

    transaction = get_transaction(id)

    if isinstance(transaction, Transaction):
        return jsonify({
            'id': transaction.id,
            'status': transaction.status.value
        })
    return jsonify(transaction), 404
