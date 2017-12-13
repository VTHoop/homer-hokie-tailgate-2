import uuid

import src.models.locations.constants as LocationConstants
from src.common.database import Database

__author__ = 'hooper-p'


class Location(object):
    def __init__(self, city, state, zip, _id=None):
        self.city = city
        self.state = state
        self.zip = zip
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_all_locations(cls):
        return [cls(**elem) for elem in
                Database.find_and_sort(LocationConstants.COLLECTION, {}, [("state", 1), ["city", 1]])]

    @classmethod
    def get_location_by_id(cls, id):
        return cls(**Database.find_one(LocationConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(LocationConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "city": self.city,
            "state": self.state,
            "zip": self.zip
        }
