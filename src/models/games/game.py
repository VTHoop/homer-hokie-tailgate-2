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
                 theme=None, hht_theme=None, TV=None, home_score=0, away_score=0, _id=None):
        self.game_num = game_num
        self.home_team = TeamYear.get_by_hokie_sports_name_and_year(home_team, year)
        self.away_team = TeamYear.get_by_hokie_sports_name_and_year(away_team, year)
        self.location = Location.get_location_by_id(
            Team.get_by_school_name(home_team).location._id) if location is None else Location.get_location_by_id(
            location['_id'])
        self.stadium = Team.get_by_school_name(home_team).stadium if stadium is None else stadium
        self.year = Year.get_year_by_id(year)
        self.date = date
        self.time = 'TBD' if time == 'TBD' else datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%I:%M %p")
        self.hht_theme = hht_theme
        self.theme = theme
        self.TV = TV
        self.home_score = home_score
        self.away_score = away_score
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
        if Database.find_one(GameConstants.COLLECTION, {"home_team": opponent}):
            return cls(**Database.find_one(GameConstants.COLLECTION, {"home_team": opponent}))
        else:
            return cls(**Database.find_one(GameConstants.COLLECTION, {"away_team": opponent}))

    @staticmethod
    def get_game_tv(opponent_name):
        # get game with opponent
        # ignore spring game and other games not defined
        if Database.find_one(GameConstants.COLLECTION,
                             {"$or": [{"home_team": opponent_name.text}, {"away_team": opponent_name.text}]}):
            game = Game.get_game_by_opponent(opponent_name.text)
            get_parent_tag = opponent_name.parent.parent.parent
            get_next_sibling = get_parent_tag.find_next_sibling()
            tv = get_next_sibling.find("img")
            game.TV = tv['alt']
            game.save_to_mongo()

    @staticmethod
    def get_game_time(opponent_name):
        # get game with opponent
        # ignore spring game and other games not defined
        if Database.find_one(GameConstants.COLLECTION,
                             {"$or": [{"home_team": opponent_name.text}, {"away_team": opponent_name.text}]}):
            game = Game.get_game_by_opponent(opponent_name.text)
            get_parent_tag = opponent_name.parent.parent.parent
            get_schedule_date = get_parent_tag.find("span", {"class": "schedule-date"})
            unformatted_time = get_schedule_date.text[get_schedule_date.text.find("/")+2:]
            if unformatted_time == 'TBD':
                game.time = 'TBD'
            elif len(unformatted_time) == 4:
                game.time = datetime.strftime(datetime.strptime(unformatted_time, "%I %p"), "%I:%M %p")
            else:
                game.time = datetime.strftime(datetime.strptime(unformatted_time, "%I:%M %p"), "%I:%M %p")
            game.save_to_mongo()

    @staticmethod
    def get_game_score(opponent_name):
        # get game with opponent
        # ignore spring game and other games not defined
        # get game with opponent
        # ignore spring game and other games not defined
        if Database.find_one(GameConstants.COLLECTION,
                             {"$or": [{"home_team": opponent_name.text}, {"away_team": opponent_name.text}]}):
            game = Game.get_game_by_opponent(opponent_name.text)
            get_parent_tag = opponent_name.parent.parent.parent
            get_next_sibling = get_parent_tag.find_next_sibling().find_next_sibling()
            raw_score = get_next_sibling.find("span", {"class": "schedule-score"})
            game_score = raw_score.text[raw_score.text.find(",")+2:]

            if game.away_team.team.school_name == 'Virginia Tech':
                game.away_score = game_score[:game_score.find("-")]
                game.home_score = game_score[game_score.find("-")+1:]
            else:
                game.home_score = game_score[:game_score.find("-")]
                game.away_score = game_score[game_score.find("-")+1:]
            game.save_to_mongo()

    @staticmethod
    def load_game_details():
        # start date of current year object will determine the schedule pulled from hokiesports.com
        year_for_link = Year.get_current_year().start_date.strftime('%Y')
        link = "http://www.hokiesports.com/football/schedule/"+year_for_link
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        opponents = soup.find_all("span", {"class": "schedule-opponent"})

        for o in opponents:
            # get tag that has opponent name
            Game.get_game_tv(o.find("a"))
            Game.get_game_time(o.find("a"))
            Game.get_game_score(o.find("a"))

    def save_to_mongo(self):
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game_num": int(self.game_num),
            "home_team": self.home_team.team.hokie_sports_name,
            "away_team": self.away_team.team.hokie_sports_name,
            "year": self.year._id,
            "date": self.date,
            "time": self.time,
            "location": self.location.json(),
            "stadium": self.stadium,
            "theme": self.theme,
            "hht_theme": self.hht_theme,
            "TV": self.TV,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "_id": self._id
        }
