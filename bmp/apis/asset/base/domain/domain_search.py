# coding: utf-8
from werkzeug.datastructures import ImmutableMultiDict
from bmp.apis.base import BaseApi
from bmp.models.asset import Domain
from flask import request
from sqlalchemy import or_
from bmp.utils.exception import ExceptionEx


class Domain_searchApi(BaseApi):
    route = ["/domain/search/<int:page>/<int:pre_page>","/domain/search"]

    def get(self):
        _filters = []
        for key in [arg for arg in request.args.keys() if arg!="_"]:
            if not hasattr(Domain,key):
                raise ExceptionEx("查询字段%s不存在"%key)

            _filters.append(or_(*[
                getattr(Domain,key).like("%"+arg+"%") for arg in request.args.getlist(key)
            ]))

        return self.succ(Domain.select(_filters=_filters))


if __name__ == "__main__":
    pass
