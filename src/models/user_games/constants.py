import os

__author__ = 'hooper-p'

COLLECTION = 'user_games'

URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API")
FROM = 'Homer Hokie <postmaster@homerhokietailgate.com>'
templateHtml = '<h1>Reminder to Submit Score for {{ opponent }} Game</h1>' \
               '<br><p>The {{ opponent }} is coming up on' \
               ' {{ next_game.date.strftime("%B %d") | replace(" 0", " ") }} and you will' \
               ' only be able to submit scores until Midnight on' \
               ' {{ deadline.strftime("%B %d")  | replace(" 0", " ") }}</p>' \
               '<br><p>Please login to <a href="homerhokietailgate.com">Homer Hokie Tailgate</a>' \
               ' to submit your scores before the deadline.</p><p>Surely you do not want zero points' \
               ' for the week!</p><br><p>Happy Prognosticating!</p><br><p>Please contact' \
               ' <a href="mailto:pat.hooper83@gmail.com">support</a> if you need assistance.</p>'
