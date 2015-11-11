# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.utils import user_ldap
from bmp.models.ref import Ref


class RefsApi(BaseApi):
    route = ["/refs", "/refs/<string:type>"]

    def get(self, type="%"):
        return self.succ(Ref.select(type))
