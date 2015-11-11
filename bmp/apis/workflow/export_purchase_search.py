# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase
from flask import request
from flask.ext import excel


class Export_purchase_searchApi(BaseApi):
    route = ["/export_purchase_search"]

    def get(self):
        submit = request.args
        resp = excel.make_response_from_records(Purchase.export(submit), "csv")
        resp.headers["Content-Disposition"] = "attachment; filename=purchase.csv"
        return resp
