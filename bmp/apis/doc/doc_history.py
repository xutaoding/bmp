# coding=utf-8

from bmp.apis.base import BaseApi
from bmp.models.doc import  DocHistory


class Doc_historyApi(BaseApi):
    route = ["/doc/history", "/doc/history/<int:page>/<int:pre_page>", "/doc/history/<int:hid>"]

    def get(self, page=None, pre_page=None, hid=None):
        if hid:
            return self.succ(DocHistory.get(hid))
        return self.succ(DocHistory.select(
            page,
            pre_page
        ))
