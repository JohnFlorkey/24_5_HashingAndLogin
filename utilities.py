from flask import session


def is_authorized(username):
    """validates that the username passed in is the logged in user"""
    if 'username' in session and username == session['username']:
        return True
    return False
