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
        if Database.find_one(PreviewConstants.COLLECTION,
                             {"game": game_id, "author": User.get_user_by_email('jrhooper@att.net')._id}):
            preview = Preview.get_pops_preview_by_game(game_id)
            preview.preview = content
            preview.author = User.get_user_by_email('jrhooper@att.net')
            preview.updated_on = datetime.datetime.now()
            preview.save_to_mongo()
        else:
            preview = Preview(game_id, User.get_user_by_email('jrhooper@att.net')._id, content, datetime.datetime.now())
            preview.save_to_mongo()
        if 'saveandemail' in request.form:
            Preview.send(preview)
        return render_template("games/edit_preview.jinja2", preview=preview)
    else:
        if Database.find_one(PreviewConstants.COLLECTION,
                             {"game": game_id, "author": User.get_user_by_email('jrhooper@att.net')._id}):
            preview = Preview.get_pops_preview_by_game(game_id)
            return render_template("games/edit_preview.jinja2", preview=preview)
        else:
            return render_template("games/create_preview.jinja2")
