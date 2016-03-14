import argparse
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from database import Database
from task_manager import TaskManager
from services import PersonService, PlaceService, AccountService, EventService
from constants import secret_key, session_duration
from flask.ext.autodoc import Autodoc
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from tracker.mailer import Mailer
from utils import setup_logger, read_config_file

# Argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c") # Config arg
args = arg_parser.parse_args()

# Config
cfg = read_config_file(args.c)

# Logging
setup_logger(cfg["logging"]["file"], cfg["logging"]["level"])

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
mailer = Mailer()

# Services
person_service = PersonService(db_wrapper, mailer)
place_service = PlaceService(db_wrapper, mailer)
account_service = AccountService(db_wrapper, mailer)
event_service = EventService(db_wrapper, mailer)

# Create Views
from tracker import views

# Run with Tornado
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(cfg["web_server"]["port"], address=cfg["web_server"]["host"])
IOLoop.instance().start()
