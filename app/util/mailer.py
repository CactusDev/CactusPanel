
from flask.ext.mail import Message
from .. import mail


def send_mail(priority, reason, details):
    msg = Message(priority + " .:. " + reason)

    msg.body = details

    mail.send(msg)
