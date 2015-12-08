# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import Stock
from flask import request
import pyexcel.ext.xlsx
from flask.ext import excel


class Export_stock_searchApi(BaseApi):
    route = ["/asset/export_stock_search"]


    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(Stock.export(submit), "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=stock.xlsx"
        return resp
