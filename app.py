import secrets

from flask import Flask, render_template, redirect
from flask_login import login_user

from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from models.user_model import User
from db_init import db

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/database.db"



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)



if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8080, debug=True)