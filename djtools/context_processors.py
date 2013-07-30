from django.conf import settings
from django.contrib.sites.models import Site

def sitevars(request):
    context = {}
    current_site = Site.objects.get_current()
    context['site_id'] = current_site.id
    context['site_name'] = current_site.name
    context['site_domain'] = current_site.domain
    context['media_root'] = settings.MEDIA_ROOT
    context['media_url'] = settings.MEDIA_URL
    context['server_url'] = settings.SERVER_URL
    context['root_url'] = settings.ROOT_URL
    context['login_url'] = settings.LOGIN_URL
    context['django_debug'] = settings.DEBUG
    context['template_debug'] = settings.TEMPLATE_DEBUG
    return context
