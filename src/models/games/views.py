from src.models.games.game import Game

__author__ = 'hooper-p'

from flask import Blueprint, render_template

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/detail')
def game_detail():
    # this_game = Game.get_game_by_id(game)
    return render_template("games/game_detail.jinja2")

