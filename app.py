import secrets
import os
import json
from flask import Flask, render_template, redirect, request
from flask_login import login_user
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.join_on_tournamentform import SoloJoin, TeamJoin
from models.user_model import User
from models.teams_model import Team
from models.solo_model import Solo
from models.news_model import News
from models.tournament_model import Tournament
from resources import TournamentListResource, SoloRegistrationResource, TeamRegistrationResource
from flask_migrate import Migrate
from db_init import db
from flask_wtf.csrf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db', 'database.db')}"

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
admin = Admin(app, name='CyberSport Admin')

admin.add_view(ModelView(User, db))
admin.add_view(ModelView(News, db))
admin.add_view(ModelView(Tournament, db))
admin.add_view(ModelView(Team, db))
admin.add_view(ModelView(Solo, db))


@app.route("/")
def index():
    latest_news = News.query.order_by(News.date.desc()).limit(3).all()
    latest_games = Tournament.query.order_by(Tournament.date.desc()).limit(3).all()
    return render_template("index.html", news_list=latest_news, games_list=latest_games)


@app.route("/news")
def news():
    all_news = News.query.order_by(News.date.desc()).all()
    return render_template("news.html", news_list=all_news)


@app.route("/news/<int:news_id>")
def news_detail(news_id):
    item = News.query.get_or_404(news_id)
    return render_template("news_detail.html", item=item)


@app.route("/games")
def games():
    all_games = Tournament.query.order_by(Tournament.date.desc()).all()
    return render_template("tournament.html", games_list=all_games)



@app.route("/join_tournament/<tournament_id>", methods=['GET', 'POST'])
def join_tournament(tournament_id):
    form = TeamJoin()
    format_parameter = True
    if form.validate_on_submit():
        db_sess = db.create_session()
        if db_sess.query(Team).filter(Team.name == form.team_name.data, Team.tournament_id == tournament_id).first():
            return render_template('tournament.html', message="Данная команда уже участвует в этом турнире",
                                   form=form, format_parameter=format_parameter)
        if db_sess.query(Tournament).filter(Tournament.id == tournament_id, Tournament.is_solo == 1).first():
            format_parameter = False
            data = {
                "steam": form.captain.steam,
                "fullname": form.captain.fullname,
                "birthday": form.captain.birthday,
                "vkontakte": form.captain.vkontakte
            }
            solo = Solo(
                nickname=form.captain.nickname,
                tournament_id=tournament_id,
                data = json.dumps(data)
            )
            db_sess.add(solo)
            db_sess.commit()
            return redirect("/")
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
            players_data=json.dumps(players_data),
            captain_data=json.dumps(captain_data)
        )
        db_sess.add(team)
        db_sess.commit()
        return redirect("/")
    elif request.method == 'POST':
        print(form.errors)
    return render_template('join_tournament.html', form=form, format_parameter=format_parameter)


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
api.add_resource(TeamRegistrationResource, '/api/v1/register/team')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
