__author__ = 'hooper-p'


class ScoreError(Exception):
    def __init__(self, message):
        self.message = message


class ScoreNotNumber(ScoreError):
    pass
