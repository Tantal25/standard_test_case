import enum


class TransactionStatus(enum.Enum):
    """Enum со статусами транзакций."""

    PENDING = 'Pending'
    CONFIRMED = 'Confrimed'
    CANCELED = 'Canceled'
    EXPIRED = 'Expired'


class UserRole(enum.Enum):
    """Enum с ролями пользователей."""

    ADMIN = 'admin'
    USER = 'user'
