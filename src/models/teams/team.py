import uuid
import requests
from bs4 import BeautifulSoup

from src.common.database import Database

import src.models.teams.constants as TeamConstants

__author__ = 'hooper-p'


class Team(object):
    def __init__(self, school_name, wins, losses, conference=None, logo=None, location=None, stadium=None,
                 short_name=None,
                 mascot=None,
                 conf_wins=None, conf_losses=None, ap_rank=None, _id=None):
        self.school_name = school_name
        self.mascot = mascot
        self.short_name = short_name
        self.conference = conference
        self.wins = wins
        self.losses = losses
        self.conf_wins = conf_wins
        self.conf_losses = conf_losses
        self.logo = logo
        self.location = location
        self.stadium = stadium
        self.ap_rank = ap_rank
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "The {} {} are {}-{}, ranked {} and are {}-{} in the {} conference.". \
            format(self.school_name, self.mascot, self.wins, self.losses, self.ap_rank, self.conf_wins,
                   self.conf_losses, self.conference)

    @staticmethod
    def update_teams():
        link = "https://www.sports-reference.com/cfb/years/2017-standings.html"
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

            if Team.get_by_school_name(sn):
                team = Team.get_by_school_name(sn)
                team.conference = conf.text
                team.wins = wins.text
                team.losses = losses.text
                team.conf_wins = conf_wins.text
                team.conf_losses = conf_losses.text
                team.ap_rank = ap_rank.text
                team.save_to_mongo()
                # team = Team(sn, conf, wins, losses, ap_rank=ap_rank, conf_wins=conf_wins, conf_losses=conf_losses)

    @classmethod
    def get_by_school_name(cls, team):
        if Database.find_one(TeamConstants.COLLECTION, {"school_name": team}) is not None:
            return cls(**Database.find_one(TeamConstants.COLLECTION, {"school_name": team}))
        else:
            return None

    @classmethod
    def get_teams(cls):
        return [cls(**elem) for elem in Database.find(TeamConstants.COLLECTION, {})]

    def json(self):
        return {
            "school_name": self.school_name,
            "mascot": self.mascot,
            "short_name": self.short_name,
            "conference": self.conference,
            "wins": self.wins,
            "losses": self.losses,
            "logo": self.logo,
            "location": self.location,
            "stadium": self.stadium,
            "conf_wins": self.conf_wins,
            "conf_losses": self.conf_losses,
            "ap_rank": self.ap_rank,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(TeamConstants.COLLECTION, {"_id": self._id}, self.json())
