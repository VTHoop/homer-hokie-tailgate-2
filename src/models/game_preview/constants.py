import os

__author__ = 'hooper-p'

COLLECTION = 'game_preview'

URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API")
FROM = 'Mailgun Sandbox <postmaster@sandbox67849019a20419c88582d1ba37e8c4a.mailgun.org>'

