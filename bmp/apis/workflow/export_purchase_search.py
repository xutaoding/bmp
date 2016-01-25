# coding=utf-8
import pyexcel.ext.xlsx
from flask import request
from flask.ext import excel

from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase


class Export_purchase_searchApi(BaseApi):
    route = ["/export_purchase_search"]

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(Purchase.export(submit), "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=purchase.xlsx"
        return resp
