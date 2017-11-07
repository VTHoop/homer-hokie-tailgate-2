from flask import session

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User

import src.models.user_games.constants as UserGameConstants

__author__ = 'hooper-p'


class UserGame(object):
    def __init__(self, user, game, attendance):
        self.user = User.get_user_by_id(session['user'])
        self.game = Game.get_game_by_num(game)
        self.attendance = attendance

    def __repr__(self):
        return "{} says for game {} that their status is {}".format()

    def save_to_mongo(self):
        Database.insert(UserGameConstants.COLLECTION, self.json())

    def json(self):
        return {
            "user": session['user'],
            "game": self.game.game_num,
            "attendance": self.attendance
        }