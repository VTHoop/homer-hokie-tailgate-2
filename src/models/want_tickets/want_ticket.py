import uuid

from flask import session

from src.common.database import Database
from src.models.users.user import User
import src.models.have_tickets.constants as WantTicketConstants

__author__ = 'hooper-p'


class WantTicket(object):
    def __init__(self, game, number, _id=None):
        self.user = session['user']
        self.user_fname = User.get_user_by_id(self.user).f_name
        self.user_lname = User.get_user_by_id(self.user).l_name
        self.game = game
        self.number = number
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} {} wants {} tickets to the {} game.".format(self.user_fname, self.user_lname, self.number, self.game)

    @staticmethod
    def get_wanttickets_by_game(game):
        return Database.find(WantTicketConstants.COLLECTION, {"game": game})

    @classmethod
    def get_wantticket_by_id(cls, _id):
        return cls(**Database.find_one(WantTicketConstants.COLLECTION, {"_id": _id}))

    def insert_new_wantticket(self):
        Database.insert(WantTicketConstants.COLLECTION, self.json())

    def json(self):
        return {
            "user": self.user,
            "game": self.game,
            "number": self.number,
            "_id": self._id
        }
