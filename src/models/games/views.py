from datetime import datetime

from src.models.game_food.food import Food
from src.models.games.game import Game
from src.models.have_tickets.have_ticket import HaveTicket
from src.models.user_games.user_game import UserGame

from flask import Blueprint, render_template, request, session

from src.models.want_tickets.want_ticket import WantTicket

__author__ = 'hooper-p'

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/detail/<int:game_num>', methods=['GET', 'POST'])
def detail(game_num):
    redirect_page = ""
    user = session['user']

    if request.method == 'POST':
        if 'AddFood' in request.form:
            food = request.form['game_food']
            game_food = Food(user, food, game_num)
            game_food.save_to_mongo()
            redirect_page = 'food'
        if 'AddWantTickets' in request.form:
            want_number = request.form['want_total_num']
            want_tickets = WantTicket(user, game_num, want_number)
            want_tickets.save_to_mongo()
        if 'AddHaveTickets' in request.form:
            number = request.form['total_num']
            section = request.form['section']
            seats = request.form['seats']
            price = request.form['price']
            have_tickets = HaveTicket(user, number, section, seats, game_num, None, price)
            have_tickets.save_to_mongo()


    this_game = Game.get_game_by_num(game_num)
    # format the date for the detail screen
    this_game.date = datetime.strftime(datetime.strptime(this_game.date, "%m/%d/%Y"), "%B %d")

    # getting attendance for each type to pass along to template
    yes_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'Yes')
    maybe_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'Maybe')
    no_attendance = UserGame.get_attendance_by_game_and_status(game_num, 'No')

    # get food for game
    food_for_game = Food.get_food_by_game(game_num)

    # get have_tickets for game
    have_tickets_for_game = HaveTicket.get_havetickets_by_game(game_num)

    # get want_tickets for game
    want_tickets_for_game = WantTicket.get_wanttickets_by_game(game_num)

    return render_template("games/game_detail.jinja2", game=this_game, yes_attendance=yes_attendance,
                           maybe_attendance=maybe_attendance, no_attendance=no_attendance, food_for_game=food_for_game,
                           have_tickets_for_game=have_tickets_for_game, want_tickets_for_game=want_tickets_for_game,
                           user=user)
