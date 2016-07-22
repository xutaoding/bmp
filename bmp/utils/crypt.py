

def desc(cipher):
    pkey = session[KEY_SESSION]
    prikey = rsa.PrivateKey(pkey["n"], pkey["e"], pkey["d"], pkey["p"], pkey["q"])
    uid = rsa.decrypt(bytearray.fromhex(uid), prikey)
    pwd = rsa.decrypt(bytearray.fromhex(pwd), prikey)