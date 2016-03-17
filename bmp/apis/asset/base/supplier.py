# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import Supplier
from flask import session
from bmp.const import USER_SESSION
from datetime import datetime

class SupplierApi(BaseApi):
    route = ["/supplier", "/supplier/<int:id>"]

    def get(self, id=0):
        if id: return self.succ(Supplier.get(id))
        return self.succ(Supplier.select(_orders=Supplier.id.desc()))

    def post(self):
        submit = self.request()

        submit["connector"] = session[USER_SESSION]["uid"]
        if not submit.__contains__("path"): submit["path"] = ""
        submit["create_time"]=datetime.now()
        submit["last_time"]=datetime.now()
        Supplier.add(submit)
        return self.succ()

    def delete(self, id):
        Supplier.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        Supplier.edit(id, submit)
        return self.succ()


if __name__ == "__main__":
    pass
