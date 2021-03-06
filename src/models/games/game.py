import uuid
from bs4 import BeautifulSoup
import requests

from src.common.database import Database
from src.models.locations.location import Location
from src.models.team_years.team_year import TeamYear
from src.models.teams.team import Team
import src.models.games.constants as GameConstants
import src.models.teams.constants as TeamConstants
from datetime import datetime

from src.models.years.year import Year

__author__ = 'hooper-p'


class Game(object):
    def __init__(self, game_num, home_team, away_team, year, date=None, time='TBA', location=None, stadium=None,
                 theme=None, hht_theme=None, TV=None, home_score=0, away_score=0, score_updated_on=None,
                 _id=None):
        self.game_num = game_num
        self.home_team = TeamYear.get_by_hokie_sports_name_and_year(home_team, year)
        self.away_team = TeamYear.get_by_hokie_sports_name_and_year(away_team, year)
        self.location = Location.get_location_by_id(
            Team.get_by_school_name(home_team).location._id) if location is None else Location.get_location_by_id(
            location['_id'])
        self.stadium = Team.get_by_school_name(home_team).stadium if stadium is None else stadium
        self.year = Year.get_year_by_id(year)
        self.date = date
        self.time = 'TBA' if time == 'TBA' else datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%I:%M %p")
        self.hht_theme = hht_theme
        self.theme = theme
        self.TV = TV
        self.home_score = home_score
        self.away_score = away_score
        self.score_updated_on = score_updated_on
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "The game of {} at {} will be played on {} at {}".format(self.away_team, self.home_team, self.date,
                                                                        self.stadium)

    @classmethod
    def get_game_by_id(cls, _id):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_game_by_num(cls, num, year):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"game_num": num, "year": year}))

    @classmethod
    def get_games_by_year(cls, year):
        return [cls(**elem) for elem in Database.find_and_sort(GameConstants.COLLECTION, {"year": year}, [("date", 1)])]

    @classmethod
    def get_all_games(cls):
        return [cls(**elem) for elem in Database.find(GameConstants.COLLECTION, {})]

    @staticmethod
    def get_all_stadiums():
        return Database.DATABASE[TeamConstants.COLLECTION].distinct("stadium")

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
            "score_updated_on": self.score_updated_on,
            "_id": self._id
        }

    @classmethod
    def get_all_prior_games_in_current_year(cls):
        """
        Get all games in current year by descending order.  Iterate through loop and return all games that have already
        happened.
        :return: return list of all games that have happened
        """
        prior_games = []
        games = [cls(**elem) for elem in
                 Database.find_and_sort(GameConstants.COLLECTION, {"year": Year.get_current_year()._id},
                                        [("date", -1)])]
        for g in games:
            if g.date < datetime.now():
                prior_games.append(g)
        return prior_games

    def get_opponent(self):
        return self.home_team.team.school_name if self.away_team.team.school_name == 'Virginia Tech'\
            else self.away_team.team.school_name

    @classmethod
    def get_next_game(cls):
        games = [cls(**elem) for elem in
                 Database.find_and_sort(GameConstants.COLLECTION, {"year": Year.get_current_year()._id},
                                        [("date", 1)])]
        for game in games:
            if game.date > datetime.now():
                return game

    @classmethod
    def get_game_by_opponent(cls, opponent, year):
        """
        If only the opponent and year is known, retrieve game of that opponent.
        :param opponent: school name of the opponent playing Virginia Tech
        :param year: _id of the year for the game being played against Virginia Tech
        :return: an instance of game for that opponent and year
        """
        if Database.find_one(GameConstants.COLLECTION, {"home_team": opponent, "year": year}):
            return cls(**Database.find_one(GameConstants.COLLECTION, {"home_team": opponent, "year": year}))
        else:
            return cls(**Database.find_one(GameConstants.COLLECTION, {"away_team": opponent, "year": year}))

    @staticmethod
    def get_game_tv(o):
        game_tv_tag = o.find("div", {"class": "sidearm-schedule-game-coverage"})
        if game_tv_tag.find("img"):
            tv = game_tv_tag.find("img")
            return tv['alt']

    @staticmethod
    def get_game_theme(o):
        theme_tag = o.find("span", {"class": "sidearm-schedule-game-promotion-name"})
        return theme_tag.text.strip() if theme_tag else None

    @staticmethod
    def get_game_time(unformatted_time_tag):
        unformatted_time = unformatted_time_tag.text.strip()
        if unformatted_time == 'TBA':
            return 'TBA'
        elif len(unformatted_time) == 4:
            return datetime.strftime(datetime.strptime(unformatted_time, "%I %p"), "%I:%M %p")
        else:
            return datetime.strftime(datetime.strptime(unformatted_time, "%I:%M %p"), "%I:%M %p")

    @staticmethod
    def get_game_score(o, game):
        game_score = o.find("div", {"class": "sidearm-schedule-game-result"}) \
            .find("span").find_next_sibling().find_next_sibling().text

        if game.away_team.team.school_name == 'Virginia Tech':
            away_score = game_score[:game_score.find("-")]
            home_score = game_score[game_score.find("-") + 1:]
        else:
            home_score = game_score[:game_score.find("-")]
            away_score = game_score[game_score.find("-") + 1:]
        return away_score, home_score

    @staticmethod
    def load_game_details():
        """
        This function will scrape the hokiesports website for a span called "schedule-opponent".
          From that tag, several elements of a game can be determined and those functions are called within
           this function.
        :return: None
        """
        # start date of current year object will determine the schedule pulled from hokiesports.com
        link = "https://hokiesports.com/schedule.aspx?path=football"
        headers = {'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0'}
        request = requests.get(link, headers=headers)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")
        opponents = soup.find_all('li', {'class': 'sidearm-schedule-game'})

        for o in opponents:
            # get tag that has opponent name
            if o.find("span", {"class": "sidearm-schedule-game-opponent-name"}):
                opponent_name = o.find("span", {"class": "sidearm-schedule-game-opponent-name"})

                # get game with opponent
                # ignore spring game and other games not defined
                if Database.DATABASE[GameConstants.COLLECTION].find_one(
                        {"$or": [{"home_team": opponent_name.text.strip()}, {"away_team": opponent_name.text.strip()}],
                         "year": Year.get_current_year()._id}):
                    game = Game.get_game_by_opponent(opponent_name.text.strip(), Year.get_current_year()._id)

                    if game.date > datetime.now():
                        unformatted_time_tag = o.find("div", {"class": "sidearm-schedule-game-opponent-date"}) \
                            .find("span").find_next_sibling()
                        game.TV = Game.get_game_tv(o)
                        game.time = Game.get_game_time(unformatted_time_tag)
                        game.theme = Game.get_game_theme(o)
                    if game.home_score == 0 and game.away_score == 0 and game.date < datetime.now() \
                            and game.score_updated_on is None:
                        game.away_score, game.home_score = Game.get_game_score(o, game)
                        game.score_updated_on = datetime.now()
                    game.save_to_mongo()
