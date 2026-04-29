from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, URLField, IntegerField, DateField
from wtforms.validators import DataRequired

class PlayerForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    steam = URLField('Профиль Steam', validators=[DataRequired()])
    fullname = StringField('ФИО', validators=[DataRequired()])
    birthday = DateField('Дата рождения', validators=[DataRequired()])
    vkontakte = URLField('Профиль Вконтакте', validators=[DataRequired()])