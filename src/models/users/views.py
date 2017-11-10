from passlib.hash import sha512_crypt

from src.common.utils import Utils
from src.models.games.game import Game
from src.models.users.user import User
from src.models.alerts.alert import Alert
from src.models.user_games.user_game import UserGame
from src.models.user_scores.user_score import UserScore
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
                return redirect(url_for(".user_dashboard"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")


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
    if request.method == 'GET':
        user = User(None, None, None, None)
        alerts = {}
        for a in AlertConstants.ALERTS:
            alerts[a] = 'On'
        attendance = {}
        games = Game.get_all_games()
        for i in games:
            if i.home_team.location == 'Blacksburg, VA':
                attendance[i.game_num]='Yes'
            else:
                attendance[i.game_num]='No'
        return render_template("users/new_user.jinja2", user=None, alerts=alerts, attendance=attendance, a_constants=AlertConstants.ALERTS)
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pword = request.form['pword']
        # admin = 'No'
        # user_id = request.form['user_id']
        alerts = {}
        for a in AlertConstants.ALERTS:
            alerts[a] = request.form['alerts_'+a]
        user = User(fname, lname, email, pword)
        games = Game.get_all_games()
        attendance = {}
        for i in games:
            attendance[i.game_num] = request.form['attendance'+i.game_num]
        if 'notification_settings' in request.form:
            return render_template("users/notification_settings.jinja2", user=user, alerts=alerts, attendance=attendance, games=games, a_constants=AlertConstants.ALERTS)
        elif 'basic_details' in request.form:
            return render_template("users/new_user.jinja2", user=user, alerts=alerts, attendance=attendance, games=games, a_constants=AlertConstants.ALERTS)
        elif 'game_attendance' in request.form:
            return render_template("users/game_attendance.jinja2", user=user, alerts=alerts, attendance=attendance, games=games, a_constants=AlertConstants.ALERTS)
        elif 'register_user' in request.form:
            pword = Utils.hash_password(request.form['pword'])
            user = User(fname, lname, email, pword)
            user.insert_new_user()

            # print(user)
            for alert in alerts:
                new_alert = Alert(user._id, alert, alerts[alert])
                new_alert.insert_alert()
                # print(new_alert)
            for na in attendance:
                new_attendance = UserGame(user._id, na, attendance[na], 0, 0)
                new_attendance.save_to_mongo()
                # print(new_attendance)
            # for game in games:
            #     new_user_score = UserScore(user._id, game.game_num, 0, 0)
            #     new_user_score.create_user_score()

            session['user'] = user._id
            user_scores = UserScore.get_scores_by_user(session['user'])

            return redirect(url_for('.user_dashboard'))

@users_blueprint.route('/notificationsettings', methods=['GET', 'POST'])
def notification_settings():
    return render_template("users/notification_settings.jinja2")


@users_blueprint.route('/gameattendance', methods=['GET', 'POST'])
def game_attendance():
    games = Game.get_all_games()
    return render_template("users/game_attendance.jinja2", games=games)


@users_blueprint.route('/creategames', methods=['GET', 'POST'])
def create_user_games(user):
    games = Game.get_all_games()
    for g in games:
        attendence = request.form['attending{% g.game_num %}']
        print(attendence)
        # user_game = UserGame(user, g, attendence)
        # user_game.save_to_mongo()
        # return render_template('/')


@users_blueprint.route('/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    attendance = UserGame.get_attendance_by_user(session['user'])
    user_scores = UserScore.get_scores_by_user(session['user'])
    return render_template("users/dashboard.jinja2", attendance=attendance, user_scores=user_scores)