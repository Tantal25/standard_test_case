from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

from source.constants import LIST_CHOICES


class UserTransactionForm(FlaskForm):
    amount = FloatField('Сумма', validators=[DataRequired()])


class AdminTransactionForm(UserTransactionForm):
    comission = FloatField('Комиссия', validators=[DataRequired()])
    status = SelectField('Статус', choices=LIST_CHOICES)
    user_id = IntegerField('ID пользователя')
    created_at = DateTimeField("Дата создания")
