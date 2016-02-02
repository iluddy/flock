from mongoengine import *
from datetime import datetime

class User(Document):
    id = SequenceField(primary_key=True)
    mail = StringField(unique=True)
    name = StringField()
    password = StringField()
    company = ReferenceField('Company')
    type = StringField() # admin, leader

class Member(Document):
    id = SequenceField(primary_key=True)
    mail = StringField(unique=True)
    name = StringField()
    company = ReferenceField('Company')

class Event(Document):
    id = SequenceField(primary_key=True)
    users = ListField(ReferenceField('User'))
    name = StringField()
    location = StringField()
    members = ListField(ReferenceField('Member'))

class Company(Document):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    status = StringField(default='trialling') # trialling
    joined = DateTimeField(default=datetime.now)

