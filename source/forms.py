from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired

from source.constants import LIST_CHOICES


class TransactionForm(FlaskForm):
    amount = DecimalField('Сумма', validators=[DataRequired()])
    comission = DecimalField('Комиссия', validators=[DataRequired()])
    status = SelectField('Статус', choices=LIST_CHOICES)
    user_id = IntegerField('ID пользователя')
