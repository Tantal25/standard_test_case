from source.models import db, User


def create_user_in_db(data):
    db.session.add(User(
        username=data.get('username'),
        email=data.get('email'),
        balance=data.get('balance')
    ))
    db.session.commit()


def find_user_in_db(username, email):
    return (
        db.session.query(User)
        .filter_by(username=username, email=email).first()
    )


def get_user(user_id):
    """Получает пользователя по ID или возвращает сообщение об ошибке."""
    result = db.session.get(User, user_id)
    return result if result else {'error': 'Такого пользователя не существует'}
