import datetime
import operator

from collections import defaultdict
from flask import request, session, render_template, Blueprint

from src.models.games.game import Game
from src.models.user_games.user_game import UserGame
from src.models.years.year import Year

import src.models.users.decorators as user_decorators

__author__ = 'hooper-p'

user_games_blueprint = Blueprint('dashboard', __name__)


@user_games_blueprint.route('/', methods=['GET', 'POST'])
@user_decorators.requires_login
def user_dashboard():
    year = Year.get_current_year()

    if request.method == 'POST':
        attendance = UserGame.get_attendance_by_user(session['user'], year.start_date, year.end_date)
        for a in attendance:
            a.home_score = request.form['home_score' + str(a.game.game_num)]
            a.away_score = request.form['away_score' + str(a.game.game_num)]
            a.attendance = request.form['attendance' + str(a.game.game_num)]
            # since user is saving all scores, only update the updated_on date for those games that are not readonly
            if a.game.date > datetime.datetime.now():
                a.admin_enter = 'No'
                a.score_updated_on = datetime.datetime.now()
            a.save_to_mongo()

    attendance = UserGame.get_attendance_by_user(session['user'], year.start_date, year.end_date)
    return render_template("users/dashboard.jinja2",
                           attendance=attendance,
                           cutoff=datetime.datetime.now()+datetime.timedelta(days=3))


@user_games_blueprint.route('/admin/editscores/<string:game_id>', methods=['GET', 'POST'])
def admin_edit_scores(game_id):
    if request.method == 'POST':
        usergame = UserGame.get_usergame_by_id(request.form['usergame'])
        usergame.home_score = request.form['home_score' + usergame._id]
        usergame.away_score = request.form['away_score' + usergame._id]
        usergame.admin_enter = 'Yes'
        usergame.score_updated_on = datetime.datetime.now()
        usergame.save_to_mongo()

    scores = UserGame.get_attendance_by_game(game_id)
    return render_template("user_games/edit_scores.jinja2", scores=scores)


@user_games_blueprint.route('/leaderboard', methods=['GET', 'POST'])
def get_leaderboard():
    """
    This function will get all games up to and including the game that is selected for the leaderboard.  The
    function receives the game._id of the game to be viewed and a dict is built to sum up the total of points
    accumulated by each user

    :return: leaderboard template with unzipped lists of leaders and the totals, as well as the user game details
    for the game passed into the function and pass through of the game id
    """

    games_prior = Game.get_all_prior_games_in_current_year()
    if games_prior:
        if request.method == 'GET':
            max_game = games_prior[0]
        elif request.method == 'POST':
            max_game = Game.get_game_by_id(request.form['game_view'])

        user_games_prior = UserGame.get_all_prior_games_in_current_year(max_game.game_num)
        user_totals = defaultdict(int)
        for ug in user_games_prior:
            user_totals[ug.user._id] += ug.total_points
        user_totals_sorted = sorted(user_totals.items(), key=operator.itemgetter(1), reverse=True)
        leaders = [x[0] for x in user_totals_sorted]
        points = [x[1] for x in user_totals_sorted]
        print(leaders, points)
        latest_user_games = UserGame.get_attendance_by_game(max_game._id)
        return render_template("user_games/leaderboard.jinja2", leaders=leaders, points=points,
                               latest_user_games=latest_user_games, games_prior=games_prior, max_game=max_game)
    else:
        return render_template("user_games/no_games_played.jinja2")


