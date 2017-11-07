from flask import Blueprint, request, session

from src.models.user_scores.user_score import UserScore
import src.models.user_scores.errors as ScoreErrors

__author__ = 'hooper-p'

score_blueprint = Blueprint('scores', __name__)


@score_blueprint.route('/updateonescore')
def update_one_score():
    """
    This function will be initiated when a user clicks the Save button next to an individual game that will update
    the score that is related to that particular game
    :return: if successful, return message of Score saved else error message
    """
    if request.method == 'POST':
        game_id = request.form['game_id']
        user = session["user"]
        home_score = request.form['home_score']
        away_score = request.form['away_score']

        try:
            home_score = int(home_score)
            away_score = int(away_score)
            score = UserScore.get_score_by_user_and_game(game_id, user)
            UserScore.update_user_score(score, home_score, away_score)
        except ScoreErrors.ScoreNotNumber('Scores are not entered as numbers.') as e:
            return e.message

@score_blueprint.route('/updateallscores')
def update_all_scores():
    """
    this function all resave all of the scores on the form for that user
    :return: if successful, reload page with successful save message else error
    """
    pass



