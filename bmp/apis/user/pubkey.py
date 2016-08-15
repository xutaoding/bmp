# coding: utf-8

import rsa
from bmp.apis.base import BaseApi
from bmp.const import KEY_SESSION
from flask import session


class PubkeyApi(BaseApi):
    route = "/login/pubkey"

    def auth(self):
        return True

    def get(self):
        pub, pri = rsa.newkeys(1024)
        session[KEY_SESSION] = {
            "n": pri.n,
            "e": pri.e,
            "d": pri.d,
            "p": pri.p,
            "q": pri.q
        }
        return self.succ({
            "n": hex(pub.n)[2:-1],
            "e": hex(pub.e)[2:]
        })
