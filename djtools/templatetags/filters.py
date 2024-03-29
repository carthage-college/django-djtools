from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from djtools.utils.date import calculate_age

from datetime import date

register = template.Library()


@register.filter
def keyvalue(dict, key):
    """
    takes a dictionary key and returns the value

    Usage: {{dictionary|keyvalue:key_variable}}
           {{dictionary|keyvalue:key_variable|keyvalue:another_key}}
    the latter is theoretical at this point for nested dictionaries.
    """
    try:
        return dict[key]
    except KeyError:
        return ''

@register.filter()
@template.defaultfilters.stringfilter
def format_phone(value):
    """
    takes a value with separated by dashes and returns it in the format:
    (415) 963-4949
    """
    phone = value.split("-")
    try:
        phone = "(%s) %s-%s" % (phone[0],phone[1],phone[2])
    except:
        if value:
            phone = "(%s) %s-%s" % (value[:3],value[3:6],value[6:10])
        else:
            phone = value
    return phone
format_phone.is_safe=True
format_phone.needs_autoescape = False

@register.filter()
@template.defaultfilters.stringfilter
def get_ldap_username(value):
    lname = value.split("@")
    try:
        lname = lname[0]
    except:
        lname = ''
    return lname

@register.filter()
@template.defaultfilters.stringfilter
def get_age(value):
    try:
        bday = value.split("-")
        age = calculate_age(date(int(bday[0]), int(bday[1]), int(bday[2])))
    except (ValueError, TypeError):
        age = 0
    return age

