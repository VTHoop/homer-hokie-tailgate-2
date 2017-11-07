__author__ = 'hooper-p'

from flask import Blueprint, session
from src.models.alerts.alert import Alert

alerts_blueprint = Blueprint('alerts', __name__)


@alerts_blueprint.route('/useralerts')
def get_alerts_by_user():
    user = session['user']
    useralerts = Alert.get_alert_by_user(user)
    for alert in useralerts:
        print(alert)
        #print the alerts and setting on page

@alerts_blueprint.route('/updatealerts')
def update_alerts_by_user():
    pass
    # for all user alerts on page
    # create an Alert object through each loop
    # pass object and Alert.update_alert_by_id(self, yesno)
