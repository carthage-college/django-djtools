from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import RequestContext, Context
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.core.mail import EmailMessage


def validateEmail(email):
    '''
    simple function to verify an email with django's validate_email validator
    '''
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def send_mail(request, recipients, subject, femail, template, data, bcc=None, content="html", attach=False):
    if not bcc:
        bcc = settings.MANAGERS
    t = loader.get_template(template)
    if request:
        c = RequestContext(request, {'data':data,})
    else:
        c = Context({'data':data,})
    headers = {'Reply-To': femail,'From': femail,}
    email = EmailMessage(
        subject, t.render(c), femail, recipients, bcc, headers=headers
    )
    email.encoding = "utf-8"
    if content:
        email.content_subtype = content
    if attach:
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
        except:
            count += 1
            if count < 5:
                pass
            else:
                break

    return status

