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
            root = "https://www.carthage.edu"
            prof = None
            user = get_novell_username(email)
            earl = "%s/live/json/profiles/search/%s/" % (root,user)
            try:
                response =  urllib2.urlopen(earl)
                data = json.loads(response.read())
            except:
                data = ""
            if len(data) > 0:
                for p in data:
                    if p.get("profiles_37") or p.get("profiles_45") \
                    or p.get("profiles_149") or p.get("profiles_80"):
                        earl = "%s/live/profiles/%s@JSON" % (root,p["id"])
                        response =  urllib2.urlopen(earl)
                        p = json.loads(response.read())
                        if p.get("parent"):
                            earl = "%s/live/profiles/%s@JSON" % (root,p["parent"])
                            response =  urllib2.urlopen(earl)
                            p = json.loads(response.read())
                        if p.get("thumb"):
                            listz = p["thumb"].split('/')
                            listz[8] = '145'
                            listz[0] = 'https:'
                            new_listz = listz[0:9]
                            new_listz.append(listz[-1])
                            p["thumbnail"] = '/'.join(new_listz)
                        prof = p
                        cache.set(key, prof)

        context[self.varname] = prof
        return ''

class DoGetProf:
    """
    {% get_prof as variable_name email_address [or] username %}
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
