from functools import wraps

from flask import session, url_for, redirect


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in session.keys() or ['user'] is None:
            return redirect(url_for('users.login_user', message='You need to be logged in to access this page.'))
        return func(*args, **kwargs)
    return decorated_function


def requires_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['useradmin'] == 'No' or session['useradmin'] is None:
            return redirect(url_for('dashboard.user_dashboard', message='You need to be an admin to access this page.'))
        return func(*args, **kwargs)
    return decorated_function
