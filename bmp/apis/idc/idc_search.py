# coding: utf-8
from werkzeug.datastructures import ImmutableMultiDict
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host
from flask import request


class Idc_searchApi(BaseApi):
    route = ["/idc/search/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        _filters = []
        for key in request.args.keys():
            arg_lst = request.args.getlist(key)

            if not hasattr(Idc_host,key):
                continue

            if 1==len(arg_lst):
                _filters.append(getattr(Idc_host,key)==arg_lst[0])
            else:
                _filters.append(getattr(Idc_host,key).in_(arg_lst))

        return self.succ(Idc_host.select(page, pre_page,_filters=_filters))


if __name__ == "__main__":
    from bmp.utils.post import test

    test("get", "http://localhost:5000/apis/v1.0/idc/search/1/10?ip=192.168&ip=192.167&dns=192.168", exe=True)
