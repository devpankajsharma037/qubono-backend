from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os


def sendEmail(subject, template_name, context, to_email):
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        from_email = f'Qubono.com <{os.getenv("DEFAULT_FROM_EMAIL")}>'
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        print(email.send())
        return True
    except Exception as e:
        print(str(e))
        return False