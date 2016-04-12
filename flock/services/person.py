from flock.app import db_wrapper as db
from flask import abort
from flock.services import mail

def invite(email, sender_id, company_id):
    recipient = db.person_get(company_id=company_id, mail=email)

    if not email or not recipient:
        abort(400, 'No email address registered for this Person, please add one to send an invitation')

    token = db.generate_token(email) if not recipient.token else recipient.token

    mail.invite(
        email,
        db.person_get(company_id, user_id=sender_id).name,
        token
    )

def add(new_person, user_id, company_id):
    if new_person['invite'] and not new_person.get('mail'):
        abort(400, 'Please specify an email address to send the invitation to, or uncheck the invitation box.')

    db.person_add(new_person)

    if new_person['invite']:
        invite(new_person['mail'], user_id, company_id)

def delete(user_id):


    # TODO - validate
    db.person_delete(user_id)

def get(company_id=None, role_id=None, mail=None, search=None, sort_by=None, sort_dir=None, limit=None,
        offset=None):
    return db.person_get(company_id=company_id, role_id=role_id, search=search, sort_by=sort_by,
                              sort_dir=sort_dir, limit=limit, offset=offset, mail=mail)