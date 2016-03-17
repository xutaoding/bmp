# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host


class IdcApi(BaseApi):
    route = ["/idc", "/idc/<int:iid>", "/idc/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None, iid=None):
        if None != iid:
            return self.succ(Idc_host.get(iid))
        return self.succ(Idc_host.select(page, pre_page))

    def post(self):
        submit = self.request()
        return self.succ(Idc_host.add(submit))

    def put(self, iid):
        submit = self.request()
        submit["id"] = iid
        return self.succ(Idc_host.edit(submit))

    def delete(self, iid):
        return self.succ(Idc_host.delete(iid))



if __name__=="__main__":
    print Idc_host.select(1,10)