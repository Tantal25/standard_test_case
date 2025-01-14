from datetime import datetime, timedelta, timezone

import requests

from source.constants import DEFAULT_URL_WEBHOOK, TRANSACTION_EXPIRATION_TIME
from source.models import (Transaction, TransactionStatus,
                           User, db)


def webhook_message_sending(transaction):
    user = db.session.get(User, transaction.user_id)

    if user:
        url_webhook = user.url_webhook
    else:
        url_webhook = DEFAULT_URL_WEBHOOK

    try:
        response = requests.post(
            url_webhook, json={
                'transaction_id': transaction.id,
                'status': transaction.status.value
                })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке вебхука: {e}")


def find_pending_transactions():
    return db.session.query(Transaction).filter(
                Transaction.status == TransactionStatus.PENDING).all()


def timedelta_check(transaction):
    return (
        datetime.now(timezone.utc) -
        transaction.created_at.replace(tzinfo=timezone.utc)
        > timedelta(seconds=TRANSACTION_EXPIRATION_TIME)
    )
