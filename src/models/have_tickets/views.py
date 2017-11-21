from src.models.have_tickets.have_ticket import HaveTicket

__author__ = 'hooper-p'

from flask import Blueprint, redirect, url_for

havetickets_blueprint = Blueprint('have_tickets', __name__)


@havetickets_blueprint.route('/delete/<string:ticket>')
def delete(ticket):
    game_num = HaveTicket.get_havetickets_by_id(ticket).game.game_num
    HaveTicket.get_havetickets_by_id(ticket).delete_haveticket()
    return redirect(url_for('games.detail', game_num=game_num))

@havetickets_blueprint.route('/sold/<string:ticket>')
def sold(ticket):
    game_num = HaveTicket.get_havetickets_by_id(ticket).game.game_num
    HaveTicket.get_havetickets_by_id(ticket).update_ticket_sold_flag()
    return redirect(url_for('games.detail', game_num=game_num))