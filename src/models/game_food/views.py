from flask import Blueprint, request, session

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


@gamefood_blueprint.route('/deletefood')
def delete_food():
    """
    THis function will receive the ID of the food that is being deleted and call the function to delete the food
    !!!! Will need to figure out how the food will be passed in to this function !!!!
    :return:
    """

    food = request.form['food']

    Food.delete_food(food)