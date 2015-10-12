#coding: utf-8
from bmp.apis.base import BaseApi
from bmp.utils import user_ldap
from bmp.models.ref import Ref

class RefsApi(BaseApi):
    route="/refs/<string:type>"
    def get(self,type):
        refs=Ref.query.filter(Ref.type==type).all()
        if refs:
            return self.succ([ref.to_dict() for ref in refs])
        return self.succ()