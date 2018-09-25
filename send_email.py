import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


def send_mail(touser, subject, content):

    msg = MIMEMultipart()

    msg['From'] = 'scheduler.communication@gmail.com'
    msg['To'] = touser
    msg['Subject'] = subject

    msg.attach(MIMEText(content, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(msg['From'], config.EMAIL)

    server.sendmail(
        msg['From'],
        touser,
        msg.as_string()
    )

    server.quit()