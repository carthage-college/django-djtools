from django.conf import settings

from Crypto.Cipher import AES
from Crypto import Random

from base64 import b64encode, b64decode
from os import urandom
import hashlib


class AESCipher(object):
    """
    AES CBC and PKCS7 padding to byte align the secret message.

    Salt:
        randomizes the hash of the key; prevents rainbow table
        attacks against the key
    IV (initialization vector):
        randomizes the encrypted message;
        prevents rainbow table attacks against the message
    Derived Key:
        lengthens and strengthens the key via hashing; used instead of the
        original key; slows down brute-force attacks against the key
    """

    def __init__( self, key=None, bs=32 ):
        self.bs = bs
        if not key:
            key = settings.SECRET_KEY[:bs]
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt( self, raw ):
        raw = self._pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return b64encode( iv + cipher.encrypt( raw ) ).replace('/','_')

    def decrypt( self, enc ):
        enc = b64decode(enc.replace('_','/'))
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

