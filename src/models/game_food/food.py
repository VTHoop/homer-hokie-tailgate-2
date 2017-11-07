import uuid

from flask import session

from src.common.database import Database
import src.models.game_food.constants as FoodConstants
from src.models.users.user import User

__author__ = 'hooper-p'


class Food(object):
    def __init__(self, food, game, _id=None):
        self.user = session['user']
        self.food = food
        self.game = game
        self.user_fname = User.get_user_by_id(self.user).f_name
        self.user_lname = User.get_user_by_id(self.user).l_name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} {} is bringing {} to the {} game.".format(self.user_fname, self.user_lname, self.food, self.game)

    @staticmethod
    def delete_food(food):
        Database.delete(FoodConstants.COLLECTION, {"_id": food})

    @classmethod
    def get_food_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(FoodConstants.COLLECTION, {"game": game})]

    def save_to_mongo(self):
        Database.insert(FoodConstants.COLLECTION, self.json())

    def json(self):
        return {
            'food': self.food,
            'game': self.game,
            'user_fname': self.user_fname,
            'user_lname': self.user_lname,
            '_id': self._id
        }
