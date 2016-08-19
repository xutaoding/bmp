# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Fund


class FundApi(BaseApi):
    route = [
        "/asset/fund/<int:fid>",
        "/asset/fund",
        "/asset/fund/<string:sort>/<int:page>/<int:pre_page>",
        "/asset/fund/<string:sort>"
    ]

    def get(self, sort, page=0, pre_page=None, fid=0):
        if fid: return self.succ(Fund.get(fid))
        field, order = sort.split(":")
        return self.succ(Fund.select(page, pre_page, _orders=getattr(getattr(Fund, field), order)()))

    def post(self):
        submit = self.request()
        Fund.add(submit)
        return self.succ()

    def delete(self, fid):
        Fund.delete(fid)
        return self.succ()

    def put(self, fid):
        submit = self.request()
        submit["id"] = fid
        Fund.edit(submit)
        return self.succ()
