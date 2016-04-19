import argparse
from database import Database
from constants import SECRET_KEY, SESSION_DURATION
from flask.ext.autodoc import Autodoc
from flask.ext.mongoengine import MongoEngine
from flask import Flask, Request
from utils import setup_logger, read_config_file
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
from celery import Celery
import __builtin__

# Config
if not hasattr(__builtin__, 'flock_cfg'):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c")
    args = arg_parser.parse_args()
    cfg = read_config_file(args.c)
else:
    cfg = __builtin__.flock_cfg

# Create App
app = Flask(__name__, static_url_path='')
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = SESSION_DURATION
documentor = Autodoc(app)
app.config['MONGODB_SETTINGS'] = {
    'db': cfg["database"]["name"],
    'host': cfg["database"]["host"],
    'port': cfg["database"]["port"]
}

# Celery
app.config['CELERY_BROKER_URL'] = cfg['redis']['url']
app.config['CELERY_RESULT_BACKEND'] = cfg['redis']['url']

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# DB
db = MongoEngine()
db.init_app(app)
db_wrapper = Database(db, cfg)

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

if __name__ == '__main__':
    # Create Views
    __builtin__.flock_app = app
    from flock import views

    # Run with Tornado
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    http_server = HTTPServer(WSGIContainer(app))

    http_server.listen(cfg["web_server"]["port"], address=cfg["web_server"]["host"])
    IOLoop.instance().start()