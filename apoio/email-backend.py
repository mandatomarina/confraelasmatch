"""SMTP email backend class."""
import smtplib
import ssl
import threading

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SimpleMailBackend(BaseEmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None,
                use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                ssl_keyfile=None, ssl_certfile=None,
                **kwargs):
        super().__init__(fail_silently=fail_silently)

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0
        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        return num_sent

    def _send(self, email_message):
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = ','.join(email_message.recipients())

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = email_message.subject
        msg.attach(email_message.body)
    
        if settings.EMAIL_METHOD == 'SMTP':
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(sender_email, receiver_email, email_message.message())
        elif settings.EMAIL_METHOD == 'LOCAL':
            print(email_message.message())