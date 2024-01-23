from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length
# необходимые библиотеки


class MapForm(FlaskForm):   # класс формы
    address = StringField('Введите адрес', validators=[DataRequired(), Length(min=5, max=50)])
    # поле ввода адреса
    submit = SubmitField('Submit')   # поле отправки результата
