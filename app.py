import secrets
import os
from flask import Flask, render_template, redirect
from flask_login import login_user
from flask_restful import Api
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.join_on_tournamentform import SoloJoin, TeamJoin
from models.user_model import User
from models.teams_model import Team
from models.solo_model import Solo
from models.tournament_model import Tournament
from resources import TournamentListResource, SoloRegistrationResource
from flask_migrate import Migrate
from db_init import db

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db', 'database.db')}"

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/news")
def news():
    return render_template("news.html")


@app.route("/games")
def games():
    return render_template("tournament.html")


@app.route("/register_ontournament")
def register_ontournament():
    return render_template("register_ontournament.html")


@app.route("/join_tournament/<tournament_id>", methods=['GET', 'POST'])
def join_tournament(tournament_id):
    form = TeamJoin()
    if form.validate_on_submit():
        db_sess = db.create_session()
        if db_sess.query(Team).filter(Team.name == form.team_name.data, Team.tournament_id == tournament_id).first():
            return render_template('join_tournament.html', message="Данная команда уже участвует в этом турнире",
                                   form=form)
        players = [form.player_one, form.player_two, form.player_three, form.player_four]
        players_data = {}
        for player in players:
            players_data[player] = {
                "nickname": player.nickname,
                "steam": player.steam,
                "fullname": player.fullname,
                "birthday": player.birthday,
                "vkontakte": player.vkontakte
            }
        captain_data = {
            "nickname": form.captain.nickname,
            "steam": form.captain.steam,
            "fullname": form.captain.fullname,
            "birthday": form.captain.birthday,
            "vkontakte": form.captain.vkontakte
        }
        team = Team(
            teamname=form.team_name.data,
            tournament_id=tournament_id,
            players_data=players_data,
            captain_data=captain_data
        )
        db_sess.add(team)
        db_sess.commit()
        return redirect("/")
    return render_template('join_tournament.html', title='Добавление команды', form=form)


@app.route("/streams")
def stream():
    return render_template("streams.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


api.add_resource(TournamentListResource, '/api/v1/tournaments')
api.add_resource(SoloRegistrationResource, '/api/v1/register/solo')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
