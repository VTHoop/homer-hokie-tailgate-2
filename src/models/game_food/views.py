from flask import Blueprint, request, session, redirect, url_for

from src.models.game_food.food import Food

__author__ = 'hooper-p'

gamefood_blueprint = Blueprint('game_food', __name__)


@gamefood_blueprint.route('/addfood')
def add_food(game):
    """
    This method will get the name of the food from the form and save that food, the logged in user, and the current
    game that the user is viewing to the database.
    :param game: This is the game that the user is currently viewing
    :return:
    """

    if request.method == 'POST':
        new_food = Food(request.form['food'], game)
        Food.save_to_mongo(new_food)


@gamefood_blueprint.route('/deletefood/<string:food>')
def delete_food(food):
    game_num = Food.get_food_by_id(food).game.game_num
    Food.get_food_by_id(food).delete_food()
    return redirect(url_for('games.detail', game_num=game_num))