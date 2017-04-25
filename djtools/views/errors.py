from django.conf import settings
from django.template import loader, Context
from django.http import HttpResponseServerError, HttpResponseNotFound

import django


def server_error(request, template_name='500.html'):
    """
    500 error handler.    Templates: `500.html`
    Context:
        media_url
            Path of static media (e.g. "media.example.org")
    """

    t = loader.get_template(template_name)

    # VERSION returns (1, x, x, u'final', 1)
    # hopefully, we will be done using django 1.6 by the time 2.x comes out
    if django.VERSION[1] > 6:
        rendered = t.render(
            {'media_url': settings.MEDIA_URL,'layout':[0,1]}, request
        )
    else:
        rendered = t.render(Context({
            'media_url': settings.MEDIA_URL,'layout':[0,1],
        }))

    return HttpResponseNotFound(rendered)


def four_oh_four_error(request, template_name='404.html'):
    """
    404 error handler.

    Templates: `404.html`
    Context:
        media_url
            Path of static media (e.g. "media.example.org")
    """

    t = loader.get_template(template_name)

    # VERSION returns (1, x, x, u'final', 1)
    # hopefully, we will be done using django 1.6 by the time 2.x comes out
    if django.VERSION[1] > 6:
        rendered = t.render(
            {'media_url': settings.MEDIA_URL,'layout':[0,1]}, request
        )
    else:
        rendered = t.render(Context({
            'media_url': settings.MEDIA_URL,'layout':[0,1],
        }))

    return HttpResponseNotFound(rendered)
