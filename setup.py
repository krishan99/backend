"""
Python package configuration.
"""

from setuptools import setup

setup(
    name='server',
    version='0.1.0',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'arrow==0.15.5',
        'astroid==2.3.3',
        'attrs==19.3.0',
        'beautifulsoup4==4.9.1',
        'bs4==0.0.1',
        'certifi==2020.4.5.2',
        'chardet==3.0.4',
        'click==7.1.2',
        'dnspython==1.16.0',
        'eventlet==0.25.2',
        'firebase-admin==4.3.0',
        'Flask==1.1.1',
        'Flask-Cors==3.0.8',
        'Flask-SocketIO==4.3.1',
        'Flask-Sockets==0.2.1',
        'gevent-websocket==0.10.1',
        'greenlet==0.4.16',
        'gunicorn==20.0.4',
        'html5validator==0.3.3',
        'idna==2.8',
        'importlib-metadata==1.6.1',
        'isort==4.3.21',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'lazy-object-proxy==1.4.3',
        'MarkupSafe==1.1.1',
        'mccabe==0.6.1',
        'monotonic==1.5',
        'more-itertools==8.3.0',
        'nodeenv==1.3.5',
        'packaging==20.4',
        'phonenumbers==8.12.6',
        'pluggy==0.13.1',
        'py==1.8.1',
        'pycodestyle==2.5.0',
        'pydocstyle==5.0.2',
        'PyJWT==1.7.1',
        'pylint==2.4.4',
        'pyparsing==2.4.7',
        'pytest==5.3.5',
        'pytest-flask==0.15.1',
        'python-dateutil==2.8.1',
        'python-engineio==3.13.1',
        'python-socketio==4.6.0',
        'pytz==2020.1',
        'requests==2.23.0',
        'selenium==3.141.0',
        'sh==1.12.14',
        'six==1.15.0',
        'snowballstemmer==2.0.0',
        'soupsieve==2.0.1',
        'twilio==6.42.0',
        'typed-ast==1.4.1',
        'urllib3==1.25.9',
        'wcwidth==0.2.3',
        'Werkzeug==1.0.1',
        'wrapt==1.11.2',
        'zipp==3.1.0',
        'zope.event==4.4',
        'zope.interface==5.1.0',
    ],
)
