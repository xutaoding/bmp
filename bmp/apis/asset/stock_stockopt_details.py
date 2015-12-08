# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Stock


class Stock_stockopt_detailsApi(BaseApi):
    route =["/asset/stock_stockopt/<string:no>"]

    def get(self, no):
        pass