import uuid

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User

import src.models.user_games.constants as UserGameConstants

__author__ = 'hooper-p'


class UserGame(object):
    def __init__(self, user, game, game_date, attendance, home_score, away_score, admin_enter=None, _id=None):
        self.user = User.get_user_by_id(user['_id'])
        self.game = Game.get_game_by_id(game)
        self.game_date = Game.get_game_by_id(game).date
        self.attendance = attendance
        self.home_score = home_score
        self.away_score = away_score
        self.admin_enter = admin_enter
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says for game {} that their status is {}".format(self.user.f_name, self.game.game_num,
                                                                    self.attendance)

    @classmethod
    def get_all_usergames(cls):
        return [cls(**elem) for elem in Database.find(UserGameConstants.COLLECTION, {})]

    @classmethod
    def get_usergame_by_id(cls, _id):
        return cls(**Database.find_one(UserGameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_attendance_by_user(cls, user, beg_date, end_date):
        return [cls(**elem) for elem in
                Database.find_and_sort(UserGameConstants.COLLECTION,
                                       {"user._id": user,
                                        "game_date": {'$lte': end_date, '$gte': beg_date}},
                                       [("game_date", 1)])]

    @classmethod
    def get_attendance_by_game(cls, game):
        return [cls(**elem) for elem in
                Database.find_and_sort(UserGameConstants.COLLECTION, {"game": game},
                                       [("user.l_name", 1), ("user.f_name", 1)])]

    @classmethod
    def get_attendance_by_game_and_status(cls, game, attendance):
        return [cls(**elem) for elem in
                Database.find(UserGameConstants.COLLECTION, {"game": game, "attendance": attendance})]

    def save_to_mongo(self):
        Database.update(UserGameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user.json(),
            "game": self.game._id,
            "game_date": self.game_date,
            "attendance": self.attendance,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "admin_enter": self.admin_enter,
            "_id": self._id
        }