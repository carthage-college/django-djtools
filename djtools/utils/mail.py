from django.conf import settings
from django.template import RequestContext
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage

def send_mail(request, recipients, subject, femail, template, data, bcc=None):
    if not bcc:
        bcc = settings.MANAGERS
    t = loader.get_template(template)
    c = RequestContext(request, {'data':data,})
    headers = {'Reply-To': femail,'From': femail,}
    email = EmailMessage(subject, t.render(c), femail, recipients, bcc, headers=headers)
    email.content_subtype = "html"
    email.send(fail_silently=True)

