from flask import session

from src.common.database import Database
from src.models.users.user import User
import src.models.game_conversations.constants as ConvoConstants

__author__ = 'hooper-p'


class GameConversation(object):
    def __init__(self, game, date, time, conversation):
        self.user = session['user']
        self.f_name = User.get_user_by_id(self.user).f_name
        self.l_name = User.get_user_by_id(self.user).l_name
        self.game = game
        self.date = date
        self.time = time
        self.conversation = conversation

    def __repr__(self):
        return '{} user had something to say about {} game on {}'.format(self.user, self.game, self.date)

    def insert_conversation(self):
        Database.insert(ConvoConstants, self.json())

    def json(self):
        return {
            "user": self.user,
            "game": self.game,
            "date": self.date,
            "time": self.time,
            "conversation": self.conversation
        }