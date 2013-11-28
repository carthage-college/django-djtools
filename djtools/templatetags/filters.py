from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from djtools.utils.encryption import do_crypt

import urllib2, os.path, base64

register = template.Library()

@register.filter()
@template.defaultfilters.stringfilter
def encrypt(value):
    try:
        encoded = do_crypt(value, "encrypt").replace("/","\/")
    except:
        encoded = ''
    return encoded
