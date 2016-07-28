# coding=utf-8

from bmp.apis.base import BaseApi
from bmp.models.doc import  DocHistory


class Doc_historyApi(BaseApi):
    route = ["/doc/history/",
             "/doc/history/<int:did>/<int:page>/<int:pre_page>",
             "/doc/history/<int:did>"]

    def get(self, page=None, pre_page=None, did=None):
        if did:
            return self.succ(DocHistory.select(
                page=page,
                pre_page=pre_page,
                _filters=DocHistory.doc_id == did
            ))
        return self.succ(DocHistory.select(
            page,
            pre_page
        ))
