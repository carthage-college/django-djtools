# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from os import remove

import errno


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

