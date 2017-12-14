from src.models.have_tickets.have_ticket import HaveTicket

__author__ = 'hooper-p'

from flask import Blueprint, redirect, url_for, session, request

havetickets_blueprint = Blueprint('have_tickets', __name__)


@havetickets_blueprint.route('/add/<string:game_id>', methods=['POST'])
def add(game_id):
    have_ticket = HaveTicket(session['user'], request.form['total_num'],request.form['section'],request.form['seats'],
                             game_id,None,request.form['price'])
    have_ticket.save_to_mongo()
    return redirect(url_for('games.detail', game_id=game_id, active='tickets'))


@havetickets_blueprint.route('/delete/<string:ticket>')
def delete(ticket):
    game_id = HaveTicket.get_havetickets_by_id(ticket).game._id
    HaveTicket.get_havetickets_by_id(ticket).delete_haveticket()
    return redirect(url_for('games.detail', game_id=game_id, active='tickets'))


@havetickets_blueprint.route('/sold/<string:ticket>')
def sold(ticket):
    game_id = HaveTicket.get_havetickets_by_id(ticket).game._id
    HaveTicket.get_havetickets_by_id(ticket).update_ticket_sold_flag()
    return redirect(url_for('games.detail', game_num=game_id, active='tickets'))
