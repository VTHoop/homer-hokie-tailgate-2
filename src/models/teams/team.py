import uuid
import requests
from bs4 import BeautifulSoup

from src.common.database import Database

import src.models.teams.constants as TeamConstants

__author__ = 'hooper-p'


class Team(object):
    def __init__(self, school_name, logo=None, location=None, stadium=None, short_name=None, mascot=None, _id=None):
        self.school_name = school_name
        self.mascot = mascot
        self.short_name = short_name
        self.logo = logo
        self.location = location
        self.stadium = stadium
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "The {} {} play in {} located in {}".format(self.school_name, self.mascot, self.stadium, self.location)

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
            "logo": self.logo,
            "location": self.location,
            "stadium": self.stadium,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(TeamConstants.COLLECTION, {"_id": self._id}, self.json())
