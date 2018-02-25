from flask import Blueprint, request, render_template

from src.models.locations.location import Location
from src.models.teams.team import Team

__author__ = 'hooper-p'


teams_blueprint = Blueprint('team', __name__)


@teams_blueprint.route('/admin/create', methods=['GET', 'POST'])
def create_team():
    locations = Location.get_all_locations()
    if request.method == 'POST':
        school_name = request.form['school_name']
        hokie_sports_name = request.form['hokie_sports_name']
        abbrev = request.form['abbrev']
        mascot = request.form['mascot']
        logo = request.form['logo']
        location = Location.get_location_by_id(request.form['location']).json()
        stadium = request.form['stadium']
        Team(school_name=school_name,
             hokie_sports_name=hokie_sports_name,
             short_name=abbrev,
             mascot=mascot,
             logo=logo,
             location=location,
             stadium=stadium).save_to_mongo()
    return render_template('teams/create_team.jinja2', locations=locations)