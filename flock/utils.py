import json
import logging
from functools import wraps
from logging.handlers import RotatingFileHandler
from uuid import uuid4, uuid5, NAMESPACE_DNS
import hashlib
from flask import make_response, session, abort
from mongoengine import QuerySet

def plain_text_to_html(content):
    import re
    # Replace what seems like an url with hyperlink
    output = re.sub(r'(https?://[^ \n$]+)', r'<a href="\1">\1</a>', unicode(content))
    # Replace two newline characters with paragraph boundry
    output = '<p>%s</p>' % output.replace('\n\n', '</p><p>')
    # Replace single newline with break-rule
    output = output.replace('\n', '<br/>')
    return output

def hash_string(string):
    return hashlib.md5(string.encode('utf-8')).digest()

def validate_password(string):
    if len(string) < 8:
        abort(400, 'Password needs to be at least 8 characters')

def read_config_file(config_file):
    with open(config_file, "r") as f:
        cfg_json = json.loads(f.read())
    return cfg_json

def list_to_title_string(list):
    string = ""
    for item in list:
        string += item.title() + ", "
    return string[0:len(string) - 2]

def make_uuid(string):
    return str(uuid5(NAMESPACE_DNS, string))

def random_uuid():
    return str(uuid4())

def random_password():
    return random_uuid()[24:]

def account_token():
    return random_uuid()

def wrapped_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception, e:
        logging.error("Fatal error calling %s" % str(func), exc_info=True)

def raw_response(response_string):
    response = make_response(response_string)
    response.mimetype = "text/plain"
    return response

def json_response(response, count=None, sort=False):
    if sort and type(response) is list:
        response = sorted(response)
    if count is not None:
        response = make_response(json.dumps({"count": count, "data": response}))
    else:
        response = make_response(json.dumps(response))
    response.mimetype = "application/json"
    return response

def setup_logger(log_file, log_level):
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=2) # File handler
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:[%(module)s:%(lineno)d]:[%(threadName)s]:%(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    ch = logging.StreamHandler() # Stream handler
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def strip_dict(dictionary):
    return dict((k, v) for k, v in dictionary.iteritems() if v not in [None, {}, []] and k not in [None, {}, []])

def float_to_two_places(x):
    return int(x * 100) / 100.0

def capitalise(string):
    return string.title()

def json_response(response):

    def dump(data):
        if type(data) in [list, QuerySet]:
            return [doc.to_dict() for doc in data]
        return data

    if "data" in response:
        response['data'] = dump(response['data'])
    else:
        response = dump(response)

    response = make_response(json.dumps(response))
    response.mimetype = "application/json"
    return response

def auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            session.clear()
            abort(403, 'You are no longer logged in!')

        # TODO - verify user and company match

        return f(*args, **kwargs)
    return decorated_function