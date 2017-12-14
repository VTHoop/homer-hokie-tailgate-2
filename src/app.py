from src.models.game_food.food import Food
from src.models.games.game import Game
from src.models.have_tickets.have_ticket import HaveTicket
from src.models.team_years.team_year import TeamYear
from src.models.user_games.user_game import UserGame
from src.models.want_tickets.want_ticket import WantTicket

__author__ = 'hooper-p'

from flask import Flask, render_template
from src.common.database import Database

from src.models.users.views import users_blueprint
from src.models.alerts.views import alerts_blueprint
from src.models.have_tickets.views import havetickets_blueprint
from src.models.game_food.views import gamefood_blueprint
from src.models.games.views import games_blueprint
from src.models.want_tickets.views import wanttickets_blueprint
from src.models.user_games.views import user_games_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(alerts_blueprint, url_prefix='/alerts')
app.register_blueprint(havetickets_blueprint, url_prefix='/havetickets')
app.register_blueprint(wanttickets_blueprint, url_prefix='/wanttickets')
app.register_blueprint(gamefood_blueprint, url_prefix='/gamefood')
app.register_blueprint(games_blueprint, url_prefix='/games')
app.register_blueprint(user_games_blueprint, url_prefix='/dashboard')


@app.before_first_request
def init_db():
    Database.initialize()
    # Game.load_game_tv()
    TeamYear.update_teams()

    # dev cleanup work
    # game_foods = Food.get_all_food()
    # for gf in game_foods:
    #     gf.save_to_mongo()
    # for wt in WantTicket.get_all_wanttickets():
    #     wt.save_to_mongo()
    # for ht in HaveTicket.get_all_havetickets():
    #     ht.save_to_mongo()
    # user_games = UserGame.get_all_usergames()
    # for ug in user_games:
    #     ug.save_to_mongo()

@app.route('/')
def home():
    return render_template('home.html')


