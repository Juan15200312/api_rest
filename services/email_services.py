from django.conf import settings
from django.template.loader import render_to_string
from mailersend import MailerSendClient, EmailBuilder


def send_email(template_name, context, to_email, subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    from_name = settings.DEFAULT_FROM_NAME
    ms = MailerSendClient(api_key=settings.MAILERSEND_API_KEY)

    msg = (EmailBuilder()
           .from_email(from_email, from_name)
           .to_many([{"email": to_email}])
           .template(template_name)
           .personalize_many([{"email": to_email,"data": context}])
           .subject(subject)
           .build())

    return ms.emails.send(msg)
