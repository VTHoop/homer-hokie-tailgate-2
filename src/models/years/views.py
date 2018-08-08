from datetime import datetime

from flask import Blueprint, request, render_template

from src.models.years.year import Year

import src.models.users.decorators as user_decorators

__author__ = 'hooper-p'

years_blueprint = Blueprint('year', __name__)


@user_decorators.requires_admin
@years_blueprint.route('/create', methods=['GET', 'POST'])
def create_year():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], "%m/%d/%Y")
        end_date = datetime.strptime(request.form['end_date'], "%m/%d/%Y")
        year_label = request.form['year_label']
        Year(start_date,end_date,year_label).save_to_mongo()
    return render_template('years/create_year.jinja2')
