from django import template
from django.conf import settings
from django.core.cache import cache

import json

# python 2.7/3.6 compatibility
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

register = template.Library()


class GetContent(template.Node):

    def __init__(self, bits):
        self.varname = bits[2]
        self.ctype=bits[3]
        self.cid=bits[4]

    def __repr__(self):
        return '<LiveWhaleContent>'

    def render(self, context):
        key = 'livewhale_{}_{}'.format(self.ctype,self.cid)
        if cache.get(key):
            content = cache.get(key)
        else:
            earl = '{}/live/{}/{}@JSON'.format(
                settings.LIVEWHALE_API_URL,self.ctype,self.cid
            )
            try:
                response =  urlopen(earl)
                data = response.read()
                content = json.loads(data)
                cache.set(key, content)
            except:
                content = ''

        context[self.varname] = content
        return ''


class DoGetLiveWhaleContent:
    """
    {% get_lw_content as variable_name content_type field ID %}
    """

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) < 4:
            raise template.TemplateSyntaxError("'{}' tag takes four arguments".format(bits[0]))
        if bits[1] != 'as':
            raise template.TemplateSyntaxError("First argument to '{}' tag must be 'as'".format(bits[0]))
        return GetContent(bits)

register.tag('get_lw_content', DoGetLiveWhaleContent('get_lw_content'))
