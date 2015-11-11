# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt


class StockoptApi(BaseApi):
    route = ["/asset/stockopt", "/asset/stockopt/<int:id>", "/asset/stockopt/<string:type>/<int:id>",
             "/asset/stockopt/<string:type>/<int:page>/<int:pre_page>"]

    def auth(self):
        return True

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


if __name__ == "__main__":
    from bmp.utils.post import test

    # 固定资产编号	名称	规格	借用人	借用时间	备注	状态
    test(
        "post",
        "http://localhost:5000/apis/v1.0/asset/stockopt",
        {
            "type": "领用1",
            "uid": "mingming.zhang",  # 领用人
            "time": "2000-01-01 00:00",  # 对应type的时间
            "reson": "理由，故障，报废原因",
            "remark": "备注",
            "status": "状态",
            "stock_id": "2",  # 库存的id
        }
    )

    test(
        "put",
        "http://localhost:5000/apis/v1.0/asset/stockopt/1",
        {
            "id": "1",
            "type": "领用1",
            "uid": "mingming.zhang",  # 领用人
            "time": "2000-01-01 00:00",  # 对应type的时间
            "reson": "理由，故障，报废原因",
            "remark": "备注",
            "status": "状态",
            "stock_id": "2",  # 库存的id
        }, True
    )

    test(
        "delete",
        "http://localhost:5000/apis/v1.0/asset/stockopt/2",
        {}
    )
