__author__ = 'hooper-p'

from src.common.database import Database
from src.models.teams.team import Team

Database.initialize()

Team.update_teams()