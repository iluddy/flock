import requests
from jinja2 import FileSystemLoader, Environment
from premailer import transform
from flock import cfg

templates_env = Environment(loader=FileSystemLoader(cfg['template_dir']))
generic_email_template = templates_env.get_template('email.html')

def plain_text_to_html(content):
    import re
    # Replace what seems like an url with hyperlink
    output = re.sub(r'(https?://[^ \n$]+)', r'<a href="\1">\1</a>', unicode(content))
    # Replace two newline characters with paragraph boundry
    output = '<p>%s</p>' % output.replace('\n\n', '</p><p>')
    # Replace single newline with break-rule
    output = output.replace('\n', '<br/>')
    return output

default_sender = "Flock Notifications <notifications@tryflock.com>"

class Mailer():
    auth = ("api", "key-97da181732b95a21257c270bd2215529")
    # TODO - use non dev server
    server = "https://api.mailgun.net/v3/sandboxd4ff99d2df0b4dbbb94cc9e08a0391d1.mailgun.org/messages"

    def send(self, recipient, subject, title, content, button_link=None, button_caption=None, sender=default_sender):

        # TODO - remove this
        recipient = 'ianluddy@gmail.com'
        sender = 'ellemarybrown@gmail.com'

        data = {
            "from": sender,
            "to": recipient,
            "subject": subject,
            "html": transform(generic_email_template.render(
                body=plain_text_to_html(content),
                title=title,
                button_caption=button_caption,
                button_link=button_link
            )),
            "text": ""
        }
        requests.post(
            self.server,
            auth=self.auth,
            data=data
        )

    def reset(self, recipient, new_password):

        subject = "Your Password has been reset"
        title = "Your Password was reset!"
        content = "Your Password has been reset.\nYour new Password is <b>{}</b>\n\nFollow this link to login with your new password".format(new_password)
        button_link = 'http://app.tryflock.com/login'
        button_caption = 'Login to Flock'

        self.send(recipient, subject, title, content, button_link=button_link, button_caption=button_caption)

    def invite(self, recipient, sender, token):

        subject = "{} has invited you to use Flock".format(sender)
        title = "Come check out the Flock App!"
        content = "<b>{}</b> has invited you to use Flock.\nClick the button below to log in.".format(sender)
        button_link = "http://app.tryflock.com/activate/{}".format(token)
        button_caption = "Login to Flock"

        self.send(recipient, subject, title, content, sender=sender, button_link=button_link, button_caption=button_caption)
