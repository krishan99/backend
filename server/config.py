"""server development configuration."""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
# We may need to change how this works
# SECRET_KEY = (b'\xfd}j[\xb2\xfc\xd2>\x178\x87\xc2'
#               b'\xa1\xe7o\xae\xed\xa7\xbe1\xaf\xff\xaf[')
SECRET_KEY = (b'\xe2\x11\xa5ax\x99fk\xd1\xaaw[7q\x97\xdb\x8a\x7fv\x1b\xd1\x88|P')
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'server.sqlite3'
)
