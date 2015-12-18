# coding=utf-8
from flask import request
from flask.ext import excel

from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt
import pyexcel.ext.xlsx

class Export_stockopt_searchApi(BaseApi):
    route = ["/asset/export_stockopt_search"]

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(StockOpt.export(submit), "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=stock.xlsx"
        return resp
