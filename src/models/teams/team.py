import uuid

from src.common.database import Database

import src.models.teams.constants as TeamConstants

__author__ = 'hooper-p'


class Team(object):
    def __init__(self, school_name, mascot, conference, wins, losses, logo, location, stadium, short_name=None, _id=None):
        self.school_name = school_name
        self.mascot = mascot
        self.short_name = short_name
        self.conference = conference
        self.wins = wins
        self.losses = losses
        self.logo = logo
        self.location = location
        self.stadium = stadium
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "The {} {} are {}-{} and play in the {} conference.".format(self.school_name, self.mascot, self.wins,
                                                                           self.losses, self.conference)

    @staticmethod
    def update_records():
        pass
        # retrieve all teams
        # iterate through teams
        # scrape website for wins and losses
        # save to database

    @classmethod
    def get_by_school_name(cls, team):
        return cls(**Database.find_one(TeamConstants.COLLECTION, {"school_name": team}))

    @classmethod
    def get_teams(cls):
        return [cls(**elem) for elem in Database.find(TeamConstants.COLLECTION, {})]

    def json(self):
        return{
            "school_name": self.school_name,
            "mascot": self.mascot,
            "short_name": self.short_name,
            "conference": self.conference,
            "wins": self.wins,
            "losses": self.losses,
            "logo": self.logo,
            "location": self.location,
            "stadium": self.stadium,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(TeamConstants.COLLECTION, {"_id": self._id}, self.json())
