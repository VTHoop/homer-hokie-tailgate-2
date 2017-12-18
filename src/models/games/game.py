import uuid
from bs4 import BeautifulSoup
import requests

from src.common.database import Database
from src.models.locations.location import Location
from src.models.team_years.team_year import TeamYear
from src.models.teams.team import Team
import src.models.games.constants as GameConstants
from datetime import datetime

from src.models.years.year import Year

__author__ = 'hooper-p'


class Game(object):
    def __init__(self, game_num, home_team, away_team, year, date=None, time='TBD', location=None, stadium=None,
                 theme=None, hht_theme=None, TV=None, _id=None):
        self.game_num = game_num
        self.home_team = TeamYear.get_by_school_name_and_year(home_team, year)
        self.away_team = TeamYear.get_by_school_name_and_year(away_team, year)
        self.location = Location.get_location_by_id(
            Team.get_by_school_name(home_team).location._id) if location is None else Location.get_location_by_id(
            location['_id'])
        self.stadium = Team.get_by_school_name(home_team).stadium if stadium is None else stadium
        self.year = Year.get_year_by_id(year)
        self.date = datetime.strptime(date, "%m/%d/%Y")
        self.time = 'TBD' if time == 'TBD' else datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%I:%M %p")
        self.hht_theme = hht_theme
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
    def get_games_by_year(cls, year):
        return [cls(**elem) for elem in Database.find_and_sort(GameConstants.COLLECTION, {"year": year}, [("date", 1)])]

    @classmethod
    def get_all_games(cls):
        return [cls(**elem) for elem in Database.find(GameConstants.COLLECTION, {})]

    @staticmethod
    def get_all_stadiums():
        return Database.DATABASE[GameConstants.COLLECTION].distinct("stadium")

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
            # get tag that has opponent name
            opponent_name = o.find("a")
            # get game with opponent
            game = Game.get_game_by_opponent(opponent_name.text)
            get_parent_tag = opponent_name.parent.parent.parent
            get_next_sibling = get_parent_tag.find_next_sibling()
            tv = get_next_sibling.find("img")
            game.TV = tv['alt']
            game.save_to_mongo()

    def save_to_mongo(self):
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game_num": int(self.game_num),
            "home_team": self.home_team.team.school_name,
            "away_team": self.away_team.team.school_name,
            "year": self.year._id,
            "date": self.date,
            "time": self.time,
            "location": self.location.json(),
            "stadium": self.stadium,
            "theme": self.theme,
            "hht_theme": self.hht_theme,
            "TV": self.TV,
            "_id": self._id
        }
