from flock.app import db_wrapper as db
from flock.app import celery
from flask import session

def get(company_id, limit=None, offset=None, sort_by=None, sort_dir=None):
    return db.notification_get(company_id, limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir)

def notify(body, message=None, mail_function=None, mail_args=None, action=None, target=None):
    _notify.delay(session['company_id'], session['user_id'], body, message, action, target)

    if mail_function:
        pass
        # TODO - send mail

@celery.task
def _notify(company_id, owner_id, body, message, action, target):
    user = db.person_get(user_id=owner_id)
    body = body.format(u'<b>{}</b>'.format(user.name))
    db.notification_add(company_id, owner_id, body, action, target, message=message)

