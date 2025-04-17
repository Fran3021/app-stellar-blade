import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class SendGridEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent_count = 0
        sg = SendGridAPIClient(api_key=env("SENDGRID_API_KEY"))

        for message in email_messages:
            from_email = message.from_email or settings.DEFAULT_FROM_EMAIL
            content = message.body
            to_emails = message.to

            mail = Mail(
                from_email=from_email,
                to_emails=to_emails,
                subject=message.subject,
                plain_text_content=content,
            )

            try:
                sg.send(mail)
                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e

        return sent_count