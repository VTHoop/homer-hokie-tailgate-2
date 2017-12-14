import datetime

from src.common.utils import Utils
from src.models.games.game import Game
from src.models.users.user import User
from src.models.alerts.alert import Alert
from src.models.user_games.user_game import UserGame
import src.models.alerts.constants as AlertConstants
import src.models.users.errors as UserErrors

__author__ = 'hooper-p'

from flask import Blueprint, request, session, render_template, redirect, url_for

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pword']

        try:
            if User.is_login_valid(email, password):
                session['user'] = User.get_user_by_email(email)._id
                return redirect(url_for("dashboard.user_dashboard"))
        except UserErrors.UserError as e:
            return render_template("users/login.jinja2", error=e.message)

    return render_template("users/login.jinja2")


@users_blueprint.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('home'))


@users_blueprint.route('/updateprofile')
def update_profile():
    if request.method == 'POST':

        if request.form['pword'] == request.form['confirmpword']:
            user = User.get_user_by_id(session['user'])
            user.f_name = request.form['f_name']
            user.l_name = request.form['l_name']
            user.password = request.form['pword']  # need to hash password
        else:
            pass
            # send user error message that passwords do not match


@users_blueprint.route('/new', methods=['GET', 'POST'])
def new_user():
    """
    This method handles both the original GET and all subsequent POST requests

    The registration of a new user is handled through three different pages and the information on those pages will
    be saved and rendered on the page if the that is the appropriate page otherwise it will be saved in a hidden
    form element.  Password will not be re-rendered, however.

    On GET, function will go build default values for a new user and keep those hidden until they get to those pages.

    All form elements are re-saved on each submit regardless of page, however the buttons will determine the appropriate
    page to render.

    :return:
    """
    if request.method == 'GET':
        alerts, attendance = User.user_default_values()
        return render_template("users/new_user.jinja2", user=None, alerts=alerts, attendance=attendance,
                               a_constants=AlertConstants.ALERTS)
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pword = request.form['pword']
        confirmpword = request.form['confirmpword']
        phone = request.form['phone']
        location = request.form['location']
        try:
            if User.new_user_valid(email, pword, confirmpword):
                # admin = 'No'
                user = User(fname, lname, email, pword, phone=phone, location=location)
                # set the values of the alert dict based on user entries
                alerts = {}
                for a in AlertConstants.ALERTS:
                    alerts[a] = request.form['alerts_' + a]
                games = Game.get_all_games()
                # set the values of the attendance dict based on user entries
                attendance = {}
                for i in games:
                    attendance[i.game_num] = request.form['attendance' + str(i.game_num)]
                # render correct page based on button clicked
                if 'notification_settings' in request.form:
                    return render_template("users/notification_settings.jinja2", user=user, alerts=alerts,
                                           attendance=attendance, games=games, a_constants=AlertConstants.ALERTS)
                elif 'basic_details' in request.form:
                    return render_template("users/new_user.jinja2", user=user, alerts=alerts, attendance=attendance,
                                           games=games, a_constants=AlertConstants.ALERTS)
                elif 'game_attendance' in request.form:
                    return render_template("users/game_attendance.jinja2", user=user, alerts=alerts,
                                           attendance=attendance,
                                           games=games, a_constants=AlertConstants.ALERTS)
                elif 'register_user' in request.form:
                    pword = Utils.hash_password(request.form['pword'])
                    user = User(fname, lname, email, pword, phone=phone, location=location,
                                created_on=datetime.datetime.utcnow())
                    user.insert_new_user()

                    for alert in alerts:
                        new_alert = Alert(user._id, alert, alerts[alert])
                        new_alert.save_to_mongo()
                    for na in attendance:
                        new_attendance = UserGame(user._id, na, attendance[na], 0, 0)
                        new_attendance.save_to_mongo()

                    session['user'] = user._id
                    return redirect(url_for('.user_dashboard'))
        except UserErrors.UserError as e:
            alerts, attendance = User.user_default_values()
            return render_template("users/new_user.jinja2", user=None, alerts=alerts, attendance=attendance,
                                   a_constants=AlertConstants.ALERTS, error=e.message)


@users_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.get_user_by_id(session['user'])
    alerts = Alert.get_alerts_by_user(session['user'])
    active = 'profile'
    if request.method == 'POST':
        if 'profile' in request.form:
            user.phone = request.form['phone']
            user.location = request.form['location']
            user.updated_on = datetime.datetime.utcnow()
            user.save_to_mongo()
            active = 'profile'
        elif 'notifications' in request.form:
            for a in alerts:
                a.yes_no = request.form['alerts' + str(a._id)]
                a.save_to_mongo()
                active = 'notifications'

    return render_template("users/user_profile.jinja2", user=user, active_page=active,
                           alerts=Alert.get_alerts_by_user(session['user']), a_constants=AlertConstants.ALERTS)

