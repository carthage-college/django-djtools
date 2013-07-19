from django.conf import settings
from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError

import httplib

register = Library()

class ApiObjectNode(Node):
    def __init__(self, context_var, app, model, id, format):
        self.context_var = context_var
        self.app = app
        self.model = model
        self.id = id
        self.format = format

    def render(self, context):
        url = 'http://%s/%s/%s/%s/%s/' % (settings.API_URL, self.app, self.model, self.id, self.format)
        try:
            conn = httplib.HTTPConnection(settings.SERVER_URL)
            conn.request("GET", url)
            response = conn.getresponse()
            if response.status != 404:
                obj = response.read()
            else:
                obj = ""
        except:
            obj = ""
        context[self.context_var] = obj
        return ''

def do_api_object(parser, token):
    """
        {% get_api_object as [varname] [app] [model] [id] [format] %}
    """
    bits = token.contents.split()
    if len(bits) != 7:
        raise TemplateSyntaxError('%s tag requires exactly six arguments' % bits[0])
    if bits[1] != 'as':
        raise TemplateSyntaxError("first argument to %s tag must be 'as'" % bits[0])
    return ApiObjectNode(bits[2], bits[3], bits[4], bits[5], bits[6])

register.tag('get_api_object', do_api_object)
