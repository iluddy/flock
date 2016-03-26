import argparse
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from database import Database
from task_manager import TaskManager
from services import PersonService, PlaceService, AccountService, EventService, RoleService
from constants import secret_key, session_duration
from flask.ext.autodoc import Autodoc
from flask.ext.mongoengine import MongoEngine
from flask import Flask, Request
from utils import setup_logger, read_config_file
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
import __builtin__

# Argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c") # Config arg
args = arg_parser.parse_args()

# Config
cfg = read_config_file(args.c)

# Create App
app = Flask(__name__, static_url_path='')
app.secret_key = secret_key
app.permanent_session_lifetime = session_duration
documentor = Autodoc(app)
app.config['MONGODB_SETTINGS'] = {
    'db': cfg["database"]["name"],
    'host': cfg["database"]["host"],
    'port': cfg["database"]["port"]
}

# DB
db = MongoEngine()
db.init_app(app)
db_wrapper = Database(db)

# Mailer
from flock.mailer import Mailer
mailer = Mailer()

# Services
person_service = PersonService(db_wrapper, mailer)
place_service = PlaceService(db_wrapper, mailer)
account_service = AccountService(db_wrapper, mailer)
event_service = EventService(db_wrapper, mailer)
role_service = RoleService(db_wrapper, mailer)

# TODO - not this
__builtin__.flock_app = app
__builtin__.flock_db_wrapper = db_wrapper
__builtin__.flock_person_service = person_service
__builtin__.flock_place_service = place_service
__builtin__.flock_account_service = account_service
__builtin__.flock_event_service = event_service
__builtin__.flock_role_service = role_service

if __name__ == '__main__':

    # Logging
    setup_logger(cfg["logging"]["file"], cfg["logging"]["level"])

    # Init Rollbar
    @app.before_first_request
    def init_rollbar():
        rollbar.init(
            cfg["rollbar"]["token"],
            cfg["rollbar"]["environment"],
            root=os.path.dirname(os.path.realpath(__file__)),
            allow_logging_basic_config=False
        )
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    class CustomRequest(Request):
        @property
        def rollbar_person(self):
            from flask import session
            return {'id': session['user_id'], 'username': session['user_name'], 'email': session['email']}

    app.request_class = CustomRequest

    # Create Views
    from flock import views

    # Run using flask development server
    # app.run(cfg["web_server"]["host"], cfg["web_server"]["port"])

    # Run with Tornado
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(cfg["web_server"]["port"], address=cfg["web_server"]["host"])
    IOLoop.instance().start()