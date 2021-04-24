from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Название предмета', validators=[DataRequired()])
    count = IntegerField('Количество', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DelForm(FlaskForm):
    name = StringField('Название предмета', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class AddRentForm(FlaskForm):
    name = StringField('Название предмета', validators=[DataRequired()])
    submit = SubmitField('Удалить')
