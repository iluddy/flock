import requests
from jinja2 import FileSystemLoader, Environment
from premailer import transform
from flock.constants import MAIL_AUTH, MAIL_SENDER, MAIL_SERVER
from flock.utils import plain_text_to_html
from flock.app import celery, cfg

@celery.task
def send(recipient, subject, title, content, button_link, button_caption):
    email_template = Environment(loader=FileSystemLoader(cfg['template_dir'])).get_template('email.html')

    html = transform(email_template.render(
        body=plain_text_to_html(content),
        title=title,
        button_caption=button_caption,
        button_link=button_link
    ))

    # TODO - remove this
    recipient = 'ianluddy@gmail.com'
    sender = MAIL_SENDER

    data = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "html": html,
        "text": ""
    }

    requests.post(
        MAIL_SERVER,
        auth=MAIL_AUTH,
        data=data
    )


def reset(recipient, new_password):
    subject = "Your Password has been reset"
    title = "Your Password was reset!"
    content = u"Your Password has been reset.\nYour new Password is <b>{}</b>\n\nFollow this link to login with your new password".format(
        new_password)
    button_link = 'http://app.tryflock.com/login'
    button_caption = 'Login to Flock'

    send.delay(recipient, subject, title, content, button_link, button_caption)


def invite(recipient, sender, token):
    subject = u"{} has invited you to use Flock".format(sender)
    title = "Come check out the Flock App!"
    content = u"<b>{}</b> has invited you to use Flock.\nClick the button below to log in.".format(sender)
    button_link = u"http://app.tryflock.com/activate/{}".format(token)
    button_caption = "Login to Flock"

    send.delay(recipient, subject, title, content, button_link, button_caption)
