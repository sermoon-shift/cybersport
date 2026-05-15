from flask_restful import Resource, reqparse, abort
from flask import jsonify, request
from db_init import db
from models.news_model import News
from models.tournament_model import Tournament
from models.teams_model import Team
from models.solo_model import Solo

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True, help="Nickname is required")
parser.add_argument('tournament_id', type=int, required=True)
parser.add_argument('data', required=True, help="Additional info (contacts/steam) required")
team_parser = reqparse.RequestParser()
team_parser.add_argument('teamname', required=True)
team_parser.add_argument('tournament_id', type=int, required=True)
team_parser.add_argument('captain_data', required=True, help="captain nickname")
team_parser.add_argument('players_data', required=True, help="player nicknames")


def abort_if_tournament_not_found(tournament_id):
    tournament = db.session.get(Tournament, tournament_id)
    if not tournament:
        abort(404, message=f"Tournament {tournament_id} not found")
    return tournament


class TournamentListResource(Resource):
    def get(self):
        tournaments = db.session.query(Tournament).all()
        output = []
        for t in tournaments:
            tournament_data = {
                "id": t.id,
                "name": t.name,
                "is_solo": t.is_solo,
                "date": t.date.isoformat() if t.date else None,
                "image": t.image
            }
            output.append(tournament_data)
        return jsonify(output)


class SoloRegistrationResource(Resource):
    def post(self):
        args = parser.parse_args()
        tournament = abort_if_tournament_not_found(args['tournament_id'])
        if not tournament.is_solo:
            abort(400, message="This is a team tournament, solo registration is nelyzya")
        new_entry = Solo(
            nickname=args['nickname'],
            tournament_id=args['tournament_id'],
            data=args['data']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'success': 'Registered', 'id': new_entry.id})


class TeamRegistrationResource(Resource):
    def post(self):
        args = team_parser.parse_args()
        tournament = abort_if_tournament_not_found(args['tournament_id'])
        if tournament.is_solo:
            abort(400, message="This is a solo tournament, team registration not allowed")
        new_team = Team(
            teamname=args['teamname'],
            tournament_id=args['tournament_id'],
            captain_data=args['captain_data'],
            players_data=args['players_data']
        )
        db.session.add(new_team)
        db.session.commit()
        return jsonify({'success': 'Team registered', 'id': new_team.id})


class SoloListResource(Resource):
    def get(self):
        tournament_id = request.args.get('tournament_id')
        if tournament_id:
            solos = db.session.query(Solo).filter(Solo.tournament_id == tournament_id).all()
        else:
            solos = db.session.query(Solo).all()
        output = []
        for s in solos:
            try:
                extra_data = json.loads(s.data) if s.data else {}
            except Exception:
                extra_data = s.data
            output.append({
                "id": s.id,
                "nickname": s.nickname,
                "tournament_id": s.tournament_id,
                "data": extra_data
            })
        return jsonify(output)


class TeamListResource(Resource):
    def get(self):
        tournament_id = request.args.get('tournament_id')
        if tournament_id:
            teams = db.session.query(Team).filter(Team.tournament_id == tournament_id).all()
        else:
            teams = db.session.query(Team).all()
        output = []
        for t in teams:
            try:
                players = json.loads(t.players_data) if t.players_data else {}
            except Exception:
                players = t.players_data
            try:
                captain = json.loads(t.captain_data) if t.captain_data else {}
            except Exception:
                captain = t.captain_data
            output.append({
                "id": t.id,
                "teamname": t.teamname,
                "tournament_id": t.tournament_id,
                "captain_data": captain,
                "players_data": players
            })
        return jsonify(output)


class NewsListResource(Resource):
    def get(self):
        all_news = db.session.query(News).order_by(News.date.desc()).all()
        output = []
        for item in all_news:
            output.append({
                "id": item.id,
                "title": getattr(item, 'title', 'Без названия'),
                "text": getattr(item, 'text', getattr(item, 'content', '')),
                "date": item.date.isoformat() if item.date else None
            })
        return jsonify(output)
