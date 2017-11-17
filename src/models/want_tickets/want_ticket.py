import uuid

from flask import session

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User
import src.models.want_tickets.constants as WantTicketConstants

__author__ = 'hooper-p'


class WantTicket(object):
    def __init__(self, user, game, number, _id=None):
        self.user = User.get_user_by_id(user)
        self.game = Game.get_game_by_num(game)
        self.number = number
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} {} wants {} tickets to the {} game.".format(self.user.f_name, self.user.l_name, self.number, self.game)

    @staticmethod
    def get_wanttickets_by_game(game):
        return Database.find(WantTicketConstants.COLLECTION, {"game": game})

    @classmethod
    def get_wantticket_by_id(cls, _id):
        return cls(**Database.find_one(WantTicketConstants.COLLECTION, {"_id": _id}))

    def save_to_mongo(self):
        Database.update(WantTicketConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game.game_num,
            "number": self.number,
            "_id": self._id
        }
