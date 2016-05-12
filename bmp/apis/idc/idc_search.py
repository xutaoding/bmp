# coding: utf-8
from flask import request
from sqlalchemy import or_

from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host, Idc_host_disk, Idc_host_interface, Idc_host_ps
from bmp.utils.exception import ExceptionEx


class Idc_searchApi(BaseApi):
    route = ["/idc/search/<int:page>/<int:pre_page>", "/idc/search/<int:page>/<int:pre_page>/<int:is_fuzzy>"]

    def get(self, page, pre_page, is_fuzzy=0):
        _filters = []

        for key in [arg for arg in request.args.keys() if arg != "_"]:
            has_key = False
            for _cls in [Idc_host, Idc_host_ps, Idc_host_disk, Idc_host_interface]:
                if not hasattr(_cls, key):
                    continue

                if is_fuzzy:
                    _filters.append(or_(*[
                         getattr(_cls, key).like(arg) for arg in request.args.getlist(key)
                        ]))
                else:
                    _filters.append(or_(*[
                         getattr(_cls, key).like(arg) for arg in request.args.getlist(key)
                        ]))

                has_key = True
                break

            if not has_key:
                raise ExceptionEx("查询字段%s不存在" % key)

        return self.succ(Idc_host.select(
            page,
            pre_page,
            _joins=[Idc_host_disk, Idc_host_interface, Idc_host_ps],
            _filters=_filters)
        )


if __name__ == "__main__":
    for host in Idc_host.select(1,10,_joins=[Idc_host_disk, Idc_host_interface, Idc_host_ps],_filters=Idc_host_interface.ip_address.like("122.144.134.95"))["items"]:
        print host
