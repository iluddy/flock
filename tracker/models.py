from mongoengine import *
from datetime import datetime
from utils import account_token

# TODO - add indexes

class Base(object):

    def to_dict(self):
        return self.to_mongo()

class Person(Document, Base):
    meta = {
        'indexes': ['mail', 'name']
    }

    id = SequenceField(primary_key=True)
    mail = StringField(unique=True, nullable=True, sparse=True)
    phone = StringField(unique=True, nullable=True, sparse=True)
    name = StringField()
    invite = BooleanField(default=True)
    active = BooleanField(default=False)
    password = StringField()
    company = ReferenceField('Company', nullable=False)
    role = ReferenceField('Role', nullable=False)
    role_name = StringField(nullable=False)
    role_theme = StringField(nullable=False)
    token = StringField()

    def generate_token(self):
        self.token = account_token()
        return self.token

    def to_dict(self):
        output = self.to_mongo()
        output['initials'] = ''.join(name[0].upper() for name in self.name.split())
        return output

class Role(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    role_type = ReferenceField('RoleType', nullable=False)
    theme = StringField(nullable=False)
    company = ReferenceField('Company', nullable=False)

    def to_dict(self):
        output = self.to_mongo()
        output['role_type_name'] = self.role_type.name
        return output

class RoleType(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    description = StringField(nullable=False)

class Event(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField(nullable=False)
    owner = ReferenceField('Person', nullable=False)
    start = DateTimeField(nullable=False)
    end = DateTimeField()
    people = ListField(ReferenceField('Person'))
    things = ListField(ReferenceField('Thing'))
    place = ReferenceField('Place')
    company = ReferenceField('Company', nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'people': [person.to_dict() for person in self.people],
            'start': str(self.start),
            'end': str(self.end),
            'owner': self.owner.to_dict(),
            'place': self.place.to_dict() if self.place else None
        }

class Place(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    address = StringField(nullable=False)
    directions = StringField()
    mail = StringField()
    phone = StringField()
    company = ReferenceField('Company', nullable=False)

class Company(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    status = StringField(default='trialling')
    joined = DateTimeField(default=datetime.now)

class Notification(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField()
    body = StringField()
    company = DateTimeField(default=datetime.now)
    person = ReferenceField('Person')

class Thing(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField()
    body = StringField()
