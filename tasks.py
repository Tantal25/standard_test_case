from datetime import datetime, timedelta
import requests

from celery import Celery

from app import app
from source.models import (
    Transaction, db, TransactionStatus,
    User, DEFAULT_URL_WEBHOOK
)


celery = Celery(
    'tasks',
    backend='db+sqlite:///results.sqlite',
    broker='sqla+sqlite:///results.sqlite'
    )
celery.conf.update(app.config)
celery.conf.broker_connection_retry_on_startup = True


@celery.task()
def check_pending_transaction():
    with app.app_context():
        pending_transactions = find_pending_transactions()

        for transaction in pending_transactions:
            if timedelta_check(transaction):
                transaction.status = TransactionStatus.EXPIRED
                # webhook_message_sending(transaction)
                db.session.commit()


# def webhook_message_sending(transaction):
#     user = db.session.query(User).filter(
#         User.id == transaction.user_id).first()

#     if user:
#         url_webhook = user.url_webhook
#     else:
#         url_webhook = DEFAULT_URL_WEBHOOK

#     try:
#         response = requests.post(
#             url_webhook, json={
#                 'transaction_id': transaction.id,
#                 'status': transaction.status.value
#                 })
#         response.raise_for_status()
#         db.session.commit()
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при отправке вебхука: {e}")


def find_pending_transactions():
    return db.session.query(Transaction).filter(
                Transaction.status == TransactionStatus.PENDING).all()


def timedelta_check(transaction):
    return datetime.now() - transaction.created_at > timedelta(seconds=900)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        20,
        check_pending_transaction.s(),
        name='Create transaction every 10 seconds'
        )
