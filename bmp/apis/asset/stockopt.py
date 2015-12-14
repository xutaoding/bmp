# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt
from flask import session
from bmp.const import USER_SESSION

class StockoptApi(BaseApi):
    route = [
        "/asset/stockopt",
        "/asset/stockopt/<int:id>",
        "/asset/stockopt/<string:type>/<int:id>",
        "/asset/stockopt/<string:type>/<int:page>/<int:pre_page>",
        "/asset/stockopt/<int:page>/<int:pre_page>"
    ]

    def get(self, type, page=0, pre_page=None, id=0):
        if id: return self.succ(StockOpt.get(type, id))
        return self.succ(StockOpt.select(type, page, pre_page))

    def post(self):
        submit = self.request()
        StockOpt.add(submit)
        return self.succ()

    def delete(self, id):
        StockOpt.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        submit["id"] = id
        StockOpt.edit(submit)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(StockOpt.search(submit, page, pre_page))

if __name__ == "__main__":
    pass
