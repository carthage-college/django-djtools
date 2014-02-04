from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_unicode
from django import template
#from django.utils.encoding import smart_text

# translation mapping table that converts
# single smart quote characters to standard
# single quotes
SINGLE_QUOTE_MAP = {
    0x2018: 39,
    0x2019: 39,
    0x201A: 39,
    0x201B: 39,
    0x2039: 39,
    0x203A: 39,
    0xc3: 39,
}

# translation mapping table that converts
# double smart quote characters to standard
# double quotes
DOUBLE_QUOTE_MAP = {
    0x00AB: 34,
    0x00BB: 34,
    0x201C: 34,
    0x201D: 34,
    0x201E: 34,
    0x201F: 34,
}

register = template.Library()

@register.filter(name = 'smart_quotes')
@stringfilter
def convert_smart_quotes(str):
    """
    Convert "smart quotes" from Microsoft products
    to standard quotes.
    """
    #return smart_unicode(str, encoding='ISO-8859-1').translate(DOUBLE_QUOTE_MAP).translate(SINGLE_QUOTE_MAP)
    #return str.translate(DOUBLE_QUOTE_MAP).translate(SINGLE_QUOTE_MAP)
    #return smart_unicode(str, encoding='ISO-8859-1')
    return smart_unicode(str, encoding='utf-8')
    #return str.encode('raw-unicode-escape')

