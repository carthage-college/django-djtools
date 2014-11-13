from django.forms import forms
from django.conf import settings
from django.db.models import FileField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

import magic
import os

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
        Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file
        size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    e.g.
        letter_interest = models.ContentTypeRestrictedFileField(
            "Letter of interest",
            upload_to="files/high-altitude-balloon-launch/letter-interest/",
            content_types=['application/pdf'],max_upload_size=5242880,
            help_text="PDF format"
        )

    """

    def __init__(self, *args, **kwargs):
        # get first, then pop, since the Django FileField class will
        # complain about unknown keys passed to it.
        if kwargs.get("content_types"):
            self.content_types = kwargs.pop("content_types")
        if kwargs.get("max_upload_size"):
            self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField,self).clean(*args,**kwargs)
        try:
            content_type = magic.from_buffer(data.read(), mime=True)
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        _(
                            '''
                                Please keep filesize under %s. Current size: %s
                            ''') % (
                                filesizeformat(self.max_upload_size),
                                filesizeformat(file._size)
                            )
                        )
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass

        return data
