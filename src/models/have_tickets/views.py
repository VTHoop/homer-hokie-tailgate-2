from src.models.have_tickets.have_ticket import HaveTicket

__author__ = 'hooper-p'

from flask import Blueprint

havetickets_blueprint = Blueprint('have_tickets', __name__)

@havetickets_blueprint.route('/gamehavetickets')
def view_game_have_tickets(game):
    game_have_tickets = HaveTicket.get_havetickets_by_game(game)
    for i in game_have_tickets:
        return game_have_tickets[i]

@havetickets_blueprint.route('/ticketssold')
def update_tickets_sold(_id):
    """
    After user clicks on Sold button next to tickets that they own, update status of sold_flag
    :param _id: this is the _id of the tickets being sold
    :return: screen of Game Tickets with updated status
    """
    sold_ticket = HaveTicket.get_havetickets_by_id(_id)
    HaveTicket.update_ticket_sold_flag(sold_ticket)
