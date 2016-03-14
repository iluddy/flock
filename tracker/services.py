from flask import abort, session

class Service:

    def __init__(self, db, mailer):
        self.db = db
        self.mailer = mailer

class EventService(Service):

    def get(self, company_id):
        return self.db.get_events(company_id)

class AccountService(Service):

    def reset(self, mail):
        new_password = self.db.reset_user(mail)
        self.mailer.reset(mail, new_password)

class PlaceService(Service):

    def add(self, new_place):
        self.db.add_place(new_place)

    def delete(self, place_id):
        # TODO - validate
        self.db.delete_place(place_id)

    def get(self, company_id, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
        return self.db.get_places(company_id, search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)

class PersonService(Service):

    def invite(self, mail, sender_id):
        if not mail:
            abort(400, 'No email address registered for this Person, please add one to send an invitation')
        sender = self.db.get_people(user_id=sender_id).name
        token = self.db.generate_token(mail)
        self.mailer.invite(mail, sender, token)

    def add(self, new_person):
        self.db.add_person(new_person)

        if new_person['invite']:
            if not new_person.get('mail'):
                abort(400, 'Please specify an email address to send the invitation to, or uncheck the invitation box.')

            self.invite(new_person['mail'], session['user_id'])

    def delete(self, user_id):
        # TODO - validate
        self.db.delete_person(user_id)

    def get(self, company_id, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
        return self.db.get_people(company_id, search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
