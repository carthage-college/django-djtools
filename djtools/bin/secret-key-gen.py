import os
import random
import string

SECRET_KEY = ''.join([random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(50)])

print SECRET_KEY
