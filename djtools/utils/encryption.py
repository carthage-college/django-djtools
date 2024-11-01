import base64
import logging
import traceback

from cryptography.fernet import Fernet
from django.conf import settings


def encrypt(txt):
    try:
        txt = str(txt)
        # key should be byte
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        # input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode('ascii')
        #encrypted_text = base64.b32encode(encrypted_text).decode('ascii')
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logfile").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        #txt = base64.b32decode(txt)
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode('ascii')
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
