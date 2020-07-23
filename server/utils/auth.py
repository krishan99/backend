"""Auth module with decorator factory for requiring username in session."""
import functools
import flask


def require(f):
    """Require username in session."""
    @functools.wraps(f)
    def authed(*args, **kwargs):
        if 'username' in flask.session:
            return f(*args, **kwargs)
        if flask.request.method == 'POST':
            flask.abort(403)
        return flask.redirect(flask.url_for('login'))
    return authed


def api_require(f):
    """Require business username in session for api."""
    @functools.wraps(f)
    def authed(*args, **kwargs):
        if 'bid' in flask.session:
            return f(*args, **kwargs)
        context = {
            'message': "Forbidden",
            'status_code': 403
        }
        print("Not logged in")
        return flask.jsonify(**context), 403
    return authed
