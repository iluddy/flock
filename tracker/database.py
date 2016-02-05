from flask import session
from utils import random_password
from models import *

class Database():
    """
    Wrapper for the database layer
    """
    PAGE_SIZE = 12

    session_cache = {}

    def __init__(self, db):
        self.db = db
        self.create_indexes()
        # self.reset_database()

    def create_indexes(self):
        # self.db.user.create_index("price")
        pass

    def reset_database(self):
        Person.drop_collection()
        Company.drop_collection()

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

    def get_user(self, user_id):
        return Person.objects.get(id=user_id)

    def get_company(self, company_id):
        return Company.objects.get(id=company_id)

    #### Utils ####
    #
    # def remove(self, collection_name, query):
    #     logging.info("Rem: col=%s qry=%s" % (collection_name, query))
    #
    #     self._get_collection(collection_name).remove(strip_dict(query))
    #
    # def query(self, collection_name, query, sort_by=None, sort_dir=None, page=None):
    #     logging.info("Qry: col=%s qry=%s srt=%s:%s pg=%s" % (collection_name, query, sort_by, sort_dir, page ) )
    #
    #     result = self._get_collection(collection_name).find(strip_dict(query))
    #     count = result.count()
    #
    #     # Sorting
    #     if sort_by is not None:
    #         sort_dir = 1 if sort_dir is None else int(sort_dir) # 1 = ascending, -1 = descending
    #         result = result.sort(sort_by, sort_dir)
    #
    #     # Pagination
    #     if page is not None:
    #         result = result.limit(self.PAGE_SIZE).skip(int(page) * self.PAGE_SIZE)
    #
    #     return self._serialise(result), count
    #
    # def all(self, collection_name):
    #     return self._serialise(self._get_collection(collection_name).find())
    #
    # def count(self, collection_name):
    #     return self._get_collection(collection_name).find().count()
    #
    # def distinct(self, collection_name, key):
    #     return self._get_collection(collection_name).find().distinct(key)
    #
    # def range(self, collection_name, key):
    #     return {
    #         "max": self.max(collection_name, key),
    #         "min": self.min(collection_name, key),
    #     }
    #
    # def max(self, collection_name, key):
    #     return self._get_collection(collection_name).find_one(sort=[(key, -1)])[key]
    #
    # def min(self, collection_name, key):
    #     return self._get_collection(collection_name).find_one(sort=[(key, 1)])[key]
    #
    # #### Internal ####
    #
    # @staticmethod
    # def _all(arguments):
    #     if arguments not in [None, []]:
    #         return {"$all": json.loads(arguments)}
    #
    # @staticmethod
    # def _gt(arguments):
    #     if arguments not in [None, []]:
    #         return {"$gt": arguments}
    #
    # @staticmethod
    # def _lt(arguments):
    #     if arguments not in [None, []]:
    #         return {"$lt": arguments}
    #
    # @staticmethod
    # def _in(arguments):
    #     if arguments is not None:
    #         if not arguments:
    #             return {"$in": arguments}
    #         return {"$in": json.loads(arguments)}
    #
    # @staticmethod
    # def _in_range(arguments):
    #     if arguments is not None:
    #         range = json.loads(arguments)
    #         return {"$gte": range[0], "$lte": range[1]}
    #
    # @staticmethod
    # def _serialise_document(object):
    #     del object["_id"] # Delete unserialisable mongo id
    #     return object
    #
    # def _serialise(self, cursor):
    #     return [self._serialise_document(obj) for obj in cursor]
    #
    # def _get_collection(self, collection_name):
    #     return getattr(self.db, collection_name)