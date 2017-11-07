import uuid

from src.common.database import Database
from src.models.users.user import User
import src.models.game_preview.constants as PreviewConstants

__author__ = 'hooper-p'


class Preview(object):
    def __init__(self, game, author, preview, date, time, _id=None):
        """

        :param game:
        :param author: This is the user ID of the author.  Will initialize with first and last name of the user
        :param preview:
        :param date:
        :param time:
        """
        self.game = game
        self.author_fname = User.get_user_by_id(author).f_name
        self.author_lname = User.get_user_by_id(author).l_name
        self.preview = preview
        self.date = date
        self.time = time
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_preview_by_id(cls, _id):
        return cls(**Database.find_one(PreviewConstants.COLLECTION, {"_id": _id}))

    def insert_new_preview(self):
        Database.insert(PreviewConstants.COLLECTION, self.json())

    def json(self):
        return {
            "game": self.game,
            "author_fname": self.author_fname,
            "author_lname": self.author_lname,
            "preview": self.preview,
            "date": self.date,
            "time": self.time,
            "_id": self._id
        }