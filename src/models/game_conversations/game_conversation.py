import uuid

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User
import src.models.game_conversations.constants as ConvoConstants

__author__ = 'hooper-p'


class GameConversation(object):
    def __init__(self, user, game, created_on, conversation, _id=None):
        self.user = User.get_user_by_id(user)
        self.game = Game.get_game_by_id(game)
        self.created_on = created_on
        self.conversation = conversation
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '{} user had something to say about {} game on {}'.format(self.user, self.game, self.created_on)

    def insert_conversation(self):
        Database.insert(ConvoConstants, self.json())

    def delete_conversation(self):
        Database.delete(ConvoConstants.COLLECTION, {"_id": self._id})

    def save_to_mongo(self):
        Database.update(ConvoConstants.COLLECTION, {"_id": self._id}, self.json())

    @classmethod
    def get_all_convos(cls):
        return [cls(**elem) for elem in Database.find(ConvoConstants.COLLECTION, {})]

    @classmethod
    def get_convo_by_id(cls, _id):
        return cls(**Database.find_one(ConvoConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_convo_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(ConvoConstants.COLLECTION, {"game": game})]

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game._id,
            "created_on": self.created_on,
            "conversation": self.conversation,
            "_id": self._id
        }