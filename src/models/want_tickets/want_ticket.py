import uuid

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

    @classmethod
    def get_all_wanttickets(cls):
        return [cls(**elem) for elem in Database.find(WantTicketConstants.COLLECTION, {})]

    @classmethod
    def get_wanttickets_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(WantTicketConstants.COLLECTION, {"game": game})]

    @classmethod
    def get_wantticket_by_id(cls, _id):
        return cls(**Database.find_one(WantTicketConstants.COLLECTION, {"_id": _id}))

    def save_to_mongo(self):
        Database.update(WantTicketConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game._id,
            "number": self.number,
            "_id": self._id
        }
