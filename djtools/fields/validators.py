from django.core.validators import *
from django.core.exceptions import ValidationError

import magic

class MimetypeValidator(object):
    def __init__(self, mimetypes):
        self.mimetypes = mimetypes

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(1024), mime=True)
            if not mime in self.mimetypes:
                raise ValidationError('%s is not an acceptable file type' % value)
        except AttributeError as e:
            raise ValidationError('This value could not be validated for file type' % value)


credit_gpa_validator = RegexValidator(
    regex='^[0-9]{1,}\.[0-9]{1,2}$',
    message='Valid inputs are: eg. 4.00 or 132.5',
    code='invalid_gpa_or_credit'
)

month_year_validator = RegexValidator(
    regex='^(0[1-9]{1}|1[0-2]{1})\/2[\d]{3}$',
    message='Valid inputs are: eg. MM/YYYY',
    code='invalid_month_year'
)

four_digit_year_validator = RegexValidator(
    regex='^2[\d]{3}$',
    message='Valid inputs are: eg. 2015',
    code='invalid_four_digit_year'
)
