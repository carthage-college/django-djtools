# -*- coding: utf-8 -*-

import django
import os
import sys

django.setup()

from django.conf import settings
from djtools.utils.mail import send_mail


def main():
    """test sendmail with gmail API"""
    frum = settings.PERMIT_EMAIL
    print(frum)
    send_mail(
        None,
        [settings.MANAGERS[0][1]],
        '[DJ Parking] email test',
        frum,
        'email_test.html',
        {'test': 'boo!'},
        reply_to=[frum,],
    )


if __name__ == '__main__':
    sys.exit(main())
