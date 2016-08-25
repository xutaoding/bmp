# coding=utf-8

from bmp.apis.base import BaseApi
from bmp.models.doc import Doc


class Doc_searchApi(BaseApi):
    route = ["/doc/search", "/doc/search/<int:page>/<int:pre_page>"]

    def get(self, page=None, pre_page=None):
        return self.succ(Doc.select(
            page,
            pre_page,
            _filters=self.get_search_fields(Doc),
            _orders=Doc.modify_time.desc()
        ))
