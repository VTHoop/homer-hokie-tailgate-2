import datetime
from flask import Blueprint, request, render_template, session

from src.common.database import Database
from src.models.game_preview.preview import Preview

import src.models.game_preview.constants as PreviewConstants
from src.models.users.user import User

__author__ = 'hooper-p'

preview_blueprint = Blueprint('preview', __name__)


@preview_blueprint.route('/admin/<string:game_id>', methods=['GET', 'POST'])
def edit_preview(game_id):
    if request.method == 'POST':
        content = request.form['content']
        if Database.find_one(PreviewConstants.COLLECTION, {"game": game_id, "author": session['user']}):
            preview = Preview.get_preview_by_game_and_user(game_id, session['user'])
            preview.preview = content
            preview.author = User.get_user_by_id(session['user'])
            preview.updated_on = datetime.datetime.now()
            preview.save_to_mongo()
        else:
            preview = Preview(game_id,session['user'],content,datetime.datetime.now())
            preview.save_to_mongo()
        return render_template("games/edit_preview.jinja2", preview=preview)
    else:
        if Database.find_one(PreviewConstants.COLLECTION, {"game": game_id, "author": session['user']}):
            preview = Preview.get_preview_by_game_and_user(game_id, session['user'])
            return render_template("games/edit_preview.jinja2", preview=preview)
        else:
            return render_template("games/create_preview.jinja2")


