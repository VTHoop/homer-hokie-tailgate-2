from src.models.user_games.user_game import UserGame
from src.common.database import Database

__author__ = 'hooper-p'

Database.initialize()
UserGame.send_reminder()
