import uuid

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User
import src.models.want_tickets.constants as WantTicketConstants

__author__ = 'hooper-p'


class WantTicket(object):
    def __init__(self, user, game, number, purchased_flag=None, _id=None):
        self.user = User.get_user_by_id(user)
        self.game = Game.get_game_by_id(game)
        self.number = number
        self.purchased_flag = purchased_flag
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} {} wants {} tickets to the {} game.".format(self.user.f_name, self.user.l_name, self.number, self.game)

    @classmethod
    def get_all_wanttickets(cls):
        return [cls(**elem) for elem in Database.find(WantTicketConstants.COLLECTION, {})]

    @classmethod
    def get_wanttickets_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(WantTicketConstants.COLLECTION, {"game": game})]

    def delete_wantticket(self):
        Database.delete(WantTicketConstants.COLLECTION, {"_id": self._id})

    @classmethod
    def get_wantticket_by_id(cls, _id):
        return cls(**Database.find_one(WantTicketConstants.COLLECTION, {"_id": _id}))

    def update_ticket_purchased_flag(self):
        self.purchased_flag = 'PURCHASED'
        Database.update(WantTicketConstants.COLLECTION, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.update(WantTicketConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "game": self.game._id,
            "number": self.number,
            "purchased_flag": self.purchased_flag,
            "_id": self._id
        }
