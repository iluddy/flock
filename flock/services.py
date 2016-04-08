from flask import abort, session

class Service:

    def __init__(self, db, mailer):
        self.db = db
        self.mailer = mailer

class EventService(Service):

    def get(self, company_id):
        return self.db.event_get(company_id=company_id)

class AccountService(Service):

    def reset(self, mail):
        new_password = self.db.reset_user(mail)
        self.mailer.reset(mail, new_password)

class PlaceService(Service):

    def add(self, new_place):
        self.db.place_add(new_place)

    def delete(self, place_id):
        place = self.db.place_get(place_id=place_id)
        events = self.db.event_get(place_id=place_id)

        if events:
            abort(400, u'There are {} Event(s) happening at {}. Delete those Events first.'.format(len(events), place.name))

        self.db.place_delete(place_id)

    def get(self, company_id, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
        return self.db.place_get(company_id, search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)

class PersonService(Service):

    def invite(self, mail, sender_id, company_id):
        recipient = self.db.person_get(company_id, mail=mail)

        if not mail or not recipient:
            abort(400, 'No email address registered for this Person, please add one to send an invitation')

        self.mailer.invite(
            mail,
            self.db.person_get(company_id, user_id=sender_id).name,
            self.db.generate_token(mail)
        )

    def add(self, new_person, user_id, company_id):

        if new_person['invite'] and not new_person.get('mail'):
            abort(400, 'Please specify an email address to send the invitation to, or uncheck the invitation box.')

        self.db.person_add(new_person)

        if new_person['invite']:
            self.invite(new_person['mail'], user_id, company_id)

    def delete(self, user_id):
        # TODO - validate
        self.db.person_delete(user_id)

    def get(self, company_id=None, role_id=None, mail=None, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
        return self.db.person_get(company_id=company_id, role_id=role_id, search=search, sort_by=sort_by,
                                  sort_dir=sort_dir, limit=limit, offset=offset, mail=mail)

class RoleService(Service):

    def add(self, role, company_id):
        self.db.role_add(role, company_id)

    def delete(self, role_id):
        people = self.db.person_get(role_id=role_id)
        role = self.get(role_id=role_id)
        if people:
            abort(400, u'There are {} {}(s) registered. Remove those People first.'.format(len(people), role.name))
        self.db.role_delete(role_id)

    def update(self, role):
        self.db.role_update(role)
        self.db.person_role_update(role)

    def get(self, role_id=None, company_id=None):
        return self.db.role_get(role_id=role_id, company_id=company_id)

