import uuid
from datetime import datetime

import src.models.years.constants as YearConstants
from src.common.database import Database

__author__ = 'hooper-p'


class Year(object):
    def __init__(self, start_date, end_date, name, _id=None):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "College Football {} year starts on {} and ends on {}".format(self.name, self.start_date, self.end_date)

    @classmethod
    def get_year_by_id(cls, _id):
        return cls(**Database.find_one(YearConstants.COLLECTION, {"_id": _id}))

    def save_to_mongo(self):
        Database.update(YearConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "name": self.name,
            "_id": self._id
        }