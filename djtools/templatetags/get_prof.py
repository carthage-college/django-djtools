from django import template
from django.conf import settings
from django.core.cache import cache

from djtools.templatetags.filters import get_novell_username

import urllib2, json, sys

register = template.Library()

class GetProf(template.Node):

    def __init__(self, bits):
        self.varname = bits[2]
        self.email=bits[3]

    def __repr__(self):
        return "<Professor>"

    def render(self, context):
        email = template.resolve_variable(self.email, context)
        key = "livewhale_get_prof_%s" % email
        if cache.get(key):
            prof = cache.get(key)
        else:
            user = get_novell_username(email)
            earl = "http://www.carthage.edu/live/json/profiles/search/%s/" % user
            response =  urllib2.urlopen(earl)
            data = response.read()
            prof = json.loads(data)[0]
            cache.set(key, prof)

        context[self.varname] = prof
        return ''

class DoGetProf:
    """
    {% get_prof as variable_name email_address %}
    """

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) < 3:
            raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
        if bits[1] != "as":
            raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
        return GetProf(bits)

register.tag('get_prof', DoGetProf('get_prof'))
