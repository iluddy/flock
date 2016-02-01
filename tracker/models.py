from mongoengine import *

class User(Document):
    id = SequenceField(primary_key=True)
    mail = StringField(unique=True)
    name = StringField()
    password = StringField()
    company = ReferenceField('Company')

class Company(Document):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)

class Session(Document):
    token = StringField(unique=True)
    user_id = IntField()
    company_id = IntField()
    # expires = DateTimeField()


