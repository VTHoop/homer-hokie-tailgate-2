import uuid

import datetime
import requests

from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.teams.team import Team
from src.models.years.year import Year

import src.models.team_years.constants as TeamYearConstants

__author__ = 'hooper-p'


class TeamYear(object):
    def __init__(self, team, year, wins=0, losses=0, conf_wins=0, conf_losses=0, ap_rank=None, conference=None,
                 _id=None):
        self.team = Team.get_by_school_name(team['school_name'])
        self.year = Year.get_year_by_id(year['_id'])
        self.wins = wins
        self.losses = losses
        self.conf_wins = conf_wins
        self.conf_losses = conf_losses
        self.ap_rank = ap_rank
        self.conference = conference
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "In {}, {} had a record of {}-{}".format(self.year.name, self.team.school_name, self.wins, self.losses)

    def save_to_mongo(self):
        Database.update(TeamYearConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "team": self.team.json(),
            "year": self.year.json(),
            "wins": self.wins,
            "losses": self.losses,
            "conf_wins": self.conf_wins,
            "conf_losses": self.conf_losses,
            "ap_rank": self.ap_rank,
            "conference": self.conference,
            "_id": self._id
        }

    @classmethod
    def get_all_teamyears(cls):
        return [cls(**elem) for elem in Database.find(TeamYearConstants.COLLECTION, {})]

    @classmethod
    def get_by_school_name_and_year(cls, sn, year):
        return cls(**Database.find_one(TeamYearConstants.COLLECTION, {"team.school_name": sn, "year._id": year}))

    @classmethod
    def get_by_hokie_sports_name_and_year(cls, sn, year):
        return cls(**Database.find_one(TeamYearConstants.COLLECTION, {"team.hokie_sports_name": sn, "year._id": year}))

    @classmethod
    def get_by_school_name_and_current_year(cls, sn):
        if Database.find_one(TeamYearConstants.COLLECTION, {"team": sn,
                                                            "year.start_date": {
                                                                '$lte': datetime.datetime.utcnow()},
                                                            "year.end_date": {
                                                                '$gte': datetime.datetime.utcnow()}
                                                            }) is not None:
            return cls(**Database.find_one(TeamYearConstants.COLLECTION, {"team": sn,
                                                                          "year.start_date": {
                                                                              '$lte': datetime.datetime.utcnow()},
                                                                          "year.end_date": {
                                                                              '$gte': datetime.datetime.utcnow()}
                                                                          }))
        else:
            return None

    @staticmethod
    def update_teams():
        link = "https://www.sports-reference.com/cfb/years/2018-standings.html"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        school_names = soup.find_all("td", {"data-stat": "school_name"})
        for school_name in school_names:
            sn = school_name.text
            conf = school_name.find_next_sibling()
            wins = conf.find_next_sibling()
            losses = wins.find_next_sibling()
            over_pct = losses.find_next_sibling()
            conf_wins = over_pct.find_next_sibling()
            conf_losses = conf_wins.find_next_sibling()
            ap_rank = conf_losses.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling() \
                .find_next_sibling().find_next_sibling()

            if TeamYear.get_by_school_name_and_current_year(sn):
                team = TeamYear.get_by_school_name_and_current_year(sn)
                team.conference = conf.text
                team.wins = wins.text
                team.losses = losses.text
                team.conf_wins = conf_wins.text
                team.conf_losses = conf_losses.text
                team.ap_rank = ap_rank.text
                team.save_to_mongo()
                # team = Team(sn, conf, wins, losses, ap_rank=ap_rank, conf_wins=conf_wins, conf_losses=conf_losses)
