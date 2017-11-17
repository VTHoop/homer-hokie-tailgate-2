from datetime import datetime

from src.models.games.game import Game
from src.models.user_games.user_game import UserGame

__author__ = 'hooper-p'

from flask import Blueprint, render_template

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/detail/<int:game_num>')
def detail(game_num):
    this_game = Game.get_game_by_num(game_num)
    yes_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'Yes')
    maybe_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'Maybe') 
    no_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'No') 
    this_game.date = datetime.strftime(datetime.strptime(this_game.date, "%m/%d/%Y"), "%B %d")
    return render_template("games/game_detail.jinja2", game=this_game, yes_attendance=yes_attendance, maybe_attendance=maybe_attendance, no_attendance=no_attendance)

