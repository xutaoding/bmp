# coding=utf-8

import json

from flask import session

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import DOC, USER_SESSION
from bmp.models.doc import DocIndex, DocHistory
from datetime import datetime

class Doc_indexApi(BaseApi):
    route = ["/doc/index", "/doc/index/<int:page>/<int:pre_page>", "/doc/index/<int:iid>"]

    def get(self, page=None, pre_page=None, iid=None):
        if iid:
            return self.succ(DocIndex.get(iid))
        return self.succ(DocIndex.select(
            page,
            pre_page
        ))

    def post(self, iid):
        submit = self.request()
        submit["doc_id"] = iid
        index = DocIndex.add(submit)
        return self.success(submit,DOC.NEW)

    def put(self, iid):
        submit = self.request()
        submit["id"] = iid
        doc = DocIndex.edit(submit, auto_commit=False)
        submit["doc_id"] = doc.doc_id
        return self.success(submit, DOC.PUT)

    def success(self, doc, opt):
        doc_id = doc.pop("doc_id")
        hist = {
            "content": json.dumps(doc),
            "doc_id": doc_id,
            "type": DocIndex.__name__,
            "opt": opt,
            "create_uid": session[USER_SESSION]["uid"],
            "create_time": datetime.now()
        }
        DocHistory.add(hist, auto_commit=False)
        db.session.commit()
        return self.succ()

    def delete(self, iid):
        index = DocIndex.get(iid)
        DocIndex.delete(iid, auto_commit=False)

        return self.success(index, DOC.DELETE)
