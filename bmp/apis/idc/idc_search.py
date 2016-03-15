# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host
from flask import request

class Idc_ps_infoApi(BaseApi):
    route = ["/idc/search/<int:page>/<int:pre_page>"]

    def get(self,page,pre_page):
        submit=request.args
        return self.succ(Idc_host.select(page,pre_page,submit))

if __name__=="__main__":
    print Idc_host.select(1,10,filter={"ip":"19"})