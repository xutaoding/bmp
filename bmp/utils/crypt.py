import random

import rsa
from bmp.const import KEY_SESSION
from flask import session


def desc(cipher):
    pkey = session[KEY_SESSION]
    prikey = rsa.PrivateKey(pkey["n"], pkey["e"], pkey["d"], pkey["p"], pkey["q"])
    return rsa.decrypt(bytearray.fromhex(cipher), prikey)


def randpass():
    return "".join([random.choice("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789") for i in range(8)])
