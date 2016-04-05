from mongoengine import Document, SequenceField, StringField, BooleanField, ReferenceField, ListField, DateTimeField
from mongoengine import PULL, DENY
from datetime import datetime
from utils import account_token

# TODO - add indexes

class Base(object):

    def to_dict(self):
        return self.to_mongo()

class Place(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    address = StringField(nullable=False)
    directions = StringField()
    mail = StringField()
    phone = StringField()
    company = ReferenceField('Company', nullable=False)

class Thing(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    description = StringField(nullable=True)
    company = ReferenceField('Company', nullable=False)

class Role(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    theme = StringField(nullable=False)
    company = ReferenceField('Company', nullable=False)
    permissions = ListField(StringField(nullable=False), nullable=False)

class Person(Document, Base):
    # TODO - allow email to be registered with multiple companies

    id = SequenceField(primary_key=True)
    mail = StringField(unique=True, nullable=False)
    phone = StringField(nullable=True)
    name = StringField()
    invite = BooleanField(default=True)
    active = BooleanField(default=False)
    password = StringField()
    company = ReferenceField('Company', nullable=False)
    role = ReferenceField('Role', nullable=False, reverse_delete_rule=DENY)
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

class Event(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField(nullable=False)
    owner = ReferenceField('Person', reverse_delete_rule=DENY)
    start = DateTimeField(nullable=False)
    end = DateTimeField()
    people = ListField(ReferenceField('Person', reverse_delete_rule=PULL))
    things = ListField(ReferenceField('Thing', reverse_delete_rule=PULL))
    place = ReferenceField('Place', reverse_delete_rule=DENY)
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

class Company(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    status = StringField(default='trialling')
    created = DateTimeField(default=datetime.now)
    owner = ReferenceField('Person', reverse_delete_rule=DENY)

    def save(self, *args, **kwargs):

        # Create default Roles
        admin = Role(name='Administrator', theme='success', company=self,
             permissions=[
                 'edit_events', 'edit_people', 'edit_places', 'edit_system_settings'
             ]
        ).save()
        Role(name='Regular User', theme='primary', company=self,
             permissions=[
                 'edit_events', 'edit_people', 'edit_places'
             ]
        ).save()
        Role(name='Read-Only User', theme='warning', company=self,
             permissions=[
                 'view_events', 'view_people', 'view_places'
             ]
        ).save()

        # Set owner as Admin
        self.owner.update(
            role=admin,
            role_name=admin.name,
            role_theme=admin.theme,
            active=True
        )

        return super(Company, self).save(*args, **kwargs)

class Notification(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField()
    body = StringField()
    company = DateTimeField(default=datetime.now)
    person = ReferenceField('Person')