from flask import request, session, render_template, Blueprint

from src.models.user_games.user_game import UserGame

__author__ = 'hooper-p'

user_games_blueprint = Blueprint('dashboard', __name__)


@user_games_blueprint.route('/', methods=['GET', 'POST'])
def user_dashboard():
    if request.method == 'POST':
        attendance = UserGame.get_attendance_by_user(session['user'])
        for game in attendance:
            game.home_score = request.form['home_score' + str(game.game.game_num)]
            game.away_score = request.form['away_score' + str(game.game.game_num)]
            game.attendance = request.form['attendance' + str(game.game.game_num)]
            game.save_to_mongo()
    else:
        attendance = UserGame.get_attendance_by_user(session['user'])

    return render_template("users/dashboard.jinja2", attendance=attendance)


@user_games_blueprint.route('/admin/editscores/<string:gameid>', methods=['GET', 'POST'])
def admin_edit_scores(gameid):
    if request.method == 'POST':
        pass
    else:
        pass

    scores = UserGame.get_attendance_by_game(gameid)
    return render_template("users/dashboard.jinja2", attendance=attendance)