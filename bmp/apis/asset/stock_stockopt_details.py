# coding: utf-8
from bmp.apis.base import BaseApi


class Stock_stockopt_detailsApi(BaseApi):
    route = ["/asset/stock_stockopt/<string:no>"]

    def get(self, no):
        pass
