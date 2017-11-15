from datetime import datetime

from src.models.games.game import Game

__author__ = 'hooper-p'

from flask import Blueprint, render_template

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/detail/<int:game_num>')
def detail(game_num):
    this_game = Game.get_game_by_num(game_num)
    this_game.date = datetime.strftime(datetime.strptime(this_game.date, "%m/%d/%Y"), "%B %d")
    return render_template("games/game_detail.jinja2", game=this_game)

