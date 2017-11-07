from src.common.database import Database
import src.models.user_scores.constants as ScoreConstants

__author__ = 'hooper-p'


class UserScore(object):
    def __init__(self, user, game, home_score, away_score):
        self.user = user
        self.game = game
        self.home_score = home_score
        self.away_score = away_score

    def __repr__(self):
        return "{} chose a score of {}-{} for the {} game".format(self.user, self.away_score, self.home_score,
                                                                  self.game)

    @classmethod
    def get_score_by_user_and_game(cls, game, user):
        return cls(**Database.find_one(ScoreConstants.COLLECTION, {"game": game, "user": user}))

    def update_user_score(self, new_home_score, new_away_score):
        self.home_score = new_home_score
        self.away_score = new_away_score
        Database.update(ScoreConstants.COLLECTION, {"game": self.game}, self.json())

    def create_user_score(self):
        Database.insert(ScoreConstants.COLLECTION, self.json())

    def json(self):
        return {
            "user": self.user,
            "game": self.game,
            "home_score": self.home_score,
            "away_score": self.away_score
        }
