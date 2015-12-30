# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import Supplier


class SupplierApi(BaseApi):
    route = ["/supplier", "/supplier/<int:id>"]

    def get(self, id=0):
        if id:
            return self.succ(Supplier.get(id))
        return self.succ(Supplier.history())

    def post(self):
        submit = self.request()
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
