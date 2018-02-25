from flask import Blueprint, request, render_template

from src.models.team_years.team_year import TeamYear
from src.models.teams.team import Team
from src.models.years.year import Year

__author__ = 'hooper-p'

team_years_blueprint = Blueprint('teamyear', __name__)


@team_years_blueprint.route('/admin/create', methods=['GET', 'POST'])
def create_team_year():
    teams = Team.get_teams()
    years = Year.get_all_years()

    if request.method == 'POST':
        TeamYear(team=Team.get_by_school_name(request.form['team']).json(),
                 year=Year.get_year_by_id(request.form['year']).json(),
                 conference=request.form['conf'],
                 wins=request.form['wins'],
                 losses=request.form['losses'],
                 conf_wins=request.form['conf_wins'],
                 conf_losses=request.form['conf_losses'],
                 ap_rank=request.form['rank']).save_to_mongo()
    return render_template('team_years/create_team_year.jinja2', teams=teams, years=years)
