__author__ = 'hooper-p'

from flask import Blueprint, session
from src.models.alerts.alert import Alert

alerts_blueprint = Blueprint('alerts', __name__)


