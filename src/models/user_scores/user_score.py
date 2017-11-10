import uuid

from src.common.database import Database

from src.models.games.game import Game
from src.models.users.user import User

import src.models.user_scores.constants as ScoreConstants

__author__ = 'hooper-p'


class UserScore(object):
    def __init__(self, user, game, home_score, away_score, _id=None):
        self.user = User.get_user_by_id(user)
        self.game = Game.get_game_by_num(game)
        self.home_score = home_score
        self.away_score = away_score
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} chose a score of {}-{} for the {} game".format(self.user, self.away_score, self.home_score,
                                                                  self.game)

    @classmethod
    def get_scores_by_user_game(cls, user, game):
        return cls(**Database.find_one(ScoreConstants.COLLECTION, {"user": user, "game": game}))

    @classmethod
    def get_scores_by_user(cls, user):
        return [cls(**elem) for elem in Database.find(ScoreConstants.COLLECTION, {"user": user})]

    def update_user_score(self, new_home_score, new_away_score):
        self.home_score = new_home_score
        self.away_score = new_away_score
        Database.update(ScoreConstants.COLLECTION, {"game": self.game}, self.json())

    def create_user_score(self):
        Database.insert(ScoreConstants.COLLECTION, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game.game_num,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "_id": self._id
        }
