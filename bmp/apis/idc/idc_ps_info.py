# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host_ps


class Idc_ps_infoApi(BaseApi):
    route = ["/idc/ps/<int:iid>"]

    def get(self,iid=None):
        return self.succ(Idc_host_ps.get(iid))

    def post(self):
        submit = self.request()
        return self.succ(Idc_host_ps.add(submit))


if __name__=="__main__":
    pass