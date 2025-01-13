from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    amount = DecimalField('Сумма', validators=[DataRequired()])
    comission = DecimalField('Комиссия', validators=[DataRequired()])
    status = SelectField('Статус', choices=[
        ('PENDING', 'pending'),
        ('CONFIRMED', 'confirmed'),
        ('CACNELED', 'canceled'),
        ('EXPIRED', 'expired')
    ])
    user_id = IntegerField('ID пользователя')
