from flask import abort
from flock.app import db_wrapper as db

def add(role, company_id):
    db.role_add(role, company_id)

def delete(role_id):

    people = db.person_get(role_id=role_id)
    role = get(role_id=role_id)

    if people:
        abort(400, u'There are {} {}(s) registered. Remove those People first.'.format(len(people), role.name))

    db.role_delete(role_id)

def update(role):

    db.role_update(role)
    db.person_role_update(role)

def get(role_id=None, company_id=None):
    return db.role_get(role_id=role_id, company_id=company_id)