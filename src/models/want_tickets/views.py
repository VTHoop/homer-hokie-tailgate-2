from src.models.want_tickets.want_ticket import WantTicket

__author__ = 'hooper-p'

from flask import Blueprint, redirect, url_for, session, request

wanttickets_blueprint = Blueprint('want_tickets',  __name__)


@wanttickets_blueprint.route('/add/<int:game_num>', methods=['POST'])
def add(game_num):
    want_ticket = WantTicket(session['user'], game_num, request.form['want_total_num'])
    want_ticket.save_to_mongo()
    return redirect(url_for('games.detail', game_num=game_num, active='tickets'))
