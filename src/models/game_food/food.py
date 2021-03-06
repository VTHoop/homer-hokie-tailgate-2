import uuid

from flask import session

from src.common.database import Database
import src.models.game_food.constants as FoodConstants
from src.models.games.game import Game
from src.models.users.user import User

__author__ = 'hooper-p'


class Food(object):
    def __init__(self, user, food, game, _id=None):
        self.user = User.get_user_by_id(user)
        self.food = food
        self.game = Game.get_game_by_id(game)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} {} is bringing {} to the {} game.".format(self.user.f_name, self.user.l_name, self.food, self.game)

    def delete_food(self):
        Database.delete(FoodConstants.COLLECTION, {"_id": self._id})

    @classmethod
    def get_all_food(cls):
        return [cls(**elem) for elem in Database.find(FoodConstants.COLLECTION, {})]

    @classmethod
    def get_food_by_id(cls, _id):
        return cls(**Database.find_one(FoodConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_food_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(FoodConstants.COLLECTION, {"game": game})]

    def save_to_mongo(self):
        Database.update(FoodConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            'user': self.user._id,
            'food': self.food,
            'game': self.game._id,
            '_id': self._id
        }
