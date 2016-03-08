import requests

class Mailer():
    auth = ("api", "key-97da181732b95a21257c270bd2215529")
    server = "https://api.mailgun.net/v3/sandboxd4ff99d2df0b4dbbb94cc9e08a0391d1.mailgun.org/messages"
    sent_from = "Flock Team <hello@flock.ie>"

    def send(self, data):
        requests.post(
            self.server,
            auth=self.auth,
            data=data
        )

    def invite(self, recipient, sender, token):

        # TODO - remove this
        recipient = 'ianluddy@gmail.com'

        self.send({
            "from": self.sent_from,
            "to": recipient,
            "subject": "{} has invited you to use Flock :)".format(sender),
            "text": """

            {} has invited you to use Flock :)

            Follow this link to activate your account:

            http://localhost:5001/activate/{}

            """.format(sender, token),
        })