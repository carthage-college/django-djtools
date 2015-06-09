from django.template import Library, Node, Variable, \
    VariableDoesNotExist, TemplateSyntaxError

import time

register = Library()

def get_var(v, context):
    try:
        return v.resolve(context)
    except VariableDoesNotExist:
        return v.var

class MungeTime(Node):

    def __init__(self, t, old, new):
        self.t = Variable(t)
        self.old = Variable(old)
        self.new = Variable(new)

    def render(self, context):
        t = unicode(get_var(self.t, context))
        old = unicode(get_var(self.old, context))
        new = unicode(get_var(self.new, context))
        try:
            t = time.strptime(t, old)
            tyme = time.strftime(new, t)
        except:
            tyme = None
        return tyme

@register.tag
def string_time(parser, token):
    """
    converts a string to time.
    accepts:
        old format e.g. "%H%M"
        new format e.g. "%I:%M %p"
    """
    args = token.split_contents()[1:]
    if len(args) != 3:
        raise TemplateSyntaxError, '%r tag requires a string, time format of string, and the new format.' % token.contents.split()[0]
    return MungeTime(*args)
