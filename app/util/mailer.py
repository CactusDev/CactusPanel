
import smtplib
from email.mime.text import MIMEText
from ..instance import config


def send_mail(priority, reason, details, username, contact):
    body = """\n
        Contact: %s
        Priority: %s
        Username: %s

        Reason: %s

        Details: %s
    """

    msg = MIMEText(body % tuple([
        str(contact), str(priority), str(username), str(reason), str(details)]))

    msg['Subject'] = str(priority) + " .:. " + str(reason) + " .:. " + str(username)
    msg['From'] = config.MAIL_USERNAME
    msg['To'] = ", ".join(config.RECIPIENTS)

    session = smtplib.SMTP(config.SMTP_SERVER)
    session.starttls()
    session.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
    session.sendmail(config.MAIL_USERNAME, config.RECIPIENTS, msg.as_string())
    session.quit()
