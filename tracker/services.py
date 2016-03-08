from flask import abort, session

class PersonService():

    def __init__(self, db, mailer):
        self.db = db
        self.mailer = mailer

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

    def get(self, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
        return self.db.get_people(search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
