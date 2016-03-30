# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import Stock
from bmp.tasks.mail.asset.stock import Mail

#todo 短信报警
class StockApi(BaseApi):
    route = ["/asset/stock",
             "/asset/stock/<int:sid>",
             "/asset/stock/<int:page>/<int:pre_page>/<int:nan_opt>",
             "/asset/stock/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None, sid=0, nan_opt=False):
        if sid: return self.succ(Stock.get(sid))
        return self.succ(Stock.select(page, pre_page, nan_opt))

    def post(self):
        submit = self.request()
        stock = Stock.add(submit)
        Mail().to(stock)
        return self.succ()

    def delete(self, sid):
        Stock.delete(sid)
        return self.succ()

    def put(self, sid):
        submit = self.request()
        submit["id"] = sid
        Stock.edit(submit)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Stock.search(submit, page, pre_page))
