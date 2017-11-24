import uuid

from bs4 import BeautifulSoup
import requests

from src.common.database import Database
from src.models.teams.team import Team
import src.models.games.constants as GameConstants
from datetime import datetime

__author__ = 'hooper-p'


class Game(object):
    def __init__(self, game_num, home_team, away_team, date=None, time='TBD', location=None ,stadium=None, theme=None, TV=None, _id=None):
        self.game_num = game_num
        self.home_team = Team.get_by_school_name(home_team)
        self.away_team = Team.get_by_school_name(away_team)
        self.location = Team.get_by_school_name(home_team).location if location is None else location
        self.stadium = Team.get_by_school_name(home_team).stadium if stadium is None else stadium
        self.date = date
        self.time = 'TBD' if time == 'TBD' else datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%I:%M %p")
        self.theme = theme
        self.TV = TV
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

    @classmethod
    def get_game_by_opponent(cls, opponent):
        team = Database.find_one(GameConstants.COLLECTION, {"home_team": opponent})
        if team is not None:
            return cls(**Database.find_one(GameConstants.COLLECTION, {"home_team": opponent}))
        else:
            return cls(**Database.find_one(GameConstants.COLLECTION, {"away_team": opponent}))

    @staticmethod
    def load_game_tv():
        link = "http://www.hokiesports.com/football/schedule/"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        opponents = soup.find_all("span", {"class": "schedule-opponent"})

        for o in opponents:
            opponent_name = o.find("a")
            game = Game.get_game_by_opponent(opponent_name.text)
            get_parent_tag = opponent_name.parent.parent.parent
            get_next_sibling = get_parent_tag.find_next_sibling()
            tv = get_next_sibling.find("img")
            game.TV= tv['alt']
            game.save_to_mongo()

    def update_game_time(self, new_date, new_time):
        self.date = new_date
        self.time = new_time
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def update_theme(self, new_theme):
        self.theme = new_theme
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game_num": int(self.game_num),
            "home_team": self.home_team.school_name,
            "away_team": self.away_team.school_name,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "stadium": self.stadium,
            "theme": self.theme,
            "TV": self.TV,
            "_id": self._id
        }
