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
