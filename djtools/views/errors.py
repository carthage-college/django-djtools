from django.conf import settings
from django.template import loader
from django.http import HttpResponseServerError, HttpResponseNotFound


def server_error(request, template_name='500.html'):
    """
    500 error handler.
    Template: `500.html`
    """

    t = loader.get_template(template_name)
    rendered = t.render({'media_url': settings.MEDIA_URL,}, request)
    return HttpResponseServerError(rendered)


def four_oh_four_error(request, exception, template_name='404.html'):
    """
    404 error handler.
    Template: `404.html`
    """

    t = loader.get_template(template_name)
    rendered = t.render({'media_url': settings.MEDIA_URL,}, request)
    return HttpResponseNotFound(rendered)
