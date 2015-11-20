# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt
from flask import request
import pyexcel.ext.xlsx
from flask.ext import excel


class Export_stockopt_searchApi(BaseApi):
    route = ["/asset/export_stockopt_search"]
    def auth(self):
        return True

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(StockOpt.export(submit), "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=stock.xlsx"
        return resp
