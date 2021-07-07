# -*- coding: utf-8 -*-

from django.conf import settings
from Crypto.Cipher import AES

import base64


def do_crypt(cid, way):
    """
    helper method to encrypt or decrypt a string
    """
    # the block size for the cipher object;
    # must be 16, 24, or 32 for AES
    BLOCK_SIZE = 16
    # character used for padding--with a block cipher such as AES,
    # the value you encrypt must be a multiple of BLOCK_SIZE in
    # length.  This character is used to ensure that your value is
    # always a multiple of BLOCK_SIZE
    PADDING = b'{'
    # one-liner to sufficiently pad the text to be encrypted
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

    # create a cipher object using the first 16 characters
    # of Django secret_key value from settings
    cipher = AES.new(settings.SECRET_KEY[:16].encode('utf-8'), AES.MODE_ECB)
    if way == "encrypt":
        # encode a string
        cid = EncodeAES(cipher, str(cid).encode('utf-8'))
    else:
        # decode the encoded string
        cid = DecodeAES(cipher, cid)
    return cid.decode('utf-8')
