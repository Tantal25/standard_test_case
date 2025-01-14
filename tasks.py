from celery import Celery

from app import app
from source.celery.celery_services import (find_pending_transactions,
                                           timedelta_check,
                                           webhook_message_sending)
from source.models import TransactionStatus, db

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
                webhook_message_sending(transaction)
                db.session.commit()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60,
        check_pending_transaction.s(),
        name='Check transactions status every 60 seconds'
    )
