from flask import Blueprint, request, session, redirect, url_for

from src.models.game_food.food import Food

__author__ = 'hooper-p'

gamefood_blueprint = Blueprint('game_food', __name__)


@gamefood_blueprint.route('/add/<string:game_id>', methods=['POST'])
def add_food(game_id):
    game_food = Food(session['user'], request.form['game_food'], game_id)
    game_food.save_to_mongo()
    return redirect(url_for('games.detail', game_id=game_id, active='food'))


@gamefood_blueprint.route('/deletefood/<string:food>')
def delete_food(food):
    game_id = Food.get_food_by_id(food).game._id
    Food.get_food_by_id(food).delete_food()
    return redirect(url_for('games.detail', game_id=game_id, active='food'))
