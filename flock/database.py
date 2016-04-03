from datetime import timedelta
from random import randint

from werkzeug.exceptions import abort

import models as mo
from constants import *
from models import *
from utils import random_password


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

    #### Utils ####

    def add_defaults(self):
        for collection_name, data in default_data.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def reset_database(self):
        Role.drop_collection()
        Permission.drop_collection()
        Person.drop_collection()
        Place.drop_collection()
        Company.drop_collection()

    def add_test_data(self):
        for collection_name, data in test_data.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

        # Update event times
        for event in Event.objects():
            event_time = datetime.utcnow()
            event_time = event_time.replace(hour=randint(6, 18))
            event.update(
                start=event_time,
                end=event_time + timedelta(hours=randint(1, 2))
            )

    #### User Account ####

    def register_user(self, name, mail, password, company):
        try:
            new_company = Company(name=company)
            new_company.save()
        except NotUniqueError:
            abort(400, 'Company name already in use :(')

        try:
            Person(name=name, mail=mail, password=password, company=new_company).save()
        except NotUniqueError:
            abort(400, 'Email address already in use :(')

    def activate_user(self, token, name, password):
        try:
            Person.objects(token=token).update_one(
                name=name,
                password=password,
                token=None,
                active=True
            )
        except DoesNotExist:
            abort(400, "Invitation expired. A new invitation will need to be sent. Please contact your Organisation's administrator.")

    def generate_token(self, mail):
        token = account_token()
        Person.objects(mail=mail).update_one(token=token, invite=True)
        return token

    def authenticate_user(self, mail, password):
        # TODO : encrypt stored passwords
        try:
            user = Person.objects.get(mail=mail, password=password)
            return user.id, user.name, user.company.id, user.company.name, user.mail
        except DoesNotExist:
            try:
                Person.objects.get(mail=mail)
            except:
                abort(400, 'Email address not registered :(')

        abort(400, 'Password is incorrect :(')

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

    #### Person ####

    def person_delete(self, person_id):
        # TODO - validate
        Person.objects.get(id=person_id).delete()

    def person_add(self, new_person):

        # TODO - handle update

        role = Role.objects(id=new_person['role']).get()
        new_person['role'] = role
        new_person['role_name'] = role.name
        new_person['role_theme'] = role.theme

        # Mail can either be a unique email address or can not exist
        if not new_person['mail']:
            del new_person['mail']

        return Person(**new_person).save()

    def person_get(self, company_id=None, role_id=None, user_id=None, mail=None, search=None, sort_by=None, sort_dir=None, token=None, limit=None, offset=None):
        if user_id:
            return Person.objects.get(id=user_id)

        if mail:
            return Person.objects.get(mail=mail)

        if token:
            return Person.objects.get(token=token)

        if role_id:
            return Person.objects(role=self.role_get(role_id=role_id))

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

    #### Event ####

    def event_get(self, company_id=None, place_id=None):
        if company_id:
            return Event.objects(company=company_id)
        if place_id:
            return Event.objects(place=place_id)

    #### Place ####

    def place_get(self, company_id, place_id=None, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):

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

    def place_delete(self, place_id):
        Place.objects.get(id=place_id).delete()

    def place_add(self, new_place):
        return Place(**new_place).save()

    #### Company ####

    def company_get(self, company_id):
        return Company.objects.get(id=company_id)

    #### Permissions ####

    def permission_get(self, permission_name=None, permission_names=None):
        if permission_name:
            return Permission.objects.get(name=permission_name)
        if permission_names:
            return Permission.objects(name__in=permission_names)

    #### Role ####

    def role_get(self, company_id=None, role_id=None):
        if company_id:
            return Role.objects(company=company_id)
        if role_id:
            return Role.objects.get(id=role_id)

    def role_add(self, role, company_id):
        role['company'] = company_id
        Role(**role).save()

    def role_update(self, role, company_id):
        Role.objects(id=role['id']).update_one(
            theme=role['theme'],
            name=role['name'],
            permissions=self.permission_get(permission_names=role['permissions'])
        )

    def role_delete(self, role_id):
        Role.objects.get(id=role_id).delete()
