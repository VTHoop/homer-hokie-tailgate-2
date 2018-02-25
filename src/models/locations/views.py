from flask import Blueprint, request, render_template

from src.models.locations.location import Location

__author__ = 'hooper-p'

locations_blueprint = Blueprint('location', __name__)


@locations_blueprint.route('/create', methods=['GET', 'POST'])
def create_location():
    if request.method == 'POST':
        Location(request.form['city'],request.form['state'],request.form['zip']).save_to_mongo()
    return render_template('locations/create_location.jinja2')