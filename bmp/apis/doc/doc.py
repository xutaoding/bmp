# coding=utf-8

import json
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import DOC, USER_SESSION
from bmp.database import Database
from bmp.models.doc import Doc, DocHistory, DocIndex, DocField
from flask import session


class DocApi(BaseApi):
    route = ["/doc", "/doc/<int:page>/<int:pre_page>", "/doc/<int:did>"]

    def get(self, page=None, pre_page=None, did=None):
        if did:
            return self.succ(Doc.get(did))
        return self.succ(Doc.select(
            page,
            pre_page
        ))

    def post(self):
        submit = self.request()
        indexs = submit.pop("indexs") if submit.__contains__("indexs") else []
        fields = submit.pop("fields") if submit.__contains__("fields") else []

        submit["create_time"] = datetime.now()
        submit["create_uid"] = session[USER_SESSION]["uid"]

        doc = Doc.add(submit, auto_commit=False)

        doc.indexs = [Database.to_cls(DocIndex, index) for index in indexs]
        doc.fields = [Database.to_cls(DocField, field) for field in fields]

        db.session.commit()
        return self.succ()

    def success(self, doc, opt):
        hist = {
            "content": json.dumps(doc),
            "doc_id": doc["id"],
            "type": Doc.__name__,
            "opt": opt,
            "create_uid": session[USER_SESSION]["uid"],
            "create_time": datetime.now()
        }
        DocHistory.add(hist, auto_commit=False)
        db.session.commit()
        return self.succ()

    def put(self, did):
        submit = self.request()
        indexs = submit["indexs"] if submit.__contains__("indexs") else []
        fields = submit["fields"] if submit.__contains__("fields") else []

        submit["id"] = did
        doc = Doc.edit(submit, auto_commit=False)

        doc.indexs = [Database.to_cls(DocIndex, index) for index in indexs]
        doc.fields = [Database.to_cls(DocField, field) for field in fields]

        return self.success(submit, DOC.PUT)

    def delete(self, did):
        doc = Doc.get(did)
        Doc.delete(did, auto_commit=False)
        return self.success(doc, DOC.DELETE)
