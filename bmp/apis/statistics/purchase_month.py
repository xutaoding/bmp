# coding=utf-8
import json

import pandas as pd

from bmp.apis.base import BaseApi
from bmp.models.purchase import PurchaseGoods


class Purchase_monthApi(BaseApi):
    route = ["/stats/purchase/month/<string:begin_time>/<string:end_time>"]

    def get(self, begin_time, end_time):
        goods = pd.read_json(
            json.dumps(PurchaseGoods.between(begin_time, end_time)))

        if goods.empty:
            return self.succ([])


        goods = goods.set_index("apply_time")
        goods = goods.price * goods.amount
        goods = goods.resample("m", how=sum)

        return self.succ(
            [{"time":time.strftime("%Y-%m"),"expend": "%f"%goods.loc[time]} for time in goods.index])


if __name__ == "__main__":
    pass
