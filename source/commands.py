from flask import Blueprint

from source.models import db, User, UserRole


admin_cli_bp = Blueprint('admin_cli', __name__)


@admin_cli_bp.cli.command('create-admin')
def create_admin():
    """CLI команда для создания дефолтного админа в БД."""

    admin = User(
        username='admin',
        email='admin@test.ru',
        balance=100000.0,
        comission_rate=0.0,
        role=UserRole.ADMIN
    )
    db.session.add(admin)
    db.session.commit()
