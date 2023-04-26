# -*- coding: utf-8 -*-

import datetime
from django.conf import settings


def get_term(start_date=None):
    """Obtain the current academic term."""
    if not start_date:
        start_date = settings.START_DATE
    today = datetime.date.today()
    term = 'RA'
    year = today.year
    if ((today.month < start_date.month) or (today.month == 12 and today.day > 10)):
        term = 'RC'
        if today.month == 12:
            year = year + 1
    return {'yr': year, 'sess': term}



def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - (
        (today.month, today.day) < (born.month, born.day)
    )
