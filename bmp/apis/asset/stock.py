# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Stock


class StockApi(BaseApi):
    route = ["/asset/stock",
             "/asset/stock/<int:sid>",
             "/asset/stock/<int:page>/<int:pre_page>/<int:nan_opt>",
             "/asset/stock/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None,sid=0,nan_opt=False):
        if sid:
            return self.succ(Stock.get(sid))
        return self.succ(Stock.select(page, pre_page,nan_opt))

    def post(self):
        submit = self.request()
        Stock.add(submit)
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

if __name__ == "__main__":
    from bmp.utils.post import test

    test(
        "post",
        "http://localhost:5000/apis/v1.0/asset/stock",
        {
            # 固定资产编号	采购编号	名称	规格	入库类型	入库人	入库时间	过保日
            "no": "固定资产编号3",
            "category_id": "33",
            "spec": "规格1",
            "purchase_id": "44",  # 采购id
            "stock_in_type": "入库类型1",
            "stock_in_uid": "mingming.zhang",  # 入库人
            "stock_in_time": "2000-01-01 00:00",  # 入库时间
            "warranty_time": "2000-01-01 00:00",  # 过保日期
        }
    )

    test(
        "search",
        "http://localhost:5000/apis/v1.0/asset/stock",
        {
            "category_id": "33"
        }, True
    )
