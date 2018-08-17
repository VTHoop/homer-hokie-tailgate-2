from functools import wraps

from flask import session, url_for, redirect


def requires_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['useradmin'] == 'No' or session['useradmin'] is None:
            return redirect(url_for('dashboard.user_dashboard', message='You need to be an admin to access this page.'))
        return func(*args, **kwargs)
    return decorated_function
