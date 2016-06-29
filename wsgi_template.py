import configparser
import sys

from beaker.middleware import SessionMiddleware

from flask import Flask

# Generated By Estus MVC Framework Builder v0.01a

#  Application Initialization

wsgi = Flask(__name__)
wsgi.secret_key = ""

# wsgi.wsgi_app = SessionMiddleware(wsgi.wsgi_app, session_opts)

config = configparser.ConfigParser()
config.read('config/settings.ini')
settings = config['SETTINGS']

# Welcome Mat


@wsgi.route('/')
def index():
    return 'Hello'

# Blueprint Registration


# Configure Favicon

if __name__ == '__main__':
    print(' * Application Configuration Successful')
    wsgi.run(host=settings['LISTEN'], port=int(settings['PORT']),
             debug=settings['DEBUG'])
