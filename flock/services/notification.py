from flock.app import db_wrapper as db
from flock.app import celery

def get(company_id, limit=None, offset=None, sort_by=None, sort_dir=None):
    return db.notification_get(company_id, limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir)

def notify(company_id, owner_id, body, message=None, mail_function=None, mail_args=None):

    _notify.delay(company_id, owner_id, body, message)

    if mail_function:
        pass
        # TODO - send mail

@celery.task
def _notify(company_id, owner_id, body, message):
    db.notification_add(company_id, owner_id, body, message=message)

