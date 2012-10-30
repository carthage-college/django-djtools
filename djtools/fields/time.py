from django.db import models
from django.utils.text import capfirst
from django import forms
from django.forms import ValidationError

import datetime
import re

class KungfuTimeField(forms.Field):
    """
    Extension to Django's time fields that parses a much larger range of times
    without explicitly needing to specify all the time formats yourself.
    """

    # Matches any string with a 24-hourish format (sans AM/PM) but puts no
    # limits on the size of the numbers (e.g. 64:99 is OK.)
    _24_HOUR_PATTERN_STRING = r'^\s*(?P<hour>\d\d?)\s*:?\s*(?P<minute>\d\d)?\s*'

    # Matches any string with a 12-hourish format (with AM/PM) but puts no
    # limits on the size of the numbers (e.g. 64:99pm is OK.)
    _TIME_PATTERN_STRING = _24_HOUR_PATTERN_STRING + \
        r'((?P<ampm>[AaPp])\s*\.?\s*[Mm]?\s*\.?\s*)?$'

    # Matcher for our time pattern.
    _TIME_PATTERN = re.compile(_TIME_PATTERN_STRING)

    # Validation error messages.
    _ERROR_MESSAGES = {
        'invalid' : u'Enter a valid time.',
    }

    def __init__(self, *args, **kwargs):
        """
        Create a new KungFuTimeField with the mojo of a thousand TimeFields.
        """
        super(KungfuTimeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Parses datetime from the given value. If it can't figure it out, throws
        a ValidationError.
        """
        super(KungfuTimeField, self).clean(value)
        if not value:
            return None
        if isinstance(value, datetime.time):
            return value
        cleaned = self._parse_time(value)
        return cleaned

    def _parse_time(self, value):
        """
        Tries to recognize a time using our hefty regexp. If it doesn't match
        the regexp, throws a validation error. If it DOES match but the
        resulting numbers are out of range (e.g. an hour of 99), will also
        throw a ValidationError.
        """
        match = self._TIME_PATTERN.match(value)
        if not match:
            raise ValidationError(self._ERROR_MESSAGES['invalid'])

        # Hour has to be there because it's required in the regexp. Set the
        # minute to 0 for now. We dunno if there's AM/PM or not.
        (hour, minute, ampm) = (int(match.group('hour')), 0, match.group('ampm'))

        # Let's see if the user typed a minute.
        try:
            # Raises TypeError if group fetch returns None.
            minute = int(match.group('minute'))
        except TypeError:
            pass  

        if ampm:
            hour = self._handle_twelve_hour_time(hour, minute, ampm)

        # If the numbers are out of range, we'll find out here.
        try:
            return datetime.time(hour, minute)
        except ValueError:
            raise ValidationError(self._ERROR_MESSAGES['invalid'])

        # I don't expect any other problems, but if there are, they'll
        # propagate.

    def _handle_twelve_hour_time(self, hour, minute, ampm):
        """
        Detect 24 hour time with an am/pm (e.g. 18:30pm, 0:30am) and do the
        necessary transform for converting pm times to 24 hour times.
        """
        if hour < 1 or hour > 12:
            raise ValidationError(self._ERROR_MESSAGES['invalid'])
        elif ampm.lower() == "a" and hour == 12:
            return 0
        elif ampm.lower() == "p" and 1 <= hour and hour <= 11:
            return hour + 12
        else:
            return hour
