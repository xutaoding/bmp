# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt
from flask import session
from bmp.const import USER_SESSION
from bmp.const import SCRAP

class ProjectApi(BaseApi):
    route = ["/project/<int:page>/<int:pre_page>"]

    def get(self,page=0, pre_page=None):
        return self.succ(StockOpt.approvals(page, pre_page))

if __name__ == "__main__":
    pass
