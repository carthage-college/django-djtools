from django import template
from django.conf import settings
from django.core.cache import cache

import json, sys

# python 2.7/3.6 compatibility
try:
    import urllib2 as urllib
except ImportError:
    import urllib


register = template.Library()

class GetProf(template.Node):

    def __init__(self, bits):
        self.varname = bits[2]
        # ldap username
        self.uname=bits[3]

    def __repr__(self):
        return '<Profile>'

    def render(self, context):
        try:
          #uname = template.resolve_variable(self.uname, context).split('@')[0]
          uname = template.Variable(self.uname).resolve(context).split('@')[0]
        except:
          return ''
        key = 'livewhale_get_prof_{}'.format(uname).replace(" ", "")
        if cache.get(key):
            prof = cache.get(key)
        else:
            root = 'https://www.carthage.edu'
            prof = None
            earl = '{}/live/json/profiles/search/{}/'.format(root,uname)
            try:
                response =  urllib.urlopen(earl)
                data = json.loads(response.read())
            except:
                data = ''
            if len(data) > 0:
                email = '{}@carthage.edu'.format(uname)
                for p in data:
                    if p.get('profiles_37').strip() == email \
                    or p.get('profiles_45').strip() == email \
                    or p.get('profiles_149').strip() == email \
                    or p.get('profiles_80').strip() == email:
                        earl = '{}/live/profiles/{}@JSON'.format(root,p['id'])
                        response =  urllib.urlopen(earl)
                        p = json.loads(response.read())
                        if p.get('parent'):
                            earl = '{}/live/profiles/{}@JSON'.format(
                                root,p['parent']
                            )
                            response =  urllib.urlopen(earl)
                            p = json.loads(response.read())
                        if p.get('thumb'):
                            listz = p['thumb'].split('/')
                            listz[8] = '145'
                            listz[0] = 'https:'
                            new_listz = listz[0:9]
                            new_listz.append(listz[-1])
                            p['thumbnail'] = '/'.join(new_listz)
                        prof = p
                        cache.set(key, prof)

        context[self.varname] = prof
        return ''

class DoGetProf:
    """
    {% get_prof as variable_name ldap_user %}
    """

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) < 3:
            raise template.TemplateSyntaxError("'{}' tag takes two arguments".format(bits[0]))
        if bits[1] != "as":
            raise template.TemplateSyntaxError("First argument to '{}' tag must be 'as'".format(bits[0]))
        return GetProf(bits)

register.tag('get_prof', DoGetProf('get_prof'))
