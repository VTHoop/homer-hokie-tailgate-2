__author__ = 'hooper-p'

from flask import Flask, render_template
from src.common.database import Database

from src.models.users.views import users_blueprint
from src.models.alerts.views import alerts_blueprint
from src.models.have_tickets.views import havetickets_blueprint
from src.models.user_scores.views import score_blueprint
from src.models.game_food.views import gamefood_blueprint
from src.models.games.views import games_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(alerts_blueprint, url_prefix='/alerts')
app.register_blueprint(havetickets_blueprint, url_prefix='/havetickets')
app.register_blueprint(score_blueprint, url_prefix='/scores')
app.register_blueprint(gamefood_blueprint, url_prefix='/gamefood')
app.register_blueprint(games_blueprint, url_prefix='/games')


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


