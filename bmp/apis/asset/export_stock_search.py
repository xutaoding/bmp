# coding=utf-8
from flask import request
from flask.ext import excel

from bmp.apis.base import BaseApi
from bmp.models.asset import Stock


class Export_stock_searchApi(BaseApi):
    route = ["/asset/export_stock_search"]

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(Stock.export(submit), "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=stock.xlsx"
        return resp
