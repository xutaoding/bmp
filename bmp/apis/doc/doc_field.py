# coding=utf-8

import json
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import DOC, USER_SESSION
from bmp.database import Database
from bmp.models.doc import DocField, DocHistory
from flask import session


class Doc_fieldApi(BaseApi):
    route = ["/doc/field", "/doc/field/<int:page>/<int:pre_page>", "/doc/field/<int:fid>"]

    def get(self, page=None, pre_page=None, fid=None):
        if fid:
            return self.succ(DocField.get(fid))
        return self.succ(DocField.select(
            page,
            pre_page
        ))

    def post(self, fid):
        submit = self.request()
        submit["doc_id"] = fid
        field = DocField.add(submit, auto_commit=False)
        return self.success(submit, DOC.NEW)

    def put(self, fid):
        submit = self.request()
        submit["id"] = fid
        doc = DocField.edit(submit, auto_commit=False)
        submit["doc_id"] = doc.doc_id
        return self.success(submit, DOC.PUT)

    def success(self, doc, opt):
        doc_id = doc.pop("doc_id")
        hist = {
            "content": json.dumps(doc),
            "doc_id": doc_id,
            "type": DocField.__name__,
            "opt": opt,
            "create_uid": session[USER_SESSION]["uid"],
            "create_time": datetime.now()
        }
        DocHistory.add(hist, auto_commit=False)
        db.session.commit()
        return self.succ()

    def delete(self, fid):
        field = DocField.get(fid)
        DocField.delete(fid, auto_commit=False)
        return self.success(field, DOC.DELETE)
