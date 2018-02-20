import uuid

from flask import session

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User
import src.models.game_preview.constants as PreviewConstants

__author__ = 'hooper-p'


class Preview(object):
    def __init__(self, game, author, preview, created_on, updated_on=None, _id=None):
        self.game = Game.get_game_by_id(game)
        self.author = User.get_user_by_id(author)
        self.preview = preview
        self.created_on = created_on
        self.updated_on = updated_on
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_preview_by_id(cls, _id):
        return cls(**Database.find_one(PreviewConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_preview_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(PreviewConstants.COLLECTION, {"game": game})]

    @classmethod
    def get_preview_by_game_and_user(cls, game, user):
        return cls(**Database.find_one(PreviewConstants.COLLECTION, {"game": game, "author": user}))

    def save_to_mongo(self):
        Database.update(PreviewConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game": self.game._id,
            "author": self.author._id,
            "preview": self.preview,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
            "_id": self._id
        }