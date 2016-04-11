from datetime import timedelta
from random import randint, choice
from werkzeug.exceptions import abort
import models as mo
from constants import *
from models import *
from utils import random_password, validate_password
from mongoengine import NotUniqueError, DoesNotExist

class Database():
    """
    Wrapper for the database layer
    """
    def __init__(self, db):
        self.db = db
        self.reset_database()
        self.add_defaults()
        self.add_test_data()
        self.add_indexes()

    #### Utils ####

    def add_indexes(self):
        pass
        # self.db.person.createIndex({"company": 1, "mail": 1})

    def add_defaults(self):
        for collection_name, data in DEFAULT_DATA.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def reset_database(self):
        Person.drop_collection()
        Role.drop_collection()
        Place.drop_collection()
        Event.drop_collection()
        Company.drop_collection()

    def add_test_data(self):
        for collection_name, data in TEST_DATA.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()
        self.create_random_events()

    def create_random_events(self):
        titles = ['Dance Class', 'Cake Class', 'Computer Class', 'Office Meeting', 'Driving Lesson', 'Arts & Crafts']
        id = -1
        for i in range(-7, 7):
            for j in range(25):
                id -= 1
                hour = randint(6, 18)
                start = datetime.utcnow() + timedelta(days=i)
                start = start.replace(hour=hour, minute=0)
                end = start.replace(hour=hour + 1)
                Event(
                    id=id,
                    start=start,
                    end=end,
                    company=-1,
                    people=[randint(-10, -1), randint(-10, -1)],
                    place=randint(-5, -1),
                    owner=randint(-10, -1),
                    title=choice(titles)
                ).save()

    #### User Account ####

    def register_user(self, name, mail, password, company):
        validate_password(password)

        new_company = Company(name=company)

        try:
            owner = Person(name=name, mail=mail.lower(), password=generate_password_hash(password), company=new_company)
            owner.save()
        except NotUniqueError:
            abort(400, 'Email address already in use :(')

        try:
            new_company.owner = owner
            new_company.save()
        except NotUniqueError:
            abort(400, 'Company name already in use :(')

    def permissions_get(self, user_id):
        try:
            return self.person_get(user_id=user_id).role.permissions
        except DoesNotExist:
            return None

    def activate_user(self, token, name, password):
        validate_password(password)

        try:
            Person.objects(token=token).update_one(
                name=name,
                password=generate_password_hash(password),
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
        try:
            user = Person.objects.get(mail=mail.lower())
            if check_password_hash(user.password, password):
                return user.id, user.name, user.company.id, user.company.name, user.mail
            abort(400, 'Password is incorrect :(')
        except DoesNotExist:
            abort(400, 'Email address not registered :(')

    def reset_user(self, mail):
        new_password = random_password()
        try:
            user = Person.objects.get(mail=mail)
            user.password = generate_password_hash(new_password)
            user.save()
            return new_password
        except DoesNotExist:
            abort(400, 'Email address not registered :(')

    #### Person ####

    def person_delete(self, person_id):
        # TODO - validate
        Person.objects.get(id=person_id).delete()

    def person_add(self, new_person):

        role = Role.objects(id=new_person['role']).get()
        new_person['role'] = role
        new_person['role_name'] = role.name
        new_person['role_theme'] = role.theme

        # Mail can either be a unique email address or can not exist
        if not new_person['mail']:
            del new_person['mail']
        else:
            new_person['mail'] = new_person['mail'].lower()

        try:
            return Person(**new_person).save()
        except NotUniqueError:
            abort(400, 'That email address is already in use.')

    def person_update(self, new_person):
        # TODO - this
        pass

    def person_get(self, company_id=None, role_id=None, user_id=None, mail=None, search=None, sort_by=None, sort_dir=None, token=None, limit=None, offset=None):
        if user_id:
            return Person.objects.get(id=user_id)

        if mail:
            return Person.objects.get(__raw__={'mail': mail, 'company': int(company_id)})

        if token:
            try:
                return Person.objects.get(token=token)
            except DoesNotExist:
                return None

        if role_id:
            return Person.objects(__raw__={'role': int(role_id)})

        query = {'company': company_id}

        if search:
            # TODO - deal with multiple search terms
            # TODO - search status. ie. active, invitation pending etc
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'mail': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'role_name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}}
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

    def event_get(self, company_id=None, start=None, end=None, show_expired=True, place_id=None, limit=None,
            offset=None, sort_by=None, sort_dir='asc', user_id=None):

        query = {'company': int(company_id)}

        if place_id:
            query['place'] = int(place_id)

        if show_expired is not True:
            query['start'] = {'$gte': datetime.now()}

        if start:
            query['start'] = {'$gte': datetime.strptime(start, '%Y-%m-%d')}

        if end:
            query['end'] = {'$lte': datetime.strptime(end, '%Y-%m-%d')}

        if user_id:
            query['$or'] = [
                {'owner': user_id},
                {'people': user_id},
            ]

        results = Event.objects(__raw__=query)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit:
            offset = 0 is not offset
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results

    #### Place ####

    def place_get(self, company_id=None, place_id=None, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):

        if place_id:
            return Place.objects.get(id=place_id)

        query = {'company': company_id}

        if search:
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'address': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'mail': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'description': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}}
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

    #### Role ####

    def role_get(self, company_id=None, role_id=None):
        if company_id:
            return Role.objects(company=company_id)
        if role_id:
            return Role.objects.get(id=role_id)

    def role_add(self, role, company_id):
        if Role.objects(company=company_id, name=role['name']):
            abort(400, 'A Role with this name already exists.')
        role['company'] = company_id
        Role(**role).save()

    def role_update(self, role):
        Role.objects(id=role['id']).update_one(
            theme=role['theme'],
            name=role['name'],
            permissions=role['permissions']
        )

    def person_role_update(self, role):
        role = Role.objects.get(id=role['id'])
        Person.objects(role=role).update(
            role=role,
            role_name=role.name,
            role_theme=role.theme
        )

    def role_delete(self, role_id):
        Role.objects.get(id=role_id).delete()
