__author__ = 'hooper-p'

from src.common.database import Database
from src.models.team_years.team_year import TeamYear

Database.initialize()
TeamYear.update_teams()
