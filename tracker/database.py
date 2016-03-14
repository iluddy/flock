import json
from flask import session
from utils import random_password, account_token
from constants import *
from models import *
import models as mo


class Database():
    """
    Wrapper for the database layer
    """
    PAGE_SIZE = 12

    session_cache = {}

    def __init__(self, db):
        self.db = db
        self.reset_database()
        self.add_defaults()
        self.add_test_data()

    def add_defaults(self):
        for collection_name, data in default_data.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def reset_database(self):
        Role.drop_collection()
        RoleType.drop_collection()
        Person.drop_collection()
        Company.drop_collection()

    def add_test_data(self):
        for collection_name, data in test_data.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def register_user(self, name, mail, password, company):
        try:
            new_company = Company(name=company)
            new_company.save()
        except NotUniqueError:
            return False, 'Company name already in use :('

        try:
            Person(name=name, mail=mail, password=password, company=new_company).save()
        except NotUniqueError:
            return False, 'Email address already in use :('

        return True, 'Registered'

    def activate_user(self, token, name, password):
        try:
            Person.objects(token=token).update_one(
                name=name,
                password=password,
                token=None,
                active=True
            )
            return True, "Activated"
        except DoesNotExist:
            return False, "Invitation expired. A new invitation will need to be sent. Please contact your Organisation's administrator."

    def generate_token(self, mail):
        token = account_token()
        Person.objects(mail=mail).update_one(token=token)
        return token

    def authenticate_user(self, mail, password):
        # TODO : encrypt stored passwords
        try:
            user = Person.objects.get(mail=mail, password=password)
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['company_id'] = user.company.id
            session['company_name'] = user.company.name
        except DoesNotExist:
            try:
                Person.objects.get(mail=mail)
            except:
                return False, 'Email address not registered :('

            return False, 'Password is incorrect :('

        return True, 'Logged In'

    def reset_user(self, mail):
        new_password = random_password()
        try:
            user = Person.objects.get(mail=mail)
            user.password = new_password
            user.save()
            return new_password
            # TODO : encrypt stored passwords
        except DoesNotExist:
            abort(400, 'Email address not registered :(')

    def delete_person(self, person_id):
        # TODO - validate
        Person.objects.get(id=person_id).delete()

    def add_person(self, new_person):
        role = Role.objects(id=new_person['role']).get()
        new_person['role'] = role
        new_person['role_name'] = role.name
        new_person['role_theme'] = role.theme

        # Mail can either be a unique email address or can not exist
        if not new_person['mail']:
            del new_person['mail']

        return Person(**new_person).save()

    def get_people(self, company_id, user_id=None, search=None, sort_by=None, sort_dir=None, token=None, limit=None, offset=None):

        if user_id:
            return Person.objects.get(id=user_id)

        if token:
            return Person.objects.get(token=token)

        query = {'company': company_id}

        if search:
            # TODO - deal with multiple search terms
            # TODO - search status. ie. active, invitation pending etc
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'mail': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'role_name': {'$options': 'i', '$regex': '.*{}.*'.format(search)}}
            ]

        results = Person.objects(__raw__=query)
        count = len(results)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit is not None and offset is not None:
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results, count

    def get_places(self, company_id, place_id=None, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):

        if place_id:
            return Place.objects.get(id=place_id)

        query = {'company': company_id}

        if search:
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'address': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'mail': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'description': {'$options': 'i', '$regex': '.*{}.*'.format(search)}}
            ]

        results = Place.objects(__raw__=query)
        count = len(results)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit is not None and offset is not None:
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results, count

    def get_events(self, company_id):
        return Event.objects()

    def delete_place(self, place_id):
        # TODO - validate
        Place.objects.get(id=place_id).delete()

    def add_place(self, new_place):
        return Place(**new_place).save()

    def get_company(self):
        return Company.objects.get(id=session['company_id'])

    def get_role_types(self):
        return RoleType.objects()

    def get_roles(self):
        return Role.objects(company=session['company_id'])

    def update_role(self, role):
        role_type = RoleType.objects(id=role['role_type']).get()
        if role.get('id'):
            Role.objects(id=role['id']).update_one(
                theme=role['theme'],
                name=role['name'],
                role_type=role_type
            )
        else:
            role['company'] = session['company_id']
            Role(**role).save()

    def delete_role(self, role_id):
        Role.objects.get(id=role_id).delete()
