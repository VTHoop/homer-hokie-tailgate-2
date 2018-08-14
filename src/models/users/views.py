import datetime
from os import abort

from src.common.security import ts
from src.common.utils import Utils
from src.models.games.game import Game
from src.models.users.user import User
from src.models.alerts.alert import Alert
from src.models.user_games.user_game import UserGame
import src.models.alerts.constants as AlertConstants
import src.models.users.errors as UserErrors
from src.models.years.year import Year

__author__ = 'hooper-p'

from flask import Blueprint, request, session, render_template, redirect, url_for

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/admin/<string:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if request.method == 'POST':
        user = User.get_user_by_id(user_id)
        user.f_name = request.form['first_name']
        user.l_name = request.form['last_name']
        user.email = request.form['email']
        user.prognosticator = request.form['prognosticator']
        user.save_to_mongo()
        users = User.get_all_users()
        return render_template('users/admin_dashboard.jinja2', users=users)
    else:
        user = User.get_user_by_id(user_id)
        return render_template('users/admin_edit_user.jinja2', user=user)


@users_blueprint.route('/admin/delete/<string:user_id>', methods=['GET'])
def admin_delete_user(user_id):
    user = User.get_user_by_id(user_id)
    alerts = Alert.get_alerts_by_user(user_id)
    attendance = UserGame.get_all_attendance_by_user(user_id)
    user.remove_user()
    for alert in alerts:
        alert.remove_alerts()

    for atten in attendance:
        atten.remove_user_games()

    users = User.get_all_users()
    return render_template('users/admin_dashboard.jinja2', users=users)


@users_blueprint.route('/admin', methods=['GET', 'POST'])
def user_administration():
    if request.method == 'POST':
        user = User(f_name=request.form['fname'],
                    l_name=request.form['lname'],
                    email=request.form['email'],
                    prognosticator=request.form['prognosticator'],
                    admin_created='Yes'
                    )
        alerts, attendance = User.user_default_values()
        user.insert_new_user()

        for alert in alerts:
            new_alert = Alert(user._id, alert, alerts[alert])
            new_alert.save_to_mongo()
        for na in attendance:
            new_attendance = UserGame(user=user.json(),
                                      game=Game.get_game_by_num(na, Year.get_current_year()._id)._id,
                                      attendance=attendance[na], home_score=0,
                                      away_score=0, game_date=0)
            new_attendance.save_to_mongo()
    users = User.get_all_users()
    return render_template('users/admin_dashboard.jinja2', users=users)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pword']

        try:
            if User.is_login_valid(email, password):
                session['user'] = User.get_user_by_email(email)._id
                session['useradmin'] = User.get_user_by_email(email).admin
                print(session['useradmin'])
                return redirect(url_for("dashboard.user_dashboard"))

        except UserErrors.UserError as e:
            return render_template("users/login.jinja2", error=e.message)

    return render_template("users/login.jinja2")


@users_blueprint.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        try:
            # if user exists
            if User.check_user_exists(request.form['email']):
                user = User.get_user_by_email(request.form['email'])
                subject = 'Password Reset Request from Homer Hokie Tailgate'
                token = ts.dumps(user.email, salt='recover-key')

                recover_url = url_for(
                    'users.reset_with_token',
                    token=token,
                    _external=True)

                html = render_template(
                    'email/recover.html',
                    recover_url=recover_url)

                User.email_password(user, subject, html)

                return redirect(url_for('home'))
            else:
                raise UserErrors.ResetPasswordWrongUser(
                    "Email is not recognized.  Try again or sign up for HHT with that email!")
        except UserErrors.UserError as e:
            return render_template("users/reset_password.jinja2", error=e.message)
    return render_template("users/reset_password.jinja2")


@users_blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    if request.method == 'POST':
        user = User.get_user_by_email(email)
        user.password = Utils.hash_password(request.form['pword'])
        user.save_to_mongo()

        return redirect(url_for('users.login_user'))

    return render_template('users/reset_with_token.jinja2', token=token)


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
                games = Game.get_games_by_year(Year.get_current_year()._id)
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
                        print(Game.get_game_by_num(na, Year.get_current_year()._id)._id)
                        new_attendance = UserGame(user=user.json(),
                                                  game=Game.get_game_by_num(na, Year.get_current_year()._id)._id,
                                                  attendance=attendance[na], home_score=0,
                                                  away_score=0, game_date=0)
                        new_attendance.save_to_mongo()

                    session['user'] = user._id
                    return redirect(url_for('dashboard.user_dashboard'))
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
