# -*- coding: utf-8 -*-
from uuid import uuid4
from os import path
from os import makedirs

import errno


def upload_to_path(self, filename):
    """
    Rename file to random string and generate path for a file field.
    Required: get_slug() method on the model
    """
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    sendero = "{}".format(
        self.get_slug()
    )
    return path.join(sendero, filename)


def handle_uploaded_file(f, sendero, filename=None):
    """
    Rename file to random string, combine it with 'sendero'
    and write to new destination. Handy when not using
    a model class for your form.
    """
    # obtain the file extension
    ext = f.name.split(".")[-1]
    if not filename:
        # set filename as random string
        filename = uuid4().hex
    filename = u'{}.{}'.format(filename, ext)
    # combine it all together
    phile = path.join(sendero, filename)
    # create directory if not already exists
    if not path.exists(path.dirname(phile)):
        try:
            makedirs(path.dirname(phile))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    # and write
    with open(phile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # tell whomever called if upload worked or not
    if path.isfile(phile):
        return filename
    else:
        return None
