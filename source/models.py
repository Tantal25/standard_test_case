import datetime
import enum
from typing import Literal

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from sqlalchemy import (
    String, Enum, Integer,
    ForeignKey, DateTime, Float
    )
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DEFAULT_BALANCE = 0.0
DEFAULT_USER_COMISSION_RATE = 0.05
DEFAULT_URL_WEBHOOK = 'user'
TRANSACTION_STATUS = Literal['pending', 'confrimed', 'canceled', 'expired']


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


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(Base, UserMixin):
    """Расширенная модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(
        Float,
        default=DEFAULT_BALANCE
        )
    comission_rate: Mapped[float] = mapped_column(
        Float,
        default=DEFAULT_USER_COMISSION_RATE
        )
    url_webhook: Mapped[str] = mapped_column(
        String,
        default='user_transactions'
        )
    role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.USER)

    def get_id(self):
        return str(self.id)


class Transaction(Base):
    """Модель стандартной транзакции."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    comission: Mapped[float]
    status: Mapped[str] = mapped_column(
        Enum(TransactionStatus),
        default=TransactionStatus.PENDING
        )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
        )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'),
        nullable=True
        )
