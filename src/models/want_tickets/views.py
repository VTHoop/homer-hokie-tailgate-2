from src.models.want_tickets.want_ticket import WantTicket

__author__ = 'hooper-p'

from flask import Blueprint, redirect, url_for, session, request

wanttickets_blueprint = Blueprint('want_tickets', __name__)


@wanttickets_blueprint.route('/add/<string:game_id>', methods=['POST'])
def add(game_id):
    want_ticket = WantTicket(session['user'], game_id, request.form['want_total_num'])
    want_ticket.save_to_mongo()
    return redirect(url_for('games.detail', game_id=game_id, active='tickets'))


@wanttickets_blueprint.route('/delete/<string:ticket>')
def delete(ticket):
    WantTicket.get_wantticket_by_id(ticket).delete_wantticket()
    return redirect(url_for('games.detail', game_id=WantTicket.get_wantticket_by_id(ticket).game._id,
                            active='tickets'))

@wanttickets_blueprint.route('/purchased/<string:ticket>')
def purchased(ticket):
    WantTicket.get_wantticket_by_id(ticket).update_ticket_purchased_flag()
    return redirect(url_for('games.detail', game_id=WantTicket.get_wantticket_by_id(ticket).game._id,
                            active='tickets'))
