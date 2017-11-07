import uuid

from src.common.database import Database
import src.models.users.constants as UserConstants

__author__ = 'hooper-p'


class User(object):
    def __init__(self, f_name, l_name, email, password, admin='No', _id=None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
        self.admin = admin
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {} has a given name of {} {}".format(self.email, self.f_name, self.l_name)

    @classmethod
    def get_user_by_id(cls, _id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": _id}))

    def update_admin(self):
        pass
    # admin saves form to update fields

    def insert_new_user(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "password": self.password,
            "admin": self.admin,
            "_id": self._id
        }
