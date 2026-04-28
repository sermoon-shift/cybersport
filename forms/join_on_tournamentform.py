from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FormField
from wtforms.validators import DataRequired
from forms.join_one_player_form import PlayerForm

class SoloJoin(FlaskForm):
    team_name = StringField('Название команды', validators=[DataRequired()])
    captain = FormField(PlayerForm)

class TeamJoin(SoloJoin):
    player_one = FormField(PlayerForm)
    player_two = FormField(PlayerForm)
    player_three = FormField(PlayerForm)
    player_four = FormField(PlayerForm)