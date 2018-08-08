from datetime import datetime

from src.models.game_food.food import Food
from src.models.game_preview.preview import Preview
from src.models.games.game import Game
from src.models.have_tickets.have_ticket import HaveTicket
from src.models.locations.location import Location
from src.models.teams.team import Team
from src.models.user_games.user_game import UserGame

import src.models.users.decorators as user_decorators

from flask import Blueprint, render_template, request, session

from src.models.users.user import User
from src.models.want_tickets.want_ticket import WantTicket
from src.models.years.year import Year

__author__ = 'hooper-p'

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/detail/<string:game_id>', methods=['GET', 'POST'])
def detail(game_id):
    user = session['user']

    this_game = Game.get_game_by_id(game_id)
    # format the date for the detail screen
    this_game.date = this_game.date.strftime("%B %d")

    # getting attendance for each type to pass along to template
    yes_attendance = UserGame.get_attendance_by_game_and_status(game_id, 'Yes')
    maybe_attendance = UserGame.get_attendance_by_game_and_status(game_id, 'Maybe')
    no_attendance = UserGame.get_attendance_by_game_and_status(game_id, 'No')

    # get preview for game
    preview = Preview.get_preview_by_game(game_id)

    # get food for game
    food_for_game = Food.get_food_by_game(game_id)

    # get have_tickets for game
    have_tickets_for_game = HaveTicket.get_havetickets_by_game(game_id)

    # get want_tickets for game
    want_tickets_for_game = WantTicket.get_wanttickets_by_game(game_id)

    return render_template("games/game_detail.jinja2", game=this_game, preview=preview, yes_attendance=yes_attendance,
                           maybe_attendance=maybe_attendance, no_attendance=no_attendance, food_for_game=food_for_game,
                           have_tickets_for_game=have_tickets_for_game, want_tickets_for_game=want_tickets_for_game,
                           user=user)


@games_blueprint.route('/admin/schedule', methods=['GET'])
@user_decorators.requires_admin
def admin_schedule():
    return render_template("games/admin_schedule.jinja2", games=Game.get_games_by_year(Year.get_current_year()._id))


@games_blueprint.route('/admin/edit/<string:game_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin
def edit_game(game_id):
    if request.method == 'POST':
        game = Game.get_game_by_id(game_id)
        game.location = Location.get_location_by_id(request.form['location'])
        game.stadium = request.form['stadium']
        game.hht_theme = request.form['hht_theme']
        game.save_to_mongo()

    game = Game.get_game_by_id(game_id)
    teams = Team.get_teams()
    locations = Location.get_all_locations()
    stadiums = Game.get_all_stadiums()
    stadiums.sort()

    return render_template("games/edit_game.jinja2", teams=teams, game=game, locations=locations, stadiums=stadiums)


@games_blueprint.route('/admin/create/', methods=['GET', 'POST'])
@user_decorators.requires_admin
def create_game():
    if request.method == 'POST':
        new_game = Game(game_num=request.form['game_num'],
                        away_team=request.form['away_team'],
                        home_team=request.form['home_team'],
                        year=request.form['year'],
                        location=Location.get_location_by_id(request.form['location']).json(),
                        stadium=request.form['stadium'],
                        date=datetime.strptime(request.form['date'], "%m/%d/%Y"))
        new_game.save_to_mongo()
        users = User.get_all_users()
        if new_game.location.city == 'Blacksburg':
            attendance = 'Yes'
        else:
            attendance = 'No'
        for u in users:
            UserGame(user=u.json(),
                     game=new_game._id,
                     attendance=attendance,
                     game_date=None,
                     home_score=0,
                     away_score=0
                     ).save_to_mongo()

    years = Year.get_all_years()
    teams = Team.get_teams()
    locations = Location.get_all_locations()
    stadiums = Game.get_all_stadiums()
    stadiums.sort()

    return render_template("games/create_game.jinja2", teams=teams, locations=locations, stadiums=stadiums, years=years)
