from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField
from wtforms.validators import DataRequired
from forms.join_one_player_form import PlayerForm


class SoloJoin(FlaskForm):
    captain = FormField(PlayerForm)
    submit = SubmitField('Отправить заявку')


class TeamJoin(FlaskForm):
    team_name = StringField('Название команды', validators=[DataRequired()])
    captain = FormField(PlayerForm)
    player_one = FormField(PlayerForm)
    player_two = FormField(PlayerForm)
    player_three = FormField(PlayerForm)
    player_four = FormField(PlayerForm)
    submit = SubmitField('Отправить заявку')
