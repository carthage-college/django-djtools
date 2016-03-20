from uuid import uuid4
from os.path import join

def upload_to_path(self, filename):
    """
    Rename file to random string and generate path for a file field.
    Required: get_slug() method on the model
    """
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    path = "{}".format(
        self.get_slug()
    )
    return join(path, filename)


def handle_uploaded_file(f, path):
    """
    Rename file to random string, combine it with 'path'
    and write to new destination. Handy when not using
    a model class for your form.
    """
    # obtain the file extension
    ext = f.name.split(".")[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # combine it all together
    phile = join(path, filename)
    # and write
    with open(phile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename
