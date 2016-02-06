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
        self.create_indexes()
        self.add_defaults()
        self.add_test_data()


    def create_indexes(self):
        # TODO - this
        # self.db.user.create_index("price")
        pass

    def add_defaults(self):
        for collection_name, data in default_data.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def reset_database(self):
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

    # def create_session(self, user_id, company_id):
    #     session_token = random_uuid()
    #     self.session_cache[session_token] = (user_id, company_id)
    #     return session_token
    #
    # def authenticate_session(self, token):
    #     return token in self.session_cache
    #
    # def end_session(self, token):
    #     if token in self.session_cache:
    #         del self.session_cache[token]
    #     print self.session_cache

    def get_people(self, company_id, user_id=None):
        if user_id:
            return Person.objects.get(id=user_id, company=company_id).to_mongo()
        return Person.objects(company=company_id)

    def get_company(self, company_id):
        return Company.objects.get(id=company_id)

    def get_roles(self, company_id):
        return Role.objects(company=company_id)
