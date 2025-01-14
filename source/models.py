import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from source.constants import (DEFAULT_BALANCE, DEFAULT_COMISSION_RATE,
                              DEFAULT_URL_WEBHOOK)
from source.enums import TransactionStatus, UserRole


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
        default=DEFAULT_COMISSION_RATE
    )
    url_webhook: Mapped[str] = mapped_column(
        String,
        default=DEFAULT_URL_WEBHOOK
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
        DateTime(timezone=True),
        default=func.now()
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=True
    )
