from mongoengine import *

class User(Document):
    username = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    password = StringField()
    company = ReferenceField('Company')

class Company(Document):
    name = StringField(unique=True)

