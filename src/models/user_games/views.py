from flask import request, session, render_template, Blueprint

from src.models.user_games.user_game import UserGame
from src.models.years.year import Year

__author__ = 'hooper-p'

user_games_blueprint = Blueprint('dashboard', __name__)


@user_games_blueprint.route('/', methods=['GET', 'POST'])
def user_dashboard():
    year = Year.get_current_year()
    if request.method == 'POST':
        attendance = UserGame.get_attendance_by_user(session['user'], year.start_date, year.end_date)
        for game in attendance:
            game.home_score = request.form['home_score' + str(game.game.game_num)]
            game.away_score = request.form['away_score' + str(game.game.game_num)]
            game.attendance = request.form['attendance' + str(game.game.game_num)]
            game.save_to_mongo()

    attendance = UserGame.get_attendance_by_user(session['user'], year.start_date, year.end_date)

    return render_template("users/dashboard.jinja2", attendance=attendance)


@user_games_blueprint.route('/admin/editscores/<string:game_id>', methods=['GET', 'POST'])
def admin_edit_scores(game_id):
    if request.method == 'POST':
        pass
    else:
        pass

    scores = UserGame.get_attendance_by_game(game_id)
    return render_template("user_games/edit_scores.jinja2", scores=scores)