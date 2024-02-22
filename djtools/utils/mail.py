from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.core.mail import EmailMessage

import logging


def validateEmail(email):
    '''
    simple function to verify an email with django's validate_email validator
    '''
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def send_mail(
    request,
    recipients,
    subject,
    femail,
    template,
    data,
    reply_to=None,
    bcc=None,
    content='html',
    attach=False,
):
    """Send an email through django EmailMessage class."""
    if not bcc:
        bcc = [settings.MANAGERS[0][1]]

    t = loader.get_template(template)
    if request:
        rendered = t.render({'data':data,}, request)
    else:
        rendered = t.render({'data':data,},)

    if not reply_to:
        reply_to = femail

    email = EmailMessage(
        subject,
        rendered,
        femail,
        recipients,
        bcc,
        reply_to=reply_to,
    )

    email.encoding = 'utf-8'
    email.content_subtype = content

    if attach:
        try:
            email.attach_file(attach)
        except:
            for field, value in request.FILES.items():
                email.attach(value.name, value.read(), value.content_type)

    status = False
    # try 5 times then quit
    count = 0
    while True:
        try:
            email.send(fail_silently=False)
            status = True
            break
        except Exception as error:
            try:
                logger = logging.getLogger('debug_logfile')
                logger.debug(error)
            except:
                pass
            count += 1
            if count < 5:
                pass
            else:
                break
    return status
