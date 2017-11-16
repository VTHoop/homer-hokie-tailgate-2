import uuid

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User

import src.models.user_games.constants as UserGameConstants

__author__ = 'hooper-p'


class UserGame(object):
    def __init__(self, user, game, attendance, home_score, away_score, _id=None):
        self.user = User.get_user_by_id(user)
        self.game = Game.get_game_by_num(game)
        self.attendance = attendance
        self.home_score = home_score
        self.away_score = away_score
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says for game {} that their status is {}".format(self.user.f_name, self.game.game_num, self.attendance)

    @classmethod
    def get_attendance_by_user(cls, user):
        return [cls(**elem) for elem in Database.find_and_sort(UserGameConstants.COLLECTION,  {"user": user }, "game", 1)]
    
    @classmethod
    def get_attendance_by_game_and_status(cls, game, attendance):
       return [cls(**elem) for elem in Database.find(UserGameConstants.COLLECTION,  {"game": game, "attendance": attendance})]

    def save_to_mongo(self):
        Database.update(UserGameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game.game_num,
            "attendance": self.attendance,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "_id": self._id
        }
