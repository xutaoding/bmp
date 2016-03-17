# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host_ps


class Idc_ps_infoApi(BaseApi):
    route = ["/idc/ps/<int:iid>"]

    def get(self,iid=None):
        return self.succ(Idc_host_ps.select(_filters=[Idc_host_ps.idc_host_id==iid]))

    def post(self,iid):
        return self.succ(Idc_host_ps.add(iid))


if __name__=="__main__":
    pass