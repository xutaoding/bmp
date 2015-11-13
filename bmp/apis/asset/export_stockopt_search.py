# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt
from flask import request
from flask.ext import excel


class Export_stockopt_searchApi(BaseApi):
    route = ["/asset/export_stockopt_search"]
    def auth(self):
        return True

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(StockOpt.export(submit), "csv")
        resp.headers["Content-Disposition"] = "attachment; filename=stock.csv"
        return resp
