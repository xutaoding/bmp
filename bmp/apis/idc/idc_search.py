# coding: utf-8
from werkzeug.datastructures import ImmutableMultiDict
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host
from flask import request
from sqlalchemy import or_
from bmp.utils.exception import ExceptionEx


class Idc_searchApi(BaseApi):
    route = ["/idc/search/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        _filters = []
        for key in [arg for arg in request.args.keys() if arg!="_"]:
            if not hasattr(Idc_host,key):
                raise ExceptionEx("查询字段%s不存在"%key)

            _filters.append(or_(*[
                getattr(Idc_host,key).like("%"+arg+"%") for arg in request.args.getlist(key)
            ]))

        return self.succ(Idc_host.select(page, pre_page,_filters=_filters))


if __name__ == "__main__":
    pass
