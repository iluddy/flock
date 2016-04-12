from flock.app import db_wrapper as db
from flock.services import mail

def reset(email):
    new_password = db.reset_user(email)
    mail.reset(email, new_password)