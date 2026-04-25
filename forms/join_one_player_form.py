from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired

class PlayerForm(FlaskForm):
    nickname = StringField('Никнейм', )
    steam_64 = IntegerField('Steam_64', validators=[DataRequired()])
    fullname = StringField('ФИО', validators=[DataRequired()])
    birthday = DateField('Дата рождения', validators=[DataRequired()])
    vkontakte = EmailField('Почта', validators=[DataRequired()])
