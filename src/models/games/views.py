from datetime import datetime

from src.models.game_food.food import Food
from src.models.games.game import Game
from src.models.have_tickets.have_ticket import HaveTicket
from src.models.locations.location import Location
from src.models.teams.team import Team
from src.models.user_games.user_game import UserGame

from flask import Blueprint, render_template, request, session

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

    # get food for game
    food_for_game = Food.get_food_by_game(game_id)

    # get have_tickets for game
    have_tickets_for_game = HaveTicket.get_havetickets_by_game(game_id)

    # get want_tickets for game
    want_tickets_for_game = WantTicket.get_wanttickets_by_game(game_id)

    return render_template("games/game_detail.jinja2", game=this_game, yes_attendance=yes_attendance,
                           maybe_attendance=maybe_attendance, no_attendance=no_attendance, food_for_game=food_for_game,
                           have_tickets_for_game=have_tickets_for_game, want_tickets_for_game=want_tickets_for_game,
                           user=user)


@games_blueprint.route('/admin/schedule', methods=['GET'])
def admin_schedule():
    return render_template("games/admin_schedule.jinja2", games=Game.get_games_by_year(Year.get_current_year()._id))


@games_blueprint.route('/admin/edit/<string:game_id>', methods=['GET', 'POST'])
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
