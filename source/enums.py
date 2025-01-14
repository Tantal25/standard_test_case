import enum


class TransactionStatus(enum.Enum):
    """Enum со статусами транзакций."""

    PENDING = 'pending'
    CONFIRMED = 'confrimed'
    CANCELED = 'canceled'
    EXPIRED = 'expired'


class UserRole(enum.Enum):
    """Enum с ролями пользователей."""

    ADMIN = 'admin'
    USER = 'user'
