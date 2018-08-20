from src.models.alerts.alert import Alert
import src.models.alerts.constants as AlertConstants

__author__ = 'hooper-p'

from flask import Blueprint, request, render_template, session, redirect, url_for

alerts_blueprint = Blueprint('alerts', __name__)


@alerts_blueprint.route('/', methods=['GET', 'POST'])
def manage_alerts():
    if request.method == 'POST':
        alerts = Alert.get_alerts_by_user(session['user'])
        for a in alerts:
            a.yes_no = request.form['alerts_' + str(a._id)]
            a.save_to_mongo()
        return redirect(url_for('dashboard.user_dashboard'))
    else:
        alerts = Alert.get_alerts_by_user(session['user'])
        return render_template("alerts/alerts.jinja2", alerts=alerts, a_constants=AlertConstants.ALERTS)