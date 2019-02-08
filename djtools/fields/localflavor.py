from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.encoding import smart_text
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

import re


class USPhoneNumberField(CharField):
    """
    A form field that validates input as a U.S. phone number.
    """
    phone_digits_re = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')
    default_error_messages = {
        'invalid': _('Phone numbers must be in XXX-XXX-XXXX format.'),
    }

    def clean(self, value):
        super(USPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        value = re.sub('(\(|\)|\s+)', '', smart_text(value))
        m = phone_digits_re.search(value)
        if m:
            return '%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        raise ValidationError(self.error_messages['invalid'])
