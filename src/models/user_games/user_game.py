import datetime
import os
import uuid

import requests
from flask import render_template, Flask
import jinja2

from src.common.database import Database
from src.models.alerts.alert import Alert
from src.models.games.game import Game
from src.models.users.user import User

import src.models.user_games.constants as UserGameConstants
from src.models.years.year import Year

__author__ = 'hooper-p'


class UserGame(object):
    def __init__(self, user, game, game_date, attendance, home_score, away_score, score_updated_on=None,
                 home_points=0, away_points=0, total_points=0, points_updated_on=None, admin_enter=None, _id=None):
        self.user = User.get_user_by_id(user['_id'])
        self.game = Game.get_game_by_id(game)
        self.game_date = Game.get_game_by_id(game).date
        self.attendance = attendance
        self.home_score = home_score
        self.away_score = away_score
        self.score_updated_on = score_updated_on
        self.home_points = home_points
        self.away_points = away_points
        self.total_points = total_points
        self.points_updated_on = points_updated_on
        self.admin_enter = admin_enter
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says for game {} that their status is {}".format(self.user.f_name, self.game.game_num,
                                                                    self.attendance)

    @classmethod
    def get_all_usergames(cls):
        return [cls(**elem) for elem in Database.find(UserGameConstants.COLLECTION, {})]

    @classmethod
    def get_usergame_by_id(cls, _id):
        return cls(**Database.find_one(UserGameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_all_attendance_by_user(cls, user):
        return [cls(**elem) for elem in
                Database.find(UserGameConstants.COLLECTION,
                              {"user._id": user})]

    @classmethod
    def get_attendance_by_user(cls, user, beg_date, end_date):
        return [cls(**elem) for elem in
                Database.find_and_sort(UserGameConstants.COLLECTION,
                                       {"user._id": user,
                                        "game_date": {'$lte': end_date, '$gte': beg_date}},
                                       [("game_date", 1)])]

    @classmethod
    def get_attendance_by_game(cls, game):
        return [cls(**elem) for elem in
                Database.find_and_sort(UserGameConstants.COLLECTION, {"game": game},
                                       [("user.l_name", 1), ("user.f_name", 1)])]

    @classmethod
    def get_attendance_by_game_and_status(cls, game, attendance):
        return [cls(**elem) for elem in
                Database.find(UserGameConstants.COLLECTION,
                              {"game": game, "attendance": attendance, "user.admin_created": "No"})]

    @classmethod
    def get_usergames_by_date(cls, beg_date, end_date):
        return [cls(**elem) for elem in Database.find_and_sort(UserGameConstants.COLLECTION,
                                                               {"game_date": {'$lte': end_date, '$gte': beg_date}},
                                                               [("game_date", 1)])]

    @staticmethod
    def get_all_prior_games_in_current_year(game_num):
        """
        initially get all user_games in the current year.  Only append them to a new list if they have a game_num
        that is less than the one being queried
        :param game_num: game number from Game object that states up to which game points will be calced
        :return: list of games up to game_num
        """
        user_games_prior = []
        current_year_user_games = UserGame.get_usergames_by_date(Year.get_current_year().start_date,
                                                                 Year.get_current_year().end_date)
        for ug in current_year_user_games:
            if ug.game.game_num <= game_num:
                user_games_prior.append(ug)

        return user_games_prior

    @staticmethod
    def update_user_points():
        user_games = UserGame.get_all_usergames()

        for ug in user_games:
            # if score has been entered
            if ug.score_updated_on is not None:
                if ug.home_score != '0' and ug.away_score != '0':
                    # if game has already happened and user somehow hasnt changed score(should be locked down after game
                    # after game has happened
                    if (ug.game.date < datetime.datetime.now()) and (
                            ug.points_updated_on is None or ug.score_updated_on > ug.points_updated_on):
                        UserGame.calc_points(ug)

    @staticmethod
    def calc_points(ug):
        max_points = 10
        ug.home_points = max(0, max_points - abs((int(ug.game.home_score) - int(ug.home_score))))
        ug.away_points = max(0, max_points - abs((int(ug.game.away_score) - int(ug.away_score))))
        ug.total_points = int(ug.home_points) + int(ug.away_points)

        if ug.admin_enter != "Yes":
            ug.total_points += 1
        ug.points_updated_on = datetime.datetime.now()
        ug.save_to_mongo()

    @staticmethod
    def get_reminder_user_list():
        alert_user_list = Alert.get_alerts_by_alert_type('score', 'On')
        email_alert_users = []
        for alert in alert_user_list:
            email_alert_users.append(alert.user.email)
        return ",".join(email_alert_users)

    @staticmethod
    def send_reminder():
        reminder_days_before_game = 4

        if (Game.get_next_game().date.date() - datetime.datetime.now().date()).days == reminder_days_before_game:
            if os.environ.get("environment") in ['QA', 'DEV']:
                email_to = 'pat.hooper83@gmail.com'
            else:
                email_to = UserGame.get_reminder_user_list()

            next_game = Game.get_next_game()

            template = jinja2.Template(UserGameConstants.templateHtml)
            html = template.render(next_game=next_game, deadline=next_game.date - datetime.timedelta(days=3),
                                   opponent=next_game.get_opponent())

            response = requests.post(UserGameConstants.URL,
                                     auth=('api', UserGameConstants.API_KEY),
                                     data={
                                         "from": UserGameConstants.FROM,
                                         "to": UserGameConstants.FROM,
                                         "bcc": email_to,
                                         "subject": "Friendly Reminder to Submit Scores for {} Game"
                                                    .format(next_game.get_opponent()),
                                         "html": html
                                     })
            response.raise_for_status()

    def save_to_mongo(self):
        Database.update(UserGameConstants.COLLECTION, {"_id": self._id}, self.json())

    def remove_user_games(self):
        Database.delete(UserGameConstants.COLLECTION, {"_id": self._id})

    @staticmethod
    def remove_user_games_by_user(email):
        Database.delete(UserGameConstants.COLLECTION, {"user.email": email})

    def json(self):
        return {
            "user": self.user.json(),
            "game": self.game._id,
            "game_date": self.game_date,
            "attendance": self.attendance,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "score_updated_on": self.score_updated_on,
            "home_points": self.home_points,
            "away_points": self.away_points,
            "total_points": self.total_points,
            "points_updated_on": self.points_updated_on,
            "admin_enter": self.admin_enter,
            "_id": self._id
        }
