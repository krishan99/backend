"""server package initializer."""
import flask
from firebase_admin import credentials
from flask_socketio import SocketIO
import firebase_admin

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
socketio = SocketIO(app, cors_allowed_origins = '*')
default_app = firebase_admin.initialize_app()

# Read settings from config module (insta485/config.py)
app.config.from_object('server.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/config/
app.config.from_envvar('SERVER_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import server.model  # noqa: E402  pylint: disable=wrong-import-position
import server.api  # noqa: E402  pylint: disable=wrong-import-position

if __name__ == "__main__":
    #socketio.run(app,port=5000, debug = True, host='0.0.0.0')
    socketio.run(app, debug = True, port=8000)
    