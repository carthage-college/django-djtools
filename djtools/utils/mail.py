from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import RequestContext, Context
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.core.mail import EmailMessage

import django


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
    request, recipients, subject, femail, template, data, bcc=None,
    content='html', attach=False
):

    if not bcc:
        bcc = [settings.MANAGERS[0][1],]

    t = loader.get_template(template)
    # VERSION returns (1, x, x, u'final', 1)
    # hopefully, we will be done using django 1.6 by the time 2.x comes out
    if django.VERSION[1] > 6:
        if request:
            rendered = t.render({'data':data,}, request)
        else:
            rendered = t.render({'data':data,},)
    else:
        if request:
            c = RequestContext(request, {'data':data,})
        else:
            c = Context({'data':data,})
        rendered = t.render(c)

    headers = {'Reply-To': femail,'From': femail,}

    email = EmailMessage(
        subject, rendered, femail, recipients, bcc, headers=headers
    )

    email.encoding = 'utf-8'

    if content:
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
        except:
            count += 1
            if count < 5:
                pass
            else:
                break

    return status
