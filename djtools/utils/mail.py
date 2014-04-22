from django.conf import settings
from django.template import RequestContext, Context
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.core.mail import EmailMessage

def send_mail(request, recipients, subject, femail, template, data, bcc=None, content="html"):
    if not bcc:
        bcc = settings.MANAGERS
    t = loader.get_template(template)
    if request:
        c = RequestContext(request, {'data':data,})
    else:
        c = Context({'data':data,})
    headers = {'Reply-To': femail,'From': femail,}
    email = EmailMessage(subject, t.render(c), femail, recipients, bcc, headers=headers)
    email.encoding = "utf-8"
    if content:
        email.content_subtype = content
    fail = settings.EMAIL_FAIL_SILENTLY
    if settings.DEBUG:
        fail = False
    #email.send(fail_silently=fail)
    email.send(fail_silently=True)

