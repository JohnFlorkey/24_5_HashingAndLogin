from flask import session


def is_authorized(username):
    if 'username' in session and username == session['username']:
        return True
    return False
