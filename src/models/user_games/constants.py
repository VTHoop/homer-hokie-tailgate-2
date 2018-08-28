import os

__author__ = 'hooper-p'

COLLECTION = 'user_games'

URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API")
FROM = 'Homer Hokie <postmaster@homerhokietailgate.com>'
