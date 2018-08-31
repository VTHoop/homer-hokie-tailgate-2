__author__ = 'hooper-p'

from src.common.database import Database
from src.models.games.game import Game

Database.initialize()
Game.load_game_details()