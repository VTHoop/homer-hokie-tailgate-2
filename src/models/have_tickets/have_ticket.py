import uuid

from src.common.database import Database
from src.models.games.game import Game
from src.models.users.user import User
import src.models.have_tickets.constants as HaveTicketsConstants

__author__ = 'hooper-p'


class HaveTicket(object):
    def __init__(self, user, number, section, seats, game, sold_flag=None, price=None, _id=None):
        self.user = User.get_user_by_id(user)
        self.number = number
        self.section = section
        self.seats = seats
        self.game = Game.get_game_by_num(game)
        self.sold_flag = sold_flag
        self.price = None if price is None else float(price)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} has {} tickets to sell in section {} for {} dollars".format(self.user, self.number, self.section,
                                                                               self.price)

    @classmethod
    def get_all_havetickets(cls):
        return [cls(**elem) for elem in Database.find(HaveTicketsConstants.COLLECTION, {})]

    @classmethod
    def get_havetickets_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(HaveTicketsConstants.COLLECTION, {"game": game})]

    @classmethod
    def get_havetickets_by_id(cls, _id):
        return cls(**Database.find_one(HaveTicketsConstants.COLLECTION, {"_id": _id}))

    def delete_haveticket(self):
        Database.delete(HaveTicketsConstants.COLLECTION, {"_id": self._id})

    def update_ticket_sold_flag(self):
        self.sold_flag = 'SOLD'
        Database.update(HaveTicketsConstants.COLLECTION, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.update(HaveTicketsConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "user": self.user._id,
            "number": self.number,
            "section": self.section,
            "seats": self.seats,
            "game": self.game._id,
            "sold_flag": self.sold_flag,
            "price": self.price,
            "_id": self._id
        }