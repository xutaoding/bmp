# coding: utf-8
from datetime import timedelta

from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Stock
from bmp.tasks.alert import Alert


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
        stock = Stock.add(submit, auto_commit=False)
        Alert().add("库存", stock, stock.warranty_time, timedelta(days=30))

        db.session.commit()
        return self.succ()

    def delete(self, sid):
        stock = Stock.delete(sid, auto_commit=False)
        Alert().delete(stock, [timedelta(30), timedelta(60)])

        db.session.commit()
        return self.succ()

    def put(self, sid):
        submit = self.request()
        submit["id"] = sid
        stock = Stock.edit(submit, auto_commit=False)
        Alert().add("库存", stock, stock.warranty_time, timedelta(days=30))

        db.session.commit()
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Stock.search(submit, page, pre_page))
