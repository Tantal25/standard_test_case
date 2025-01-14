from typing import Literal

TRANSACTIONS_PER_PAGE = 5
DEFAULT_BALANCE = 0.0
DEFAULT_COMISSION_RATE = 0.05
TRANSACTION_EXPIRATION_TIME = 900
DEFAULT_URL_WEBHOOK = 'http://127.0.0.1:5000/webhook'
TRANSACTION_STATUS = Literal['pending', 'confrimed', 'canceled', 'expired']
LIST_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CACNELED', 'Canceled'),
        ('EXPIRED', 'Expired')
]
