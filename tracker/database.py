import json
from flask import session
from utils import random_password
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
            # TODO : encrypt stored passwords
            # TODO : send email
            return True, 'Password reset. You should receive an email shortly :)'
        except DoesNotExist:
            return False, 'Email address not registered :('

    def delete_person(self, person_id):
        Person.objects.get(id=person_id).delete()

    def add_person(self, new_person):
        new_person['role'] = Role.objects(id=new_person['role']).get()
        return Person(**new_person).save()

    def get_people(self, user_id=None, search=None):
        query = {'company': session["company_id"]}
        if user_id:
            query["user_id"] = user_id
        if search:
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'mail': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
                {'role': {'$options': 'i', '$regex': '.*{}.*'.format(search)}},
            ]
        return Person.objects(__raw__=query)

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
