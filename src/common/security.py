import os

from itsdangerous import URLSafeTimedSerializer

ts = URLSafeTimedSerializer(os.environ.get('HHT_API_KEY'))
# figure out secret key later
