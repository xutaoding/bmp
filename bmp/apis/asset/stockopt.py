# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt


class StockoptApi(BaseApi):
    route = [
        "/asset/stockopt",
        "/asset/stockopt/<int:id>",
        "/asset/stockopt/<string:type>/<int:id>",
        "/asset/stockopt/<string:type>/<int:page>/<int:pre_page>",
        "/asset/stockopt/<int:page>/<int:pre_page>"
    ]

    def get(self, type, page=0, pre_page=None, id=0):
        if id: return self.succ(StockOpt.get(id,_filters={"type":type}))
        return self.succ(StockOpt.select(page, pre_page,
                                         _filters=[StockOpt.type==type],
                                         _orders=[StockOpt.time.desc(),StockOpt.update_time.desc()]))

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
