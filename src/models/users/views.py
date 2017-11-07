from src.models.games.game import Game
from src.models.users.user import User

__author__ = 'hooper-p'

from flask import Blueprint, request, session, render_template

users_blueprint = Blueprint('users', __name__)


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


@users_blueprint.route('/newuser', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        user = User(None, None, None, None)
        hht_preview = 'On'
        score = 'On'
        tickets = 'On'
        attendance = {}
        games = Game.get_all_games()
        for i in games:
            if i.home_team.location == 'Blacksburg, VA':
                attendance[i.game_num]='Yes'
            else:
                attendance[i.game_num]='No'
        return render_template("users/new_user.jinja2", user=None, hht_preview=hht_preview, score=score,
                               tickets=tickets, attendance=attendance)
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pword = request.form['pword']
        # admin = 'No'
        # user_id = request.form['user_id']
        hht_preview = request.form['hht_preview']
        score = request.form['score']
        tickets = request.form['tickets']
        user = User(fname, lname, email, pword)
        games = Game.get_all_games()
        attendance = {}
        for i in games:
            attendance[i.game_num] = request.form['attendance'+i.game_num]
        if 'notification_settings' in request.form:
            return render_template("users/notification_settings.jinja2", user=user, hht_preview=hht_preview,
                                   score=score, tickets=tickets, attendance=attendance, games=games)
        elif 'basic_details' in request.form:
            return render_template("users/new_user.jinja2", user=user, hht_preview=hht_preview, score=score,
                                   tickets=tickets, attendance=attendance, games=games)
        elif 'game_attendance' in request.form:
            return render_template("users/game_attendance.jinja2", user=user, hht_preview=hht_preview, score=score,
                                   tickets=tickets, attendance=attendance, games=games)



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
