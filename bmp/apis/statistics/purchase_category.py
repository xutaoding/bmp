# coding=utf-8
import json

import pandas as pd

from bmp.apis.base import BaseApi
from bmp.models.purchase import PurchaseGoods


class Purchase_categoryApi(BaseApi):
    route = ["/stats/purchase/category/<string:begin_time>/<string:end_time>"]

    def get(self, begin_time, end_time):
        goods = pd.read_json(
            json.dumps(PurchaseGoods.between(begin_time,end_time)))

        if goods.empty:
            return self.succ([])

        total=(goods.price*goods.amount).sum()

        def func(x):
            x["name"]=x.category["name"]
            x["rate"]=float(x.price*x.amount)/total*100
            return x

        goods=goods.apply(func,axis=1).loc[:,["name","rate"]]
        goods=goods.groupby("name").sum()

        return self.succ([
            {"category":name,"rate":"%f"%goods.loc[name]}
            for name in goods.index
        ])



if __name__ == "__main__":
    for pg in PurchaseGoods.between("1990-01-01","2017-01-01"):
        print(pg["category"]["name"])
        print(pg)





