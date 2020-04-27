import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def send_mail(subject, text, sender_email, receiver_email, fail_silently=True):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ','.join(receiver_email)
    msg['Subject'] = subject
    if settings.EMAIL_METHOD == 'SMTP':
        msg.attach(MIMEText(text, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            if not fail_silently:
                server.set_debuglevel(1)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    elif settings.EMAIL_METHOD == 'LOCAL':
        print(msg)