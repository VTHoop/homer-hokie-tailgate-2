__author__ = 'hooper-p'

from src.common.database import Database
from src.models.user_games.user_game import UserGame

Database.initialize()
UserGame.update_user_points()
