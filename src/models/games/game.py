import uuid

from src.common.database import Database
from src.models.teams.team import Team
import src.models.games.constants as GameConstants

__author__ = 'hooper-p'


class Game(object):
    def __init__(self, game_num, home_team, away_team, date=None, time=None, location=None ,stadium=None, theme=None, _id=None):
        self.game_num = game_num
        self.home_team = Team.get_by_school_name(home_team)
        self.away_team = Team.get_by_school_name(away_team)
        self.location = Team.get_by_school_name(home_team).location if location is None else location
        self.stadium = Team.get_by_school_name(home_team).stadium if stadium is None else stadium
        self.date = date
        self.time = 'TBD' if time is None else time
        self.theme = theme
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "The game of {} at {} will be played on {} at {}".format(self.away_team, self.home_team, self.date,
                                                                        self.stadium)

    @classmethod
    def get_game_by_id(cls, _id):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_game_by_num(cls, num):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"game_num": num}))

    @classmethod
    def get_all_games(cls):
        return [cls (**elem) for elem in Database.find(GameConstants.COLLECTION, {})]

    def update_game_time(self, new_date, new_time):
        self.date = new_date
        self.time = new_time
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def update_theme(self, new_theme):
        self.theme = new_theme
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.insert(GameConstants.COLLECTION, self.json())

    def json(self):
        return {
            "game_num": self.game_num,
            "home_team": self.home_team.school_name,
            "away_team": self.away_team.school_name,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "stadium": self.stadium,
            "theme": self.theme,
            "_id": self._id
        }