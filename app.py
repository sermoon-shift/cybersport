from flask import Flask, render_template

app = Flask(__name__)


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

@app.route("/join_tournament")
def join():
    return render_template("join_tournament.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)