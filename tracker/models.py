from mongoengine import *
from datetime import datetime

# TODO - add indexes

class Base(object):

    def to_dict(self):
        return self.to_mongo()

class Person(Document, Base):
    meta = {
        'indexes': ['mail', 'name']
    }

    id = SequenceField(primary_key=True)
    mail = StringField(unique=True, nullable=True)
    name = StringField()
    invite = BooleanField() # Null = dont invite, False = invite not yet sent, True = invite sent
    password = StringField()
    company = ReferenceField('Company')
    role = ReferenceField('Role')

    def to_dict(self):
        output = self.to_mongo()
        output['role_name'] = self.role.name
        output['role_theme'] = self.role.theme
        return output

class Role(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    role_type = ReferenceField('RoleType')
    theme = StringField()
    company = ReferenceField('Company')

    def to_dict(self):
        output = self.to_mongo()
        output['role_type_name'] = self.role_type.name
        return output

class RoleType(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField()
    description = StringField()

class Event(Document, Base):
    id = SequenceField(primary_key=True)
    owner = ReferenceField('Person')
    people = ListField(ReferenceField('Person'))
    things = ListField(ReferenceField('Thing'))
    name = StringField()
    place = ReferenceField('Place')

class Place(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    description = StringField()

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
