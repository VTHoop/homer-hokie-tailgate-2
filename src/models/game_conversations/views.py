import datetime

from flask import Blueprint, session, request, redirect, url_for

from src.models.game_conversations.game_conversation import GameConversation

__author__ = 'hooper-p'

convo_blueprint = Blueprint('convo', __name__)


@convo_blueprint.route('/add/<string:game_id>', methods=['POST'])
def add_convo(game_id):
    game_convo = GameConversation(
        user=session['user'],
        conversation=request.form['convo'],
        game=game_id,
        created_on=datetime.datetime.now())
    game_convo.save_to_mongo()
    return redirect(url_for('games.detail', game_id=game_id, active='convo'))


@convo_blueprint.route('/delete/<string:convo>', methods=['GET'])
def delete_convo(convo):
    game_id = GameConversation.get_convo_by_id(convo).game._id
    GameConversation.get_convo_by_id(convo).delete_conversation()
    return redirect(url_for('games.detail', game_id=game_id, active='convo'))
